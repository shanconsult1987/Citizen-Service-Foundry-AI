from azure.identity import DefaultAzureCredential


_credential = None


def get_credential():
    global _credential

    if _credential is None:
        _credential = DefaultAzureCredential(
            exclude_interactive_browser_credential=True
        )

    return _credential


def get_cognitive_token():
    token = get_credential().get_token(
        "https://cognitiveservices.azure.com/.default"
    )

    return token.token


def get_ai_project_token():
    token = get_credential().get_token(
        "https://ai.azure.com/.default"
    )

    return token.token