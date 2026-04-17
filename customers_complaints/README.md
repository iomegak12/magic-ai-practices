# customers_complaints

A modular SQLAlchemy + SQLite library for managing customers, IT complaints, and customer profile preferences. All public functions are decorated with `@tool` for seamless integration with the `agent-framework`.

## Library Structure

```
customers_complaints/
├── __init__.py                # Re-exports all tools + init_db
├── __main__.py                # python -m customers_complaints  →  runs seed
├── database.py                # Engine, session factory, Base
├── models.py                  # ORM models: Customer, Complaint, CustomerProfilePreference
├── customer_tools.py          # get_customer_by_id, search_customers
├── complaint_tools.py         # get_complaints_by_customer, get_complaints_by_status, register_complaint
├── profile_preferences.py     # get_customer_profile
├── seed.py                    # Seeds 15 Indian customers + 60-75 IT complaints + profile preferences
└── README.md
```

## Configuration

Set `DATABASE_PATH` in a `.env` file at the workspace root:

```env
DATABASE_PATH=./data
```

The database file `customers_complaints.db` will be created inside that directory. If `DATABASE_PATH` is not set, it defaults to `./data`.

## Quick Start

```python
from customers_complaints import init_db
from customers_complaints.seed import seed

# Create tables
init_db()

# Populate sample data (15 customers, 60-75 complaints, profiles)
seed()
```

## Available Tools

| Tool | Description |
|------|-------------|
| `get_customer_by_id(customer_id)` | Retrieve a customer record by ID |
| `search_customers(name?, address?, email?)` | Partial, case-insensitive search |
| `get_complaints_by_customer(customer_id)` | All complaints for a customer |
| `get_complaints_by_status(status)` | Filter complaints by status |
| `register_complaint(customer_id, description, priority?, status?)` | Register a new complaint (platinum → auto High) |
| `get_customer_profile(customer_id)` | Get customer profile preference (platinum/gold/silver/general) |

## Models

### Customer
- `customer_id` — PK, auto-generated (`CUST10001`, `CUST10002`, …)
- `customer_name`, `address`, `email`, `phone`, `active_status` (active/inactive), `remarks`

### Complaint
- `complaint_id` — PK, auto-generated (`COMP10001`, `COMP10002`, …)
- `complaint_date`, `customer_id` (FK), `complaint_description`
- `priority` — Critical, High, Medium, Low
- `status` — Open, In Progress, Resolved, Closed, Reopened

### CustomerProfilePreference
- `customer_id` (FK, unique 1:1), `customer_type` — platinum, gold, silver, general

## Seeding

```bash
python -m customers_complaints
```

Seeds 15 Indian customers, assigns profile types (Shweta Iyer = platinum), and creates 4-5 IT complaints per customer.
