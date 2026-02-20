import asyncio
import os
from agent_framework.azure import AzureOpenAIResponsesClient
from azure.identity import AzureCliCredential

# Import all CRM tools
from crm_tools.tools import (
    create_customer,
    get_customer_by_id,
    get_all_customers,
    search_customers,
    customers_db
)
