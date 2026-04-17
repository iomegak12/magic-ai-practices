"""
Integration Tests for Agent Endpoints

Tests for agent API endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from app.server import app


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


class TestCreateSession:
    """Tests for POST /agent/sessions endpoint."""
    
    def test_create_session_success(self, client, mock_agent_manager):
        """Test successful session creation."""
        with patch("app.routes.agent.get_agent_manager", return_value=mock_agent_manager):
            response = client.post(
                "/agent/sessions",
                json={"tenant_id": "test-tenant"}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert "session_id" in data
            assert data["session_id"].startswith("SES-")
    
    def test_create_session_with_metadata(self, client, mock_agent_manager):
        """Test session creation with metadata."""
        with patch("app.routes.agent.get_agent_manager", return_value=mock_agent_manager):
            response = client.post(
                "/agent/sessions",
                json={
                    "tenant_id": "test-tenant",
                    "metadata": {"user_id": "user123"}
                }
            )
            
            assert response.status_code == 200
            data = response.json()
            assert "session_id" in data
    
    def test_create_session_missing_tenant(self, client):
        """Test session creation without tenant_id."""
        response = client.post(
            "/agent/sessions",
            json={}
        )
        
        assert response.status_code == 422  # Validation error
    
    def test_create_session_invalid_json(self, client):
        """Test session creation with invalid JSON."""
        response = client.post(
            "/agent/sessions",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code == 422


class TestSendMessage:
    """Tests for POST /agent/messages endpoint."""
    
    def test_send_message_success(self, client, mock_agent_manager):
        """Test successful message sending."""
        with patch("app.routes.agent.get_agent_manager", return_value=mock_agent_manager):
            response = client.post(
                "/agent/messages",
                json={
                    "session_id": "SES-test-123",
                    "message": "Hello, agent!"
                }
            )
            
            assert response.status_code == 200
            data = response.json()
            assert "response" in data
            assert "session_id" in data
    
    def test_send_message_invalid_session(self, client, mock_agent_manager):
        """Test sending message with invalid session."""
        mock_agent_manager.execute = AsyncMock(
            side_effect=Exception("Session not found")
        )
        
        with patch("app.routes.agent.get_agent_manager", return_value=mock_agent_manager):
            response = client.post(
                "/agent/messages",
                json={
                    "session_id": "INVALID-ID",
                    "message": "Hello"
                }
            )
            
            assert response.status_code in [404, 500]
    
    def test_send_message_empty_message(self, client):
        """Test sending empty message."""
        response = client.post(
            "/agent/messages",
            json={
                "session_id": "SES-test-123",
                "message": ""
            }
        )
        
        # Should reject empty messages
        assert response.status_code in [400, 422]
    
    def test_send_message_missing_fields(self, client):
        """Test sending message with missing required fields."""
        response = client.post(
            "/agent/messages",
            json={"session_id": "SES-test-123"}
        )
        
        assert response.status_code == 422


class TestGetSession:
    """Tests for GET /agent/sessions endpoint."""
    
    def test_get_all_sessions(self, client, mock_agent_manager):
        """Test getting all sessions."""
        mock_agent_manager.get_all_sessions = AsyncMock(return_value=[
            {"session_id": "SES-1", "created_at": "2024-01-01"},
            {"session_id": "SES-2", "created_at": "2024-01-02"}
        ])
        
        with patch("app.routes.agent.get_agent_manager", return_value=mock_agent_manager):
            response = client.get("/agent/sessions")
            
            assert response.status_code == 200
            data = response.json()
            assert isinstance(data, list)
    
    def test_get_session_by_id(self, client, mock_agent_manager, sample_session_data):
        """Test getting specific session."""
        session_id = sample_session_data["session_id"]
        mock_agent_manager.get_session = AsyncMock(return_value=sample_session_data)
        
        with patch("app.routes.agent.get_agent_manager", return_value=mock_agent_manager):
            response = client.get(f"/agent/sessions?session_id={session_id}")
            
            assert response.status_code == 200
            data = response.json()
            assert data["session_id"] == session_id


class TestDeleteSession:
    """Tests for DELETE /agent/sessions/{session_id} endpoint."""
    
    def test_delete_session_success(self, client, mock_agent_manager):
        """Test successful session deletion."""
        mock_agent_manager.delete_session = AsyncMock(return_value=True)
        
        with patch("app.routes.agent.get_agent_manager", return_value=mock_agent_manager):
            response = client.delete("/agent/sessions/SES-test-123")
            
            assert response.status_code == 200
            data = response.json()
            assert "message" in data or "status" in data
    
    def test_delete_nonexistent_session(self, client, mock_agent_manager):
        """Test deleting non-existent session."""
        mock_agent_manager.delete_session = AsyncMock(
            side_effect=Exception("Session not found")
        )
        
        with patch("app.routes.agent.get_agent_manager", return_value=mock_agent_manager):
            response = client.delete("/agent/sessions/INVALID-ID")
            
            assert response.status_code in [404, 500]


class TestAgentEndpointErrors:
    """Tests for error handling in agent endpoints."""
    
    def test_agent_not_initialized(self, client, mock_agent_manager):
        """Test request when agent not initialized."""
        mock_agent_manager.is_initialized = lambda: False
        
        with patch("app.routes.agent.get_agent_manager", return_value=mock_agent_manager):
            response = client.post(
                "/agent/messages",
                json={
                    "session_id": "SES-test-123",
                    "message": "Hello"
                }
            )
            
            # Should return service unavailable
            assert response.status_code in [500, 503]
    
    def test_agent_execution_error(self, client, mock_agent_manager):
        """Test handling of agent execution errors."""
        mock_agent_manager.execute = AsyncMock(
            side_effect=Exception("Agent error")
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


class TestAgentEndpointValidation:
    """Tests for request validation."""
    
    def test_session_id_format_validation(self, client):
        """Test session ID format validation."""
        response = client.post(
            "/agent/messages",
            json={
                "session_id": "invalid-format",
                "message": "Hello"
            }
        )
        
        # May reject invalid format
        assert response.status_code in [200, 400, 422, 404]
    
    def test_message_length_validation(self, client):
        """Test message length validation."""
        # Very long message
        long_message = "x" * 100000
        
        response = client.post(
            "/agent/messages",
            json={
                "session_id": "SES-test-123",
                "message": long_message
            }
        )
        
        # Should handle or reject very long messages
        assert response.status_code in [200, 400, 413, 422]
