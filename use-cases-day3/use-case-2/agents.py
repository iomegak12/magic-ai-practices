"""Agent factory for the TechWeatherAssistant."""

from collections.abc import Callable

from agent_framework.azure import AzureOpenAIResponsesClient
from azure.identity import AzureCliCredential

from middleware import (
    ExceptionHandlingMiddleware,
    LLMInputGuardrailMiddleware,
    LLMOutputGuardrailMiddleware,
    LoggingFunctionMiddleware,
)
from tools import get_weather, unstable_data_service


def create_tech_weather_agent(
    project_endpoint: str,
    deployment_name: str,
    classify_fn: Callable[[str, str], dict],
):
    """Create a TechWeatherAssistant agent with guardrails, exception handling, and logging.

    Args:
        project_endpoint: Azure AI project endpoint.
        deployment_name: Azure OpenAI deployment/model name.
        classify_fn: A callable (text, system_prompt) -> dict for guardrail classification.

    Returns:
        A tuple of (client, agent) — client is kept alive for the agent's lifetime.
    """
    credential = AzureCliCredential()
    client = AzureOpenAIResponsesClient(
        project_endpoint=project_endpoint,
        deployment_name=deployment_name,
        credential=credential,
    )

    agent = client.as_agent(
        name="TechWeatherAssistant",
        instructions=(
            "You are a helpful technology assistant specializing in Weather Information, "
            "IT, Computer Science, Software Engineering, and Technology topics. "
            "Use the get_weather tool when asked about weather conditions for any location. "
            "Use the unstable_data_service tool when asked to fetch data or user statistics. "
            "Always provide clear, concise, and technically accurate answers."
        ),
        tools=[get_weather, unstable_data_service],
        middleware=[
            LLMInputGuardrailMiddleware(classify_fn=classify_fn),
            ExceptionHandlingMiddleware(),
            LLMOutputGuardrailMiddleware(classify_fn=classify_fn),
            LoggingFunctionMiddleware(),
        ],
    )

    return client, agent
