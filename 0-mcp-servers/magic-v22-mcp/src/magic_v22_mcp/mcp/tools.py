"""MCP Tools — all 8 business capabilities exposed as FastMCP tools."""

from __future__ import annotations

from typing import Annotated, Optional

from fastmcp import FastMCP
from fastmcp.exceptions import ToolError
from pydantic import Field

from magic_v22_mcp.enums import ComplaintPriority, ComplaintStatus, ResolverTeam
from magic_v22_mcp.services import complaint_service, order_service
from magic_v22_mcp.services.complaint_service import ComplaintServiceError
from magic_v22_mcp.services.order_service import OrderServiceError


def register_tools(mcp: FastMCP) -> None:
    """Register all order and complaint tools onto the FastMCP instance."""

    # ── Orders ────────────────────────────────────────────────────────────────

    @mcp.tool(
        name="make_order",
        description="Create a new customer order. Returns the created order with its assigned order_id and order_number.",
        annotations={"readOnlyHint": False},
    )
    def make_order(
        customer_name: Annotated[str, Field(description="Full name of the customer placing the order.")],
        product_sku: Annotated[str, Field(description="Product SKU identifier.")],
        units: Annotated[int, Field(description="Number of units ordered. Must be greater than 0.", gt=0)],
        order_amount: Annotated[int, Field(description="Total order amount in cents/base currency unit. Must be >= 0.", ge=0)],
        remarks: Annotated[str, Field(description="Optional remarks or special instructions for the order.")] = "",
        order_number: Annotated[
            Optional[str],
            Field(description="Optional order number in format ORDxxxxx (e.g. ORD10001). Auto-generated if omitted."),
        ] = None,
    ) -> dict:
        try:
            order = order_service.make_order(
                customer_name=customer_name,
                product_sku=product_sku,
                units=units,
                order_amount=order_amount,
                remarks=remarks,
                order_number=order_number,
            )
            return order.model_dump(mode="json")
        except OrderServiceError as e:
            raise ToolError(str(e)) from e

    @mcp.tool(
        name="query_orders",
        description="Search orders by customer name and/or product SKU. Both filters are optional, case-insensitive, and support partial matching. Returns all orders if both are omitted.",
        annotations={"readOnlyHint": True},
    )
    def query_orders(
        customer_name: Annotated[
            Optional[str],
            Field(description="Partial customer name to filter by (case-insensitive)."),
        ] = None,
        product_sku: Annotated[
            Optional[str],
            Field(description="Partial product SKU to filter by (case-insensitive)."),
        ] = None,
    ) -> list[dict]:
        orders = order_service.query_orders(customer_name=customer_name, product_sku=product_sku)
        return [o.model_dump(mode="json") for o in orders]

    @mcp.tool(
        name="get_order_details",
        description="Retrieve full details of a specific order by its order_id.",
        annotations={"readOnlyHint": True},
    )
    def get_order_details(
        order_id: Annotated[int, Field(description="The integer ID of the order to retrieve.")],
    ) -> dict:
        try:
            return order_service.get_order_details(order_id).model_dump(mode="json")
        except OrderServiceError as e:
            raise ToolError(str(e)) from e

    # ── Complaints ────────────────────────────────────────────────────────────

    @mcp.tool(
        name="register_complaint",
        description="Register a new complaint against an existing order. The complaint starts with status OPEN.",
        annotations={"readOnlyHint": False},
    )
    def register_complaint(
        order_id: Annotated[int, Field(description="The order_id of the order this complaint is about.")],
        registered_by: Annotated[str, Field(description="Full name of the person registering the complaint.")],
        complaint_description: Annotated[str, Field(description="Detailed description of the complaint.")],
        priority: Annotated[ComplaintPriority, Field(description="Complaint priority: LOW, MEDIUM, HIGH, or CRITICAL.")],
    ) -> dict:
        try:
            complaint = complaint_service.register_complaint(
                order_id=order_id,
                registered_by=registered_by,
                complaint_description=complaint_description,
                priority=priority,
            )
            return complaint.model_dump(mode="json")
        except ComplaintServiceError as e:
            raise ToolError(str(e)) from e

    @mcp.tool(
        name="get_complaint_details",
        description="Retrieve full details of a specific complaint by its complaint_id.",
        annotations={"readOnlyHint": True},
    )
    def get_complaint_details(
        complaint_id: Annotated[int, Field(description="The integer ID of the complaint to retrieve.")],
    ) -> dict:
        try:
            return complaint_service.get_complaint_details(complaint_id).model_dump(mode="json")
        except ComplaintServiceError as e:
            raise ToolError(str(e)) from e

    @mcp.tool(
        name="search_complaints",
        description=(
            "Search complaints using any combination of optional filters. "
            "All text filters are case-insensitive partial matches. "
            "Returns all complaints if no filters are provided."
        ),
        annotations={"readOnlyHint": True},
    )
    def search_complaints(
        order_id: Annotated[Optional[int], Field(description="Filter by exact order_id.")] = None,
        customer_name: Annotated[Optional[str], Field(description="Partial customer name (case-insensitive).")] = None,
        registered_by: Annotated[Optional[str], Field(description="Partial registrant name (case-insensitive).")] = None,
        priority: Annotated[Optional[ComplaintPriority], Field(description="Filter by priority: LOW, MEDIUM, HIGH, CRITICAL.")] = None,
        status: Annotated[Optional[ComplaintStatus], Field(description="Filter by status: OPEN, IN_PROGRESS, RESOLVED, CLOSED, REOPENED, CANCELLED.")] = None,
        resolved_by: Annotated[Optional[ResolverTeam], Field(description="Filter by resolver team name.")] = None,
        description: Annotated[Optional[str], Field(description="Partial text match on complaint description (case-insensitive).")] = None,
    ) -> list[dict]:
        results = complaint_service.search_complaints(
            order_id=order_id,
            customer_name=customer_name,
            registered_by=registered_by,
            priority=priority,
            status=status,
            resolved_by=resolved_by,
            description=description,
        )
        return [c.model_dump(mode="json") for c in results]

    @mcp.tool(
        name="resolve_complaint",
        description=(
            "Resolve a complaint by assigning it to a resolver team and providing resolution remarks. "
            "Only complaints with status OPEN, IN_PROGRESS, or REOPENED can be resolved."
        ),
        annotations={"readOnlyHint": False},
    )
    def resolve_complaint(
        complaint_id: Annotated[int, Field(description="ID of the complaint to resolve.")],
        resolved_by_team: Annotated[ResolverTeam, Field(description="Team resolving the complaint.")],
        resolution_remarks: Annotated[str, Field(description="Description of how the complaint was resolved.", min_length=1)],
    ) -> dict:
        try:
            updated = complaint_service.resolve_complaint(
                complaint_id=complaint_id,
                resolved_by_team=resolved_by_team,
                resolution_remarks=resolution_remarks,
            )
            return updated.model_dump(mode="json")
        except ComplaintServiceError as e:
            raise ToolError(str(e)) from e

    @mcp.tool(
        name="close_complaint",
        description="Close a complaint. Only complaints with status RESOLVED can be closed.",
        annotations={"readOnlyHint": False, "destructiveHint": False},
    )
    def close_complaint(
        complaint_id: Annotated[int, Field(description="ID of the complaint to close.")],
    ) -> dict:
        try:
            updated = complaint_service.close_complaint(complaint_id=complaint_id)
            return updated.model_dump(mode="json")
        except ComplaintServiceError as e:
            raise ToolError(str(e)) from e
