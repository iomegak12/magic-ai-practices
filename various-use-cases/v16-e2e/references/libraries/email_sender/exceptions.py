"""
Custom exceptions for email sender library.
"""


class EmailSenderError(Exception):
    """Base exception for email sender library."""
    pass


class ConfigurationError(EmailSenderError):
    """Raised when email configuration is invalid or missing."""
    pass


class ValidationError(EmailSenderError):
    """Raised when email data validation fails."""
    pass


class SMTPConnectionError(EmailSenderError):
    """Raised when SMTP connection fails."""
    pass


class EmailSendError(EmailSenderError):
    """Raised when sending email fails."""
    pass
