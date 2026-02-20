"""
Test Configuration

Test-specific configuration and utilities.
"""
import os
from pathlib import Path

# Test directories
TEST_ROOT = Path(__file__).parent
PROJECT_ROOT = TEST_ROOT.parent
DATA_DIR = TEST_ROOT / "data"
FIXTURES_DIR = TEST_ROOT / "fixtures"

# Test data paths
TEST_DATABASE = DATA_DIR / "test_orders.db"
TEST_LOGS = DATA_DIR / "test_logs"

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True)
FIXTURES_DIR.mkdir(exist_ok=True)
TEST_LOGS.mkdir(exist_ok=True)

# Test configuration
TEST_CONFIG = {
    "api": {
        "host": "127.0.0.1",
        "port": 9080,
        "base_url": "http://127.0.0.1:9080"
    },
    "database": {
        "path": str(TEST_DATABASE),
        "reset_on_start": True
    },
    "azure": {
        "endpoint": "https://test-endpoint.example.com",
        "api_key": "test-api-key-1234567890",
        "model_name": "gpt-4o"
    },
    "email": {
        "sender": "test@example.com",
        "password": "test-password",
        "smtp_server": "smtp.test.com",
        "smtp_port": 587
    },
    "mcp": {
        "url": "http://localhost:8000/mcp",
        "required": False,
        "timeout": 10
    },
    "logging": {
        "level": "DEBUG",
        "file": str(TEST_LOGS / "test.log")
    }
}

# Sample test data
SAMPLE_ORDERS = [
    {
        "order_date": "2024-01-15",
        "customer_name": "John Doe",
        "billing_address": "123 Main St, Anytown, ST 12345",
        "product_sku": "PROD-001",
        "quantity": 2,
        "order_amount": 99.99,
        "remarks": "Standard delivery"
    },
    {
        "order_date": "2024-01-16",
        "customer_name": "Jane Smith",
        "billing_address": "456 Oak Ave, Somewhere, ST 67890",
        "product_sku": "PROD-002",
        "quantity": 1,
        "order_amount": 149.99,
        "remarks": "Express shipping requested"
    },
    {
        "order_date": "2024-01-17",
        "customer_name": "Bob Johnson",
        "billing_address": "789 Pine Rd, Elsewhere, ST 11223",
        "product_sku": "PROD-003",
        "quantity": 5,
        "order_amount": 499.95,
        "remarks": "Bulk order"
    }
]

SAMPLE_EMAILS = [
    {
        "recipients": "customer@example.com",
        "subject": "Order Confirmation",
        "body": "Your order has been confirmed."
    },
    {
        "recipients": "admin@example.com",
        "subject": "Daily Report",
        "body": "Here is your daily report."
    }
]

SAMPLE_MESSAGES = [
    "Hello, I need help with my order",
    "What's the status of order ORD-123?",
    "Can you send me a confirmation email?",
    "I want to update my order status",
    "Show me all my orders"
]

# Test user agents
TEST_USER_AGENTS = [
    "Mozilla/5.0 (Test Client)",
    "TestRunner/1.0",
    "pytest-httpx/0.1.0"
]


def get_test_config(section: str = None):
    """
    Get test configuration.
    
    Args:
        section: Optional section name to get specific config
        
    Returns:
        dict: Configuration dictionary
    """
    if section:
        return TEST_CONFIG.get(section, {})
    return TEST_CONFIG


def cleanup_test_data():
    """Clean up test data files."""
    if TEST_DATABASE.exists():
        TEST_DATABASE.unlink()
    
    for log_file in TEST_LOGS.glob("*.log"):
        log_file.unlink()


# Export all
__all__ = [
    "TEST_ROOT",
    "PROJECT_ROOT",
    "DATA_DIR",
    "FIXTURES_DIR",
    "TEST_DATABASE",
    "TEST_LOGS",
    "TEST_CONFIG",
    "SAMPLE_ORDERS",
    "SAMPLE_EMAILS",
    "SAMPLE_MESSAGES",
    "TEST_USER_AGENTS",
    "get_test_config",
    "cleanup_test_data"
]
