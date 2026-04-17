"""
Unit Tests for Tool Wrappers

Tests for tool wrapper functions in app/tools/.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.utils.exceptions import OrderManagementError, EmailSendError


class TestOrderTools:
    """Tests for order management tool wrappers."""
    
    @pytest.mark.asyncio
    async def test_create_order_wrapper(self, sample_order_data):
        """Test create_order tool wrapper."""
        with patch("app.tools.order_tools.create_order") as mock_create:
            mock_create.return_value = {"order_id": "ORD-123", "status": "created"}
            
            from app.tools.order_tools import create_order_tool
            
            result = await create_order_tool(
                customer_name=sample_order_data["customer_name"],
                items=sample_order_data["items"],
                total_amount=sample_order_data["total_amount"]
            )
            
            assert "order_id" in result
            assert result["status"] == "created"
    
    @pytest.mark.asyncio
    async def test_get_order_wrapper(self):
        """Test get_order tool wrapper."""
        with patch("app.tools.order_tools.get_order") as mock_get:
            mock_get.return_value = {
                "order_id": "ORD-123",
                "customer_name": "John Doe",
                "status": "pending"
            }
            
            from app.tools.order_tools import get_order_tool
            
            result = await get_order_tool(order_id="ORD-123")
            
            assert result["order_id"] == "ORD-123"
            assert "customer_name" in result
    
    @pytest.mark.asyncio
    async def test_update_order_wrapper(self):
        """Test update_order tool wrapper."""
        with patch("app.tools.order_tools.update_order") as mock_update:
            mock_update.return_value = {"order_id": "ORD-123", "status": "shipped"}
            
            from app.tools.order_tools import update_order_tool
            
            result = await update_order_tool(
                order_id="ORD-123",
                status="shipped"
            )
            
            assert result["status"] == "shipped"
    
    @pytest.mark.asyncio
    async def test_list_orders_wrapper(self):
        """Test list_orders tool wrapper."""
        with patch("app.tools.order_tools.list_orders") as mock_list:
            mock_list.return_value = [
                {"order_id": "ORD-123"},
                {"order_id": "ORD-124"}
            ]
            
            from app.tools.order_tools import list_orders_tool
            
            result = await list_orders_tool()
            
            assert isinstance(result, list)
            assert len(result) == 2
    
    @pytest.mark.asyncio
    async def test_order_tool_error_handling(self):
        """Test order tool error handling."""
        with patch("app.tools.order_tools.get_order", side_effect=Exception("DB error")):
            from app.tools.order_tools import get_order_tool
            
            with pytest.raises(OrderManagementError):
                await get_order_tool(order_id="ORD-123")


class TestEmailTools:
    """Tests for email tool wrappers."""
    
    @pytest.mark.asyncio
    async def test_send_email_wrapper(self, sample_email_data):
        """Test send_email tool wrapper."""
        with patch("app.tools.email_tools.send_email") as mock_send:
            mock_send.return_value = {"status": "sent", "message_id": "MSG-123"}
            
            from app.tools.email_tools import send_email_tool
            
            result = await send_email_tool(
                to_email=sample_email_data["to_email"],
                subject=sample_email_data["subject"],
                body=sample_email_data["body"]
            )
            
            assert result["status"] == "sent"
            assert "message_id" in result
    
    @pytest.mark.asyncio
    async def test_send_bulk_emails_wrapper(self):
        """Test send_bulk_emails tool wrapper."""
        with patch("app.tools.email_tools.send_bulk_emails") as mock_send:
            mock_send.return_value = {
                "sent": 3,
                "failed": 0,
                "results": []
            }
            
            from app.tools.email_tools import send_bulk_emails_tool
            
            recipients = [
                {"email": "user1@example.com", "name": "User 1"},
                {"email": "user2@example.com", "name": "User 2"}
            ]
            
            result = await send_bulk_emails_tool(
                recipients=recipients,
                subject="Test",
                body="Test message"
            )
            
            assert "sent" in result
            assert result["sent"] >= 0
    
    @pytest.mark.asyncio
    async def test_email_tool_error_handling(self):
        """Test email tool error handling."""
        with patch("app.tools.email_tools.send_email", side_effect=Exception("SMTP error")):
            from app.tools.email_tools import send_email_tool
            
            with pytest.raises(EmailSendError):
                await send_email_tool(
                    to_email="test@example.com",
                    subject="Test",
                    body="Test"
                )


class TestMCPHandler:
    """Tests for MCP handler."""
    
    @pytest.mark.asyncio
    async def test_mcp_handler_initialization(self, mock_settings):
        """Test MCP handler initialization."""
        from app.tools.mcp_handler import MCPHandler
        
        handler = MCPHandler()
        
        assert handler is not None
        assert hasattr(handler, "connect")
        assert hasattr(handler, "disconnect")
    
    @pytest.mark.asyncio
    async def test_mcp_handler_connect(self, mock_mcp_handler):
        """Test MCP handler connection."""
        await mock_mcp_handler.connect()
        
        assert mock_mcp_handler.is_connected() is True
    
    @pytest.mark.asyncio
    async def test_mcp_handler_get_tool(self, mock_mcp_handler):
        """Test getting MCP tool."""
        tool = mock_mcp_handler.get_mcp_tool()
        
        assert tool is not None
    
    @pytest.mark.asyncio
    async def test_mcp_handler_disconnect(self, mock_mcp_handler):
        """Test MCP handler disconnection."""
        await mock_mcp_handler.disconnect()
        
        # Should not raise
        assert True


class TestToolDecorators:
    """Tests for tool decorator functionality."""
    
    def test_tool_decorator_metadata(self):
        """Test that tools have proper metadata."""
        from app.tools.order_tools import create_order_tool
        
        # Tool should have name, description, etc.
        assert hasattr(create_order_tool, "__name__")
        assert callable(create_order_tool)
    
    def test_async_tool_wrapper(self):
        """Test that tool wrappers are async."""
        from app.tools.order_tools import create_order_tool
        from inspect import iscoroutinefunction
        
        assert iscoroutinefunction(create_order_tool)
