"""MCP Resources — 4 data resources exposed via FastMCP."""

from __future__ import annotations

import json

from fastmcp import FastMCP
from fastmcp.exceptions import ResourceError

from magic_v22_mcp.enums import ComplaintPriority, ComplaintStatus, OrderStatus, ResolverTeam
from magic_v22_mcp.repositories import complaints_repo, orders_repo

_CATALOG_KINDS = {
    "order-statuses": [s.value for s in OrderStatus],
    "complaint-statuses": [s.value for s in ComplaintStatus],
    "complaint-priorities": [s.value for s in ComplaintPriority],
    "resolver-teams": [s.value for s in ResolverTeam],
}


def register_resources(mcp: FastMCP) -> None:
    """Register all resources onto the FastMCP instance."""

    @mcp.resource(
        "stats://orders-summary",
        name="OrdersSummary",
        description="Aggregated orders statistics: total count, total revenue, and count by status.",
        mime_type="application/json",
        annotations={"readOnlyHint": True},
    )
    def orders_summary() -> str:
        stats = orders_repo.order_number_stats()
        return json.dumps(stats, indent=2)

    @mcp.resource(
        "stats://complaints-summary",
        name="ComplaintsSummary",
        description="Aggregated complaints statistics: total count, count by status, priority, and resolver team.",
        mime_type="application/json",
        annotations={"readOnlyHint": True},
    )
    def complaints_summary() -> str:
        stats = complaints_repo.complaint_stats()
        return json.dumps(stats, indent=2)

    @mcp.resource(
        "catalog://{kind}",
        name="EnumCatalog",
        description=(
            "Enum value catalog. Supply one of: "
            "order-statuses, complaint-statuses, complaint-priorities, resolver-teams."
        ),
        mime_type="application/json",
        annotations={"readOnlyHint": True, "idempotentHint": True},
    )
    def enum_catalog(kind: str) -> str:
        if kind not in _CATALOG_KINDS:
            valid = ", ".join(_CATALOG_KINDS.keys())
            raise ResourceError(
                f"Unknown catalog kind '{kind}'. Valid kinds: {valid}."
            )
        return json.dumps({"kind": kind, "values": _CATALOG_KINDS[kind]}, indent=2)

    @mcp.resource(
        "complaints://open",
        name="OpenComplaints",
        description="List of all complaints with status OPEN, IN_PROGRESS, or REOPENED.",
        mime_type="application/json",
        annotations={"readOnlyHint": True},
    )
    def open_complaints() -> str:
        complaints = complaints_repo.get_open_complaints()
        data = [c.model_dump(mode="json") for c in complaints]
        return json.dumps(data, indent=2)
