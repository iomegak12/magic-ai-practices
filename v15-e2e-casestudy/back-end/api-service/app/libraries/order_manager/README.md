# Order Manager Library

A Python library for managing customer orders with SQLite database backend.

## Overview

Order Manager is a lightweight, easy-to-use Python library that provides a complete solution for managing customer orders. It uses SQLite for data storage and SQLAlchemy as the ORM layer.

### Key Features

- ✅ **Create Orders** - Add new customer orders with validation
- ✅ **Retrieve Orders** - Get orders by ID or customer name
- ✅ **Search Orders** - Flexible search by customer, status, SKU, or address
- ✅ **Update Orders** - Modify order status with validation
- ✅ **Type Safe** - Full type hints for better IDE support
- ✅ **Transaction Safe** - Automatic rollback on errors
- ✅ **Well Tested** - Comprehensive test coverage

## Installation

### From Source

```bash
cd path/to/order_manager
pip install -e .
```

### With Development Dependencies

```bash
pip install -e .[dev]
```

## Quick Start

### Basic Usage

```python
from datetime import datetime
from order_manager import OrderManager

# Initialize the manager
manager = OrderManager(db_path="data/orders.db")

# Create an order
order = manager.create_order(
    order_date=datetime.now(),
    customer_name="John Smith",
    billing_address="123 George Street, Sydney, NSW 2000, Australia",
    product_sku="LAPTOP-HP-001",
    quantity=2,
    order_amount=299900,  # Amount in cents
    order_status="Pending",
    remarks="Express shipping requested"
)

print(f"Order created with ID: {order.order_id}")
```

### Integration with REST API

**Your Application's settings.py:**

```python
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_PATH = os.getenv('DATABASE_PATH', 'data/orders.db')
    API_HOST = os.getenv('API_HOST', '0.0.0.0')
    API_PORT = int(os.getenv('API_PORT', 8000))

settings = Settings()
```

**Your Application's main.py:**

```python
from fastapi import FastAPI
from order_manager import OrderManager
from config.settings import settings

# Initialize library with config from your application
order_manager = OrderManager(db_path=settings.DATABASE_PATH)

app = FastAPI()

@app.get("/orders/{order_id}")
def get_order(order_id: int):
    order = order_manager.get_order_by_id(order_id)
    return order.to_dict()
```

## API Reference

### OrderManager

Main class for all order operations.

#### Constructor

```python
OrderManager(db_path: str = "orders.db")
```

**Parameters:**
- `db_path` (str): Path to SQLite database file

**Example:**
```python
manager = OrderManager(db_path="data/orders.db")
```

---

### Methods

#### create_order()

Create a new customer order.

```python
def create_order(
    order_date: datetime,
    customer_name: str,
    billing_address: str,
    product_sku: str,
    quantity: int,
    order_amount: int,
    order_status: str = "Pending",
    remarks: Optional[str] = None
) -> Order
```

**Returns:** Created `Order` object

**Raises:** `InvalidOrderDataException`, `DatabaseException`

---

#### get_order_by_id()

Retrieve a specific order by ID.

```python
def get_order_by_id(order_id: int) -> Order
```

**Returns:** `Order` object

**Raises:** `OrderNotFoundException`, `DatabaseException`

---

#### get_orders_by_customer()

Get all orders for a specific customer (exact match).

```python
def get_orders_by_customer(customer_name: str) -> List[Order]
```

**Returns:** List of `Order` objects

**Raises:** `DatabaseException`

---

#### search_orders_by_customer()

Search orders by partial customer name (case-insensitive).

```python
def search_orders_by_customer(customer_name_partial: str) -> List[Order]
```

**Returns:** List of `Order` objects

**Raises:** `DatabaseException`

---

#### search_orders()

Advanced search with multiple filters.

```python
def search_orders(
    order_status: Optional[str] = None,
    product_sku: Optional[str] = None,
    billing_address_partial: Optional[str] = None
) -> List[Order]
```

**Returns:** List of `Order` objects

**Raises:** `DatabaseException`

---

#### update_order_status()

Update the status of an existing order.

```python
def update_order_status(order_id: int, new_status: str) -> Order
```

**Returns:** Updated `Order` object

**Raises:** `OrderNotFoundException`, `InvalidOrderDataException`, `DatabaseException`

---

## Order Status Values

Valid order statuses:
- `Pending` - Order received, awaiting processing
- `Processing` - Order is being prepared
- `Confirmed` - Order confirmed and ready for shipment
- `Shipped` - Order has been dispatched
- `Delivered` - Order successfully delivered
- `Cancelled` - Order cancelled
- `Returned` - Order returned by customer

## Examples

### Example 1: Get Orders by Customer

```python
from order_manager import OrderManager

manager = OrderManager()

# Get all orders for a customer (exact match)
orders = manager.get_orders_by_customer("John Smith")

for order in orders:
    print(f"Order {order.order_id}: {order.product_sku} - {order.order_status}")
```

### Example 2: Search Orders

```python
from order_manager import OrderManager

manager = OrderManager()

# Search by partial customer name
orders = manager.search_orders_by_customer("Smith")

# Advanced search by status
pending_orders = manager.search_orders(order_status="Pending")

# Search by product SKU
laptop_orders = manager.search_orders(product_sku="LAPTOP-HP-001")

# Search by billing address
sydney_orders = manager.search_orders(billing_address_partial="Sydney")

# Combined search
results = manager.search_orders(
    order_status="Shipped",
    billing_address_partial="NSW"
)
```

### Example 3: Update Order Status

```python
from order_manager import OrderManager

manager = OrderManager()

# Update order status
updated_order = manager.update_order_status(
    order_id=1,
    new_status="Shipped"
)

print(f"Order {updated_order.order_id} status: {updated_order.order_status}")
```

### Example 4: Error Handling

```python
from order_manager import (
    OrderManager,
    OrderNotFoundException,
    InvalidOrderDataException,
    ValidationException
)

manager = OrderManager()

try:
    order = manager.get_order_by_id(999)
except OrderNotFoundException as e:
    print(f"Error: {e}")

try:
    order = manager.create_order(
        order_date=datetime.now(),
        customer_name="Jane Doe",
        billing_address="456 Queen St, Auckland, NZ",
        product_sku="PHONE-SAM-002",
        quantity=-5,  # Invalid!
        order_amount=50000
    )
except ValidationException as e:
    print(f"Validation error: {e}")
```

## Exceptions

The library defines the following exceptions:

- `OrderManagerException` - Base exception for all errors
- `OrderNotFoundException` - Order with specified ID not found
- `InvalidOrderDataException` - Order data validation failed
- `DatabaseException` - Database operation failed
- `ValidationException` - Input validation failed

## Configuration

This is a **library**, not an application. Configuration is passed via constructor:

```python
# Library accepts configuration directly
manager = OrderManager(db_path="data/orders.db")
```

For REST API applications, load configuration from `.env` and pass to library:

```python
# Your REST API application
import os
from dotenv import load_dotenv
from order_manager import OrderManager

load_dotenv()
db_path = os.getenv('DATABASE_PATH', 'data/orders.db')
manager = OrderManager(db_path=db_path)
```

## Development

### Running Tests

```bash
pytest
```

### Code Coverage

```bash
pytest --cov=order_manager --cov-report=html
```

### Code Formatting

```bash
black order_manager/
```

### Type Checking

```bash
mypy order_manager/
```

## Requirements

- Python 3.12+
- SQLAlchemy 2.0.25+

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For questions or issues, please contact: team@example.com

---

**Version:** 1.0.0  
**Author:** Your Team
