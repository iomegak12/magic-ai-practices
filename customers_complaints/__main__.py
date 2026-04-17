"""Allow running seed as:  python -m customers_complaints.seed"""

# Import directly from seed (avoids __init__.py which requires agent_framework)
from customers_complaints.seed import seed

seed()
