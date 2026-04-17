"""
Email operations for sending emails via Gmail SMTP.
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os

from .config import get_email_config
from .validations import validate_email_data, validate_attachments
from .exceptions import SMTPConnectionError, EmailSendError


def send_email(recipients, subject, body, html=False, cc=None, bcc=None, attachments=None):
    """
    Send an email using Gmail SMTP.
    
    Args:
        recipients: String of comma-separated emails or list of emails
        subject: Email subject line
        body: Email body content
        html: If True, send as HTML email (default: False for plain text)
        cc: Optional CC recipients (string or list)
        bcc: Optional BCC recipients (string or list)
        attachments: Optional list of file paths to attach
        
    Returns:
        dict: Result with status, message, and details
        
    Raises:
        ValidationError: If email data is invalid
        SMTPConnectionError: If SMTP connection fails
        EmailSendError: If sending email fails
    """
    try:
        # Get configuration
        config = get_email_config()
        
        # Validate email data
        validated = validate_email_data(recipients, subject, body, cc, bcc)
        
        # Validate attachments if provided
        validated_attachments = validate_attachments(attachments) if attachments else []
        
        # Create message
        message = MIMEMultipart()
        message['From'] = config.get_sender_address()
        message['To'] = ", ".join(validated['to'])
        message['Subject'] = validated['subject']
        
        if validated['cc']:
            message['Cc'] = ", ".join(validated['cc'])
        
        # Add body
        content_type = 'html' if html else 'plain'
        message.attach(MIMEText(validated['body'], content_type))
        
        # Add attachments
        for filepath in validated_attachments:
            filename = os.path.basename(filepath)
            
            with open(filepath, 'rb') as file:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(file.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename= {filename}')
                message.attach(part)
        
        # Combine all recipients
        all_recipients = validated['to'] + validated['cc'] + validated['bcc']
        
        # Connect and send
        try:
            with smtplib.SMTP(config.smtp_server, config.smtp_port) as server:
                server.starttls()
                server.login(config.sender_email, config.sender_password)
                server.sendmail(config.sender_email, all_recipients, message.as_string())
        except smtplib.SMTPAuthenticationError as e:
            raise SMTPConnectionError(f"SMTP authentication failed: {str(e)}")
        except smtplib.SMTPException as e:
            raise SMTPConnectionError(f"SMTP connection error: {str(e)}")
        except Exception as e:
            raise EmailSendError(f"Failed to send email: {str(e)}")
        
        return {
            "status": "success",
            "message": "Email sent successfully",
            "recipients": validated['to'],
            "cc": validated['cc'],
            "bcc": validated['bcc'],
            "subject": validated['subject'],
            "attachments": len(validated_attachments)
        }
        
    except (SMTPConnectionError, EmailSendError):
        raise
    except Exception as e:
        raise EmailSendError(f"Unexpected error sending email: {str(e)}")


def send_text_email(recipients, subject, body, cc=None, bcc=None):
    """
    Send a plain text email.
    
    Args:
        recipients: String of comma-separated emails or list of emails
        subject: Email subject line
        body: Plain text email body
        cc: Optional CC recipients
        bcc: Optional BCC recipients
        
    Returns:
        dict: Result with status and details
    """
    return send_email(recipients, subject, body, html=False, cc=cc, bcc=bcc)


def send_html_email(recipients, subject, html_body, cc=None, bcc=None):
    """
    Send an HTML formatted email.
    
    Args:
        recipients: String of comma-separated emails or list of emails
        subject: Email subject line
        html_body: HTML formatted email body
        cc: Optional CC recipients
        bcc: Optional BCC recipients
        
    Returns:
        dict: Result with status and details
    """
    return send_email(recipients, subject, html_body, html=True, cc=cc, bcc=bcc)


def send_email_with_attachments(recipients, subject, body, attachments, html=False, cc=None, bcc=None):
    """
    Send an email with file attachments.
    
    Args:
        recipients: String of comma-separated emails or list of emails
        subject: Email subject line
        body: Email body content
        attachments: List of file paths to attach
        html: If True, send as HTML email (default: False)
        cc: Optional CC recipients
        bcc: Optional BCC recipients
        
    Returns:
        dict: Result with status and details
    """
    return send_email(recipients, subject, body, html=html, cc=cc, bcc=bcc, attachments=attachments)


def test_connection():
    """
    Test SMTP connection and authentication.
    
    Returns:
        dict: Result with status and message
        
    Raises:
        ConfigurationError: If configuration is invalid
        SMTPConnectionError: If connection test fails
    """
    try:
        config = get_email_config()
        
        with smtplib.SMTP(config.smtp_server, config.smtp_port, timeout=10) as server:
            server.starttls()
            server.login(config.sender_email, config.sender_password)
        
        return {
            "status": "success",
            "message": "SMTP connection successful",
            "server": config.smtp_server,
            "port": config.smtp_port,
            "sender": config.sender_email
        }
        
    except smtplib.SMTPAuthenticationError as e:
        raise SMTPConnectionError(f"SMTP authentication failed: {str(e)}")
    except smtplib.SMTPException as e:
        raise SMTPConnectionError(f"SMTP connection error: {str(e)}")
    except Exception as e:
        raise SMTPConnectionError(f"Connection test failed: {str(e)}")
