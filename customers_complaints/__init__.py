"""Customer Complaints Management Library.

Provides SQLAlchemy-backed tools for managing customers, IT complaints,
and customer profile preferences with an agent-framework compatible interface.
"""

from .complaint_tools import (
    get_complaints_by_customer,
    get_complaints_by_status,
    register_complaint,
)
from .customer_tools import get_customer_by_id, search_customers
from .database import init_db
from .profile_preferences import get_customer_profile

__all__ = [
    "init_db",
    "get_customer_by_id",
    "search_customers",
    "get_complaints_by_customer",
    "get_complaints_by_status",
    "register_complaint",
    "get_customer_profile",
]
