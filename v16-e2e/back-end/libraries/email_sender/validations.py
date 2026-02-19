"""
Validation logic for email data.
"""
import re
from typing import List, Union
from .exceptions import ValidationError

# Email regex pattern (basic validation)
EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')


def validate_email_address(email: str) -> None:
    """
    Validate email address format.
    
    Args:
        email: Email address to validate
        
    Raises:
        ValidationError: If email format is invalid
    """
    if not email or not isinstance(email, str):
        raise ValidationError("Email address must be a non-empty string")
    
    email = email.strip()
    if not EMAIL_PATTERN.match(email):
        raise ValidationError(f"Invalid email address format: {email}")


def validate_recipient_list(recipients: Union[str, List[str]]) -> List[str]:
    """
    Validate and normalize recipient list.
    
    Args:
        recipients: Single email or list of emails
        
    Returns:
        List[str]: Validated list of email addresses
        
    Raises:
        ValidationError: If any email is invalid
    """
    if isinstance(recipients, str):
        recipients = [recipients]
    
    if not recipients:
        raise ValidationError("At least one recipient is required")
    
    validated = []
    for email in recipients:
        email = email.strip()
        validate_email_address(email)
        validated.append(email)
    
    return validated


def validate_email_data(
    recipients: Union[str, List[str]],
    subject: str,
    body: str,
    cc: Union[str, List[str], None] = None,
    bcc: Union[str, List[str], None] = None
) -> tuple:
    """
    Validate all email data.
    
    Args:
        recipients: Recipient email(s)
        subject: Email subject
        body: Email body
        cc: CC email(s) (optional)
        bcc: BCC email(s) (optional)
        
    Returns:
        tuple: (validated_recipients, validated_cc, validated_bcc)
        
    Raises:
        ValidationError: If validation fails
    """
    # Validate recipients
    validated_recipients = validate_recipient_list(recipients)
    
    # Validate subject
    if not subject or not isinstance(subject, str):
        raise ValidationError("Email subject must be a non-empty string")
    
    if len(subject.strip()) == 0:
        raise ValidationError("Email subject cannot be empty")
    
    # Validate body
    if not body or not isinstance(body, str):
        raise ValidationError("Email body must be a non-empty string")
    
    if len(body.strip()) == 0:
        raise ValidationError("Email body cannot be empty")
    
    # Validate CC if provided
    validated_cc = []
    if cc:
        validated_cc = validate_recipient_list(cc)
    
    # Validate BCC if provided
    validated_bcc = []
    if bcc:
        validated_bcc = validate_recipient_list(bcc)
    
    return validated_recipients, validated_cc, validated_bcc
