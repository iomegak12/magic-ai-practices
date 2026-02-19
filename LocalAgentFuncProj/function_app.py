import os
from dotenv import load_dotenv
from typing import Any

from agent_framework.azure import AgentFunctionApp, AzureOpenAIResponsesClient
from azure.identity import AzureCliCredential

load_dotenv(override=True)
project_endpoint = os.environ.get("AZURE_AI_PROJECT_ENDPOINT")
deployment_name = os.environ.get("AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME")


def _create_agent() -> Any:
    """Create a hosted agent backed by Azure OpenAI."""
    credential = AzureCliCredential()

    client = AzureOpenAIResponsesClient(
        project_endpoint=project_endpoint,
        deployment_name=deployment_name,
        credential=credential,
    )

    return client.as_agent(
        name="HostedAgent",
        instructions="You are a helpful assistant hosted in Azure Functions.",
    )


app = AgentFunctionApp(
    agents=[_create_agent()],
    enable_health_check=True,
    max_poll_retries=50)
