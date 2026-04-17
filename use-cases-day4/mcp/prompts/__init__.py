"""Register all MCP prompts on the FastMCP server instance."""

from typing import Annotated
from pydantic import Field


def register_prompts(mcp) -> None:
    """Decorate and register all prompt templates."""

    from prompts.definitions import (
        ANALYZE_CUSTOMER_ORDERS_TEMPLATE,
        COMPLAINT_RESOLUTION_GUIDE_TEMPLATE,
        ESCALATION_REVIEW_TEMPLATE,
        ORDER_STATUS_INQUIRY_TEMPLATE,
    )

    @mcp.prompt(
        name="analyze_customer_orders",
        description="Analyze a customer's complete order history and highlight issues.",
        tags={"orders", "analysis"},
    )
    def analyze_customer_orders(
        customer_name: Annotated[str, Field(description="Customer name to analyze")],
    ) -> str:
        return ANALYZE_CUSTOMER_ORDERS_TEMPLATE.format(customer_name=customer_name)

    @mcp.prompt(
        name="complaint_resolution_guide",
        description="Get a step-by-step resolution guide for a specific complaint.",
        tags={"complaints", "resolution"},
    )
    def complaint_resolution_guide(
        complaint_id: Annotated[str, Field(description="Complaint ID to review, e.g. COMP10001")],
    ) -> str:
        return COMPLAINT_RESOLUTION_GUIDE_TEMPLATE.format(complaint_id=complaint_id)

    @mcp.prompt(
        name="escalation_review",
        description="Review all high-priority unresolved complaints and recommend escalation actions.",
        tags={"complaints", "escalation"},
    )
    def escalation_review() -> str:
        return ESCALATION_REVIEW_TEMPLATE

    @mcp.prompt(
        name="order_status_inquiry",
        description="Help a customer understand their current order statuses in a friendly tone.",
        tags={"orders", "support"},
    )
    def order_status_inquiry(
        customer_name: Annotated[str, Field(description="Customer name to look up")],
    ) -> str:
        return ORDER_STATUS_INQUIRY_TEMPLATE.format(customer_name=customer_name)
