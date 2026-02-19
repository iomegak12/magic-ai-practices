"""
Example usage of the order_management library.

This script demonstrates all the main features of the library.
"""

import sys
from pathlib import Path

# Add the libraries directory to the Python path
libraries_path = Path(__file__).parent.parent / "libraries"
sys.path.insert(0, str(libraries_path))

from datetime import datetime
from order_management import (
    init_db,
    create_order,
    get_order_by_id,
    get_orders_by_customer,
    search_orders,
    update_order_status,
    get_all_orders,
    VALID_ORDER_STATUSES,
    ValidationError,
    OrderNotFoundError,
    DatabaseError
)


def main():
    print("=" * 60)
    print("Order Management Library - Example Usage")
    print("=" * 60)
    print()
    
    # Initialize the database
    print("1. Initializing database...")
    init_db()
    print("   ✓ Database initialized")
    print()
    
    # Create sample orders
    print("2. Creating sample orders...")
    try:
        order1 = create_order(
            customer_name="John Doe",
            billing_address="123 Main St, New York, NY 10001",
            product_sku="LAPTOP-001",
            quantity=1,
            order_amount=1299.99,
            remarks="Express delivery required",
            order_status="PENDING"
        )
        print(f"   ✓ Created order #{order1['order_id']} for {order1['customer_name']}")
        
        order2 = create_order(
            customer_name="Jane Smith",
            billing_address="456 Oak Ave, Los Angeles, CA 90001",
            product_sku="MOUSE-002",
            quantity=3,
            order_amount=89.97,
            remarks="Gift wrap please",
            order_status="PENDING"
        )
        print(f"   ✓ Created order #{order2['order_id']} for {order2['customer_name']}")
        
        order3 = create_order(
            customer_name="John Doe",
            billing_address="123 Main St, New York, NY 10001",
            product_sku="KEYBOARD-003",
            quantity=2,
            order_amount=199.98,
            order_status="CONFIRMED"
        )
        print(f"   ✓ Created order #{order3['order_id']} for {order3['customer_name']}")
        
    except ValidationError as e:
        print(f"   ✗ Validation error: {e}")
    except DatabaseError as e:
        print(f"   ✗ Database error: {e}")
    print()
    
    # Get order by ID
    print("3. Retrieving order by ID...")
    try:
        order = get_order_by_id(order1['order_id'])
        print(f"   Order ID: {order['order_id']}")
        print(f"   Customer: {order['customer_name']}")
        print(f"   Product: {order['product_sku']}")
        print(f"   Amount: ${order['order_amount']:.2f}")
        print(f"   Status: {order['order_status']}")
    except OrderNotFoundError as e:
        print(f"   ✗ {e}")
    print()
    
    # Get orders by customer
    print("4. Getting all orders for John Doe...")
    orders = get_orders_by_customer("John Doe")
    print(f"   Found {len(orders)} order(s):")
    for order in orders:
        print(f"   - Order #{order['order_id']}: {order['product_sku']} - ${order['order_amount']:.2f} - {order['order_status']}")
    print()
    
    # Search orders by product SKU (partial match, case-insensitive)
    print("5. Searching orders by product SKU (partial: 'mouse')...")
    orders = search_orders(product_sku="mouse")
    print(f"   Found {len(orders)} order(s):")
    for order in orders:
        print(f"   - Order #{order['order_id']}: {order['product_sku']} for {order['customer_name']}")
    print()
    
    # Search orders by billing address (partial match, case-insensitive)
    print("6. Searching orders by billing address (partial: 'new york')...")
    orders = search_orders(billing_address="new york")
    print(f"   Found {len(orders)} order(s):")
    for order in orders:
        print(f"   - Order #{order['order_id']}: {order['customer_name']} - {order['billing_address']}")
    print()
    
    # Search orders by status
    print("7. Searching orders by status (PENDING)...")
    orders = search_orders(order_status="PENDING")
    print(f"   Found {len(orders)} pending order(s):")
    for order in orders:
        print(f"   - Order #{order['order_id']}: {order['customer_name']} - {order['product_sku']}")
    print()
    
    # Update order status
    print("8. Updating order status...")
    try:
        updated_order = update_order_status(order1['order_id'], "CONFIRMED")
        print(f"   ✓ Order #{updated_order['order_id']} status changed to: {updated_order['order_status']}")
        
        updated_order = update_order_status(order2['order_id'], "SHIPPED")
        print(f"   ✓ Order #{updated_order['order_id']} status changed to: {updated_order['order_status']}")
        
    except (ValidationError, OrderNotFoundError) as e:
        print(f"   ✗ {e}")
    print()
    
    # Get all orders
    print("9. Getting all orders...")
    all_orders = get_all_orders()
    print(f"   Total orders in system: {len(all_orders)}")
    print()
    
    # Display valid order statuses
    print("10. Valid order statuses:")
    for status in VALID_ORDER_STATUSES:
        print(f"    - {status}")
    print()
    
    # Example of validation error
    print("11. Demonstrating validation error...")
    try:
        invalid_order = create_order(
            customer_name="",  # Invalid: empty name
            billing_address="Test Address",
            product_sku="TEST-001",
            quantity=-1,  # Invalid: negative quantity
            order_amount=100.00
        )
    except ValidationError as e:
        print(f"   ✓ Validation caught errors: {e}")
    print()
    
    # Example of OrderNotFoundError
    print("12. Demonstrating order not found error...")
    try:
        non_existent = get_order_by_id(99999)
    except OrderNotFoundError as e:
        print(f"   ✓ Error caught: {e}")
    print()
    
    print("=" * 60)
    print("Example completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
