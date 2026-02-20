"""
Agent factory for creating and configuring AI agents.

This module handles the creation of agent instances with
proper configuration, tools, and instructions.
"""
import logging
from typing import List, Optional
from agent_framework.azure import AzureOpenAIResponsesClient
from azure.identity import AzureCliCredential

from ..config.settings import get_settings
from ..tools.wrappers import (
    # Order tools
    create_new_order,
    get_order,
    get_customer_orders,
    find_orders,
    update_order,
    list_all_orders,
    # Email tools
    send_simple_email,
    send_formatted_email,
    send_email_with_files,
    send_complete_email,
    test_email_connection,
)
from ..tools.mcp_handler import get_mcp_tool, is_mcp_available
from .instructions import get_full_system_prompt
from ..utils.exceptions import AgentInitializationError

logger = logging.getLogger(__name__)


class AgentFactory:
    """Factory for creating AI agent instances."""
    
    @staticmethod
    def create_client() -> AzureOpenAIResponsesClient:
        """
        Create Azure OpenAI Responses client.
        
        Returns:
            AzureOpenAIResponsesClient: Configured client instance
            
        Raises:
            AgentInitializationError: If client creation fails
        """
        try:
            settings = get_settings()
            
            logger.info("Creating Azure OpenAI Responses client...")
            
            credential = AzureCliCredential()
            client = AzureOpenAIResponsesClient(
                project_endpoint=settings.azure_ai_project_endpoint,
                deployment_name=settings.azure_openai_model_name,
                credential=credential
            )
            
            logger.info("Azure OpenAI Responses client created successfully")
            return client
            
        except Exception as e:
            error_msg = f"Failed to create Azure OpenAI client: {str(e)}"
            logger.error(error_msg)
            raise AgentInitializationError(error_msg)
    
    @staticmethod
    def create_agent(
        client: AzureOpenAIResponsesClient,
        name: str = "CustomerServiceAgent",
        instructions: Optional[str] = None,
        tools: Optional[List] = None
    ):
        """
        Create a new AI agent with configured tools.
        
        Args:
            client: Azure OpenAI Responses client
            name: Agent name
            instructions: System instructions (default: from instructions.py)
            tools: List of tools to register (default: all available tools)
            
        Returns:
            Agent instance from agent_framework
            
        Raises:
            AgentInitializationError: If agent creation fails
        """
        try:
            logger.info(f"Creating agent '{name}'...")
            
            # Use default instructions if not provided
            if instructions is None:
                instructions = get_full_system_prompt()
            
            # Gather all tools if not provided
            if tools is None:
                tools = AgentFactory._get_all_tools()
            
            logger.info(f"Registering {len(tools)} tools with agent")
            
            # Create agent using client
            agent = client.as_agent(
                name=name,
                instructions=instructions,
                tools=tools
            )
            
            logger.info(f"Agent '{name}' created successfully")
            return agent
            
        except Exception as e:
            error_msg = f"Failed to create agent: {str(e)}"
            logger.error(error_msg)
            raise AgentInitializationError(error_msg)
    
    @staticmethod
    def _get_all_tools() -> List:
        """
        Get all available tools for agent registration.
        
        Returns:
            List: List of all tools
        """
        tools = []
        
        # Add order management tools (6)
        order_tools = [
            create_new_order,
            get_order,
            get_customer_orders,
            find_orders,
            update_order,
            list_all_orders
        ]
        tools.extend(order_tools)
        logger.debug(f"Added {len(order_tools)} order management tools")
        
        # Add email tools (5)
        email_tools = [
            send_simple_email,
            send_formatted_email,
            send_email_with_files,
            send_complete_email,
            test_email_connection
        ]
        tools.extend(email_tools)
        logger.debug(f"Added {len(email_tools)} email tools")
        
        # Add MCP tool if available (1)
        if is_mcp_available():
            mcp_tool = get_mcp_tool()
            if mcp_tool:
                tools.append(mcp_tool)
                logger.debug("Added MCP complaint management tool")
        else:
            logger.warning("MCP tool not available - complaint management disabled")
        
        logger.info(f"Total tools available: {len(tools)}")
        return tools
    
    @staticmethod
    def get_tool_descriptions() -> dict:
        """
        Get descriptions of all available tools.
        
        Returns:
            dict: Tool names and descriptions
        """
        descriptions = {
            # Order tools
            "create_new_order": "Create a new order in the system",
            "get_order": "Retrieve a specific order by ID",
            "get_customer_orders": "Get all orders for a customer",
            "find_orders": "Search orders by multiple criteria",
            "update_order": "Update order status",
            "list_all_orders": "List all orders in system",
            
            # Email tools
            "send_simple_email": "Send plain text email",
            "send_formatted_email": "Send HTML formatted email",
            "send_email_with_files": "Send email with attachments",
            "send_complete_email": "Send email with full options",
            "test_email_connection": "Test SMTP connection",
        }
        
        # Add MCP tool if available
        if is_mcp_available():
            descriptions["complaint_management"] = "Manage customer complaints (register, track, resolve, archive)"
        
        return descriptions


# Export public API
__all__ = [
    "AgentFactory",
]
