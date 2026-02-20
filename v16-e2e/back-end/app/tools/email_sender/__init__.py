"""
Email Sender Library

A Python library for sending emails using Gmail SMTP with app passwords.

Features:
- Send plain text and HTML emails
- Support for CC and BCC recipients
- File attachments support
- Configurable via .env file
- Gmail SMTP with app password authentication
- Connection testing

Usage:
    from email_sender import send_email, send_text_email, test_connection
    
    # Test connection
    result = test_connection()
    
    # Send simple text email
    result = send_text_email(
        recipients="recipient@example.com",
        subject="Hello",
        body="This is a test email"
    )
    
    # Send HTML email with attachments
    result = send_email(
        recipients=["user1@example.com", "user2@example.com"],
        subject="Report",
        body="<h1>Monthly Report</h1><p>See attachment</p>",
        html=True,
        attachments=["report.pdf"]
    )
"""

__version__ = "1.0.0"

# Configuration
from .config import (
    get_email_config,
    reload_config,
    EmailConfig
)

# Operations
from .operations import (
    send_email,
    send_text_email,
    send_html_email,
    send_email_with_attachments,
    test_connection
)

# Exceptions
from .exceptions import (
    EmailSenderError,
    ConfigurationError,
    ValidationError,
    SMTPConnectionError,
    EmailSendError
)

# Public API
__all__ = [
    # Configuration
    "get_email_config",
    "reload_config",
    "EmailConfig",
    
    # Operations
    "send_email",
    "send_text_email",
    "send_html_email",
    "send_email_with_attachments",
    "test_connection",
    
    # Exceptions
    "EmailSenderError",
    "ConfigurationError",
    "ValidationError",
    "SMTPConnectionError",
    "EmailSendError",
]
