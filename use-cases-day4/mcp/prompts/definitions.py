"""Prompt template definitions for the MCP server."""


ANALYZE_CUSTOMER_ORDERS_TEMPLATE = (
    "You are a customer-service analyst. Analyze all orders for the customer "
    "'{customer_name}'. Summarize their order history including total orders, "
    "order statuses, products purchased, and total spending. Highlight any "
    "anomalies such as cancelled or returned orders and suggest follow-up actions."
)

COMPLAINT_RESOLUTION_GUIDE_TEMPLATE = (
    "You are a complaint resolution specialist. Review complaint '{complaint_id}'. "
    "Examine the complaint description, priority, and current status. "
    "Suggest step-by-step resolution actions, recommended timelines based on "
    "priority, and a draft resolution note that can be used to close the complaint."
)

ESCALATION_REVIEW_TEMPLATE = (
    "You are a senior support manager. Review all unresolved complaints with "
    "High or Critical priority. For each complaint, assess whether escalation "
    "is warranted based on priority, age of the complaint, and current assignment. "
    "Provide a prioritized list of complaints requiring immediate attention and "
    "recommended actions for each."
)

ORDER_STATUS_INQUIRY_TEMPLATE = (
    "You are a friendly customer support agent. Help the customer "
    "'{customer_name}' understand the current status of their orders. "
    "Provide a clear, concise summary of each order including the order ID, "
    "product, status, and expected next steps. Use a polite and professional tone."
)
