from __future__ import annotations

from typing import Optional

from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential

from src.utils.config import get_settings
from src.utils.logger import get_logger

logger = get_logger(__name__)


def get_ml_client() -> MLClient:
    """
    Create an Azure ML client using Managed Identity / DefaultAzureCredential.
    """

    settings = get_settings()

    required = {
        "AZURE_SUBSCRIPTION_ID": settings.azure_subscription_id,
        "AZURE_RESOURCE_GROUP": settings.azure_resource_group,
        "AZURE_ML_WORKSPACE": settings.azure_ml_workspace,
    }

    missing = [
        name
        for name, value in required.items()
        if not value
    ]

    if missing:
        raise ValueError(
            "Missing Azure ML configuration: "
            + ", ".join(missing)
        )

    credential = DefaultAzureCredential()

    client = MLClient(
        credential=credential,
        subscription_id=settings.azure_subscription_id,
        resource_group_name=settings.azure_resource_group,
        workspace_name=settings.azure_ml_workspace,
    )

    logger.info(
        "Azure ML client initialized. workspace=%s",
        settings.azure_ml_workspace,
    )

    return client


class BankCoreFeatureStore:
    """
    Azure ML Feature Store integration boundary.

    This class isolates Feature Store operations from the rest of BankCore.

    Exact Feature Store APIs can vary with the installed Azure ML SDK version,
    so the MLClient creation is kept separate from feature retrieval logic.
    """

    def __init__(
        self,
        ml_client: Optional[MLClient] = None,
    ) -> None:
        self.ml_client = ml_client or get_ml_client()

    def get_workspace(self):
        """Return the configured Azure ML workspace."""

        return self.ml_client.workspaces.get(
            self.ml_client.workspace_name
        )

    def get_feature_store(self):
        """
        Return the Feature Store resource when available in the SDK.

        Feature Store support depends on the Azure ML SDK version.
        """

        feature_stores = getattr(
            self.ml_client,
            "feature_stores",
            None,
        )

        if feature_stores is None:
            raise RuntimeError(
                "Feature Store client is not exposed by the installed "
                "azure-ai-ml version. Install a compatible Azure ML SDK."
            )

        return feature_stores

    def get_features(
        self,
        feature_set_name: str,
        version: Optional[str] = None,
    ):
        """
        Retrieve a Feature Set definition.

        The exact invocation should be aligned with the Azure ML
        Feature Store SDK version used by the environment.
        """

        feature_stores = self.get_feature_store()

        if version:
            return feature_stores.get(
                name=feature_set_name,
                version=version,
            )

        return feature_stores.get(
            name=feature_set_name
        )

    def health_check(self) -> dict:
        """Simple Azure ML connectivity check."""

        try:
            workspace = self.get_workspace()

            return {
                "status": "healthy",
                "workspace": workspace.name,
            }

        except Exception as exc:
            logger.exception(
                "Azure ML Feature Store health check failed."
            )

            return {
                "status": "unhealthy",
                "error": str(exc),
            }