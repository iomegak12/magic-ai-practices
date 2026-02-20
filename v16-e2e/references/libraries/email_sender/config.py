"""
Email configuration management for Gmail SMTP.
"""
import os
from dotenv import load_dotenv
from .exceptions import ConfigurationError

# Load environment variables
load_dotenv()


class EmailConfig:
    """Email configuration class."""
    
    def __init__(self):
        """Initialize email configuration from environment variables."""
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.sender_email = os.getenv('SENDER_EMAIL')
        self.sender_password = os.getenv('SENDER_PASSWORD')
        self.sender_name = os.getenv('SENDER_NAME', '')
        
        # Validate configuration
        self._validate()
    
    def _validate(self):
        """
        Validate that required configuration is present.
        
        Raises:
            ConfigurationError: If required configuration is missing
        """
        if not self.sender_email:
            raise ConfigurationError(
                "SENDER_EMAIL is not configured. Please set it in your .env file."
            )
        
        if not self.sender_password:
            raise ConfigurationError(
                "SENDER_PASSWORD is not configured. Please set it in your .env file."
            )
        
        if not self.smtp_server:
            raise ConfigurationError(
                "SMTP_SERVER is not configured. Please set it in your .env file."
            )
    
    def get_sender_address(self):
        """
        Get formatted sender address.
        
        Returns:
            str: Formatted sender address with name if available
        """
        if self.sender_name:
            return f"{self.sender_name} <{self.sender_email}>"
        return self.sender_email
    
    def __repr__(self):
        return f"<EmailConfig(server={self.smtp_server}, port={self.smtp_port}, sender={self.sender_email})>"


# Global configuration instance
_config = None


def get_email_config():
    """
    Get the email configuration instance.
    
    Returns:
        EmailConfig: Email configuration object
        
    Raises:
        ConfigurationError: If configuration is invalid
    """
    global _config
    if _config is None:
        _config = EmailConfig()
    return _config


def reload_config():
    """
    Reload configuration from environment variables.
    Useful if .env file is updated during runtime.
    
    Returns:
        EmailConfig: New email configuration object
    """
    global _config
    load_dotenv(override=True)
    _config = EmailConfig()
    return _config
