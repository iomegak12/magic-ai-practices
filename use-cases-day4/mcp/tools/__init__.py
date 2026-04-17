"""Register all MCP tools on the FastMCP server instance."""

from typing import Annotated
from pydantic import Field


def register_tools(mcp) -> None:
    """Decorate and register all order & complaint tools."""

    # -- lazy imports so modules are resolved after sys.path is ready --
    from tools.order_tools import (
        get_orders_by_customer as _get_orders_by_customer,
        search_orders_by_sku as _search_orders_by_sku,
        search_orders_by_status as _search_orders_by_status,
    )
    from tools.complaint_tools import (
        get_complaints_by_order as _get_complaints_by_order,
        get_complaints_by_customer as _get_complaints_by_customer,
        register_complaint as _register_complaint,
        resolve_complaint as _resolve_complaint,
    )

    # ---- Order tools (read-only) ----------------------------------------

    @mcp.tool(
        name="get_orders_by_customer",
        description="Get all orders for a customer name. Supports partial and case-insensitive matching.",
        tags={"orders", "search"},
        annotations={"readOnlyHint": True},
    )
    def get_orders_by_customer(
        customer_name: Annotated[str, Field(description="Full or partial customer name to search for")],
    ) -> dict:
        """Get orders matching a customer name."""
        return _get_orders_by_customer(customer_name)

    @mcp.tool(
        name="search_orders_by_sku",
        description="Search orders by exact product SKU (8-character alphanumeric code).",
        tags={"orders", "search"},
        annotations={"readOnlyHint": True},
    )
    def search_orders_by_sku(
        product_sku: Annotated[str, Field(description="Exact 8-char product SKU, e.g. MSSFPRO9")],
    ) -> dict:
        """Search orders by product SKU."""
        return _search_orders_by_sku(product_sku)

    @mcp.tool(
        name="search_orders_by_status",
        description="Search orders filtered by order status. Valid statuses: Pending, Processing, Shipped, Delivered, Cancelled, Returned.",
        tags={"orders", "search"},
        annotations={"readOnlyHint": True},
    )
    def search_orders_by_status(
        order_status: Annotated[str, Field(description="Order status to filter by")],
    ) -> dict:
        """Search orders by status."""
        return _search_orders_by_status(order_status)

    # ---- Complaint tools -------------------------------------------------

    @mcp.tool(
        name="get_complaints_by_order",
        description="Get all complaints filed against a specific order ID.",
        tags={"complaints", "search"},
        annotations={"readOnlyHint": True},
    )
    def get_complaints_by_order(
        order_id: Annotated[str, Field(description="Order ID, e.g. ORD10001")],
    ) -> dict:
        """Get complaints for an order."""
        return _get_complaints_by_order(order_id)

    @mcp.tool(
        name="get_complaints_by_customer",
        description="Get all complaints for a customer name. Supports partial and case-insensitive matching via order join.",
        tags={"complaints", "search"},
        annotations={"readOnlyHint": True},
    )
    def get_complaints_by_customer(
        customer_name: Annotated[str, Field(description="Full or partial customer name to search for")],
    ) -> dict:
        """Get complaints for a customer."""
        return _get_complaints_by_customer(customer_name)

    @mcp.tool(
        name="register_complaint",
        description="Register a new complaint against an existing order. Priority defaults to Medium if not specified.",
        tags={"complaints", "write"},
    )
    def register_complaint(
        order_id: Annotated[str, Field(description="The order ID to file the complaint against, e.g. ORD10001")],
        complaint_description: Annotated[str, Field(description="Detailed description of the complaint")],
        priority: Annotated[str | None, Field(description="Complaint priority: Low, Medium, High, or Critical. Defaults to Medium.")] = None,
    ) -> dict:
        """Register a complaint."""
        return _register_complaint(order_id, complaint_description, priority)

    @mcp.tool(
        name="resolve_complaint",
        description="Resolve an existing complaint by providing a resolution note. Changes status to Resolved.",
        tags={"complaints", "write"},
    )
    def resolve_complaint(
        complaint_id: Annotated[str, Field(description="The complaint ID to resolve, e.g. COMP10001")],
        resolution_note: Annotated[str, Field(description="Detailed note explaining how the complaint was resolved")],
    ) -> dict:
        """Resolve a complaint."""
        return _resolve_complaint(complaint_id, resolution_note)
