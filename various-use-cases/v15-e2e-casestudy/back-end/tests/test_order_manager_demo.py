"""
Demonstration script for Order Manager Library.

This script showcases all 6 features of the Order Manager library:
- F-001: Create Order
- F-002: Get Orders by Customer
- F-003: Get Order by ID
- F-004: Search by Customer Name
- F-005: Advanced Search
- F-006: Update Order Status
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add parent directory to path to import order_manager
sys.path.insert(0, str(Path(__file__).parent.parent / "libraries"))

from order_manager import (
    OrderManager,
    Order,
    OrderNotFoundException,
    InvalidOrderDataException,
    ValidationException
)


def print_header(text: str) -> None:
    """Print a formatted header."""
    print("\n" + "=" * 80)
    print(f"  {text}")
    print("=" * 80)


def print_order(order: Order, prefix: str = "") -> None:
    """Print order details in a formatted way."""
    print(f"{prefix}Order ID: {order.order_id}")
    print(f"{prefix}Customer: {order.customer_name}")
    print(f"{prefix}Product SKU: {order.product_sku}")
    print(f"{prefix}Quantity: {order.quantity}")
    print(f"{prefix}Amount: ${order.order_amount / 100:.2f}")
    print(f"{prefix}Status: {order.order_status}")
    print(f"{prefix}Order Date: {order.order_date}")
    if order.remarks:
        print(f"{prefix}Remarks: {order.remarks}")
    print()


def feature_1_create_orders(manager: OrderManager) -> None:
    """Feature F-001: Create Order"""
    print_header("FEATURE 1: Create Orders")
    
    # Create multiple sample orders
    orders_data = [
        {
            "customer_name": "John Smith",
            "billing_address": "123 George Street, Sydney, NSW 2000, Australia",
            "product_sku": "LAPTOP-HP-001",
            "quantity": 2,
            "order_amount": 299900,
            "order_status": "Pending",
            "remarks": "Customer requested express shipping"
        },
        {
            "customer_name": "Sarah Johnson",
            "billing_address": "456 Queen Street, Auckland, 1010, New Zealand",
            "product_sku": "PHONE-SAM-002",
            "quantity": 1,
            "order_amount": 89900,
            "order_status": "Processing",
            "remarks": None
        },
        {
            "customer_name": "John Smith",
            "billing_address": "123 George Street, Sydney, NSW 2000, Australia",
            "product_sku": "TABLET-APL-003",
            "quantity": 3,
            "order_amount": 149900,
            "order_status": "Confirmed",
            "remarks": "Gift wrapping requested"
        },
        {
            "customer_name": "Emily Williams",
            "billing_address": "789 Collins Street, Melbourne, VIC 3000, Australia",
            "product_sku": "LAPTOP-HP-001",
            "quantity": 1,
            "order_amount": 149950,
            "order_status": "Shipped",
            "remarks": "Standard delivery"
        },
        {
            "customer_name": "Michael Brown",
            "billing_address": "321 Lambton Quay, Wellington, 6011, New Zealand",
            "product_sku": "MONITOR-DEL-004",
            "quantity": 2,
            "order_amount": 79900,
            "order_status": "Delivered",
            "remarks": None
        }
    ]
    
    created_orders = []
    for i, order_data in enumerate(orders_data, 1):
        print(f"\n[{i}] Creating order for {order_data['customer_name']}...")
        
        order = manager.create_order(
            order_date=datetime.now() - timedelta(days=5-i),
            customer_name=order_data["customer_name"],
            billing_address=order_data["billing_address"],
            product_sku=order_data["product_sku"],
            quantity=order_data["quantity"],
            order_amount=order_data["order_amount"],
            order_status=order_data["order_status"],
            remarks=order_data["remarks"]
        )
        
        print(f"    ✓ Order created with ID: {order.order_id}")
        created_orders.append(order)
    
    print(f"\n✓ Successfully created {len(created_orders)} orders!")
    return created_orders


def feature_2_get_orders_by_customer(manager: OrderManager) -> None:
    """Feature F-002: Get Orders by Customer (exact match)"""
    print_header("FEATURE 2: Get Orders by Customer (Exact Match)")
    
    customer_name = "John Smith"
    print(f"\nRetrieving all orders for customer: '{customer_name}'")
    
    orders = manager.get_orders_by_customer(customer_name)
    
    print(f"\n✓ Found {len(orders)} order(s):\n")
    for order in orders:
        print_order(order, prefix="  ")


def feature_3_get_order_by_id(manager: OrderManager) -> None:
    """Feature F-003: Get Order by ID"""
    print_header("FEATURE 3: Get Order by ID")
    
    # Test with existing order
    order_id = 1
    print(f"\nRetrieving order with ID: {order_id}")
    
    try:
        order = manager.get_order_by_id(order_id)
        print(f"\n✓ Order found:\n")
        print_order(order, prefix="  ")
    except OrderNotFoundException as e:
        print(f"✗ {e}")
    
    # Test with non-existent order
    print("\n" + "-" * 80)
    order_id = 9999
    print(f"\nTrying to retrieve non-existent order with ID: {order_id}")
    
    try:
        order = manager.get_order_by_id(order_id)
        print_order(order, prefix="  ")
    except OrderNotFoundException as e:
        print(f"✓ Expected error caught: {e}")


def feature_4_search_by_customer_name(manager: OrderManager) -> None:
    """Feature F-004: Search by Customer Name (partial match)"""
    print_header("FEATURE 4: Search by Customer Name (Partial Match)")
    
    search_term = "Smith"
    print(f"\nSearching for customers with name containing: '{search_term}'")
    
    orders = manager.search_orders_by_customer(search_term)
    
    print(f"\n✓ Found {len(orders)} order(s):\n")
    for order in orders:
        print_order(order, prefix="  ")


def feature_5_advanced_search(manager: OrderManager) -> None:
    """Feature F-005: Advanced Search"""
    print_header("FEATURE 5: Advanced Search")
    
    # Search by status
    print("\n[1] Search by Order Status")
    status = "Pending"
    print(f"    Searching for orders with status: '{status}'")
    
    orders = manager.search_orders(order_status=status)
    print(f"    ✓ Found {len(orders)} order(s)")
    for order in orders:
        print(f"       - Order {order.order_id}: {order.customer_name} - {order.product_sku}")
    
    # Search by product SKU
    print("\n[2] Search by Product SKU")
    sku = "LAPTOP-HP-001"
    print(f"    Searching for orders with product SKU: '{sku}'")
    
    orders = manager.search_orders(product_sku=sku)
    print(f"    ✓ Found {len(orders)} order(s)")
    for order in orders:
        print(f"       - Order {order.order_id}: {order.customer_name} - Qty: {order.quantity}")
    
    # Search by billing address (partial match)
    print("\n[3] Search by Billing Address (Partial Match)")
    address_partial = "Sydney"
    print(f"    Searching for orders with address containing: '{address_partial}'")
    
    orders = manager.search_orders(billing_address_partial=address_partial)
    print(f"    ✓ Found {len(orders)} order(s)")
    for order in orders:
        print(f"       - Order {order.order_id}: {order.customer_name} - {order.billing_address[:50]}...")
    
    # Combined search
    print("\n[4] Combined Search (Status + Address)")
    status = "Confirmed"
    address_partial = "Australia"
    print(f"    Searching for orders with status '{status}' AND address containing '{address_partial}'")
    
    orders = manager.search_orders(
        order_status=status,
        billing_address_partial=address_partial
    )
    print(f"    ✓ Found {len(orders)} order(s)")
    for order in orders:
        print(f"       - Order {order.order_id}: {order.customer_name} - {order.order_status}")


def feature_6_update_order_status(manager: OrderManager) -> None:
    """Feature F-006: Update Order Status"""
    print_header("FEATURE 6: Update Order Status")
    
    order_id = 1
    new_status = "Shipped"
    
    print(f"\nUpdating order {order_id} status to: '{new_status}'")
    
    # Get current order
    order_before = manager.get_order_by_id(order_id)
    print(f"\nBefore update:")
    print(f"  Order ID: {order_before.order_id}")
    print(f"  Status: {order_before.order_status}")
    print(f"  Updated At: {order_before.updated_at}")
    
    # Update status
    order_after = manager.update_order_status(order_id, new_status)
    
    print(f"\n✓ After update:")
    print(f"  Order ID: {order_after.order_id}")
    print(f"  Status: {order_after.order_status}")
    print(f"  Updated At: {order_after.updated_at}")
    
    # Test invalid status
    print("\n" + "-" * 80)
    print("\nTrying to update with invalid status...")
    
    try:
        manager.update_order_status(order_id, "InvalidStatus")
    except ValidationException as e:
        print(f"✓ Expected validation error caught: {e}")


def test_error_handling(manager: OrderManager) -> None:
    """Demonstrate error handling"""
    print_header("ERROR HANDLING DEMONSTRATION")
    
    print("\n[1] Test: Create order with invalid quantity")
    try:
        manager.create_order(
            order_date=datetime.now(),
            customer_name="Test Customer",
            billing_address="Test Address",
            product_sku="TEST-001",
            quantity=-5,  # Invalid!
            order_amount=10000
        )
    except ValidationException as e:
        print(f"    ✓ Validation error caught: {e}")
    
    print("\n[2] Test: Create order with invalid status")
    try:
        manager.create_order(
            order_date=datetime.now(),
            customer_name="Test Customer",
            billing_address="Test Address",
            product_sku="TEST-001",
            quantity=1,
            order_amount=10000,
            order_status="InvalidStatus"  # Invalid!
        )
    except ValidationException as e:
        print(f"    ✓ Validation error caught: {e}")
    
    print("\n[3] Test: Get non-existent order")
    try:
        manager.get_order_by_id(99999)
    except OrderNotFoundException as e:
        print(f"    ✓ Not found error caught: {e}")


def test_valid_statuses() -> None:
    """Display valid order statuses"""
    print_header("VALID ORDER STATUSES")
    
    from order_manager import Config
    
    print("\nThe following order statuses are supported:\n")
    for i, status in enumerate(Config.VALID_STATUSES, 1):
        print(f"  {i}. {status}")


def main():
    """Main demonstration function"""
    print("\n" + "╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "ORDER MANAGER LIBRARY DEMO" + " " * 32 + "║")
    print("║" + " " * 25 + "Full Feature Showcase" + " " * 32 + "║")
    print("╚" + "=" * 78 + "╝")
    
    # Use a test database
    test_db_path = "test_orders_demo.db"
    print(f"\nInitializing Order Manager with database: {test_db_path}")
    
    # Clean up test database if it exists
    import os
    if os.path.exists(test_db_path):
        os.remove(test_db_path)
        print(f"✓ Cleaned up existing test database")
    
    # Initialize manager
    manager = OrderManager(db_path=test_db_path)
    print(f"✓ Order Manager initialized successfully\n")
    
    try:
        # Display valid statuses
        test_valid_statuses()
        
        # Feature demonstrations
        feature_1_create_orders(manager)
        feature_2_get_orders_by_customer(manager)
        feature_3_get_order_by_id(manager)
        feature_4_search_by_customer_name(manager)
        feature_5_advanced_search(manager)
        feature_6_update_order_status(manager)
        
        # Error handling
        test_error_handling(manager)
        
        # Final summary
        print_header("DEMONSTRATION COMPLETE")
        print("\n✓ All 6 features demonstrated successfully!")
        print(f"✓ Test database created at: {test_db_path}")
        print("\nYou can inspect the database or run this script again to see all features.\n")
        
    except Exception as e:
        print(f"\n✗ Error during demonstration: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Close manager
        manager.close()
        print("✓ Database connection closed")


if __name__ == "__main__":
    main()
