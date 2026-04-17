"""Build the fully-assembled MAF agent from application settings."""

import logging
from functools import partial

from agent_framework import MCPStreamableHTTPTool
from agent_framework.openai import OpenAIChatClient
from azure.identity.aio import AzureCliCredential

from app.agent.instructions import AGENT_INSTRUCTIONS
from app.agent.tools import get_current_time, get_location_info, get_weather
from app.config import Settings
from app.history import SQLiteHistoryProvider
from app.middleware.exception_handler import ExceptionHandlingMiddleware
from app.middleware.function_logger import TrackingFunctionMiddleware
from app.middleware.guardrails import (
    LLMInputGuardrailMiddleware,
    LLMOutputGuardrailMiddleware,
    classify_text,
    create_guardrail_client,
)

logger = logging.getLogger("agent")


def build_agent(settings: Settings):
    """Construct the agent with all tools, middleware, and history.

    Returns:
        tuple: (agent, credential, history_provider)
    """
    # --- Auth ---
    credential = None
    if settings.AZURE_AUTH_METHOD == "cli":
        credential = AzureCliCredential()
        client = OpenAIChatClient(
            model=settings.AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME,
            azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
            credential=credential,
        )
    else:
        client = OpenAIChatClient(
            model=settings.AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME,
            azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
            api_key=settings.AZURE_OPENAI_API_KEY,
        )

    # --- MCP Tools ---
    ms_learn_mcp = MCPStreamableHTTPTool(
        name="Microsoft Learn MCP Tool",
        url=settings.MCP_LEARN_URL,
    )
    orders_complaints_mcp = MCPStreamableHTTPTool(
        name="Orders and Complaints MCP Tool",
        url=settings.MCP_ORDERS_URL,
    )

    # --- History ---
    history_provider = SQLiteHistoryProvider(db_path=settings.DB_PATH)
    logger.info("SQLite history DB: %s", settings.DB_PATH)

    # --- Guardrail classifier ---
    guardrail_client = create_guardrail_client(
        azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
        api_key=settings.AZURE_OPENAI_API_KEY,
        api_version=settings.AZURE_OPENAI_API_VERSION,
    )
    classify_fn = partial(
        classify_text,
        guardrail_client,
        settings.AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME,
    )

    # --- Observability (opt-in) ---
    if settings.ENABLE_OBSERVABILITY:
        try:
            from agent_framework.observability import configure_otel_providers

            configure_otel_providers()
            logger.info("OpenTelemetry providers configured")
        except Exception as e:
            logger.warning("Failed to configure OpenTelemetry: %s", e)

    # --- Agent assembly ---
    agent = client.as_agent(
        name="CustomerServiceAgent",
        instructions=AGENT_INSTRUCTIONS,
        tools=[
            ms_learn_mcp,
            orders_complaints_mcp,
            get_weather,
            get_current_time,
            get_location_info,
        ],
        middleware=[
            LLMInputGuardrailMiddleware(classify_fn=classify_fn),
            ExceptionHandlingMiddleware(),
            LLMOutputGuardrailMiddleware(classify_fn=classify_fn),
            TrackingFunctionMiddleware(),
        ],
        context_providers=[history_provider],
    )

    logger.info(
        "Agent '%s' created with MCP + local tools, middleware pipeline, "
        "and SQLite history provider.",
        agent.name,
    )

    return agent, credential, history_provider, [ms_learn_mcp, orders_complaints_mcp]
