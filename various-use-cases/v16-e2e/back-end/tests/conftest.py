"""
Pytest Configuration and Shared Fixtures

This module provides shared fixtures and configuration for all tests.
"""
import pytest
import os
import tempfile
from pathlib import Path
from typing import Generator
from unittest.mock import Mock, MagicMock

# Set test environment variables before importing app modules
os.environ["TESTING"] = "true"
os.environ["LOG_LEVEL"] = "DEBUG"


@pytest.fixture(scope="session")
def test_env_vars():
    """Set up test environment variables."""
    env_vars = {
        "AZURE_AI_PROJECT_ENDPOINT": "https://test-endpoint.example.com",
        "AZURE_OPENAI_API_KEY": "test-api-key-1234567890",
        "AZURE_OPENAI_MODEL_NAME": "gpt-4o",
        "DATABASE_PATH": "./test_data/test_orders.db",
        "SENDER_EMAIL": "test@example.com",
        "SENDER_PASSWORD": "test-password",
        "SMTP_SERVER": "smtp.test.com",
        "SMTP_PORT": "587",
        "MCP_SERVER_URL": "http://localhost:8000/mcp",
        "MCP_SERVER_REQUIRED": "false",
        "API_HOST": "127.0.0.1",
        "API_PORT": "9080",
        "LOG_LEVEL": "DEBUG",
    }
    
    # Store original env vars
    original_env = {}
    for key, value in env_vars.items():
        original_env[key] = os.environ.get(key)
        os.environ[key] = value
    
    yield env_vars
    
    # Restore original env vars
    for key, value in original_env.items():
        if value is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = value


@pytest.fixture(scope="session")
def test_data_dir() -> Generator[Path, None, None]:
    """Create temporary directory for test data."""
    with tempfile.TemporaryDirectory() as temp_dir:
        test_dir = Path(temp_dir)
        yield test_dir


@pytest.fixture(scope="session")
def test_database(test_data_dir: Path) -> Generator[Path, None, None]:
    """Create temporary test database."""
    db_path = test_data_dir / "test_orders.db"
    
    # Import and initialize database
    from app.tools.order_management import init_db, set_database_path
    
    set_database_path(str(db_path))
    init_db()
    
    yield db_path
    
    # Cleanup
    if db_path.exists():
        db_path.unlink()


@pytest.fixture
def mock_settings():
    """Mock settings object for testing."""
    from app.config.settings import Settings
    
    settings = Settings(
        azure_ai_project_endpoint="https://test-endpoint.example.com",
        azure_openai_api_key="test-api-key-1234567890",
        azure_openai_model_name="gpt-4o",
        database_path="./test_data/test_orders.db",
        sender_email="test@example.com",
        sender_password="test-password",
        smtp_server="smtp.test.com",
        smtp_port=587,
        mcp_server_url="http://localhost:8000/mcp",
        mcp_server_required=False,
        api_host="127.0.0.1",
        api_port=9080,
        log_level="DEBUG"
    )
    
    return settings


@pytest.fixture
def mock_agent_manager():
    """Mock agent manager for testing."""
    manager = MagicMock()
    manager.is_initialized.return_value = True
    manager.get_session_count.return_value = 0
    manager.list_sessions.return_value = []
    
    async def mock_execute(session_id, message):
        return {
            "session_id": session_id,
            "response": f"Mock response to: {message}",
            "status": "success"
        }
    
    manager.execute.side_effect = mock_execute
    manager.create_session.return_value = "test-session-123"
    manager.delete_session.return_value = True
    
    return manager


@pytest.fixture
def mock_mcp_handler():
    """Mock MCP handler for testing."""
    handler = MagicMock()
    handler.is_connected.return_value = True
    handler.get_mcp_tool.return_value = MagicMock()
    handler.get_connection_error.return_value = None
    
    return handler


@pytest.fixture
def sample_order_data():
    """Sample order data for testing."""
    return {
        "order_date": "2024-01-15",
        "customer_name": "John Doe",
        "billing_address": "123 Main St, City, State 12345",
        "product_sku": "PROD-001",
        "quantity": 2,
        "order_amount": 99.99,
        "remarks": "Test order"
    }


@pytest.fixture
def sample_email_data():
    """Sample email data for testing."""
    return {
        "recipients": "test@example.com",
        "subject": "Test Email",
        "body": "This is a test email message.",
    }


@pytest.fixture
def sample_session_data():
    """Sample session data for testing."""
    return {
        "session_id": "test-session-123",
        "message": "Hello, I need help with my order",
    }


@pytest.fixture
def mock_azure_client():
    """Mock Azure OpenAI client for testing."""
    client = MagicMock()
    
    # Mock agent
    mock_agent = MagicMock()
    mock_agent.create_session.return_value = MagicMock()
    
    async def mock_run(message, session=None):
        return f"Mock agent response to: {message}"
    
    mock_agent.run.side_effect = mock_run
    
    client.as_agent.return_value = mock_agent
    
    return client


@pytest.fixture(autouse=True)
def reset_singletons():
    """Reset singleton instances between tests."""
    yield
    
    # Reset agent manager
    from app.agent import manager as agent_manager_module
    agent_manager_module._agent_manager = None
    
    # Reset MCP handler
    from app.tools import mcp_handler as mcp_handler_module
    mcp_handler_module._mcp_handler = None
    
    # Reset settings
    from app.config import settings as settings_module
    settings_module._settings = None


# Pytest configuration
def pytest_configure(config):
    """Configure pytest."""
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
    config.addinivalue_line(
        "markers", "requires_azure: mark test as requiring Azure credentials"
    )
    config.addinivalue_line(
        "markers", "requires_mcp: mark test as requiring MCP server"
    )


# Test collection hooks
def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers automatically."""
    for item in items:
        # Add unit marker to unit tests
        if "unit" in item.nodeid:
            item.add_marker(pytest.mark.unit)
        
        # Add integration marker to integration tests
        if "integration" in item.nodeid:
            item.add_marker(pytest.mark.integration)
