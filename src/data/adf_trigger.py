from __future__ import annotations

from typing import Any, Optional

import requests
from azure.identity import DefaultAzureCredential

from src.utils.config import get_settings
from src.utils.logger import get_logger

logger = get_logger(__name__)


class ADFPipelineTrigger:
    """
    Azure Data Factory pipeline trigger.

    Uses Azure Resource Manager REST APIs and DefaultAzureCredential.
    """

    ARM_SCOPE = "https://management.azure.com/.default"

    def __init__(
        self,
        subscription_id: Optional[str] = None,
        resource_group: Optional[str] = None,
        factory_name: Optional[str] = None,
    ) -> None:
        settings = get_settings()

        self.subscription_id = (
            subscription_id
            or settings.azure_subscription_id
        )

        self.resource_group = (
            resource_group
            or settings.azure_resource_group
        )

        self.factory_name = (
            factory_name
            or getattr(
                settings,
                "azure_data_factory",
                "",
            )
        )

        if not self.subscription_id:
            raise ValueError(
                "AZURE_SUBSCRIPTION_ID is required."
            )

        if not self.resource_group:
            raise ValueError(
                "AZURE_RESOURCE_GROUP is required."
            )

        if not self.factory_name:
            raise ValueError(
                "Azure Data Factory name is required."
            )

        self.credential = DefaultAzureCredential()

    def _get_access_token(self) -> str:
        """Get an Azure Resource Manager access token."""

        token = self.credential.get_token(
            self.ARM_SCOPE
        )

        return token.token

    def trigger(
        self,
        pipeline_name: str,
        parameters: Optional[dict[str, Any]] = None,
    ) -> str:
        """
        Trigger an ADF pipeline.

        Returns:
            ADF pipeline run ID.
        """

        if not pipeline_name:
            raise ValueError(
                "pipeline_name cannot be empty."
            )

        token = self._get_access_token()

        url = (
            "https://management.azure.com"
            f"/subscriptions/{self.subscription_id}"
            f"/resourceGroups/{self.resource_group}"
            f"/providers/Microsoft.DataFactory"
            f"/factories/{self.factory_name}"
            f"/pipelines/{pipeline_name}"
            "/createRun"
            "?api-version=2018-06-01"
        )

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        payload = {
            "parameters": parameters or {}
        }

        logger.info(
            "Triggering ADF pipeline: %s",
            pipeline_name,
        )

        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=30,
        )

        response.raise_for_status()

        result = response.json()

        run_id = result.get("runId")

        if not run_id:
            raise RuntimeError(
                "ADF pipeline was triggered but no runId was returned."
            )

        logger.info(
            "ADF pipeline started successfully. run_id=%s",
            run_id,
        )

        return run_id

    def get_pipeline_run(
        self,
        run_id: str,
    ) -> dict[str, Any]:
        """Get details about an ADF pipeline run."""

        token = self._get_access_token()

        url = (
            "https://management.azure.com"
            f"/subscriptions/{self.subscription_id}"
            f"/resourceGroups/{self.resource_group}"
            f"/providers/Microsoft.DataFactory"
            f"/factories/{self.factory_name}"
            f"/pipelineruns/{run_id}"
            "?api-version=2018-06-01"
        )

        response = requests.get(
            url,
            headers={
                "Authorization": f"Bearer {token}",
            },
            timeout=30,
        )

        response.raise_for_status()

        return response.json()

    def cancel_pipeline_run(
        self,
        run_id: str,
    ) -> None:
        """Cancel an active ADF pipeline run."""

        token = self._get_access_token()

        url = (
            "https://management.azure.com"
            f"/subscriptions/{self.subscription_id}"
            f"/resourceGroups/{self.resource_group}"
            f"/providers/Microsoft.DataFactory"
            f"/factories/{self.factory_name}"
            f"/pipelineruns/{run_id}"
            "/cancel"
            "?api-version=2018-06-01"
        )

        response = requests.post(
            url,
            headers={
                "Authorization": f"Bearer {token}",
            },
            timeout=30,
        )

        response.raise_for_status()

        logger.info(
            "Cancelled ADF pipeline run: %s",
            run_id,
        )


def trigger_adf_pipeline(
    subscription_id: str,
    resource_group: str,
    factory_name: str,
    pipeline_name: str,
    parameters: Optional[dict[str, Any]] = None,
) -> str:
    """
    Backwards-compatible helper for triggering ADF.
    """

    trigger = ADFPipelineTrigger(
        subscription_id=subscription_id,
        resource_group=resource_group,
        factory_name=factory_name,
    )

    return trigger.trigger(
        pipeline_name=pipeline_name,
        parameters=parameters,
    )