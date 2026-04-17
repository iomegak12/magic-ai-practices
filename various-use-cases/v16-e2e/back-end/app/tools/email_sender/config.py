"""
Email configuration management for Gmail SMTP.
"""
import os
from .exceptions import ConfigurationError


class EmailConfig:
    """Email configuration class."""
    
    def __init__(self, smtp_server=None, smtp_port=None, sender_email=None, 
                 sender_password=None, sender_name=None):
        """
        Initialize email configuration.
        
        Args:
            smtp_server: SMTP server address (default: from settings)
            smtp_port: SMTP port (default: from settings)
            sender_email: Sender email address (default: from settings)
            sender_password: Sender password (default: from settings

)
            sender_name: Sender display name (default: from settings)
        """
        # Allow passing configuration directly (for testing or custom setup)
        # Otherwise will be initialized from application settings
        self.smtp_server = smtp_server or os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = smtp_port or int(os.getenv('SMTP_PORT', '587'))
        self.sender_email = sender_email or os.getenv('SENDER_EMAIL')
        self.sender_password = sender_password or os.getenv('SENDER_PASSWORD')
        self.sender_name = sender_name or os.getenv('SENDER_NAME', '')
        
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
    _config = EmailConfig()
    return _config


def set_email_config(config: EmailConfig):
    """
    Set custom email configuration.
    
    Args:
        config: EmailConfig instance
    """
    global _config
    _config = config
