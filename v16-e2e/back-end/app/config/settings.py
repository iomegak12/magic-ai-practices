"""
Configuration Settings Management

This module provides centralized configuration management using Pydantic Settings.
All settings are loaded from environment variables with validation and type checking.
"""

from typing import Optional
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # ============================================
    # Server Configuration
    # ============================================
    SERVER_HOST: str = Field(default="0.0.0.0", description="Server host address")
    SERVER_PORT: int = Field(default=9080, ge=1024, le=65535, description="Server port")
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")
    
    # ============================================
    # CORS Configuration
    # ============================================
    ENABLE_CORS: bool = Field(default=True, description="Enable CORS middleware")
    CORS_ORIGINS: str = Field(default="*", description="Allowed CORS origins (comma-separated)")
    
    # ============================================
    # Rate Limiting
    # ============================================
    ENABLE_RATE_LIMITING: bool = Field(default=False, description="Enable rate limiting")
    RATE_LIMIT_PER_MINUTE: int = Field(default=100, ge=1, description="Requests per minute per IP")
    
    # ============================================
    # Azure OpenAI Configuration
    # ============================================
    AZURE_AI_PROJECT_ENDPOINT: str = Field(..., description="Azure AI project endpoint URL")
    AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME: str = Field(default="gpt-4o", description="Deployment name")
    AZURE_OPENAI_API_KEY: str = Field(..., description="Azure OpenAI API key")
    
    # ============================================
    # MCP Server Configuration
    # ============================================
    MCP_SERVER_URL: str = Field(default="http://localhost:8000/mcp", description="MCP server URL")
    MCP_SERVER_REQUIRED: bool = Field(default=False, description="Fail startup if MCP unavailable")
    
    # ============================================
    # Database Configuration
    # ============================================
    ORDER_DB_PATH: str = Field(default="./data/orders.db", description="SQLite database path")
    
    # ============================================
    # Email Configuration
    # ============================================
    SMTP_SERVER: str = Field(..., description="SMTP server address")
    SMTP_PORT: int = Field(default=587, ge=1, le=65535, description="SMTP server port")
    SENDER_EMAIL: str = Field(..., description="Sender email address")
    SENDER_PASSWORD: str = Field(..., description="Sender email password/app password")
    SENDER_NAME: str = Field(default="Customer Service", description="Sender display name")
    
    # ============================================
    # Logging Configuration
    # ============================================
    LOG_TO_FILE: bool = Field(default=True, description="Enable file logging")
    LOG_FILE_PATH: str = Field(default="./logs/app.log", description="Log file path")
    LOG_MAX_SIZE_MB: int = Field(default=100, ge=1, description="Max log file size in MB")
    LOG_BACKUP_COUNT: int = Field(default=5, ge=0, description="Number of log backups")
    
    # ============================================
    # Agent Configuration
    # ============================================
    AGENT_NAME: str = Field(default="CustomerServiceAgent", description="Agent name")
    AGENT_MODEL: str = Field(default="gpt-4o", description="AI model name")
    AGENT_MAX_TURNS: int = Field(default=10, ge=1, description="Max conversation turns")
    AGENT_TIMEOUT_SECONDS: int = Field(default=300, ge=10, description="Agent timeout in seconds")
    
    # ============================================
    # Session Configuration
    # ============================================
    SESSION_CLEANUP_ENABLED: bool = Field(default=False, description="Enable session cleanup")
    SESSION_MAX_AGE_HOURS: int = Field(default=24, ge=1, description="Session max age in hours")
    SESSION_CLEANUP_INTERVAL_MINUTES: int = Field(default=60, ge=1, description="Cleanup interval")
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )
    
    @field_validator("LOG_LEVEL")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level is a valid Python logging level"""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        v_upper = v.upper()
        if v_upper not in valid_levels:
            raise ValueError(f"LOG_LEVEL must be one of: {', '.join(valid_levels)}")
        return v_upper
    
    @field_validator("AZURE_AI_PROJECT_ENDPOINT", "MCP_SERVER_URL")
    @classmethod
    def validate_url(cls, v: str) -> str:
        """Validate URL format"""
        if not v.startswith(("http://", "https://")):
            raise ValueError("URL must start with http:// or https://")
        return v.rstrip("/")
    
    @field_validator("SENDER_EMAIL")
    @classmethod
    def validate_email(cls, v: str) -> str:
        """Basic email validation"""
        if "@" not in v or "." not in v.split("@")[1]:
            raise ValueError("Invalid email address format")
        return v.lower()
    
    @property
    def cors_origins_list(self) -> list[str]:
        """Parse CORS origins into a list"""
        if self.CORS_ORIGINS == "*":
            return ["*"]
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    @property
    def log_max_bytes(self) -> int:
        """Convert log size from MB to bytes"""
        return self.LOG_MAX_SIZE_MB * 1024 * 1024
    
    @property
    def api_host(self) -> str:
        """Alias for SERVER_HOST"""
        return self.SERVER_HOST
    
    @property
    def api_port(self) -> int:
        """Alias for SERVER_PORT"""
        return self.SERVER_PORT
    
    @property
    def database_path(self) -> str:
        """Alias for ORDER_DB_PATH"""
        return self.ORDER_DB_PATH
    
    @property
    def log_level(self) -> str:
        """Lowercase log level for uvicorn"""
        return self.LOG_LEVEL.lower()
    
    # Azure OpenAI aliases (snake_case)
    @property
    def azure_ai_project_endpoint(self) -> str:
        """Alias for AZURE_AI_PROJECT_ENDPOINT"""
        return self.AZURE_AI_PROJECT_ENDPOINT
    
    @property
    def azure_openai_model_name(self) -> str:
        """Alias for AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME"""
        return self.AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME
    
    @property
    def azure_openai_api_key(self) -> str:
        """Alias for AZURE_OPENAI_API_KEY"""
        return self.AZURE_OPENAI_API_KEY
    
    # MCP Server aliases (snake_case)
    @property
    def mcp_server_url(self) -> str:
        """Alias for MCP_SERVER_URL"""
        return self.MCP_SERVER_URL
    
    @property
    def mcp_server_required(self) -> bool:
        """Alias for MCP_SERVER_REQUIRED"""
        return self.MCP_SERVER_REQUIRED
    
    # Email aliases (snake_case)
    @property
    def smtp_server(self) -> str:
        """Alias for SMTP_SERVER"""
        return self.SMTP_SERVER
    
    @property
    def smtp_port(self) -> int:
        """Alias for SMTP_PORT"""
        return self.SMTP_PORT
    
    @property
    def sender_email(self) -> str:
        """Alias for SENDER_EMAIL"""
        return self.SENDER_EMAIL
    
    @property
    def sender_password(self) -> str:
        """Alias for SENDER_PASSWORD"""
        return self.SENDER_PASSWORD
    
    @property
    def sender_name(self) -> str:
        """Alias for SENDER_NAME"""
        return self.SENDER_NAME
    
    def mask_sensitive(self) -> dict:
        """Return configuration with sensitive data masked"""
        config = self.model_dump()
        
        # Mask sensitive fields
        sensitive_fields = [
            "AZURE_OPENAI_API_KEY",
            "SENDER_PASSWORD",
        ]
        
        for field in sensitive_fields:
            if field in config and config[field]:
                # Show first 4 and last 4 characters
                value = config[field]
                if len(value) > 8:
                    config[field] = f"{value[:4]}...{value[-4:]}"
                else:
                    config[field] = "***"
        
        return config
    
    def display_config(self) -> str:
        """Return formatted configuration for display"""
        masked = self.mask_sensitive()
        
        lines = ["Configuration:"]
        lines.append("=" * 60)
        
        sections = {
            "Server": ["SERVER_HOST", "SERVER_PORT", "LOG_LEVEL"],
            "CORS": ["ENABLE_CORS", "CORS_ORIGINS"],
            "Rate Limiting": ["ENABLE_RATE_LIMITING", "RATE_LIMIT_PER_MINUTE"],
            "Azure OpenAI": ["AZURE_AI_PROJECT_ENDPOINT", "AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME", "AZURE_OPENAI_API_KEY"],
            "MCP Server": ["MCP_SERVER_URL", "MCP_SERVER_REQUIRED"],
            "Database": ["ORDER_DB_PATH"],
            "Email": ["SMTP_SERVER", "SMTP_PORT", "SENDER_EMAIL", "SENDER_PASSWORD", "SENDER_NAME"],
            "Logging": ["LOG_TO_FILE", "LOG_FILE_PATH", "LOG_MAX_SIZE_MB", "LOG_BACKUP_COUNT"],
            "Agent": ["AGENT_NAME", "AGENT_MODEL", "AGENT_MAX_TURNS", "AGENT_TIMEOUT_SECONDS"],
            "Session": ["SESSION_CLEANUP_ENABLED", "SESSION_MAX_AGE_HOURS", "SESSION_CLEANUP_INTERVAL_MINUTES"],
        }
        
        for section, fields in sections.items():
            lines.append(f"\n{section}:")
            for field in fields:
                value = masked.get(field, "N/A")
                lines.append(f"  {field}: {value}")
        
        lines.append("=" * 60)
        return "\n".join(lines)


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance (singleton pattern).
    
    Returns:
        Settings: Application settings instance
    """
    return Settings()


# Convenience function to access settings
def get_config() -> Settings:
    """Alias for get_settings()"""
    return get_settings()
