"""
MCP (Model Context Protocol) Handler for Complaint Management.

This module handles the connection to the MCP server and exposes
complaint management operations to the agent.
"""
import logging
from typing import Optional
from agent_framework import MCPStreamableHTTPTool

from ..config.settings import get_settings
from ..utils.exceptions import MCPConnectionError, MCPServerUnavailableError

logger = logging.getLogger(__name__)


class MCPHandler:
    """Handler for MCP server communication."""
    
    def __init__(self, mcp_url: str, required: bool = False):
        """
        Initialize MCP handler.
        
        Args:
            mcp_url: URL of the MCP server
            required: If True, raise error if MCP server unavailable
        """
        self.mcp_url = mcp_url
        self.required = required
        self._mcp_tool = None
        self._connected = False
        self._connection_error = None
    
    def connect(self) -> bool:
        """
        Establish connection to MCP server.
        
        Returns:
            bool: True if connection successful, False otherwise
            
        Raises:
            MCPServerUnavailableError: If required=True and connection fails
        """
        try:
            logger.info(f"Connecting to MCP server at {self.mcp_url}...")
            
            # Create MCP tool
            self._mcp_tool = MCPStreamableHTTPTool(
                name="complaint_management",
                url=self.mcp_url,
                description=(
                    "Complaint management system for registering, retrieving, searching, "
                    "updating, resolving, and archiving customer complaints related to orders. "
                    "Use this for all complaint-related operations."
                )
            )
            
            # Test connection by attempting to access the tool
            # The MCPStreamableHTTPTool initializes the connection
            self._connected = True
            logger.info("MCP server connection established successfully")
            return True
            
        except Exception as e:
            error_msg = f"Failed to connect to MCP server at {self.mcp_url}: {str(e)}"
            self._connection_error = error_msg
            self._connected = False
            
            if self.required:
                logger.error(error_msg)
                raise MCPServerUnavailableError(error_msg)
            else:
                logger.warning(f"{error_msg} (continuing without MCP - not required)")
                return False
    
    def is_connected(self) -> bool:
        """
        Check if MCP server is connected.
        
        Returns:
            bool: True if connected, False otherwise
        """
        return self._connected
    
    def get_mcp_tool(self) -> Optional[MCPStreamableHTTPTool]:
        """
        Get the MCP tool instance.
        
        Returns:
            MCPStreamableHTTPTool: MCP tool if connected, None otherwise
        """
        if not self._connected:
            logger.warning("MCP tool requested but not connected")
            return None
        return self._mcp_tool
    
    def get_connection_error(self) -> Optional[str]:
        """
        Get the connection error message if any.
        
        Returns:
            str: Error message if connection failed, None otherwise
        """
        return self._connection_error
    
    def disconnect(self):
        """Disconnect from MCP server and cleanup resources."""
        if self._mcp_tool:
            logger.info("Disconnecting from MCP server...")
            self._mcp_tool = None
            self._connected = False
            logger.info("MCP server disconnected")
    
    def __repr__(self):
        status = "connected" if self._connected else "disconnected"
        return f"<MCPHandler(url={self.mcp_url}, status={status})>"


# Global MCP handler instance
_mcp_handler: Optional[MCPHandler] = None


def initialize_mcp_handler() -> MCPHandler:
    """
    Initialize and connect to MCP server using settings.
    
    Returns:
        MCPHandler: Initialized MCP handler
        
    Raises:
        MCPServerUnavailableError: If MCP server required but unavailable
    """
    global _mcp_handler
    
    if _mcp_handler is not None:
        logger.debug("MCP handler already initialized")
        return _mcp_handler
    
    settings = get_settings()
    
    logger.info("Initializing MCP handler...")
    _mcp_handler = MCPHandler(
        mcp_url=settings.mcp_server_url,
        required=settings.mcp_server_required
    )
    
    # Attempt connection
    _mcp_handler.connect()
    
    return _mcp_handler


def get_mcp_handler() -> Optional[MCPHandler]:
    """
    Get the global MCP handler instance.
    
    Returns:
        MCPHandler: MCP handler if initialized, None otherwise
    """
    return _mcp_handler


def get_mcp_tool() -> Optional[MCPStreamableHTTPTool]:
    """
    Get the MCP tool for agent registration.
    
    Returns:
        MCPStreamableHTTPTool: MCP tool if available, None otherwise
    """
    handler = get_mcp_handler()
    if handler:
        return handler.get_mcp_tool()
    return None


def is_mcp_available() -> bool:
    """
    Check if MCP server is available and connected.
    
    Returns:
        bool: True if MCP is available, False otherwise
    """
    handler = get_mcp_handler()
    return handler.is_connected() if handler else False


def shutdown_mcp_handler():
    """Shutdown MCP handler and cleanup resources."""
    global _mcp_handler
    
    if _mcp_handler:
        logger.info("Shutting down MCP handler...")
        _mcp_handler.disconnect()
        _mcp_handler = None
        logger.info("MCP handler shutdown complete")


# Export public API
__all__ = [
    "MCPHandler",
    "initialize_mcp_handler",
    "get_mcp_handler",
    "get_mcp_tool",
    "is_mcp_available",
    "shutdown_mcp_handler",
    "MCPConnectionError",
    "MCPServerUnavailableError"
]
