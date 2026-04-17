"""Register all MCP resources on the FastMCP server instance."""


def register_resources(mcp) -> None:
    """Decorate and register all resources."""

    from resources.definitions import (
        _orders_summary,
        _complaints_summary,
        _config_statuses,
        _recent_orders,
        _unresolved_complaints,
    )

    @mcp.resource(
        "orders://summary",
        name="OrdersSummary",
        description="Total orders with breakdown by status.",
        mime_type="application/json",
        tags={"orders", "summary"},
    )
    def orders_summary() -> str:
        return _orders_summary()

    @mcp.resource(
        "complaints://summary",
        name="ComplaintsSummary",
        description="Total complaints with breakdown by status and priority.",
        mime_type="application/json",
        tags={"complaints", "summary"},
    )
    def complaints_summary() -> str:
        return _complaints_summary()

    @mcp.resource(
        "config://statuses",
        name="ConfigStatuses",
        description="All valid enums: order statuses, complaint priorities, complaint statuses.",
        mime_type="application/json",
        tags={"config"},
    )
    def config_statuses() -> str:
        return _config_statuses()

    @mcp.resource(
        "orders://recent",
        name="RecentOrders",
        description="Last 10 orders sorted by date descending.",
        mime_type="application/json",
        tags={"orders", "recent"},
    )
    def recent_orders() -> str:
        return _recent_orders()

    @mcp.resource(
        "complaints://unresolved",
        name="UnresolvedComplaints",
        description="All complaints with status Open or In Progress.",
        mime_type="application/json",
        tags={"complaints", "unresolved"},
    )
    def unresolved_complaints() -> str:
        return _unresolved_complaints()
