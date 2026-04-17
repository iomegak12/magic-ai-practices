"""
API Information Endpoints

Endpoints for retrieving API information and available tools.
"""
import logging
from fastapi import APIRouter, status

from ..models import APIInfo, ListToolsResponse, ToolInfo
from ...config.settings import get_settings
from ...agent.factory import AgentFactory
from ...tools.mcp_handler import is_mcp_available
from ... import __version__

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/info", tags=["Info"])


@router.get(
    "",
    response_model=APIInfo,
    status_code=status.HTTP_200_OK,
    summary="API Information",
    description="Get information about the API"
)
async def get_api_info() -> APIInfo:
    """
    Get API information.
    
    Returns:
        APIInfo: API information including version and documentation
    """
    settings = get_settings()
    
    return APIInfo(
        name="Customer Service Agent API",
        version=__version__,
        description=(
            "REST API for AI-powered customer service agent with order management, "
            "email communication, and complaint tracking capabilities."
        ),
        documentation_url="/docs",
        contact={
            "name": "API Support",
            "email": settings.sender_email if settings.sender_email else "support@example.com",
            "url": "https://github.com/yourusername/project"
        }
    )


@router.get(
    "/tools",
    response_model=ListToolsResponse,
    status_code=status.HTTP_200_OK,
    summary="List Tools",
    description="Get information about available agent tools"
)
async def list_tools() -> ListToolsResponse:
    """
    List all available agent tools.
    
    Returns:
        ListToolsResponse: Information about available tools
    """
    # Get tool descriptions from factory
    tool_descriptions = AgentFactory.get_tool_descriptions()
    
    # Create tool info objects
    tools = []
    
    # Order tools
    order_tool_names = [
        "create_new_order", "get_order", "get_customer_orders",
        "find_orders", "update_order", "list_all_orders"
    ]
    for name in order_tool_names:
        if name in tool_descriptions:
            tools.append(ToolInfo(
                name=name,
                description=tool_descriptions[name],
                category="order",
                available=True
            ))
    
    # Email tools
    email_tool_names = [
        "send_simple_email", "send_formatted_email", "send_email_with_files",
        "send_complete_email", "test_email_connection"
    ]
    for name in email_tool_names:
        if name in tool_descriptions:
            tools.append(ToolInfo(
                name=name,
                description=tool_descriptions[name],
                category="email",
                available=True
            ))
    
    # MCP tool (complaint management)
    if "complaint_management" in tool_descriptions:
        tools.append(ToolInfo(
            name="complaint_management",
            description=tool_descriptions["complaint_management"],
            category="complaint",
            available=is_mcp_available()
        ))
    
    categories = ["order", "email"]
    if is_mcp_available():
        categories.append("complaint")
    
    return ListToolsResponse(
        tools=tools,
        total_count=len(tools),
        categories=categories
    )


# Export router
__all__ = ["router"]
