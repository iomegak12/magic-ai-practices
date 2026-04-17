"""
Configuration module for Complaint Manager
Loads environment variables and provides configuration settings
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)


class Config:
    """Configuration class for the application"""
    
    # Server Configuration
    SERVER_NAME = os.getenv('SERVER_NAME', 'complaint-management-server')
    SERVER_VERSION = os.getenv('SERVER_VERSION', '1.0.0')
    SERVER_HOST = os.getenv('SERVER_HOST', '0.0.0.0')
    SERVER_PORT = int(os.getenv('SERVER_PORT', '8000'))
    MCP_MOUNT_PATH = os.getenv('MCP_MOUNT_PATH', '/mcp')
    
    # Database Configuration
    DATABASE_PATH = os.getenv('DATABASE_PATH', 'db/complaints.db')
    
    # Seed Database Configuration
    SEED_DATABASE = os.getenv('SEED_DATABASE', 'false').lower() in ('true', '1', 'yes')
    
    # Complaint Status Options
    VALID_STATUSES = ["New", "Open", "In Progress", "Resolved", "Closed"]
    
    # Complaint Priority Options
    VALID_PRIORITIES = ["Low", "Medium", "High", "Critical"]
    
    @classmethod
    def get_db_path(cls) -> Path:
        """Get the absolute database path"""
        base_dir = Path(__file__).parent.parent
        db_path = base_dir / cls.DATABASE_PATH
        # Ensure the db directory exists
        db_path.parent.mkdir(parents=True, exist_ok=True)
        return db_path


config = Config()
