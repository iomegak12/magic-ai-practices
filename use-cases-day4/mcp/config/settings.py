"""
Configuration module for Orders & Complaints MCP Server.
Loads environment variables and provides centralized settings.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


class Settings:
    """Centralized configuration loaded from environment variables."""

    # Server
    SERVER_NAME = os.getenv("SERVER_NAME", "orders-complaints-mcp-server")
    SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
    SERVER_PORT = int(os.getenv("SERVER_PORT", "8700"))

    # Database
    DB_NAME = os.getenv("DB_NAME", "orders_complaints.db")

    # Seeding
    SEED_ON_STARTUP = os.getenv("SEED_ON_STARTUP", "true").lower() in ("true", "1", "yes")

    # Rate Limiting (per-client IP)
    RATE_LIMIT_ENABLED = os.getenv("RATE_LIMIT_ENABLED", "false").lower() in ("true", "1", "yes")
    RATE_LIMIT_MAX_REQUESTS = int(os.getenv("RATE_LIMIT_MAX_REQUESTS", "50"))
    RATE_LIMIT_WINDOW_SECONDS = int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", "60"))

    # Validation enums
    VALID_ORDER_STATUSES = [
        "Pending",
        "Processing",
        "Shipped",
        "Delivered",
        "Cancelled",
        "Returned",
    ]

    VALID_COMPLAINT_PRIORITIES = ["Low", "Medium", "High", "Critical"]

    VALID_COMPLAINT_STATUSES = [
        "Open",
        "In Progress",
        "Resolved",
        "Closed",
        "Escalated",
    ]

    DEFAULT_COMPLAINT_PRIORITY = "Medium"
    DEFAULT_COMPLAINT_STATUS = "Open"
    DEFAULT_ASSIGNED_TO = "Unassigned"

    @classmethod
    def get_db_path(cls) -> Path:
        """Return the absolute database path, creating parent dirs if needed."""
        base_dir = Path(__file__).parent.parent
        db_path = base_dir / cls.DB_NAME
        db_path.parent.mkdir(parents=True, exist_ok=True)
        return db_path


settings = Settings()
