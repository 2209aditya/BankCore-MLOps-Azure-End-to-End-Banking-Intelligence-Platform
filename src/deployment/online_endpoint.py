from azure.ai.ml import MLClient
from azure.ai.ml.entities import ManagedOnlineEndpoint
from azure.identity import DefaultAzureCredential

from src.utils.config import get_settings


def get_ml_client():

    settings = get_settings()

    return MLClient(
        DefaultAzureCredential(),
        settings.azure_subscription_id,
        settings.azure_resource_group,
        settings.azure_ml_workspace,
    )


def create_endpoint(name: str):

    client = get_ml_client()

    endpoint = ManagedOnlineEndpoint(
        name=name,
        auth_mode="key",
        description="BankCore real-time ML endpoint",
    )

    return client.online_endpoints.begin_create_or_update(
        endpoint
    ).result()


if __name__ == "__main__":

    settings = get_settings()

    endpoint = create_endpoint(
        f"{settings.model_name}-endpoint"
    )

    print(endpoint.name)