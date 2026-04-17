"""
Unit Tests for Configuration

Tests for app/config/settings.py configuration management.
"""
import pytest
import os
from pathlib import Path
from app.config.settings import Settings, get_settings


class TestSettings:
    """Tests for Settings class."""
    
    def test_settings_from_env(self, test_env_vars):
        """Test settings loaded from environment variables."""
        settings = Settings()
        
        assert settings.azure_ai_project_endpoint == test_env_vars["AZURE_AI_PROJECT_ENDPOINT"]
        assert settings.azure_openai_model_name == test_env_vars["AZURE_OPENAI_MODEL_NAME"]
        assert settings.sender_email == test_env_vars["SENDER_EMAIL"]
        assert settings.api_port == int(test_env_vars["API_PORT"])
    
    def test_settings_defaults(self):
        """Test settings with default values."""
        # Clear specific env var
        original = os.environ.pop("LOG_LEVEL", None)
        
        try:
            settings = Settings()
            # Should have default log level
            assert hasattr(settings, "log_level")
        finally:
            if original:
                os.environ["LOG_LEVEL"] = original
    
    def test_database_path_type(self, test_env_vars):
        """Test database path is Path object."""
        settings = Settings()
        
        assert isinstance(settings.database_path, Path)
    
    def test_smtp_port_type(self, test_env_vars):
        """Test SMTP port is integer."""
        settings = Settings()
        
        assert isinstance(settings.smtp_port, int)
        assert settings.smtp_port > 0
    
    def test_api_port_type(self, test_env_vars):
        """Test API port is integer."""
        settings = Settings()
        
        assert isinstance(settings.api_port, int)
        assert settings.api_port > 0
    
    def test_mcp_server_required_type(self, test_env_vars):
        """Test MCP server required is boolean."""
        settings = Settings()
        
        assert isinstance(settings.mcp_server_required, bool)


class TestSettingsSingleton:
    """Tests for settings singleton pattern."""
    
    def test_get_settings_singleton(self, test_env_vars):
        """Test get_settings returns same instance."""
        settings1 = get_settings()
        settings2 = get_settings()
        
        assert settings1 is settings2
    
    def test_get_settings_caches_instance(self, test_env_vars):
        """Test settings instance is cached."""
        from app.config import settings as settings_module
        
        # Clear cache
        settings_module._settings = None
        
        settings1 = get_settings()
        settings2 = get_settings()
        
        assert settings1 is settings2


class TestSettingsValidation:
    """Tests for settings validation."""
    
    def test_valid_log_level(self, test_env_vars):
        """Test valid log level values."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        
        for level in valid_levels:
            os.environ["LOG_LEVEL"] = level
            settings = Settings()
            assert settings.log_level == level
    
    def test_display_config_masks_sensitive(self, test_env_vars):
        """Test display_config masks sensitive values."""
        settings = Settings()
        config_str = settings.display_config()
        
        # Should not contain actual sensitive values
        assert test_env_vars["AZURE_OPENAI_API_KEY"] not in config_str
        assert test_env_vars["SENDER_PASSWORD"] not in config_str
        
        # Should contain masked indicators
        assert "***" in config_str or "..." in config_str


class TestConfigurationPaths:
    """Tests for configuration path handling."""
    
    def test_log_directory_path(self, test_env_vars):
        """Test log directory is Path object."""
        settings = Settings()
        
        assert isinstance(settings.log_directory, Path)
    
    def test_data_directory_path(self, test_env_vars):
        """Test data directory is Path object."""
        settings = Settings()
        
        assert isinstance(settings.data_directory, Path)


class TestEnvironmentVariables:
    """Tests for environment variable handling."""
    
    def test_missing_optional_env_var(self):
        """Test handling of missing optional environment variable."""
        # SENDER_NAME is optional
        original = os.environ.pop("SENDER_NAME", None)
        
        try:
            settings = Settings()
            # Should not raise, should have default or None
            assert hasattr(settings, "sender_name")
        finally:
            if original:
                os.environ["SENDER_NAME"] = original
    
    def test_env_var_type_conversion(self, test_env_vars):
        """Test environment variables are converted to correct types."""
        settings = Settings()
        
        # Integer conversions
        assert isinstance(settings.api_port, int)
        assert isinstance(settings.smtp_port, int)
        
        # Boolean conversions
        assert isinstance(settings.mcp_server_required, bool)
        
        # String values stay as strings
        assert isinstance(settings.api_host, str)
        assert isinstance(settings.log_level, str)
