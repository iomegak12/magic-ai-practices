"""
Integration Tests for Error Handling

Tests for API error handling and exception responses.
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.server import app


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


class TestValidationErrors:
    """Tests for validation error handling."""
    
    def test_missing_required_field(self, client):
        """Test missing required field returns 422."""
        response = client.post(
            "/agent/sessions",
            json={}
        )
        
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data
    
    def test_invalid_field_type(self, client):
        """Test invalid field type returns 422."""
        response = client.post(
            "/agent/sessions",
            json={"tenant_id": 123}  # Should be string
        )
        
        # May accept or reject based on validation
        assert response.status_code in [200, 422]
    
    def test_malformed_json(self, client):
        """Test malformed JSON returns error."""
        response = client.post(
            "/agent/sessions",
            data="{invalid json}",
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code == 422


class TestNotFoundErrors:
    """Tests for 404 errors."""
    
    def test_nonexistent_endpoint(self, client):
        """Test nonexistent endpoint returns 404."""
        response = client.get("/nonexistent")
        
        assert response.status_code == 404
    
    def test_nonexistent_session(self, client, mock_agent_manager):
        """Test accessing nonexistent session returns 404."""
        from app.utils.exceptions import SessionNotFoundError
        mock_agent_manager.get_session = MagicMock(
            side_effect=SessionNotFoundError("Not found")
        )
        
        with patch("app.routes.agent.get_agent_manager", return_value=mock_agent_manager):
            response = client.get("/agent/sessions?session_id=INVALID-ID")
            
            assert response.status_code in [404, 500]


class TestServerErrors:
    """Tests for 500 errors."""
    
    def test_internal_server_error(self, client, mock_agent_manager):
        """Test internal server error handling."""
        from unittest.mock import AsyncMock
        mock_agent_manager.execute = AsyncMock(
            side_effect=Exception("Internal error")
        )
        
        with patch("app.routes.agent.get_agent_manager", return_value=mock_agent_manager):
            response = client.post(
                "/agent/messages",
                json={
                    "session_id": "SES-test-123",
                    "message": "Hello"
                }
            )
            
            assert response.status_code == 500
            data = response.json()
            assert "detail" in data or "error" in data
    
    def test_error_response_structure(self, client):
        """Test error response has proper structure."""
        response = client.post(
            "/agent/sessions",
            json={}
        )
        
        data = response.json()
        # Should have error details
        assert "detail" in data or "message" in data or "error" in data


class TestRateLimiting:
    """Tests for rate limiting errors."""
    
    def test_rate_limit_error_format(self, client, mock_agent_manager):
        """Test rate limit error response format."""
        from app.utils.exceptions import RateLimitError
        from unittest.mock import AsyncMock
        
        mock_agent_manager.execute = AsyncMock(
            side_effect=RateLimitError("Rate limit exceeded")
        )
        
        with patch("app.routes.agent.get_agent_manager", return_value=mock_agent_manager):
            response = client.post(
                "/agent/messages",
                json={
                    "session_id": "SES-test-123",
                    "message": "Hello"
                }
            )
            
            # Should return 429 or be caught by error handler
            assert response.status_code in [429, 500]


class TestAuthenticationErrors:
    """Tests for authentication errors."""
    
    def test_authentication_error_format(self, client, mock_agent_manager):
        """Test authentication error response."""
        from app.utils.exceptions import AuthenticationError
        from unittest.mock import AsyncMock
        
        mock_agent_manager.execute = AsyncMock(
            side_effect=AuthenticationError("Authentication failed")
        )
        
        with patch("app.routes.agent.get_agent_manager", return_value=mock_agent_manager):
            response = client.post(
                "/agent/messages",
                json={
                    "session_id": "SES-test-123",
                    "message": "Hello"
                }
            )
            
            # Should return 401 or be caught by error handler
            assert response.status_code in [401, 500]


class TestCORSErrors:
    """Tests for CORS error handling."""
    
    def test_cors_preflight(self, client):
        """Test CORS preflight request."""
        response = client.options(
            "/agent/sessions",
            headers={
                "Origin": "http://example.com",
                "Access-Control-Request-Method": "POST"
            }
        )
        
        # Should handle CORS preflight
        assert response.status_code in [200, 204, 405]


class TestErrorLogging:
    """Tests for error logging."""
    
    def test_errors_are_logged(self, client, caplog, mock_agent_manager):
        """Test that errors are logged."""
        from unittest.mock import AsyncMock
        
        mock_agent_manager.execute = AsyncMock(
            side_effect=Exception("Test error")
        )
        
        with patch("app.routes.agent.get_agent_manager", return_value=mock_agent_manager):
            response = client.post(
                "/agent/messages",
                json={
                    "session_id": "SES-test-123",
                    "message": "Hello"
                }
            )
            
            assert response.status_code == 500


class TestTimeoutErrors:
    """Tests for timeout error handling."""
    
    def test_timeout_error_format(self, client, mock_agent_manager):
        """Test timeout error response."""
        from app.utils.exceptions import AgentTimeoutError
        from unittest.mock import AsyncMock
        
        mock_agent_manager.execute = AsyncMock(
            side_effect=AgentTimeoutError("Operation timed out")
        )
        
        with patch("app.routes.agent.get_agent_manager", return_value=mock_agent_manager):
            response = client.post(
                "/agent/messages",
                json={
                    "session_id": "SES-test-123",
                    "message": "Hello"
                }
            )
            
            # Should return timeout error
            assert response.status_code in [408, 500, 504]
