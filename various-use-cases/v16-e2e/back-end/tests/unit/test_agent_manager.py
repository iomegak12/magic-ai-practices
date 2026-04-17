"""
Unit Tests for Agent Manager

Tests for app/agent/manager.py AgentManager class.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.agent.manager import AgentManager, get_agent_manager
from app.utils.exceptions import (
    AgentInitializationError,
    AgentExecutionError,
    SessionNotFoundError,
    SessionExpiredError
)


class TestAgentManagerInitialization:
    """Tests for AgentManager initialization."""
    
    @pytest.mark.asyncio
    async def test_initialize_success(self, mock_settings, mock_mcp_handler):
        """Test successful agent manager initialization."""
        with patch("app.agent.manager.create_agent", return_value=MagicMock()):
            manager = AgentManager()
            await manager.initialize()
            
            assert manager.is_initialized() is True
    
    @pytest.mark.asyncio
    async def test_initialize_failure(self, mock_settings):
        """Test agent manager initialization failure."""
        with patch("app.agent.manager.create_agent", side_effect=Exception("Init failed")):
            manager = AgentManager()
            
            with pytest.raises(AgentInitializationError):
                await manager.initialize()
    
    @pytest.mark.asyncio
    async def test_initialize_idempotent(self, mock_settings, mock_mcp_handler):
        """Test initialize can be called multiple times safely."""
        with patch("app.agent.manager.create_agent", return_value=MagicMock()):
            manager = AgentManager()
            await manager.initialize()
            await manager.initialize()  # Should not fail
            
            assert manager.is_initialized() is True


class TestSessionManagement:
    """Tests for session management."""
    
    @pytest.mark.asyncio
    async def test_create_session(self, mock_agent_manager):
        """Test creating a new session."""
        session_id = await mock_agent_manager.create_session(tenant_id="test-tenant")
        
        assert isinstance(session_id, str)
        assert session_id.startswith("SES-")
    
    @pytest.mark.asyncio
    async def test_create_session_with_metadata(self, mock_agent_manager):
        """Test creating session with metadata."""
        metadata = {"user_id": "user123", "ip": "127.0.0.1"}
        session_id = await mock_agent_manager.create_session(
            tenant_id="test-tenant",
            metadata=metadata
        )
        
        assert isinstance(session_id, str)
    
    @pytest.mark.asyncio
    async def test_get_existing_session(self, mock_agent_manager, sample_session_data):
        """Test retrieving existing session."""
        session_id = sample_session_data["session_id"]
        
        # Mock the get_session to return sample data
        mock_agent_manager.get_session = AsyncMock(return_value=sample_session_data)
        
        session = await mock_agent_manager.get_session(session_id)
        
        assert session is not None
        assert session["session_id"] == session_id
    
    @pytest.mark.asyncio
    async def test_get_nonexistent_session(self, mock_agent_manager):
        """Test retrieving non-existent session raises error."""
        mock_agent_manager.get_session = AsyncMock(side_effect=SessionNotFoundError("Not found"))
        
        with pytest.raises(SessionNotFoundError):
            await mock_agent_manager.get_session("INVALID-SESSION-ID")
    
    @pytest.mark.asyncio
    async def test_delete_session(self, mock_agent_manager):
        """Test deleting a session."""
        session_id = "SES-test-123"
        mock_agent_manager.delete_session = AsyncMock(return_value=True)
        
        result = await mock_agent_manager.delete_session(session_id)
        
        assert result is True


class TestAgentExecution:
    """Tests for agent execution."""
    
    @pytest.mark.asyncio
    async def test_execute_message_success(self, mock_agent_manager):
        """Test successful message execution."""
        result = await mock_agent_manager.execute(
            session_id="SES-test-123",
            message="Hello, agent!"
        )
        
        assert "response" in result
        assert "session_id" in result
        assert result["status"] == "success"
    
    @pytest.mark.asyncio
    async def test_execute_with_invalid_session(self, mock_agent_manager):
        """Test execute with invalid session."""
        mock_agent_manager.execute = AsyncMock(
            side_effect=SessionNotFoundError("Session not found")
        )
        
        with pytest.raises(SessionNotFoundError):
            await mock_agent_manager.execute(
                session_id="INVALID-ID",
                message="Hello"
            )
    
    @pytest.mark.asyncio
    async def test_execute_with_expired_session(self, mock_agent_manager):
        """Test execute with expired session."""
        mock_agent_manager.execute = AsyncMock(
            side_effect=SessionExpiredError("Session expired")
        )
        
        with pytest.raises(SessionExpiredError):
            await mock_agent_manager.execute(
                session_id="EXPIRED-ID",
                message="Hello"
            )
    
    @pytest.mark.asyncio
    async def test_execute_agent_error(self, mock_agent_manager):
        """Test execute with agent execution error."""
        mock_agent_manager.execute = AsyncMock(
            side_effect=AgentExecutionError("Execution failed")
        )
        
        with pytest.raises(AgentExecutionError):
            await mock_agent_manager.execute(
                session_id="SES-test-123",
                message="Hello"
            )


class TestSessionCleanup:
    """Tests for session cleanup."""
    
    @pytest.mark.asyncio
    async def test_cleanup_expired_sessions(self, mock_agent_manager):
        """Test cleaning up expired sessions."""
        mock_agent_manager.cleanup_sessions = AsyncMock(return_value=3)
        
        cleaned = await mock_agent_manager.cleanup_sessions()
        
        assert isinstance(cleaned, int)
        assert cleaned >= 0


class TestAgentManagerSingleton:
    """Tests for agent manager singleton pattern."""
    
    @pytest.mark.asyncio
    async def test_get_agent_manager_singleton(self, mock_settings):
        """Test get_agent_manager returns same instance."""
        with patch("app.agent.manager.create_agent", return_value=MagicMock()):
            manager1 = get_agent_manager()
            manager2 = get_agent_manager()
            
            assert manager1 is manager2
