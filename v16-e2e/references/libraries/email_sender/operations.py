"""
Email sending operations using Gmail SMTP.
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import List, Union, Optional
from pathlib import Path

from .config import get_email_config
from .validations import validate_email_data
from .exceptions import SMTPConnectionError, EmailSendError, ValidationError


def send_email(
    recipients: Union[str, List[str]],
    subject: str,
    body: str,
    cc: Union[str, List[str], None] = None,
    bcc: Union[str, List[str], None] = None,
    html: bool = False,
    attachments: Optional[List[str]] = None
) -> dict:
    """
    Send an email using Gmail SMTP.
    
    Args:
        recipients: Single recipient email or list of emails
        subject: Email subject
        body: Email body (plain text or HTML)
        cc: CC recipients (optional)
        bcc: BCC recipients (optional)
        html: If True, body is treated as HTML (default: False)
        attachments: List of file paths to attach (optional)
        
    Returns:
        dict: Result with status and details
        
    Raises:
        ValidationError: If validation fails
        ConfigurationError: If email configuration is invalid
        SMTPConnectionError: If SMTP connection fails
        EmailSendError: If sending email fails
    """
    # Get configuration
    config = get_email_config()
    
    # Validate email data
    validated_recipients, validated_cc, validated_bcc = validate_email_data(
        recipients, subject, body, cc, bcc
    )
    
    # Create message
    msg = MIMEMultipart()
    msg['From'] = config.get_sender_address()
    msg['To'] = ', '.join(validated_recipients)
    msg['Subject'] = subject
    
    if validated_cc:
        msg['Cc'] = ', '.join(validated_cc)
    
    # Attach body
    mime_type = 'html' if html else 'plain'
    msg.attach(MIMEText(body, mime_type))
    
    # Attach files if provided
    if attachments:
        for file_path in attachments:
            try:
                _attach_file(msg, file_path)
            except Exception as e:
                raise EmailSendError(f"Failed to attach file {file_path}: {str(e)}")
    
    # Combine all recipients
    all_recipients = validated_recipients + validated_cc + validated_bcc
    
    # Send email
    try:
        with smtplib.SMTP(config.smtp_server, config.smtp_port) as server:
            server.starttls()  # Enable TLS encryption
            server.login(config.sender_email, config.sender_password)
            server.send_message(msg, to_addrs=all_recipients)
        
        return {
            "success": True,
            "message": "Email sent successfully",
            "recipients": validated_recipients,
            "cc": validated_cc,
            "bcc": validated_bcc,
            "subject": subject
        }
        
    except smtplib.SMTPAuthenticationError as e:
        raise SMTPConnectionError(
            f"SMTP authentication failed. Check your email and app password: {str(e)}"
        )
    except smtplib.SMTPException as e:
        raise SMTPConnectionError(f"SMTP error occurred: {str(e)}")
    except Exception as e:
        raise EmailSendError(f"Failed to send email: {str(e)}")


def send_text_email(
    recipients: Union[str, List[str]],
    subject: str,
    body: str,
    cc: Union[str, List[str], None] = None,
    bcc: Union[str, List[str], None] = None
) -> dict:
    """
    Send a plain text email.
    
    Args:
        recipients: Single recipient email or list of emails
        subject: Email subject
        body: Plain text email body
        cc: CC recipients (optional)
        bcc: BCC recipients (optional)
        
    Returns:
        dict: Result with status and details
    """
    return send_email(
        recipients=recipients,
        subject=subject,
        body=body,
        cc=cc,
        bcc=bcc,
        html=False
    )


def send_html_email(
    recipients: Union[str, List[str]],
    subject: str,
    html_body: str,
    cc: Union[str, List[str], None] = None,
    bcc: Union[str, List[str], None] = None
) -> dict:
    """
    Send an HTML email.
    
    Args:
        recipients: Single recipient email or list of emails
        subject: Email subject
        html_body: HTML email body
        cc: CC recipients (optional)
        bcc: BCC recipients (optional)
        
    Returns:
        dict: Result with status and details
    """
    return send_email(
        recipients=recipients,
        subject=subject,
        body=html_body,
        cc=cc,
        bcc=bcc,
        html=True
    )


def send_email_with_attachments(
    recipients: Union[str, List[str]],
    subject: str,
    body: str,
    attachments: List[str],
    cc: Union[str, List[str], None] = None,
    bcc: Union[str, List[str], None] = None,
    html: bool = False
) -> dict:
    """
    Send an email with file attachments.
    
    Args:
        recipients: Single recipient email or list of emails
        subject: Email subject
        body: Email body
        attachments: List of file paths to attach
        cc: CC recipients (optional)
        bcc: BCC recipients (optional)
        html: If True, body is treated as HTML (default: False)
        
    Returns:
        dict: Result with status and details
    """
    return send_email(
        recipients=recipients,
        subject=subject,
        body=body,
        cc=cc,
        bcc=bcc,
        html=html,
        attachments=attachments
    )


def _attach_file(msg: MIMEMultipart, file_path: str) -> None:
    """
    Attach a file to the email message.
    
    Args:
        msg: MIMEMultipart message object
        file_path: Path to file to attach
        
    Raises:
        ValidationError: If file doesn't exist
        Exception: If file cannot be read or attached
    """
    path = Path(file_path)
    
    if not path.exists():
        raise ValidationError(f"Attachment file not found: {file_path}")
    
    if not path.is_file():
        raise ValidationError(f"Attachment path is not a file: {file_path}")
    
    # Read file and create attachment
    with open(path, 'rb') as file:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(file.read())
    
    # Encode file in base64
    encoders.encode_base64(part)
    
    # Add header
    part.add_header(
        'Content-Disposition',
        f'attachment; filename= {path.name}'
    )
    
    msg.attach(part)


def test_connection() -> dict:
    """
    Test SMTP connection and authentication.
    
    Returns:
        dict: Test result with status
        
    Raises:
        ConfigurationError: If configuration is invalid
        SMTPConnectionError: If connection fails
    """
    config = get_email_config()
    
    try:
        with smtplib.SMTP(config.smtp_server, config.smtp_port, timeout=10) as server:
            server.starttls()
            server.login(config.sender_email, config.sender_password)
        
        return {
            "success": True,
            "message": "SMTP connection successful",
            "server": config.smtp_server,
            "port": config.smtp_port,
            "email": config.sender_email
        }
        
    except smtplib.SMTPAuthenticationError as e:
        raise SMTPConnectionError(
            f"SMTP authentication failed. Check your email and app password: {str(e)}"
        )
    except smtplib.SMTPException as e:
        raise SMTPConnectionError(f"SMTP error occurred: {str(e)}")
    except Exception as e:
        raise SMTPConnectionError(f"Connection test failed: {str(e)}")
