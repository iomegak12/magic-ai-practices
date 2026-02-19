# Order Manager Library - Implementation Guide

**Version:** 1.0.0  
**Date:** February 19, 2026  
**Client:** Ramkumar  
**Target:** Development Team  

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Business Requirements](#business-requirements)
3. [Technical Specifications](#technical-specifications)
4. [Database Schema](#database-schema)
5. [Project Structure](#project-structure)
6. [Module Specifications](#module-specifications)
7. [Configuration Setup](#configuration-setup)
8. [API Reference](#api-reference)
9. [Validation Rules](#validation-rules)
10. [Usage Examples](#usage-examples)
11. [Testing Requirements](#testing-requirements)
12. [Deliverables](#deliverables)

---

## 📖 Overview

### Purpose
Design and implement a Python library for managing customer orders. The library will provide a simple, modular interface for creating, retrieving, searching, and updating orders stored in a SQLite database.

### Target Market
Primary customers are from Australia and New Zealand regions.

### Library Type
Pure Python library (import and use in code) - No CLI interface required.

---

## 🎯 Business Requirements

### Core Features

The library must support the following operations:

| Feature ID | Feature Name | Description |
|------------|--------------|-------------|
| F-001 | Create Order | Create a new customer order with all required details |
| F-002 | Get Orders by Customer | Retrieve all orders for a specific customer (exact name match) |
| F-003 | Get Order by ID | Retrieve a specific order by its order_id |
| F-004 | Search by Customer Name | Search orders by partial customer name match |
| F-005 | Advanced Search | Search orders by order status, product SKU, or billing address (partial) |
| F-006 | Update Order Status | Update the status of an existing order |

---

## 🛠 Technical Specifications

### Technology Stack

| Component | Technology | Version |
|-----------|------------|---------|
| Programming Language | Python | 3.12 |
| Database | SQLite | 3.x |
| ORM | SQLAlchemy | 2.0+ |
| Date/Time Format | ISO 8601 | - |

### Design Principles

- **Modularity**: Clean separation of concerns (models, database, operations)
- **Simplicity**: Easy to integrate and use
- **Standards**: Follow PEP 8 style guidelines
- **Type Hints**: Use Python type hints for better IDE support
- **Error Handling**: Comprehensive exception handling

---

## 🗄 Database Schema

### Order Table

**Table Name:** `orders`

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| `order_id` | INTEGER | PRIMARY KEY, AUTO INCREMENT | Unique order identifier |
| `order_date` | DATETIME | NOT NULL | Date and time when order was placed (ISO format) |
| `customer_name` | VARCHAR(255) | NOT NULL | Full name of the customer |
| `billing_address` | TEXT | NOT NULL | Free-form billing address |
| `product_sku` | VARCHAR(100) | NOT NULL | Product SKU/code |
| `quantity` | INTEGER | NOT NULL, CHECK > 0 | Order quantity |
| `order_amount` | INTEGER | NOT NULL, CHECK > 0 | Total order amount in cents/smallest currency unit |
| `remarks` | TEXT | NULLABLE | Optional notes or comments |
| `order_status` | VARCHAR(50) | NOT NULL | Current order status |
| `created_at` | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Record creation timestamp |
| `updated_at` | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP, ON UPDATE | Last modification timestamp |

### Order Status Values

The following are valid order status values:

1. **Pending** - Order received, awaiting processing
2. **Processing** - Order is being prepared
3. **Confirmed** - Order confirmed and ready for shipment
4. **Shipped** - Order has been dispatched
5. **Delivered** - Order successfully delivered to customer
6. **Cancelled** - Order cancelled by customer or system
7. **Returned** - Order returned by customer

---

## 📁 Project Structure

```
back-end/
└── libraries/
    └── order_manager/
        ├── __init__.py              # Package initialization, exports main API
        ├── config.py                # Configuration constants (status values, defaults)
        ├── models.py                # SQLAlchemy ORM model definitions
        ├── database.py              # Database connection and session management
        ├── manager.py               # Main OrderManager class with business logic
        ├── exceptions.py            # Custom exception classes
        ├── validators.py            # Validation functions
        ├── setup.py                 # Package setup and dependencies
        └── README.md                # Library documentation
```

**Note:** Configuration files (`.env`, `.env.example`) and application-level `requirements.txt` belong in your REST API application, not in the library itself.

### File Responsibilities

#### `__init__.py`
- Package initialization
- Export main classes and functions
- Version information

#### `config.py`
- Valid status constants
- Default values
- Configuration constants (no .env loading at library level)

#### `setup.py`
- Package metadata
- Dependencies declaration
- Installation configuration

#### `models.py`
- SQLAlchemy Order model
- Database table mapping
- Data serialization methods

#### `database.py`
- Database engine creation
- Session management
- Context manager for transactions

#### `manager.py`
- OrderManager class
- All CRUD operations
- Search and filter methods

#### `exceptions.py`
- OrderNotFoundException
- InvalidOrderDataException
- DatabaseException
- ValidationException

#### `validators.py`
- Input validation functions
- Data sanitization
- Business rule validations

---

## 📦 Module Specifications

### 1. models.py

#### Order Model

```python
class Order(Base):
    """
    SQLAlchemy model for customer orders
    """
    __tablename__ = 'orders'
    
    # Fields as per schema
    order_id: int (Primary Key, Auto Increment)
    order_date: datetime
    customer_name: str
    billing_address: str
    product_sku: str
    quantity: int
    order_amount: int
    remarks: Optional[str]
    order_status: str
    created_at: datetime
    updated_at: datetime
    
    # Methods
    def to_dict() -> dict
    def __repr__() -> str
```

### 2. config.py

#### Config Class

```python
class Config:
    """
    Configuration constants for the library
    """
    # Order Status Constants
    VALID_STATUSES: List[str] = [
        "Pending", "Processing", "Confirmed", 
        "Shipped", "Delivered", "Cancelled", "Returned"
    ]
    
    # Default database path (can be overridden by application)
    DEFAULT_DB_PATH: str = "orders.db"
```

### 3. database.py

#### Database Class

```python
class Database:
    """
    Database manager for SQLite with SQLAlchemy
    """
    def __init__(db_path: str)
    def initialize() -> None
    def get_session() -> ContextManager[Session]
```

### 4. manager.py

#### OrderManager Class

```python
class OrderManager:
    """
    Main class for order management operations
    """
    def __init__(db_path: str = Config.DEFAULT_DB_PATH)
    
    # Feature F-001: Create Order
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
    
    # Feature F-002: Get Orders by Customer (exact match)
    def get_orders_by_customer(customer_name: str) -> List[Order]
    
    # Feature F-003: Get Order by ID
    def get_order_by_id(order_id: int) -> Order
    
    # Feature F-004: Search by Customer Name (partial match)
    def search_orders_by_customer(customer_name_partial: str) -> List[Order]
    
    # Feature F-005: Advanced Search
    def search_orders(
        order_status: Optional[str] = None,
        product_sku: Optional[str] = None,
        billing_address_partial: Optional[str] = None
    ) -> List[Order]
    
    # Feature F-006: Update Order Status
    def update_order_status(order_id: int, new_status: str) -> Order
```

### 5. validators.py

#### Validation Functions

```python
def validate_quantity(quantity: int) -> bool
def validate_order_amount(amount: int) -> bool
def validate_order_status(status: str) -> bool
def validate_required_fields(**kwargs) -> bool
def sanitize_customer_name(name: str) -> str
```

### 6. exceptions.py

#### Custom Exceptions

```python
class OrderManagerException(Exception)
class OrderNotFoundException(OrderManagerException)
class InvalidOrderDataException(OrderManagerException)
class DatabaseException(OrderManagerException)
class ValidationException(OrderManagerException)
```

---

## ⚙️ Library Configuration

### Configuration Approach

This is a **library**, not an application. Therefore:

- ❌ No `.env` files at library level
- ❌ No `requirements.txt` at library level
- ✅ Configuration passed via constructor parameters
- ✅ Dependencies declared in `setup.py`
- ✅ Consuming application (your REST API) manages `.env` files

### How It Works

**In the Library:**
```python
# config.py - Only constants, no environment loading
class Config:
    VALID_STATUSES = ["Pending", "Processing", "Confirmed", "Shipped", "Delivered", "Cancelled", "Returned"]
    DEFAULT_DB_PATH = "orders.db"
```

**In Your REST API Application:**
```python
# Your REST API application loads .env and passes config to library
import os
from dotenv import load_dotenv
from order_manager import OrderManager

load_dotenv()  # Load from your application's .env

db_path = os.getenv('DATABASE_PATH', 'data/orders.db')
manager = OrderManager(db_path=db_path)
```

### Application-Level Configuration (Your REST API)

**Your REST API project structure:**
```
back-end/
├── libraries/
│   └── order_manager/       # Library (no .env here)
│       ├── __init__.py
│       ├── config.py
│       ├── models.py
│       ├── database.py
│       ├── manager.py
│       ├── exceptions.py
│       ├── validators.py
│       └── setup.py
│
└── api/                      # Your REST API application
    ├── main.py
    ├── routes.py
    ├── .env                  # ✅ Application configuration here
    ├── .env.example          # ✅ Example configuration here
    ├── requirements.txt      # ✅ Application dependencies here
    └── config/
        └── settings.py       # Application settings
```

**Your Application's .env:**
```env
# Application configuration (REST API level)
DATABASE_PATH=data/orders.db
API_HOST=0.0.0.0
API_PORT=8000
```

**Your Application's settings.py:**
```python
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_PATH = os.getenv('DATABASE_PATH', 'data/orders.db')
    API_HOST = os.getenv('API_HOST', '0.0.0.0')
    API_PORT = int(os.getenv('API_PORT', 8000))
```

**Your Application's main.py:**
```python
from order_manager import OrderManager
from config.settings import Settings

# Initialize library with configuration from your application
manager = OrderManager(db_path=Settings.DATABASE_PATH)
```

---

## 🔧 API Reference

### OrderManager Class

#### Constructor

```python
OrderManager(db_path: str = "orders.db")
```

**Parameters:**
- `db_path` (str): Path to SQLite database file. Default: "orders.db"

**Examples:**
```python
# Use default database path
manager = OrderManager()

# Specify custom database path (recommended for production)
manager = OrderManager(db_path="data/orders.db")

# In your REST API - load from application's .env
import os
from dotenv import load_dotenv

load_dotenv()  # Loads from your API's .env
db_path = os.getenv('DATABASE_PATH', 'data/orders.db')
manager = OrderManager(db_path=db_path)
```

---

#### Method: create_order()

```python
create_order(
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

**Parameters:**
- `order_date` (datetime): When the order was placed (ISO format)
- `customer_name` (str): Full customer name (required)
- `billing_address` (str): Customer billing address (required)
- `product_sku` (str): Product SKU/code (required)
- `quantity` (int): Order quantity, must be > 0 (required)
- `order_amount` (int): Total amount in cents, must be > 0 (required)
- `order_status` (str): Order status, default "Pending"
- `remarks` (str, optional): Additional notes

**Returns:**
- `Order`: The created order object

**Raises:**
- `InvalidOrderDataException`: If validation fails
- `DatabaseException`: If database operation fails

---

#### Method: get_orders_by_customer()

```python
get_orders_by_customer(customer_name: str) -> List[Order]
```

**Parameters:**
- `customer_name` (str): Exact customer name to search

**Returns:**
- `List[Order]`: List of orders for the customer (empty list if none found)

**Raises:**
- `DatabaseException`: If database operation fails

---

#### Method: get_order_by_id()

```python
get_order_by_id(order_id: int) -> Order
```

**Parameters:**
- `order_id` (int): The order ID to retrieve

**Returns:**
- `Order`: The order object

**Raises:**
- `OrderNotFoundException`: If order with given ID doesn't exist
- `DatabaseException`: If database operation fails

---

#### Method: search_orders_by_customer()

```python
search_orders_by_customer(customer_name_partial: str) -> List[Order]
```

**Parameters:**
- `customer_name_partial` (str): Partial customer name to search (case-insensitive)

**Returns:**
- `List[Order]`: List of matching orders (empty list if none found)

**Raises:**
- `DatabaseException`: If database operation fails

---

#### Method: search_orders()

```python
search_orders(
    order_status: Optional[str] = None,
    product_sku: Optional[str] = None,
    billing_address_partial: Optional[str] = None
) -> List[Order]
```

**Parameters:**
- `order_status` (str, optional): Filter by exact order status
- `product_sku` (str, optional): Filter by exact product SKU
- `billing_address_partial` (str, optional): Filter by partial address match

**Returns:**
- `List[Order]`: List of matching orders (empty list if none found)

**Notes:**
- Multiple filters are combined with AND logic
- At least one filter parameter should be provided

**Raises:**
- `DatabaseException`: If database operation fails

---

#### Method: update_order_status()

```python
update_order_status(order_id: int, new_status: str) -> Order
```

**Parameters:**
- `order_id` (int): The order ID to update
- `new_status` (str): New status value (must be valid status)

**Returns:**
- `Order`: The updated order object

**Raises:**
- `OrderNotFoundException`: If order with given ID doesn't exist
- `InvalidOrderDataException`: If status is invalid
- `DatabaseException`: If database operation fails

---

## ✅ Validation Rules

### Field Validations

| Field | Validation Rule | Error Message |
|-------|----------------|---------------|
| `customer_name` | Not empty, max 255 chars | "Customer name is required and must be <= 255 characters" |
| `billing_address` | Not empty | "Billing address is required" |
| `product_sku` | Not empty, max 100 chars | "Product SKU is required and must be <= 100 characters" |
| `quantity` | Integer > 0 | "Quantity must be a positive integer" |
| `order_amount` | Integer > 0 | "Order amount must be a positive integer" |
| `order_status` | Must be in valid status list | "Invalid order status. Must be one of: Pending, Processing, Confirmed, Shipped, Delivered, Cancelled, Returned" |
| `order_date` | Valid datetime | "Order date must be a valid datetime object" |

### Business Rules

1. **Order Creation:**
   - All required fields must be provided
   - Quantity and amount must be positive integers
   - Order date cannot be more than 1 year in the future
   - Default status is "Pending" if not specified

2. **Order Status Update:**
   - Only valid status transitions allowed (implement business logic)
   - Cannot change status of cancelled/delivered orders (optional - confirm with business)
   - Updated_at timestamp must be automatically updated

3. **Search Operations:**
   - Case-insensitive partial name searches
   - Case-insensitive partial address searches
   - Exact match for status and SKU

---

## 💡 Usage Examples

### Example 1: Basic Library Usage (Standalone)

```python
from order_manager import OrderManager

# Use default database path
manager = OrderManager()

# Or specify custom path
manager = OrderManager(db_path="data/orders.db")
```

### Example 2: Integration with REST API Application

**In your REST API application (not in library):**

**File: api/.env**
```env
# Your REST API application's configuration
DATABASE_PATH=data/orders.db
API_HOST=0.0.0.0
API_PORT=8000
```

**File: api/config/settings.py**
```python
import os
from dotenv import load_dotenv

load_dotenv()  # Loads from your API's .env

class Settings:
    DATABASE_PATH = os.getenv('DATABASE_PATH', 'data/orders.db')
    API_HOST = os.getenv('API_HOST', '0.0.0.0')
    API_PORT = int(os.getenv('API_PORT', 8000))

settings = Settings()
```

**File: api/main.py**
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

### Example 3: Create an Order

```python
from datetime import datetime
from order_manager import OrderManager

manager = OrderManager()

order = manager.create_order(
    order_date=datetime.now(),
    customer_name="John Smith",
    billing_address="123 George Street, Sydney, NSW 2000, Australia",
    product_sku="LAPTOP-HP-001",
    quantity=2,
    order_amount=299900,  # $2,999.00 in cents
    order_status="Pending",
    remarks="Customer requested express shipping"
)

print(f"Order created with ID: {order.order_id}")
```

### Example 4: Get Orders by Customer

```python
from order_manager import OrderManager

manager = OrderManager()

# Exact match
orders = manager.get_orders_by_customer("John Smith")

for order in orders:
    print(f"Order {order.order_id}: {order.product_sku} - {order.order_status}")
```

### Example 5: Search Orders by Partial Customer Name

```python
from order_manager import OrderManager

manager = OrderManager()

# Find all orders for customers with "Smith" in their name
orders = manager.search_orders_by_customer("Smith")

print(f"Found {len(orders)} orders")
```

### Example 6: Advanced Search

```python
from order_manager import OrderManager

manager = OrderManager()

# Search by status
pending_orders = manager.search_orders(order_status="Pending")

# Search by product SKU
laptop_orders = manager.search_orders(product_sku="LAPTOP-HP-001")

# Search by billing address (partial match)
sydney_orders = manager.search_orders(billing_address_partial="Sydney")

# Combined search
results = manager.search_orders(
    order_status="Shipped",
    billing_address_partial="NSW"
)
```

### Example 7: Get Order by ID

```python
from order_manager import OrderManager, OrderNotFoundException

manager = OrderManager()

try:
    order = manager.get_order_by_id(1)
    print(f"Order details: {order.to_dict()}")
except OrderNotFoundException as e:
    print(f"Order not found: {e}")
```

### Example 8: Update Order Status

```python
from order_manager import OrderManager

manager = OrderManager()

# Update order status
updated_order = manager.update_order_status(
    order_id=1,
    new_status="Shipped"
)

print(f"Order {updated_order.order_id} status updated to {updated_order.order_status}")
print(f"Last updated: {updated_order.updated_at}")
```

### Example 9: Error Handling

```python
from order_manager import (
    OrderManager,
    OrderNotFoundException,
    InvalidOrderDataException,
    ValidationException
)

manager = OrderManager()

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
except InvalidOrderDataException as e:
    print(f"Invalid data: {e}")
```

---

## 🧪 Testing Requirements

### Unit Tests Required

1. **Configuration Tests** (`test_config.py`)
   - Validate status constants
   - Default values
   - Configuration immutability

2. **Model Tests** (`test_models.py`)
   - Order model creation
   - Field validations
   - to_dict() serialization
   - Datetime handling

3. **Database Tests** (`test_database.py`)
   - Database initialization
   - Session management
   - Connection handling
   - Transaction rollback
   - Different database paths

4. **Manager Tests** (`test_manager.py`)
   - Create order (valid data)
   - Create order (invalid data)
   - Get orders by customer
   - Get order by ID (exists)
   - Get order by ID (not found)
   - Search by customer name
   - Advanced search (all filters)
   - Update order status
   - Initialize with different db_path values

5. **Validator Tests** (`test_validators.py`)
   - Quantity validation
   - Amount validation
   - Status validation
   - Required fields validation

### Test Coverage Target
- Minimum 85% code coverage
- All public API methods must have tests
- Error paths must be tested

---

## 📦 Deliverables

### Required Files

**Library Level:**

1. **Source Code**
   - All Python modules as per project structure
   - Well-commented code
   - Type hints included

2. **Package Configuration**
   - `setup.py` - Package metadata and dependencies
   - `config.py` - Constants only (no env file loading)

3. **Documentation**
   - README.md with library usage
   - API documentation (docstrings)
   - Integration guide for REST API applications

4. **Examples**
   - Standalone usage examples
   - REST API integration examples

**Application Level (Your REST API):**

1. **Configuration Files**
   - `.env.example` - Template for environment variables
   - `.env` - Actual configuration (not committed)
   - `.gitignore` - Exclude .env and database files
   - `settings.py` - Application settings with dotenv

2. **Dependencies**
   - `requirements.txt` - Application and library dependencies
   - Python 3.12 compatibility tested

### Quality Standards

**Library Standards:**
- ✅ PEP 8 compliant code
- ✅ Type hints for all functions
- ✅ Comprehensive docstrings
- ✅ Error handling implemented
- ✅ No hardcoded paths (accept via constructor)
- ✅ Transaction safety (rollback on errors)
- ✅ Clean code, no TODO comments
- ✅ Reusable and application-agnostic
- ✅ Dependencies declared in setup.py

**Application Standards (Your REST API):**
- ✅ Configuration via .env files
- ✅ .env.example provided as template
- ✅ Settings module for centralized config
- ✅ Library instantiation with application config

---

## 📝 Package Dependencies

### Library: setup.py

```python
from setuptools import setup, find_packages

setup(
    name="order_manager",
    version="1.0.0",
    description="Python library for managing customer orders",
    author="Your Team",
    packages=find_packages(),
    install_requires=[
        "sqlalchemy>=2.0.25",
    ],
    python_requires=">=3.12",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.12",
    ],
)
```

### Your REST API Application: requirements.txt

```
# Application requirements (including the library)
-e ./libraries/order_manager

# Application dependencies
fastapi>=0.109.0
uvicorn>=0.27.0
python-dotenv>=1.0.0
pydantic>=2.5.0
```

### Your REST API Application: .env.example

```env
# Database Configuration
DATABASE_PATH=data/orders.db

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
ENVIRONMENT=development
```

### Your REST API Application: .gitignore

```
# Environment files (Application level)
.env

# Database files
*.db
*.sqlite
*.sqlite3
data/

# Python
__pycache__/
*.py[cod]
*.egg-info/
.pytest_cache/

# IDE
.vscode/
.idea/
```

---

## 🔒 Important Notes

### Configuration Management (Library Design)

1. **Library Principles:**
   - Library accepts configuration via constructor (not .env)
   - No .env files in library code
   - Application (REST API) manages environment configuration
   - Library remains application-agnostic and reusable

2. **Application Responsibilities:**
   - REST API loads .env using python-dotenv
   - REST API passes configuration to library
   - Keep .env out of version control (.gitignore)
   - Provide .env.example as template

3. **Database Path:**
   - Library accepts path via constructor
   - Application determines path from .env
   - Use relative paths for portability
   - Ensure parent directories exist before DB creation

### Database Considerations

1. **SQLite Limitations:**
   - Single writer at a time
   - Not suitable for high-concurrency production
   - Suitable for small to medium order volumes

2. **Data Integrity:**
   - Use transactions for all write operations
   - Implement rollback on errors
   - Validate data before database operations

3. **Performance:**
   - Add indexes on frequently searched columns (customer_name, product_sku, order_status)
   - Consider query optimization for large datasets

### Security Considerations

1. **Input Sanitization:**
   - Sanitize all user inputs
   - Protect against SQL injection (SQLAlchemy handles this)
   - Validate data types

2. **Error Messages:**
   - Don't expose internal database errors
   - Provide user-friendly error messages
   - Log detailed errors for debugging

### Application Configuration Best Practices (REST API Level)

1. **File Management (Application Level):**
   - Never commit .env to version control
   - Always provide .env.example as a template
   - Document all environment variables clearly
   - Use meaningful variable names
   - Load .env in application, not library

2. **Library Integration:**
   - Pass configuration from application to library
   - Library constructor accepts db_path parameter
   - Don't let library depend on application's .env
   - Keep library reusable and portable

3. **Path Configuration:**
   - Use relative paths for portability
   - Support both relative and absolute paths
   - Create directories if they don't exist (in application)
   - Validate path accessibility before passing to library

4. **Multiple Environments:**
   - Use separate .env files for dev/test/prod (in application)
   - Examples: `.env.development`, `.env.production`
   - Or use different directories: `data/dev/`, `data/prod/`
   - Application's settings module handles environment switching

5. **Error Handling:**
   - Application validates configuration on startup
   - Provide clear error messages for invalid paths
   - Log configuration being used (for debugging)
   - Gracefully handle missing configuration

---

## 📞 Support & Questions

For any questions or clarifications during implementation:

**Client Contact:** Ramkumar (Ram)  
**Project:** Order Manager Library  
**Location:** `v15-e2e-casestudy/back-end/libraries/order_manager`

---

## ✅ Implementation Checklist

**Library Development:**
- [ ] Create library project structure
- [ ] Implement config.py (Constants only, no .env loading)
- [ ] Implement models.py (Order model)
- [ ] Implement database.py (Database class)
- [ ] Implement exceptions.py (Custom exceptions)
- [ ] Implement validators.py (Validation functions)
- [ ] Implement manager.py (OrderManager class)
- [ ] Implement __init__.py (Package exports)
- [ ] Create setup.py (Package metadata and dependencies)
- [ ] Write unit tests for library
- [ ] Write README.md (library usage, no .env)
- [ ] Create standalone usage examples
- [ ] Test library independently
- [ ] Code review and refactoring
- [ ] Library testing and validation

**REST API Application Development:**
- [ ] Create REST API project structure
- [ ] Create .env.example file (application level)
- [ ] Create .gitignore file (application level)
- [ ] Create settings.py with .env loading
- [ ] Integrate order_manager library
- [ ] Pass configuration from application to library
- [ ] Implement REST API endpoints
- [ ] Write REST API integration examples
- [ ] Test library integration with different .env configs
- [ ] Final testing and validation
- [ ] Documentation review
- [ ] Deliverable package ready

---

**End of Implementation Guide**

*This document should be reviewed and approved by Ramkumar before implementation begins.*
