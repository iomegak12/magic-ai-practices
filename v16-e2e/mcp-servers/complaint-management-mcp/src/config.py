"""
Configuration Management

This module handles loading and validating configuration from environment variables.

Classes:
    - Config: Configuration class with all application settings
"""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv


class Config:
    """
    Application configuration loaded from environment variables.
    
    Attributes:
        server_name: Name of the MCP server
        server_description: Description of the server
        server_version: Server version
        host: Server host address
        port: Server port number
        mount_path: MCP endpoint mount path
        database_path: Path to SQLite database file
        database_echo: Enable SQL query logging
        auto_seed: Auto-seed database on startup
        seed_count: Number of records to seed
        log_level: Logging level
        log_format: Log message format
        timezone: Application timezone
    """
    
    def __init__(self):
        """Initialize configuration from environment variables."""
        # Load .env file if it exists
        env_path = Path(__file__).parent.parent / '.env'
        if env_path.exists():
            load_dotenv(env_path)
        
        # Server Configuration
        self.server_name = os.getenv('MCP_SERVER_NAME', 'complaint-management-server')
        self.server_description = os.getenv(
            'MCP_SERVER_DESCRIPTION',
            'MCP Server for managing customer complaints and orders'
        )
        self.server_version = os.getenv('MCP_SERVER_VERSION', '1.0.0')
        self.host = os.getenv('MCP_SERVER_HOST', '0.0.0.0')
        self.port = int(os.getenv('MCP_SERVER_PORT', '8000'))
        self.mount_path = os.getenv('MCP_MOUNT_PATH', '/mcp')
        
        # Database Configuration
        self.database_path = os.getenv('DATABASE_PATH', 'db/complaints.db')
        self.database_echo = os.getenv('DATABASE_ECHO', 'false').lower() == 'true'
        
        # Seeding Configuration
        self.auto_seed = os.getenv('AUTO_SEED_DATABASE', 'true').lower() == 'true'
        self.seed_count = int(os.getenv('SEED_RECORD_COUNT', '20'))
        
        # Logging Configuration
        self.log_level = os.getenv('LOG_LEVEL', 'INFO')
        self.log_format = os.getenv(
            'LOG_FORMAT',
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Application Settings
        self.timezone = os.getenv('TIMEZONE', 'UTC')
    
    def validate(self) -> tuple[bool, Optional[str]]:
        """
        Validate configuration values.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Validate port range
        if not (1 <= self.port <= 65535):
            return False, f"Invalid port number: {self.port}. Must be between 1 and 65535."
        
        # Validate seed count
        if self.seed_count < 0:
            return False, f"Invalid seed count: {self.seed_count}. Must be non-negative."
        
        # Validate log level
        valid_log_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if self.log_level.upper() not in valid_log_levels:
            return False, f"Invalid log level: {self.log_level}. Must be one of {valid_log_levels}."
        
        return True, None
    
    def get_database_url(self) -> str:
        """
        Get SQLAlchemy database URL.
        
        Returns:
            SQLite database URL string
        """
        # Ensure database directory exists
        db_path = Path(self.database_path)
        db_dir = db_path.parent
        
        # Create parent directory if it doesn't exist
        if not db_dir.exists():
            # Get absolute path relative to project root
            project_root = Path(__file__).parent.parent
            full_db_dir = project_root / db_dir
            full_db_dir.mkdir(parents=True, exist_ok=True)
        
        # Return SQLite URL with absolute path
        project_root = Path(__file__).parent.parent
        abs_db_path = (project_root / db_path).resolve()
        return f"sqlite:///{abs_db_path}"
    
    def __repr__(self) -> str:
        """String representation of configuration (masks sensitive values)."""
        return (
            f"Config(server_name='{self.server_name}', "
            f"host='{self.host}', "
            f"port={self.port}, "
            f"database_path='{self.database_path}', "
            f"auto_seed={self.auto_seed})"
        )


# Global configuration instance
_config: Optional[Config] = None


def get_config() -> Config:
    """
    Get or create the global configuration instance.
    
    Returns:
        Config instance
    """
    global _config
    if _config is None:
        _config = Config()
    return _config


def load_config() -> Config:
    """
    Load and validate configuration.
    
    Returns:
        Validated Config instance
        
    Raises:
        ValueError: If configuration is invalid
    """
    config = get_config()
    is_valid, error_message = config.validate()
    
    if not is_valid:
        raise ValueError(f"Invalid configuration: {error_message}")
    
    return config
