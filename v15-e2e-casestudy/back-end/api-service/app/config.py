"""
Configuration management for MSAv15Service

Loads environment variables and provides application settings.
"""
from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Service Configuration
    SERVICE_NAME: str = "MSAv15Service"
    SERVICE_VERSION: str = "0.1.0"
    SERVICE_PORT: int = 9080
    
    # Azure OpenAI Configuration
    AZURE_AI_PROJECT_ENDPOINT: str
    AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME: str
    AZURE_OPENAI_API_KEY: Optional[str] = None
    
    # Database Configuration
    ORDER_DB_PATH: str = "./data/orders.db"
    ORDER_DB_SEEDING_ENABLED: bool = True
    ORDER_DB_SEED_COUNT: int = 25
    
    # MCP Server Configuration (External)
    MCP_COMPLAINT_SERVER_URL: str = "http://localhost:8000/mcp"
    
    # API Configuration
    CORS_ALLOW_ORIGINS: str = "*"
    RATE_LIMITING_ENABLED: bool = False
    RATE_LIMIT_REQUESTS_PER_MINUTE: int = 60
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Singleton settings instance
settings = Settings()
