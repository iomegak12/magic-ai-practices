"""
Email validation utilities.
"""
import re
from .exceptions import ValidationError


def validate_email_address(email):
    """
    Validate email address format.
    
    Args:
        email: Email address to validate
        
    Returns:
        bool: True if email is valid
        
    Raises:
        ValidationError: If email format is invalid
    """
    if not email or not isinstance(email, str):
        raise ValidationError("Email address must be a non-empty string")
    
    # Basic email regex pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(pattern, email.strip()):
        raise ValidationError(f"Invalid email address format: {email}")
    
    return True


def validate_recipients(recipients):
    """
    Validate recipients list.
    
    Args:
        recipients: String of comma-separated emails or list of emails
        
    Returns:
        list: List of valid email addresses
        
    Raises:
        ValidationError: If any email is invalid
    """
    if not recipients:
        raise ValidationError("At least one recipient is required")
    
    # Convert string to list if needed
    if isinstance(recipients, str):
        recipients = [r.strip() for r in recipients.split(",")]
    elif not isinstance(recipients, list):
        raise ValidationError("Recipients must be a string or list")
    
    # Validate each email
    validated_emails = []
    for email in recipients:
        if email:  # Skip empty strings
            validate_email_address(email)
            validated_emails.append(email.strip())
    
    if not validated_emails:
        raise ValidationError("At least one valid recipient is required")
    
    return validated_emails


def validate_email_data(recipients, subject, body, cc=None, bcc=None):
    """
    Validate all email data.
    
    Args:
        recipients: String or list of recipient emails
        subject: Email subject
        body: Email body content
        cc: Optional CC recipients
        bcc: Optional BCC recipients
        
    Returns:
        dict: Dictionary with validated data
        
    Raises:
        ValidationError: If any validation fails
    """
    # Validate recipients
    validated_to = validate_recipients(recipients)
    
    # Validate subject
    if not subject or not isinstance(subject, str):
        raise ValidationError("Email subject must be a non-empty string")
    
    # Validate body
    if not body or not isinstance(body, str):
        raise ValidationError("Email body must be a non-empty string")
    
    # Validate CC if provided
    validated_cc = []
    if cc:
        validated_cc = validate_recipients(cc)
    
    # Validate BCC if provided
    validated_bcc = []
    if bcc:
        validated_bcc = validate_recipients(bcc)
    
    return {
        "to": validated_to,
        "cc": validated_cc,
        "bcc": validated_bcc,
        "subject": subject.strip(),
        "body": body
    }


def validate_attachments(attachments):
    """
    Validate attachment file paths.
    
    Args:
        attachments: List of file paths
        
    Returns:
        list: List of valid file paths
        
    Raises:
        ValidationError: If any file doesn't exist
    """
    import os
    
    if not attachments:
        return []
    
    if not isinstance(attachments, list):
        raise ValidationError("Attachments must be a list of file paths")
    
    validated_files = []
    for filepath in attachments:
        if not isinstance(filepath, str):
            raise ValidationError(f"Attachment path must be a string: {filepath}")
        
        if not os.path.isfile(filepath):
            raise ValidationError(f"Attachment file not found: {filepath}")
        
        validated_files.append(filepath)
    
    return validated_files
