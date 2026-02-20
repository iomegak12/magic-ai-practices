"""
Test Initialization

Initialize test environment and provide common test utilities.
"""

__version__ = "0.1.0"

# Test markers (defined in conftest.py)
MARKERS = {
    "unit": "Unit tests",
    "integration": "Integration tests",
    "slow": "Slow running tests",
    "requires_azure": "Tests requiring Azure credentials",
    "requires_mcp": "Tests requiring MCP server"
}

# Export test configuration
from .test_config import (
    TEST_CONFIG,
    SAMPLE_ORDERS,
    SAMPLE_EMAILS,
    SAMPLE_MESSAGES,
    get_test_config,
    cleanup_test_data
)

__all__ = [
    "TEST_CONFIG",
    "SAMPLE_ORDERS",
    "SAMPLE_EMAILS",
    "SAMPLE_MESSAGES",
    "get_test_config",
    "cleanup_test_data",
    "MARKERS"
]
