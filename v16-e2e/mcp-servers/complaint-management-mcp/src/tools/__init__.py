"""
MCP Tools Package

This package contains all MCP tool implementations for complaint management.

Tools:
    - register_complaint:  Register a new complaint
    - get_complaint:       Retrieve complaint details by ID
    - search_complaints:   Search complaints with OR-logic filters
    - resolve_complaint:   Mark a complaint as resolved
    - update_complaint:    Update complaint title / description / remarks
    - archive_complaint:   Soft-delete a complaint

Usage:
    from src.tools import register_all_tools
    register_all_tools(mcp)
"""

from src.tools.register_complaint import register_complaint
from src.tools.get_complaint import get_complaint
from src.tools.search_complaints import search_complaints
from src.tools.resolve_complaint import resolve_complaint
from src.tools.update_complaint import update_complaint
from src.tools.archive_complaint import archive_complaint


def register_all_tools(mcp) -> None:
    """
    Register all 6 complaint-management tools onto a FastMCP instance.

    Args:
        mcp: A :class:`fastmcp.FastMCP` application instance.
    """
    mcp.tool()(register_complaint)
    mcp.tool()(get_complaint)
    mcp.tool()(search_complaints)
    mcp.tool()(resolve_complaint)
    mcp.tool()(update_complaint)
    mcp.tool()(archive_complaint)


__all__ = [
    "register_complaint",
    "get_complaint",
    "search_complaints",
    "resolve_complaint",
    "update_complaint",
    "archive_complaint",
    "register_all_tools",
]
