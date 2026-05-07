"""Configuration loaded from .env via pydantic-settings."""

from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from magic_v22_mcp import __description__, __title__, __version__


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Identity
    server_name: str = __title__
    description: str = __description__
    version: str = __version__

    # Server
    mcp_host: str = Field(default="0.0.0.0", alias="MCP_HOST")
    mcp_port: int = Field(default=9898, alias="MCP_PORT")

    # Database
    db_path: str = Field(default="./data/magic_v22.db", alias="DB_PATH")

    # Auth
    api_key: str = Field(alias="API_KEY")
    require_auth: bool = Field(default=True, alias="REQUIRE_AUTH")

    # Logging
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
