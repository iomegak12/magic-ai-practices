"""MCP Prompts — 4 reusable prompt templates exposed via FastMCP."""

from __future__ import annotations

from datetime import datetime, timezone

from fastmcp import FastMCP
from fastmcp.prompts import Message

from magic_v22_mcp.repositories import complaints_repo, orders_repo
from magic_v22_mcp.services import complaint_service, order_service
from magic_v22_mcp.services.complaint_service import ComplaintServiceError
from magic_v22_mcp.services.order_service import OrderServiceError


def register_prompts(mcp: FastMCP) -> None:
    """Register all prompt templates onto the FastMCP instance."""

    @mcp.prompt(
        name="complaint_triage",
        description=(
            "Given an order_id, fetches the order and its open complaints, then asks the LLM "
            "to recommend the appropriate priority level and resolver team for triage."
        ),
    )
    def complaint_triage(
        order_id: int,
    ) -> list[Message]:
        try:
            order = order_service.get_order_details(order_id)
        except OrderServiceError:
            return [Message(f"No order found with id={order_id}. Please verify the order_id and try again.")]

        complaints = complaint_service.search_complaints(order_id=order_id)
        open_complaints = [c for c in complaints if c.status.value in ("OPEN", "IN_PROGRESS", "REOPENED")]

        order_ctx = (
            f"Order #{order.order_number} (id={order.order_id})\n"
            f"  Customer : {order.customer_name}\n"
            f"  Product  : {order.product_sku}\n"
            f"  Units    : {order.units}  |  Amount: {order.order_amount}\n"
            f"  Status   : {order.status}\n"
            f"  Remarks  : {order.remarks or 'None'}\n"
        )
        if open_complaints:
            c_lines = "\n".join(
                f"  [{c.complaint_id}] {c.priority} | {c.status} — {c.complaint_description[:120]}"
                for c in open_complaints
            )
            complaints_ctx = f"\nActive complaints ({len(open_complaints)}):\n{c_lines}"
        else:
            complaints_ctx = "\nNo active complaints on this order."

        return [
            Message(
                f"You are a customer service triage specialist.\n\n"
                f"Order context:\n{order_ctx}{complaints_ctx}\n\n"
                f"Based on the above information:\n"
                f"1. Recommend the most appropriate complaint PRIORITY (LOW / MEDIUM / HIGH / CRITICAL) "
                f"and explain your reasoning.\n"
                f"2. Recommend the best RESOLVER TEAM from: CUSTOMER_SUPPORT, ORDER_FULFILLMENT, "
                f"LOGISTICS, BILLING, RETURNS_AND_REFUNDS, QUALITY_ASSURANCE, TECHNICAL_SUPPORT.\n"
                f"3. Suggest immediate next steps the resolver team should take."
            )
        ]

    @mcp.prompt(
        name="customer_order_summary",
        description=(
            "Given a customer name (partial match supported), fetches all their orders and "
            "asks the LLM to produce a concise order history summary."
        ),
    )
    def customer_order_summary(
        customer_name: str,
    ) -> list[Message]:
        orders = order_service.query_orders(customer_name=customer_name)
        if not orders:
            return [Message(f"No orders found for customer matching '{customer_name}'.")]

        lines = "\n".join(
            f"  [{o.order_id}] {o.order_number}  {o.order_date.strftime('%Y-%m-%d')}  "
            f"SKU={o.product_sku}  Units={o.units}  Amount={o.order_amount}  Status={o.status}"
            for o in orders
        )
        total_spent = sum(o.order_amount for o in orders)
        return [
            Message(
                f"You are a customer success analyst.\n\n"
                f"Order history for customer matching '{customer_name}' ({len(orders)} orders):\n"
                f"{lines}\n\n"
                f"Total spent: {total_spent}\n\n"
                f"Please provide:\n"
                f"1. A concise summary of this customer's purchase history.\n"
                f"2. Any notable patterns (e.g. favourite product lines, order frequency).\n"
                f"3. The overall order health (% delivered vs cancelled).\n"
                f"4. Any proactive recommendations for customer retention."
            )
        ]

    @mcp.prompt(
        name="complaint_resolution_drafter",
        description=(
            "Given a complaint_id, fetches the complaint and linked order details, then asks "
            "the LLM to draft a professional resolution note in the voice of the assigned resolver team."
        ),
    )
    def complaint_resolution_drafter(
        complaint_id: int,
    ) -> list[Message]:
        try:
            complaint = complaint_service.get_complaint_details(complaint_id)
        except ComplaintServiceError:
            return [Message(f"No complaint found with id={complaint_id}. Please verify and try again.")]

        try:
            order = order_service.get_order_details(complaint.order_id)
        except OrderServiceError:
            order = None

        team = complaint.resolved_by.value if complaint.resolved_by else "CUSTOMER_SUPPORT"
        order_ctx = (
            f"Order #{order.order_number} — {order.product_sku} x{order.units} — Status: {order.status}"
            if order else f"Order id={complaint.order_id} (details unavailable)"
        )

        return [
            Message(
                f"You are a senior representative from the {team} team.\n\n"
                f"Complaint #{complaint.complaint_id} details:\n"
                f"  Customer order : {order_ctx}\n"
                f"  Registered by  : {complaint.registered_by}\n"
                f"  Priority       : {complaint.priority}\n"
                f"  Status         : {complaint.status}\n"
                f"  Description    : {complaint.complaint_description}\n"
                f"  Existing notes : {complaint.resolution_remarks or 'None'}\n\n"
                f"Please draft a professional, empathetic resolution note to the customer that:\n"
                f"1. Acknowledges the issue clearly.\n"
                f"2. Explains what action has been or will be taken.\n"
                f"3. Sets clear expectations for next steps and timeline.\n"
                f"4. Closes with a goodwill statement appropriate for the {team} team."
            )
        ]

    @mcp.prompt(
        name="escalation_decision",
        description=(
            "Given a complaint_id, analyses the complaint age, priority, and current status, "
            "then asks the LLM to decide whether to escalate, reassign, or keep the complaint "
            "with the current team."
        ),
    )
    def escalation_decision(
        complaint_id: int,
    ) -> list[Message]:
        try:
            complaint = complaint_service.get_complaint_details(complaint_id)
        except ComplaintServiceError:
            return [Message(f"No complaint found with id={complaint_id}. Please verify and try again.")]

        age_days = (datetime.now(timezone.utc) - complaint.complaint_date.replace(tzinfo=timezone.utc)).days
        team = complaint.resolved_by.value if complaint.resolved_by else "Unassigned"

        return [
            Message(
                f"You are a customer operations manager reviewing complaint escalations.\n\n"
                f"Complaint #{complaint.complaint_id}:\n"
                f"  Priority       : {complaint.priority}\n"
                f"  Status         : {complaint.status}\n"
                f"  Age            : {age_days} day(s)\n"
                f"  Registered by  : {complaint.registered_by}\n"
                f"  Assigned team  : {team}\n"
                f"  Description    : {complaint.complaint_description}\n"
                f"  Resolution so far: {complaint.resolution_remarks or 'None'}\n\n"
                f"Escalation policy reference:\n"
                f"  CRITICAL complaints unresolved > 1 day → immediate escalation\n"
                f"  HIGH complaints unresolved > 3 days → escalate\n"
                f"  MEDIUM complaints unresolved > 7 days → reassign\n"
                f"  LOW complaints unresolved > 14 days → reassign\n\n"
                f"Based on the above, please:\n"
                f"1. State your escalation decision: ESCALATE / REASSIGN / KEEP.\n"
                f"2. Justify the decision against the policy.\n"
                f"3. If ESCALATE or REASSIGN, recommend which team should take over and why.\n"
                f"4. Suggest specific actions the new or current team should take immediately."
            )
        ]
