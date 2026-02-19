# Order Management Library

A comprehensive Python library for managing customer orders with SQLAlchemy ORM and SQLite database.

## Features

- ✅ **Python 3.12** compatible
- ✅ **SQLAlchemy ORM** with SQLite database
- ✅ **Configurable database path** via .env file
- ✅ **Modular architecture** with clean separation of concerns
- ✅ **Comprehensive validation** for all data inputs
- ✅ **Complete CRUD operations** for order management
- ✅ **Case-insensitive partial search** for product SKU and billing address
- ✅ **Type hints** for better code completion

## Installation

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

2. Copy `.env.example` to `.env` and configure your database path:

```bash
cp .env.example .env
```

3. Edit `.env` to set your database path:

```
DATABASE_PATH=orders.db
```

## Quick Start

```python
from order_management import (
    init_db,
    create_order,
    get_order_by_id,
    get_orders_by_customer,
    search_orders,
    update_order_status,
    VALID_ORDER_STATUSES
)

# Initialize the database (call once)
init_db()

# Create a new order
order = create_order(
    customer_name="John Doe",
    billing_address="123 Main St, New York, NY 10001",
    product_sku="LAPTOP-001",
    quantity=2,
    order_amount=2499.98,
    remarks="Express delivery required",
    order_status="PENDING"
)
print(f"Created order: {order['order_id']}")

# Get order by ID
order_details = get_order_by_id(order['order_id'])
print(f"Order details: {order_details}")

# Get all orders for a customer
customer_orders = get_orders_by_customer("John Doe")
print(f"Found {len(customer_orders)} orders for John Doe")

# Search orders by product SKU (partial match, case-insensitive)
laptop_orders = search_orders(product_sku="laptop")
print(f"Found {len(laptop_orders)} laptop orders")

# Search orders by billing address (partial match, case-insensitive)
ny_orders = search_orders(billing_address="new york")
print(f"Found {len(ny_orders)} orders with 'new york' in address")

# Search orders by status
pending_orders = search_orders(order_status="PENDING")
print(f"Found {len(pending_orders)} pending orders")

# Update order status
updated_order = update_order_status(order['order_id'], "CONFIRMED")
print(f"Order status updated to: {updated_order['order_status']}")
```

## Order Data Structure

Each order contains the following fields:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `order_id` | int | Auto | Unique identifier (auto-incremented) |
| `order_date` | datetime | Auto | Order date in ISO format (defaults to current time) |
| `customer_name` | str | Yes | Customer name (max 255 chars) |
| `billing_address` | str | Yes | Billing address (max 500 chars) |
| `product_sku` | str | Yes | Product SKU/code (max 100 chars) |
| `quantity` | int | Yes | Quantity ordered (must be positive) |
| `order_amount` | float | Yes | Total order amount (must be positive) |
| `remarks` | str | No | Additional notes (max 1000 chars) |
| `order_status` | str | Yes | Order status (default: PENDING) |

## Valid Order Statuses

The library supports the following order statuses:

- `PENDING` - Order placed, awaiting confirmation
- `CONFIRMED` - Order confirmed and being processed
- `SHIPPED` - Order shipped to customer
- `DELIVERED` - Order delivered to customer
- `CANCELLED` - Order cancelled

Access the list programmatically via `VALID_ORDER_STATUSES`.

## API Reference

### Database Management

#### `init_db()`
Initialize the database by creating all tables. Call this once before using the library.

```python
init_db()
```

#### `get_database_path()`
Get the current database path.

```python
path = get_database_path()
```

### Order Operations

#### `create_order()`
Create a new order.

```python
order = create_order(
    customer_name="Jane Smith",
    billing_address="456 Oak Ave, Los Angeles, CA 90001",
    product_sku="MOUSE-002",
    quantity=5,
    order_amount=149.95,
    remarks="Gift wrap requested",  # Optional
    order_status="PENDING",  # Optional, defaults to PENDING
    order_date=datetime.now()  # Optional, defaults to current time
)
```

**Returns:** Dictionary with created order data

**Raises:** `ValidationError`, `DatabaseError`

#### `get_order_by_id(order_id)`
Retrieve order details by order ID.

```python
order = get_order_by_id(123)
```

**Returns:** Dictionary with order data

**Raises:** `OrderNotFoundError`, `DatabaseError`

#### `get_orders_by_customer(customer_name)`
Get all orders for a specific customer.

```python
orders = get_orders_by_customer("John Doe")
```

**Returns:** List of order dictionaries

**Raises:** `DatabaseError`

#### `search_orders(product_sku=None, billing_address=None, order_status=None)`
Search orders by product SKU, billing address, or order status. All parameters are optional and can be combined.

```python
# Search by product SKU (partial match, case-insensitive)
orders = search_orders(product_sku="laptop")

# Search by billing address (partial match, case-insensitive)
orders = search_orders(billing_address="los angeles")

# Search by order status (exact match, case-insensitive)
orders = search_orders(order_status="SHIPPED")

# Combine multiple criteria (OR condition)
orders = search_orders(product_sku="mouse", order_status="PENDING")
```

**Returns:** List of matching order dictionaries

**Raises:** `ValidationError`, `DatabaseError`

#### `update_order_status(order_id, new_status)`
Update the status of an existing order.

```python
updated_order = update_order_status(123, "SHIPPED")
```

**Returns:** Dictionary with updated order data

**Raises:** `ValidationError`, `OrderNotFoundError`, `DatabaseError`

#### `get_all_orders(limit=None)`
Get all orders with optional limit.

```python
# Get all orders
all_orders = get_all_orders()

# Get latest 10 orders
recent_orders = get_all_orders(limit=10)
```

**Returns:** List of order dictionaries

**Raises:** `DatabaseError`

## Exception Handling

The library provides specific exception types for different error scenarios:

```python
from order_management import (
    OrderManagementError,    # Base exception
    ValidationError,         # Validation failures
    OrderNotFoundError,      # Order not found
    DatabaseError           # Database operation failures
)

try:
    order = create_order(
        customer_name="",  # Invalid: empty name
        product_sku="ABC",
        quantity=-1,  # Invalid: negative quantity
        order_amount=100
    )
except ValidationError as e:
    print(f"Validation error: {e}")
except DatabaseError as e:
    print(f"Database error: {e}")
except OrderManagementError as e:
    print(f"General error: {e}")
```

## Validation Rules

- **Customer name**: Required, non-empty string, max 255 characters
- **Billing address**: Max 500 characters
- **Product SKU**: Required, non-empty string, max 100 characters
- **Quantity**: Required, must be positive number
- **Order amount**: Must be positive number
- **Remarks**: Optional, max 1000 characters
- **Order status**: Must be one of the valid statuses (case-insensitive)
- **Order date**: Must be valid ISO format or datetime object

## Project Structure

```
order_management/
├── __init__.py          # Public API and exports
├── database.py          # Database configuration and session management
├── models.py            # SQLAlchemy Order model
├── operations.py        # CRUD operations
├── validations.py       # Validation logic and rules
├── exceptions.py        # Custom exception classes
├── requirements.txt     # Python dependencies
├── .env.example         # Example environment configuration
└── README.md           # This file
```

## Development

### Running Tests

Create test scripts in a `tests/` directory and run them with pytest:

```bash
pytest tests/
```

### Database Location

By default, the database file is created in the current working directory. You can change this by setting the `DATABASE_PATH` environment variable in your `.env` file:

```
# Absolute path
DATABASE_PATH=/path/to/your/orders.db

# Relative path
DATABASE_PATH=./data/orders.db
```

## License

This library is provided as-is for use in your projects.

## Support

For issues or questions, please refer to the inline documentation and docstrings in the source code.
