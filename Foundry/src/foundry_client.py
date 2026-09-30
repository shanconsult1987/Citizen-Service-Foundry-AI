from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

from src.config import (
    FOUNDRY_PROJECT_ENDPOINT,
    validate_config,
)


def get_credential():
    """
    Uses Microsoft Entra ID authentication.

    The workshop user authenticates with:

        az login
    """
    return DefaultAzureCredential(
        exclude_interactive_browser_credential=True
    )


def get_project_client():
    validate_config()

    credential = get_credential()

    return AIProjectClient(
        endpoint=FOUNDRY_PROJECT_ENDPOINT,
        credential=credential,
    )


def ask_foundry(question: str) -> str:
    """
    Send a question to the deployed Foundry model.
    """

    with get_project_client() as project_client:

        openai_client = project_client.get_openai_client()

        from src.config import FOUNDRY_MODEL_DEPLOYMENT

        response = openai_client.responses.create(
            model=FOUNDRY_MODEL_DEPLOYMENT,
            input=question,
        )

        return response.output_text