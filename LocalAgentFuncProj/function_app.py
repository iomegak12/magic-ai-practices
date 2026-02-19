import os
from dotenv import load_dotenv
from typing import Any

from agent_framework.azure import AgentFunctionApp, AzureOpenAIResponsesClient
from azure.identity import AzureCliCredential


load_dotenv(override=True)
endpoint = os.environ.get("AZURE_AI_PROJECT_ENDPOINT")
deployment_name = os.environ.get("AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME")

if not endpoint or not deployment_name:
    raise ValueError(
        "AZURE_AI_PROJECT_ENDPOINT and AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME must be set in the environment variables.")


def _create_agent() -> Any:
    """Create a hosted agent backed by Azure OpenAI."""
    credential = AzureCliCredential()
    client = AzureOpenAIResponsesClient(
        project_endpoint=endpoint,
        deployment_name=deployment_name,
        credential=credential,
    )
    agent = client.as_agent(
        name="HelloAgent",
        instructions="You are a friendly assistant. Keep your answers brief.",
    )
    return agent


app = AgentFunctionApp(
    agents=[_create_agent()],
    enable_health_check=True,
    max_poll_retries=50)
