import os
from dotenv import load_dotenv
from typing import Any

from agent_framework.azure import AgentFunctionApp, AzureOpenAIResponsesClient
from azure.identity import AzureCliCredential

<<<<<<< HEAD

load_dotenv(override=True)
endpoint = os.environ.get("AZURE_AI_PROJECT_ENDPOINT")
deployment_name = os.environ.get("AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME")

if not endpoint or not deployment_name:
    raise ValueError(
        "AZURE_AI_PROJECT_ENDPOINT and AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME must be set in the environment variables.")

=======
load_dotenv(override=True)
project_endpoint = os.environ.get("AZURE_AI_PROJECT_ENDPOINT")
deployment_name = os.environ.get("AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME")

>>>>>>> 01273dd9e129a9d9a0826640db770c7c8f024eb1

def _create_agent() -> Any:
    """Create a hosted agent backed by Azure OpenAI."""
    credential = AzureCliCredential()
<<<<<<< HEAD
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
=======

    client = AzureOpenAIResponsesClient(
        project_endpoint=project_endpoint,
        deployment_name=deployment_name,
        credential=credential,
    )

    return client.as_agent(
        name="HostedAgent",
        instructions="You are a helpful assistant hosted in Azure Functions.",
    )
>>>>>>> 01273dd9e129a9d9a0826640db770c7c8f024eb1


app = AgentFunctionApp(
    agents=[_create_agent()],
    enable_health_check=True,
    max_poll_retries=50)
