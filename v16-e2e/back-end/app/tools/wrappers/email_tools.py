"""
Email tools for AI agent.

These tools wrap the email_sender library operations
and expose them to the agent framework using the @tool decorator.
"""
from agent_framework import tool
from typing import Optional, List

# Import email operations
from ..email_sender import (
    send_email,
    send_text_email,
    send_html_email,
    send_email_with_attachments,
    test_connection,
    ValidationError,
    SMTPConnectionError,
    EmailSendError
)


@tool
def send_simple_email(recipients: str, subject: str, body: str, cc: Optional[str] = None) -> dict:
    """
    Send a plain text email to one or more recipients.
    
    Args:
        recipients: Email addresses (comma-separated for multiple recipients)
        subject: Email subject line
        body: Plain text email body
        cc: Optional CC recipients (comma-separated)
        
    Returns:
        dict: Result with status, message, and delivery details
        
    Example:
        ```
        result = send_simple_email(
            recipients="customer@example.com",
            subject="Order Confirmation",
            body="Your order has been confirmed. Order ID: ORD-123"
        )
        
        # With multiple recipients and CC
        result = send_simple_email(
            recipients="customer1@example.com, customer2@example.com",
            subject="Monthly Newsletter",
            body="Here is your monthly update...",
            cc="manager@example.com"
        )
        ```
    """
    try:
        return send_text_email(
            recipients=recipients,
            subject=subject,
            body=body,
            cc=cc
        )
    except (ValidationError, SMTPConnectionError, EmailSendError) as e:
        return {
            "status": "error",
            "error": str(e),
            "error_type": type(e).__name__
        }


@tool
def send_formatted_email(recipients: str, subject: str, html_body: str, cc: Optional[str] = None) -> dict:
    """
    Send an HTML formatted email with styling and formatting.
    
    Args:
        recipients: Email addresses (comma-separated for multiple recipients)
        subject: Email subject line
        html_body: HTML formatted email body
        cc: Optional CC recipients (comma-separated)
        
    Returns:
        dict: Result with status, message, and delivery details
        
    Example:
        ```
        html_content = '''
        <html>
            <body>
                <h1>Order Shipped</h1>
                <p>Your order <b>ORD-123</b> has been shipped.</p>
                <p>Tracking: <a href="https://track.example.com">Track Package</a></p>
            </body>
        </html>
        '''
        
        result = send_formatted_email(
            recipients="customer@example.com",
            subject="Order Shipped - ORD-123",
            html_body=html_content
        )
        ```
    """
    try:
        return send_html_email(
            recipients=recipients,
            subject=subject,
            html_body=html_body,
            cc=cc
        )
    except (ValidationError, SMTPConnectionError, EmailSendError) as e:
        return {
            "status": "error",
            "error": str(e),
            "error_type": type(e).__name__
        }


@tool
def send_email_with_files(
    recipients: str,
    subject: str,
    body: str,
    attachment_paths: List[str],
    html: bool = False,
    cc: Optional[str] = None
) -> dict:
    """
    Send an email with file attachments.
    
    Args:
        recipients: Email addresses (comma-separated for multiple recipients)
        subject: Email subject line
        body: Email body (plain text or HTML)
        attachment_paths: List of file paths to attach
        html: If True, body is treated as HTML (default: False for plain text)
        cc: Optional CC recipients (comma-separated)
        
    Returns:
        dict: Result with status, message, and delivery details
        
    Example:
        ```
        result = send_email_with_files(
            recipients="customer@example.com",
            subject="Monthly Report",
            body="Please find the monthly report attached.",
            attachment_paths=["./data/report.pdf", "./data/summary.xlsx"]
        )
        ```
    """
    try:
        return send_email_with_attachments(
            recipients=recipients,
            subject=subject,
            body=body,
            attachments=attachment_paths,
            html=html,
            cc=cc
        )
    except (ValidationError, SMTPConnectionError, EmailSendError) as e:
        return {
            "status": "error",
            "error": str(e),
            "error_type": type(e).__name__
        }


@tool
def send_complete_email(
    recipients: str,
    subject: str,
    body: str,
    html: bool = False,
    cc: Optional[str] = None,
    bcc: Optional[str] = None,
    attachments: Optional[List[str]] = None
) -> dict:
    """
    Send an email with full control over all options.
    This is the most flexible email tool supporting all features.
    
    Args:
        recipients: Email addresses (comma-separated for multiple recipients)
        subject: Email subject line
        body: Email body content
        html: If True, body is treated as HTML (default: False for plain text)
        cc: Optional CC recipients (comma-separated)
        bcc: Optional BCC recipients (comma-separated)
        attachments: Optional list of file paths to attach
        
    Returns:
        dict: Result with status, message, and delivery details
        
    Example:
        ```
        result = send_complete_email(
            recipients="customer@example.com",
            subject="Order Update",
            body="<h1>Order Delivered</h1><p>Your order has been delivered.</p>",
            html=True,
            cc="manager@example.com",
            bcc="archive@example.com",
            attachments=["./data/invoice.pdf"]
        )
        ```
    """
    try:
        return send_email(
            recipients=recipients,
            subject=subject,
            body=body,
            html=html,
            cc=cc,
            bcc=bcc,
            attachments=attachments
        )
    except (ValidationError, SMTPConnectionError, EmailSendError) as e:
        return {
            "status": "error",
            "error": str(e),
            "error_type": type(e).__name__
        }


@tool
def test_email_connection() -> dict:
    """
    Test the SMTP connection and authentication.
    Use this to verify email configuration is correct.
    
    Returns:
        dict: Connection test result with status and server details
        
    Example:
        ```
        result = test_email_connection()
        ```
    """
    try:
        return test_connection()
    except (SMTPConnectionError, Exception) as e:
        return {
            "status": "error",
            "error": str(e),
            "error_type": type(e).__name__
        }


# Export all tools
__all__ = [
    "send_simple_email",
    "send_formatted_email",
    "send_email_with_files",
    "send_complete_email",
    "test_email_connection"
]
