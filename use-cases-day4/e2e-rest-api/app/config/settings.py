"""Application settings loaded from environment variables and .env file."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central configuration for the Enterprise E2E REST API."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # --- Server ---
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8800
    LOG_LEVEL: str = "INFO"

    # --- Azure OpenAI ---
    AZURE_OPENAI_ENDPOINT: str = ""
    AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME: str = ""
    AZURE_OPENAI_API_KEY: str = ""
    AZURE_OPENAI_API_VERSION: str = "2025-03-01-preview"
    AZURE_AUTH_METHOD: str = "cli"  # "cli" or "api_key"

    # --- MCP Servers ---
    MCP_ORDERS_URL: str = "http://localhost:8700/mcp"
    MCP_LEARN_URL: str = "https://learn.microsoft.com/api/mcp"

    # --- Observability ---
    ENABLE_OBSERVABILITY: bool = False
    OTEL_EXPORTER_OTLP_ENDPOINT: str = "http://localhost:4317"

    # --- Rate Limiting ---
    ENABLE_RATE_LIMITING: bool = False
    RATE_LIMIT_PER_MINUTE: int = 60

    # --- CORS ---
    ENABLE_CORS: bool = True

    # --- Database ---
    DB_PATH: str = "./data/conversation_history.db"

    # --- Application Metadata ---
    APP_TITLE: str = "Enterprise E2E Use Case"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = (
        "Production-grade REST API wrapping a Microsoft Agent Framework agent "
        "with MCP tools, guardrails, conversation history, and observability."
    )


@lru_cache
def get_settings() -> Settings:
    """Return a cached singleton Settings instance."""
    return Settings()
