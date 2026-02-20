# Test Suite Documentation

This directory contains comprehensive tests for the V16 E2E Back-End REST API service.

## Table of Contents
- [Overview](#overview)
- [Test Structure](#test-structure)
- [Running Tests](#running-tests)
- [Test Categories](#test-categories)
- [Writing Tests](#writing-tests)
- [Fixtures](#fixtures)
- [Coverage](#coverage)

## Overview

The test suite includes:
- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test API endpoints and component interactions
- **Fixtures**: Shared test data and mock objects
- **Test Configuration**: Centralized test settings

## Test Structure

```
tests/
├── __init__.py              # Test suite initialization
├── conftest.py              # Pytest configuration & fixtures
├── test_config.py           # Test configuration & sample data
├── unit/                    # Unit tests
│   ├── test_helpers.py      # Helper functions
│   ├── test_exceptions.py   # Exception classes
│   ├── test_config.py       # Configuration management
│   ├── test_agent_manager.py # Agent manager
│   ├── test_agent_factory.py # Agent factory
│   └── test_tools.py        # Tool wrappers
└── integration/             # Integration tests
    ├── test_health_endpoints.py
    ├── test_agent_endpoints.py
    ├── test_info_endpoints.py
    └── test_error_handling.py
```

## Running Tests

### Quick Start

**All tests:**
```bash
# Linux/Mac
./scripts/run_tests.sh

# Windows
scripts\run_tests.bat
```

### Test Categories

**Unit tests only:**
```bash
./scripts/run_tests.sh unit
pytest tests/unit/ -v
```

**Integration tests only:**
```bash
./scripts/run_tests.sh integration
pytest tests/integration/ -v
```

**Fast tests (exclude slow):**
```bash
./scripts/run_tests.sh fast
pytest tests/ -m "not slow"
```

**Tests by marker:**
```bash
pytest tests/ -m unit            # Unit tests
pytest tests/ -m integration     # Integration tests
pytest tests/ -m "not slow"      # Exclude slow tests
pytest tests/ -m requires_azure  # Azure-dependent tests
pytest tests/ -m requires_mcp    # MCP-dependent tests
```

### Specific Tests

**Run specific file:**
```bash
pytest tests/unit/test_helpers.py -v
```

**Run specific test:**
```bash
pytest tests/unit/test_helpers.py::TestIDGeneration::test_generate_request_id_format -v
```

**Run by keyword:**
```bash
pytest tests/ -k "test_health" -v
pytest tests/ -k "session" -v
```

### Coverage Reports

**Generate coverage report:**
```bash
./scripts/run_tests.sh coverage
pytest tests/ --cov=app --cov-report=html --cov-report=term
```

**View HTML report:**
```bash
# Open htmlcov/index.html in browser
```

### Other Options

**Watch mode (re-run on changes):**
```bash
./scripts/run_tests.sh watch
pytest tests/ -f
```

**Re-run failed tests:**
```bash
./scripts/run_tests.sh failed
pytest tests/ --lf
```

**Stop on first failure:**
```bash
pytest tests/ -x
```

**Stop after N failures:**
```bash
pytest tests/ --maxfail=3
```

**Verbose output:**
```bash
./scripts/run_tests.sh verbose
pytest tests/ -vv --tb=long
```

## Test Categories

### Available Markers

Tests are marked with the following categories:

- `unit` - Unit tests (fast, isolated)
- `integration` - Integration tests (may be slower)
- `slow` - Slow-running tests
- `requires_azure` - Requires Azure OpenAI connection
- `requires_mcp` - Requires MCP server connection

### Applying Markers

Markers are automatically applied based on test location:
- Tests in `tests/unit/` → `unit` marker
- Tests in `tests/integration/` → `integration` marker

Manual markers in test code:
```python
@pytest.mark.slow
def test_long_operation():
    # Test that takes a long time
    pass

@pytest.mark.requires_azure
def test_azure_integration():
    # Test that needs Azure connection
    pass
```

## Writing Tests

### Unit Test Example

```python
"""tests/unit/test_my_module.py"""
import pytest
from app.utils.helpers import my_function

class TestMyFunction:
    """Tests for my_function."""
    
    def test_basic_case(self):
        """Test basic functionality."""
        result = my_function("input")
        assert result == "expected"
    
    def test_edge_case(self):
        """Test edge case."""
        result = my_function("")
        assert result == ""
    
    def test_error_handling(self):
        """Test error handling."""
        with pytest.raises(ValueError):
            my_function(None)
```

### Integration Test Example

```python
"""tests/integration/test_my_endpoint.py"""
import pytest
from fastapi.testclient import TestClient
from app.server import app

@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)

class TestMyEndpoint:
    """Tests for /my-endpoint."""
    
    def test_success_case(self, client):
        """Test successful request."""
        response = client.post(
            "/my-endpoint",
            json={"key": "value"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "result" in data
    
    def test_validation_error(self, client):
        """Test validation error."""
        response = client.post(
            "/my-endpoint",
            json={}
        )
        
        assert response.status_code == 422
```

### Async Test Example

```python
@pytest.mark.asyncio
async def test_async_function():
    """Test async function."""
    result = await my_async_function()
    assert result == "expected"
```

## Fixtures

### Available Fixtures

Defined in `conftest.py`:

**Environment & Setup:**
- `test_env_vars` - Sets test environment variables
- `test_data_dir` - Temporary test data directory
- `test_database` - Test database instance

**Mock Objects:**
- `mock_settings` - Mock Settings object
- `mock_agent_manager` - Mock AgentManager
- `mock_mcp_handler` - Mock MCPHandler
- `mock_azure_client` - Mock Azure AI client

**Sample Data:**
- `sample_order_data` - Sample order data
- `sample_email_data` - Sample email data
- `sample_session_data` - Sample session data

**Automatic:**
- `reset_singletons` - Resets singletons between tests (autouse)

### Using Fixtures

```python
def test_with_fixture(sample_order_data):
    """Test using fixture."""
    order = sample_order_data
    assert order["customer_name"] == "John Doe"

@pytest.mark.asyncio
async def test_with_mock_agent(mock_agent_manager):
    """Test with mock agent manager."""
    result = await mock_agent_manager.execute(
        session_id="SES-test",
        message="Hello"
    )
    assert result["status"] == "success"
```

### Custom Fixtures

```python
@pytest.fixture
def my_fixture():
    """Custom fixture."""
    # Setup
    data = {"key": "value"}
    
    yield data
    
    # Teardown (optional)
    data.clear()
```

## Test Configuration

### Test Settings

Located in `test_config.py`:

```python
TEST_CONFIG = {
    "api": {
        "host": "127.0.0.1",
        "port": 9080,
        "base_url": "http://127.0.0.1:9080"
    },
    "database": {
        "path": "test_database.db",
        "reset_on_start": True
    },
    # ... more settings
}
```

### Accessing Test Config

```python
from tests.test_config import get_test_config

def test_with_config():
    """Test using test config."""
    api_config = get_test_config("api")
    base_url = api_config["base_url"]
    # Use config...
```

### Sample Data

Pre-defined sample data in `test_config.py`:

```python
from tests.test_config import SAMPLE_ORDERS, SAMPLE_EMAILS

def test_with_sample_data():
    """Test with sample data."""
    order = SAMPLE_ORDERS[0]
    email = SAMPLE_EMAILS[0]
    # Use sample data...
```

## Coverage

### Running Coverage

```bash
pytest tests/ --cov=app --cov-report=html --cov-report=term
```

### Coverage Report Files

- `htmlcov/index.html` - Interactive HTML report
- `.coverage` - Coverage data file
- Terminal output - Summary in console

### Coverage Targets

Aim for:
- **Overall**: 80%+ coverage
- **Critical modules**: 90%+ coverage
- **Utilities**: 95%+ coverage

## Best Practices

1. **Test Organization**
   - One test class per component
   - Descriptive test names
   - Group related tests

2. **Assertions**
   - One assertion per test (when possible)
   - Clear failure messages
   - Test both success and failure cases

3. **Fixtures**
   - Use fixtures for repeated setup
   - Scope appropriately (function/session)
   - Clean up in teardown

4. **Mock External Services**
   - Mock Azure OpenAI calls
   - Mock SMTP connections
   - Mock MCP server requests

5. **Test Independence**
   - Tests should not depend on each other
   - Use `reset_singletons` fixture
   - Clean up after each test

6. **Performance**
   - Keep unit tests fast (<100ms)
   - Mark slow tests with `@pytest.mark.slow`
   - Use appropriate markers

## Troubleshooting

### Common Issues

**Import errors:**
```bash
# Ensure you're in the correct directory
cd v16-e2e/back-end

# Install dependencies
pip install -r requirements.txt
```

**Fixture not found:**
```python
# Make sure fixture is defined in conftest.py
# or imported in the test file
```

**Database errors:**
```python
# Test database is reset between tests
# Check test_database fixture in conftest.py
```

**Environment variables:**
```python
# Test environment variables are set in conftest.py
# via test_env_vars fixture
```

## Examples

### Complete Test Suite Example

```python
"""Complete test example."""
import pytest
from app.utils.helpers import generate_session_id

class TestSessionID:
    """Tests for session ID generation."""
    
    def test_format(self):
        """Test ID format."""
        session_id = generate_session_id()
        assert session_id.startswith("SES-")
    
    def test_uniqueness(self):
        """Test IDs are unique."""
        id1 = generate_session_id()
        id2 = generate_session_id()
        assert id1 != id2
    
    def test_length(self):
        """Test ID length."""
        session_id = generate_session_id()
        assert len(session_id) > 10
    
    @pytest.mark.parametrize("count", [10, 100, 1000])
    def test_uniqueness_batch(self, count):
        """Test batch uniqueness."""
        ids = {generate_session_id() for _ in range(count)}
        assert len(ids) == count
```

## Further Reading

- [Pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [Python unittest.mock](https://docs.python.org/3/library/unittest.mock.html)

---

**Need help?** Check the main project README or reach out to the development team.
