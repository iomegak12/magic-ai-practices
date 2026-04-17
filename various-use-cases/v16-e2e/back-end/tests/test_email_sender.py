"""
Test script for email_sender library.

This script demonstrates all the main features of the email sender library.
Run this from the back-end directory.
"""

import sys
from pathlib import Path

# Add the libraries directory to the Python path
libraries_path = Path(__file__).parent.parent / "libraries"
sys.path.insert(0, str(libraries_path))

from email_sender import (
    send_email,
    send_text_email,
    send_html_email,
    test_connection,
    get_email_config,
    ConfigurationError,
    ValidationError,
    SMTPConnectionError,
    EmailSendError
)


def print_section(title):
    """Print a section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def main():
    print_section("Email Sender Library - Test Script")
    
    # 1. Test configuration
    print("\n1. Testing configuration...")
    try:
        config = get_email_config()
        print(f"   ✓ Configuration loaded")
        print(f"   Server: {config.smtp_server}:{config.smtp_port}")
        print(f"   Sender: {config.sender_email}")
        print(f"   Name: {config.sender_name or '(not set)'}")
    except ConfigurationError as e:
        print(f"   ✗ Configuration error: {e}")
        print("\n   Please check your .env file!")
        return
    
    # 2. Test SMTP connection
    print("\n2. Testing SMTP connection...")
    try:
        result = test_connection()
        print(f"   ✓ {result['message']}")
        print(f"   Connected to: {result['server']}:{result['port']}")
    except SMTPConnectionError as e:
        print(f"   ✗ Connection failed: {e}")
        print("\n   Please check your credentials and internet connection!")
        return
    except Exception as e:
        print(f"   ✗ Unexpected error: {e}")
        return
    
    # 3. Send simple text email
    print("\n3. Sending simple text email to jtdhamodharan@gmail.com...")
    try:
        result = send_text_email(
            recipients="jtdhamodharan@gmail.com",
            subject="Test Email - Plain Text",
            body="This is a test email sent using the email_sender library.\n\n"
                 "If you received this, the library is working correctly!"
        )
        if result['success']:
            print(f"   ✓ Email sent successfully!")
            print(f"   Recipients: {', '.join(result['recipients'])}")
            print(f"   Subject: {result['subject']}")
    except Exception as e:
        print(f"   ✗ Failed to send: {e}")
    
    # 4. Send HTML email
    print("\n4. Sending HTML email to jtdhamodharan@gmail.com...")
    try:
        html_content = """
        <html>
            <body style="font-family: Arial, sans-serif;">
                <h1 style="color: #2c3e50;">Email Sender Library Test</h1>
                <p>This is an <strong>HTML email</strong> sent using the email_sender library.</p>
                <ul>
                    <li>✅ Plain text emails</li>
                    <li>✅ HTML emails</li>
                    <li>✅ Multiple recipients</li>
                    <li>✅ CC and BCC</li>
                    <li>✅ File attachments</li>
                </ul>
                <p style="color: #27ae60;"><em>Library is working correctly!</em></p>
            </body>
        </html>
        """
        
        result = send_html_email(
            recipients="jtdhamodharan@gmail.com",
            subject="Test Email - HTML",
            html_body=html_content
        )
        if result['success']:
            print(f"   ✓ HTML email sent successfully!")
    except Exception as e:
        print(f"   ✗ Failed to send: {e}")
    
    # 5. Test validation errors
    print("\n5. Testing validation (intentional errors)...")
    
    # Invalid email
    print("   - Testing invalid email address...")
    try:
        send_text_email(
            recipients="invalid-email",
            subject="Test",
            body="Test"
        )
        print("   ✗ Should have raised ValidationError!")
    except ValidationError as e:
        print(f"   ✓ Validation caught error: {e}")
    
    # Empty subject
    print("   - Testing empty subject...")
    try:
        send_text_email(
            recipients="test@example.com",
            subject="",
            body="Test"
        )
        print("   ✗ Should have raised ValidationError!")
    except ValidationError as e:
        print(f"   ✓ Validation caught error: {e}")
    
    # Empty body
    print("   - Testing empty body...")
    try:
        send_text_email(
            recipients="test@example.com",
            subject="Test",
            body=""
        )
        print("   ✗ Should have raised ValidationError!")
    except ValidationError as e:
        print(f"   ✓ Validation caught error: {e}")
    
    # 6. Test multiple recipients with CC
    print("\n6. Testing multiple recipients with CC...")
    try:
        result = send_email(
            recipients="jtdhamodharan@gmail.com",
            subject="Test Email - Multiple Recipients",
            body="This email was sent to multiple recipients using CC.",
            cc=config.sender_email
        )
        if result['success']:
            print(f"   ✓ Email sent with CC!")
            print(f"   To: {', '.join(result['recipients'])}")
            print(f"   CC: {', '.join(result['cc'])}")
    except Exception as e:
        print(f"   ✗ Failed to send: {e}")
    
    # Summary
    print_section("Test Summary")
    print("\n✓ All tests completed!")
    print("\nEmails sent to: jtdhamodharan@gmail.com")
    print("CC copy sent to:", config.sender_email)
    print("\nYou should have received 3 test emails:")
    print("  1. Plain text email")
    print("  2. HTML email")
    print("  3. Email with CC")
    print("\nNote: Check your spam folder if you don't see them.")
    print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
