from __future__ import annotations

from io import BytesIO
from typing import Optional

import pandas as pd
from azure.identity import DefaultAzureCredential
from azure.storage.filedatalake import DataLakeServiceClient

from src.utils.config import get_settings
from src.utils.logger import get_logger

logger = get_logger(__name__)


class ADLSConnector:
    """
    Azure Data Lake Storage Gen2 connector.

    Authentication uses DefaultAzureCredential so the same code can work with:
    - Azure Managed Identity
    - Azure CLI login
    - Visual Studio Code / developer credentials
    - Service principals
    """

    def __init__(
        self,
        storage_account: Optional[str] = None,
        filesystem: Optional[str] = None,
    ) -> None:
        settings = get_settings()

        self.storage_account = (
            storage_account or settings.azure_storage_account
        )
        self.filesystem = (
            filesystem or settings.adls_filesystem
        )

        if not self.storage_account:
            raise ValueError(
                "Azure Storage Account is not configured. "
                "Set AZURE_STORAGE_ACCOUNT."
            )

        if not self.filesystem:
            raise ValueError(
                "ADLS filesystem is not configured. "
                "Set ADLS_FILESYSTEM."
            )

        self.credential = DefaultAzureCredential()

        account_url = (
            f"https://{self.storage_account}.dfs.core.windows.net"
        )

        self.service_client = DataLakeServiceClient(
            account_url=account_url,
            credential=self.credential,
        )

        self.filesystem_client = (
            self.service_client.get_file_system_client(
                self.filesystem
            )
        )

        logger.info(
            "Initialized ADLS connector for storage account=%s filesystem=%s",
            self.storage_account,
            self.filesystem,
        )

    def file_exists(self, path: str) -> bool:
        """Check whether a file exists in ADLS."""

        try:
            self.filesystem_client.get_file_client(path).get_file_properties()
            return True

        except Exception:
            return False

    def read_bytes(self, path: str) -> bytes:
        """Read a file from ADLS as bytes."""

        logger.info("Reading ADLS file: %s", path)

        file_client = self.filesystem_client.get_file_client(path)

        response = file_client.download_file()

        data = response.readall()

        logger.info(
            "Successfully downloaded %s bytes from %s",
            len(data),
            path,
        )

        return data

    def write_bytes(
        self,
        data: bytes,
        path: str,
        overwrite: bool = True,
    ) -> None:
        """Write bytes to an ADLS file."""

        logger.info("Writing ADLS file: %s", path)

        file_client = self.filesystem_client.get_file_client(path)

        file_client.upload_data(
            data,
            overwrite=overwrite,
        )

        logger.info("Successfully uploaded ADLS file: %s", path)

    def read_csv(
        self,
        path: str,
        **kwargs,
    ) -> pd.DataFrame:
        """Read CSV from ADLS into a pandas DataFrame."""

        data = self.read_bytes(path)

        dataframe = pd.read_csv(
            BytesIO(data),
            **kwargs,
        )

        logger.info(
            "Loaded CSV %s with rows=%d columns=%d",
            path,
            len(dataframe),
            len(dataframe.columns),
        )

        return dataframe

    def write_csv(
        self,
        dataframe: pd.DataFrame,
        path: str,
        index: bool = False,
    ) -> None:
        """Write pandas DataFrame to ADLS as CSV."""

        csv_data = dataframe.to_csv(
            index=index
        ).encode("utf-8")

        self.write_bytes(
            data=csv_data,
            path=path,
            overwrite=True,
        )

    def read_json(
        self,
        path: str,
        **kwargs,
    ) -> pd.DataFrame:
        """Read JSON from ADLS into a pandas DataFrame."""

        data = self.read_bytes(path)

        dataframe = pd.read_json(
            BytesIO(data),
            **kwargs,
        )

        logger.info(
            "Loaded JSON %s with rows=%d",
            path,
            len(dataframe),
        )

        return dataframe

    def list_paths(
        self,
        directory: Optional[str] = None,
    ) -> list[str]:
        """List files/directories in an ADLS directory."""

        paths = self.filesystem_client.get_paths(
            path=directory,
            recursive=False,
        )

        result = []

        for item in paths:
            result.append(item.name)

        logger.info(
            "Found %d paths under %s",
            len(result),
            directory or "/",
        )

        return result

    def delete_file(self, path: str) -> None:
        """Delete a file from ADLS."""

        logger.warning(
            "Deleting ADLS file: %s",
            path,
        )

        file_client = self.filesystem_client.get_file_client(path)

        file_client.delete_file()

        logger.info(
            "Deleted ADLS file: %s",
            path,
        )