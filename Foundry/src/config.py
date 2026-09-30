import os

from dotenv import load_dotenv

load_dotenv()


FOUNDRY_PROJECT_ENDPOINT = os.getenv("FOUNDRY_PROJECT_ENDPOINT")
FOUNDRY_MODEL_DEPLOYMENT = os.getenv("FOUNDRY_MODEL_DEPLOYMENT")
FOUNDRY_TOOLS_ENDPOINT = os.getenv("FOUNDRY_TOOLS_ENDPOINT")
FOUNDRY_REGION = os.getenv("FOUNDRY_REGION", "eastus")


def validate_config():
    required = {
        "FOUNDRY_PROJECT_ENDPOINT": FOUNDRY_PROJECT_ENDPOINT,
        "FOUNDRY_MODEL_DEPLOYMENT": FOUNDRY_MODEL_DEPLOYMENT,
        "FOUNDRY_TOOLS_ENDPOINT": FOUNDRY_TOOLS_ENDPOINT,
    }

    missing = [
        name for name, value in required.items()
        if not value
    ]

    if missing:
        raise RuntimeError(
            "Missing configuration: "
            + ", ".join(missing)
            + "\nCreate a .env file from .env.example."
        )