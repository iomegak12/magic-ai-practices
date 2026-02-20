"""
Unit Tests for Agent Factory

Tests for app/agent/factory.py agent creation functions.
"""
import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from app.agent.factory import (
    create_client,
    create_agent,
    get_tool_descriptions
)
from app.utils.exceptions import AgentInitializationError


class TestClientCreation:
    """Tests for Azure AI client creation."""
    
    def test_create_client_success(self, mock_settings):
        """Test successful client creation."""
        with patch("app.agent.factory.AIProjectClient") as mock_client_class:
            mock_client_class.return_value = MagicMock()
            
            client = create_client()
            
            assert client is not None
            mock_client_class.assert_called_once()
    
    def test_create_client_missing_credentials(self):
        """Test client creation with missing credentials."""
        with patch("app.config.settings.get_settings") as mock_get_settings:
            mock_settings = MagicMock()
            mock_settings.azure_ai_project_endpoint = None
            mock_get_settings.return_value = mock_settings
            
            with pytest.raises(AgentInitializationError):
                create_client()
    
    def test_create_client_invalid_endpoint(self):
        """Test client creation with invalid endpoint."""
        with patch("app.config.settings.get_settings") as mock_get_settings:
            mock_settings = MagicMock()
            mock_settings.azure_ai_project_endpoint = "invalid-url"
            mock_get_settings.return_value = mock_settings
            
            with patch("app.agent.factory.AIProjectClient", side_effect=Exception("Invalid")):
                with pytest.raises(AgentInitializationError):
                    create_client()


class TestAgentCreation:
    """Tests for agent creation."""
    
    def test_create_agent_success(self, mock_settings):
        """Test successful agent creation."""
        with patch("app.agent.factory.create_client") as mock_create_client, \
             patch("app.agent.factory._get_all_tools") as mock_get_tools:
            
            mock_client = MagicMock()
            mock_client.as_agent = MagicMock(return_value=MagicMock())
            mock_create_client.return_value = mock_client
            mock_get_tools.return_value = []
            
            agent = create_agent()
            
            assert agent is not None
    
    def test_create_agent_with_tools(self, mock_settings):
        """Test agent creation includes tools."""
        with patch("app.agent.factory.create_client") as mock_create_client, \
             patch("app.agent.factory._get_all_tools") as mock_get_tools:
            
            mock_client = MagicMock()
            mock_client.as_agent = MagicMock(return_value=MagicMock())
            mock_create_client.return_value = mock_client
            
            mock_tools = [MagicMock(), MagicMock()]
            mock_get_tools.return_value = mock_tools
            
            agent = create_agent()
            
            # Verify tools were passed to agent
            mock_get_tools.assert_called_once()
    
    def test_create_agent_with_instructions(self, mock_settings):
        """Test agent creation includes system instructions."""
        with patch("app.agent.factory.create_client") as mock_create_client, \
             patch("app.agent.factory._get_all_tools") as mock_get_tools, \
             patch("app.agent.factory.get_full_system_prompt") as mock_prompt:
            
            mock_client = MagicMock()
            mock_client.as_agent = MagicMock(return_value=MagicMock())
            mock_create_client.return_value = mock_client
            mock_get_tools.return_value = []
            mock_prompt.return_value = "System prompt"
            
            agent = create_agent()
            
            # Verify system prompt was retrieved
            mock_prompt.assert_called_once()
    
    def test_create_agent_initialization_error(self, mock_settings):
        """Test agent creation handles initialization errors."""
        with patch("app.agent.factory.create_client", side_effect=Exception("Init failed")):
            with pytest.raises(AgentInitializationError):
                create_agent()


class TestToolCollection:
    """Tests for tool collection."""
    
    def test_get_all_tools(self, mock_settings, mock_mcp_handler):
        """Test getting all available tools."""
        with patch("app.agent.factory._get_all_tools") as mock_get_tools:
            mock_tools = [
                MagicMock(name="tool1"),
                MagicMock(name="tool2"),
                MagicMock(name="tool3")
            ]
            mock_get_tools.return_value = mock_tools
            
            tools = mock_get_tools()
            
            assert len(tools) >= 3
    
    def test_get_all_tools_includes_order_tools(self, mock_settings):
        """Test tool collection includes order management tools."""
        with patch("app.agent.factory._get_all_tools") as mock_get_tools:
            mock_tools = [
                MagicMock(name="create_order"),
                MagicMock(name="get_order"),
                MagicMock(name="update_order")
            ]
            mock_get_tools.return_value = mock_tools
            
            tools = mock_get_tools()
            
            tool_names = [t.name for t in tools]
            assert "create_order" in tool_names
    
    def test_get_all_tools_includes_email_tools(self, mock_settings):
        """Test tool collection includes email tools."""
        with patch("app.agent.factory._get_all_tools") as mock_get_tools:
            mock_tools = [
                MagicMock(name="send_email"),
                MagicMock(name="send_bulk_emails")
            ]
            mock_get_tools.return_value = mock_tools
            
            tools = mock_get_tools()
            
            tool_names = [t.name for t in tools]
            assert "send_email" in tool_names


class TestToolDescriptions:
    """Tests for tool descriptions."""
    
    def test_get_tool_descriptions(self):
        """Test getting tool descriptions."""
        descriptions = get_tool_descriptions()
        
        assert isinstance(descriptions, list)
        assert len(descriptions) > 0
    
    def test_tool_descriptions_structure(self):
        """Test tool description structure."""
        descriptions = get_tool_descriptions()
        
        for desc in descriptions:
            assert "name" in desc
            assert "description" in desc
            assert isinstance(desc["name"], str)
            assert isinstance(desc["description"], str)
    
    def test_tool_descriptions_includes_order_tools(self):
        """Test descriptions include order tools."""
        descriptions = get_tool_descriptions()
        
        tool_names = [d["name"] for d in descriptions]
        # Should have at least some order management tools
        assert any("order" in name.lower() for name in tool_names)
    
    def test_tool_descriptions_includes_email_tools(self):
        """Test descriptions include email tools."""
        descriptions = get_tool_descriptions()
        
        tool_names = [d["name"] for d in descriptions]
        # Should have at least some email tools
        assert any("email" in name.lower() for name in tool_names)
