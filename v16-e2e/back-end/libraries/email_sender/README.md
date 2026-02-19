# Email Sender Library

A Python library for sending emails using Gmail SMTP server with app passwords.

## Features

- ✅ **Gmail SMTP** integration with app password support
- ✅ **Plain text and HTML** email support
- ✅ **CC and BCC** recipients
- ✅ **File attachments** support
- ✅ **Configurable via .env** file
- ✅ **Connection testing** to verify SMTP settings
- ✅ **Comprehensive validation** and error handling
- ✅ **Type hints** for better code completion

## Installation

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

2. Set up Gmail App Password:
   - Go to your Google Account settings
   - Navigate to Security > 2-Step Verification
   - Scroll down to "App passwords"
   - Generate a new app password for "Mail"
   - Copy the 16-character password

3. Configure your email settings:

Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

Edit `.env` with your Gmail credentials:
```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password_here
SENDER_NAME=Your Name
```

## Quick Start

```python
from email_sender import send_text_email, test_connection

# Test your connection first
try:
    result = test_connection()
    print(f"✓ {result['message']}")
except Exception as e:
    print(f"✗ Connection failed: {e}")

# Send a simple text email
result = send_text_email(
    recipients="recipient@example.com",
    subject="Hello from Python",
    body="This is a test email sent using the email_sender library!"
)
print(f"Email sent: {result['success']}")
```

## Usage Examples

### 1. Send Plain Text Email

```python
from email_sender import send_text_email

result = send_text_email(
    recipients="user@example.com",
    subject="Meeting Reminder",
    body="Don't forget about our meeting tomorrow at 10 AM."
)
```

### 2. Send HTML Email

```python
from email_sender import send_html_email

html_content = """
<html>
  <body>
    <h1>Welcome!</h1>
    <p>Thanks for signing up.</p>
    <a href="https://example.com">Visit our website</a>
  </body>
</html>
"""

result = send_html_email(
    recipients="user@example.com",
    subject="Welcome!",
    html_body=html_content
)
```

### 3. Send to Multiple Recipients with CC and BCC

```python
from email_sender import send_email

result = send_email(
    recipients=["user1@example.com", "user2@example.com"],
    subject="Team Update",
    body="Here's the latest team update...",
    cc="manager@example.com",
    bcc=["admin@example.com", "backup@example.com"]
)
```

### 4. Send Email with Attachments

```python
from email_sender import send_email_with_attachments

result = send_email_with_attachments(
    recipients="client@example.com",
    subject="Monthly Report",
    body="Please find attached the monthly report.",
    attachments=["report.pdf", "data.xlsx"]
)
```

### 5. Send HTML Email with Attachments

```python
from email_sender import send_email

html_body = "<h1>Invoice</h1><p>Please see attached invoice.</p>"

result = send_email(
    recipients="customer@example.com",
    subject="Invoice #12345",
    body=html_body,
    html=True,
    attachments=["invoice_12345.pdf"]
)
```

### 6. Test SMTP Connection

```python
from email_sender import test_connection, SMTPConnectionError

try:
    result = test_connection()
    print(f"✓ Connection successful!")
    print(f"  Server: {result['server']}:{result['port']}")
    print(f"  Email: {result['email']}")
except SMTPConnectionError as e:
    print(f"✗ Connection failed: {e}")
```

## API Reference

### Email Operations

#### `send_email(recipients, subject, body, cc=None, bcc=None, html=False, attachments=None)`

Send an email with full control over all options.

**Parameters:**
- `recipients` (str | List[str]): Recipient email address(es)
- `subject` (str): Email subject
- `body` (str): Email body (plain text or HTML)
- `cc` (str | List[str], optional): CC recipients
- `bcc` (str | List[str], optional): BCC recipients
- `html` (bool, optional): If True, body is treated as HTML. Default: False
- `attachments` (List[str], optional): List of file paths to attach

**Returns:** `dict` with status and details

**Raises:** `ValidationError`, `ConfigurationError`, `SMTPConnectionError`, `EmailSendError`

#### `send_text_email(recipients, subject, body, cc=None, bcc=None)`

Send a plain text email.

**Returns:** `dict` with status and details

#### `send_html_email(recipients, subject, html_body, cc=None, bcc=None)`

Send an HTML email.

**Returns:** `dict` with status and details

#### `send_email_with_attachments(recipients, subject, body, attachments, cc=None, bcc=None, html=False)`

Send an email with file attachments.

**Returns:** `dict` with status and details

#### `test_connection()`

Test SMTP connection and authentication.

**Returns:** `dict` with connection status

**Raises:** `ConfigurationError`, `SMTPConnectionError`

### Configuration

#### `get_email_config()`

Get the current email configuration.

**Returns:** `EmailConfig` object

#### `reload_config()`

Reload configuration from .env file.

**Returns:** `EmailConfig` object with updated settings

## Exception Handling

The library provides specific exception types:

```python
from email_sender import (
    send_email,
    EmailSenderError,      # Base exception
    ConfigurationError,    # Configuration issues
    ValidationError,       # Invalid email data
    SMTPConnectionError,   # Connection failures
    EmailSendError        # Sending failures
)

try:
    result = send_email(
        recipients="invalid-email",
        subject="Test",
        body="Test"
    )
except ValidationError as e:
    print(f"Validation error: {e}")
except SMTPConnectionError as e:
    print(f"Connection error: {e}")
except EmailSendError as e:
    print(f"Send error: {e}")
except ConfigurationError as e:
    print(f"Configuration error: {e}")
```

## Configuration Options

| Variable | Description | Default |
|----------|-------------|---------|
| `SMTP_SERVER` | Gmail SMTP server | smtp.gmail.com |
| `SMTP_PORT` | SMTP port (TLS) | 587 |
| `SENDER_EMAIL` | Your Gmail address | Required |
| `SENDER_PASSWORD` | Gmail app password | Required |
| `SENDER_NAME` | Display name | Optional |

## Gmail App Password Setup

To use this library with Gmail, you need to:

1. **Enable 2-Step Verification** on your Google account
2. **Generate an App Password**:
   - Go to Google Account → Security
   - Under "2-Step Verification", click "App passwords"
   - Select "Mail" and your device
   - Copy the 16-character password (remove spaces)
3. **Use the app password** in your .env file, not your regular Gmail password

## Important Notes

- ⚠️ **Never commit your .env file** to version control
- ⚠️ **App passwords are required** - regular Gmail passwords won't work with SMTP
- ⚠️ **TLS encryption is enabled** by default for security
- ⚠️ **Gmail sending limits** apply (500 emails per day for free accounts)

## Validation Rules

- **Email addresses**: Must be valid email format
- **Recipients**: At least one recipient required
- **Subject**: Cannot be empty
- **Body**: Cannot be empty
- **Attachments**: Files must exist and be readable

## Project Structure

```
email_sender/
├── __init__.py          # Public API and exports
├── config.py            # Email configuration management
├── operations.py        # Email sending operations
├── validations.py       # Email data validation
├── exceptions.py        # Custom exception classes
├── requirements.txt     # Python dependencies
├── .env.example         # Example configuration
└── README.md           # This file
```

## Troubleshooting

### Authentication Error

If you get an authentication error:
- Verify 2-Step Verification is enabled on your Google account
- Make sure you're using an app password, not your regular password
- Check that the app password is correct (16 characters, no spaces)

### Connection Timeout

If connection times out:
- Check your internet connection
- Verify SMTP_SERVER and SMTP_PORT are correct
- Check if your firewall is blocking port 587

### "Less secure app access"

Gmail no longer supports "less secure apps". You **must** use app passwords with 2-Step Verification enabled.

## License

This library is provided as-is for use in your projects.

## Support

For issues or questions, please refer to the inline documentation and docstrings in the source code.
