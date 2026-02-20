"""
Database Seeding Service

Seeds the order database with sample data for testing and demonstration.
"""
from datetime import datetime, timedelta
import random

# Import order_manager from local libraries
from app.libraries.order_manager import OrderManager


# Sample data for seeding (25 orders as per specification)
SAMPLE_ORDERS = [
    {
        "order_date": datetime.now() - timedelta(days=4, hours=14, minutes=30),
        "customer_name": "John Smith",
        "billing_address": "123 George Street, Sydney, NSW 2000, Australia",
        "product_sku": "LAPTOP-HP-001",
        "quantity": 1,
        "order_amount": 249900,
        "order_status": "Delivered",
        "remarks": "Gift wrapped"
    },
    {
        "order_date": datetime.now() - timedelta(days=3, hours=10, minutes=20),
        "customer_name": "Sarah Johnson",
        "billing_address": "456 Collins St, Melbourne, VIC 3000, Australia",
        "product_sku": "MONITOR-DELL-24",
        "quantity": 2,
        "order_amount": 79900,
        "order_status": "Shipped",
        "remarks": None
    },
    {
        "order_date": datetime.now() - timedelta(days=2, hours=15, minutes=45),
        "customer_name": "Michael Chen",
        "billing_address": "789 Queen St, Brisbane, QLD 4000, Australia",
        "product_sku": "KEYBOARD-LOGITECH",
        "quantity": 1,
        "order_amount": 12900,
        "order_status": "Pending",
        "remarks": "Urgent delivery requested"
    },
    {
        "order_date": datetime.now() - timedelta(days=1, hours=8, minutes=15),
        "customer_name": "Emma Wilson",
        "billing_address": "321 King William St, Adelaide, SA 5000, Australia",
        "product_sku": "MOUSE-RAZER-PRO",
        "quantity": 3,
        "order_amount": 26900,
        "order_status": "Processing",
        "remarks": "Corporate purchase"
    },
    {
        "order_date": datetime.now() - timedelta(hours=16),
        "customer_name": "Ramkumar Sundaram",
        "billing_address": "555 St Georges Terrace, Perth, WA 6000, Australia",
        "product_sku": "LAPTOP-LENOVO-X1",
        "quantity": 1,
        "order_amount": 289900,
        "order_status": "Confirmed",
        "remarks": "Include extended warranty"
    },
    {
        "order_date": datetime.now() - timedelta(days=5, hours=11),
        "customer_name": "David Brown",
        "billing_address": "88 Elizabeth St, Hobart, TAS 7000, Australia",
        "product_sku": "LAPTOP-DELL-XPS",
        "quantity": 1,
        "order_amount": 219900,
        "order_status": "Delivered",
        "remarks": None
    },
    {
        "order_date": datetime.now() - timedelta(days=3, hours=9, minutes=30),
        "customer_name": "Lisa Anderson",
        "billing_address": "234 Smith St, Darwin, NT 0800, Australia",
        "product_sku": "MONITOR-LG-27",
        "quantity": 1,
        "order_amount": 54900,
        "order_status": "Shipped",
        "remarks": "Handle with care - fragile"
    },
    {
        "order_date": datetime.now() - timedelta(days=1, hours=14),
        "customer_name": "James Taylor",
        "billing_address": "567 London Circuit, Canberra, ACT 2600, Australia",
        "product_sku": "HEADSET-SONY-WH",
        "quantity": 2,
        "order_amount": 89800,
        "order_status": "Processing",
        "remarks": "Express shipping required"
    },
    {
        "order_date": datetime.now() - timedelta(hours=6),
        "customer_name": "Sophia Martinez",
        "billing_address": "101 Pitt St, Sydney, NSW 2000, Australia",
        "product_sku": "KEYBOARD-LOGITECH",
        "quantity": 5,
        "order_amount": 64500,
        "order_status": "Confirmed",
        "remarks": "Bulk order for office"
    },
    {
        "order_date": datetime.now() - timedelta(days=7),
        "customer_name": "Oliver Thompson",
        "billing_address": "789 Flinders St, Melbourne, VIC 3000, Australia",
        "product_sku": "LAPTOP-HP-001",
        "quantity": 1,
        "order_amount": 249900,
        "order_status": "Returned",
        "remarks": "Customer requested refund"
    },
    {
        "order_date": datetime.now() - timedelta(days=2, hours=12),
        "customer_name": "Isabella Lee",
        "billing_address": "432 Adelaide St, Brisbane, QLD 4000, Australia",
        "product_sku": "MOUSE-RAZER-PRO",
        "quantity": 1,
        "order_amount": 8900,
        "order_status": "Shipped",
        "remarks": None
    },
    {
        "order_date": datetime.now() - timedelta(days=4, hours=16),
        "customer_name": "William Garcia",
        "billing_address": "654 Grenfell St, Adelaide, SA 5000, Australia",
        "product_sku": "MONITOR-DELL-24",
        "quantity": 1,
        "order_amount": 39950,
        "order_status": "Delivered",
        "remarks": "Left at reception"
    },
    {
        "order_date": datetime.now() - timedelta(hours=20),
        "customer_name": "Charlotte Davis",
        "billing_address": "876 Hay St, Perth, WA 6000, Australia",
        "product_sku": "LAPTOP-LENOVO-X1",
        "quantity": 1,
        "order_amount": 289900,
        "order_status": "Pending",
        "remarks": "Needs authorization"
    },
    {
        "order_date": datetime.now() - timedelta(days=6),
        "customer_name": "Benjamin White",
        "billing_address": "321 Collins St, Hobart, TAS 7000, Australia",
        "product_sku": "HEADSET-SONY-WH",
        "quantity": 1,
        "order_amount": 44900,
        "order_status": "Cancelled",
        "remarks": "Customer cancelled before shipping"
    },
    {
        "order_date": datetime.now() - timedelta(days=1, hours=10),
        "customer_name": "Mia Rodriguez",
        "billing_address": "567 Mitchell St, Darwin, NT 0800, Australia",
        "product_sku": "LAPTOP-DELL-XPS",
        "quantity": 2,
        "order_amount": 439800,
        "order_status": "Processing",
        "remarks": "Bulk corporate order"
    },
    {
        "order_date": datetime.now() - timedelta(days=3, hours=8),
        "customer_name": "Alexander Martinez",
        "billing_address": "890 Northbourne Ave, Canberra, ACT 2600, Australia",
        "product_sku": "MONITOR-LG-27",
        "quantity": 3,
        "order_amount": 164700,
        "order_status": "Shipped",
        "remarks": "Deliver to loading dock"
    },
    {
        "order_date": datetime.now() - timedelta(hours=2),
        "customer_name": "Amelia Wilson",
        "billing_address": "234 George St, Sydney, NSW 2000, Australia",
        "product_sku": "KEYBOARD-LOGITECH",
        "quantity": 1,
        "order_amount": 12900,
        "order_status": "Confirmed",
        "remarks": None
    },
    {
        "order_date": datetime.now() - timedelta(days=5, hours=13),
        "customer_name": "Ethan Anderson",
        "billing_address": "678 Bourke St, Melbourne, VIC 3000, Australia",
        "product_sku": "MOUSE-RAZER-PRO",
        "quantity": 10,
        "order_amount": 89000,
        "order_status": "Delivered",
        "remarks": "Office supplies order"
    },
    {
        "order_date": datetime.now() - timedelta(days=2, hours=7),
        "customer_name": "Harper Thomas",
        "billing_address": "432 Edward St, Brisbane, QLD 4000, Australia",
        "product_sku": "LAPTOP-HP-001",
        "quantity": 1,
        "order_amount": 249900,
        "order_status": "Shipped",
        "remarks": "Gift for employee"
    },
    {
        "order_date": datetime.now() - timedelta(days=4, hours=9),
        "customer_name": "Lucas Jackson",
        "billing_address": "789 Hindley St, Adelaide, SA 5000, Australia",
        "product_sku": "HEADSET-SONY-WH",
        "quantity": 1,
        "order_amount": 44900,
        "order_status": "Delivered",
        "remarks": None
    },
    {
        "order_date": datetime.now() - timedelta(days=1, hours=5),
        "customer_name": "Ava Harris",
        "billing_address": "123 Murray St, Perth, WA 6000, Australia",
        "product_sku": "MONITOR-DELL-24",
        "quantity": 2,
        "order_amount": 79900,
        "order_status": "Processing",
        "remarks": "Dual monitor setup"
    },
    {
        "order_date": datetime.now() - timedelta(days=6, hours=11),
        "customer_name": "Mason Clark",
        "billing_address": "456 Liverpool St, Hobart, TAS 7000, Australia",
        "product_sku": "LAPTOP-LENOVO-X1",
        "quantity": 1,
        "order_amount": 289900,
        "order_status": "Returned",
        "remarks": "Defective unit - replacement sent"
    },
    {
        "order_date": datetime.now() - timedelta(hours=12),
        "customer_name": "Evelyn Lewis",
        "billing_address": "789 Cavenagh St, Darwin, NT 0800, Australia",
        "product_sku": "KEYBOARD-LOGITECH",
        "quantity": 2,
        "order_amount": 25800,
        "order_status": "Confirmed",
        "remarks": None
    },
    {
        "order_date": datetime.now() - timedelta(days=3, hours=14),
        "customer_name": "Logan Walker",
        "billing_address": "321 Constitution Ave, Canberra, ACT 2600, Australia",
        "product_sku": "LAPTOP-DELL-XPS",
        "quantity": 1,
        "order_amount": 219900,
        "order_status": "Shipped",
        "remarks": "Standard delivery"
    },
    {
        "order_date": datetime.now() - timedelta(days=1, hours=18),
        "customer_name": "Aria Hall",
        "billing_address": "567 King St, Sydney, NSW 2000, Australia",
        "product_sku": "MONITOR-LG-27",
        "quantity": 1,
        "order_amount": 54900,
        "order_status": "Processing",
        "remarks": "4K display for design work"
    }
]


def seed_database(db_path: str, count: int = 25):
    """
    Seed the database with sample orders if it's empty.
    
    Args:
        db_path: Path to the order database
        count: Number of orders to seed (default: 25)
    """
    try:
        print(f"\n🌱 Checking database seeding requirements...")
        print(f"   Database path: {db_path}")
        
        # Create OrderManager instance
        manager = OrderManager(db_path=db_path)
        
        # Check if database already has data
        existing_orders = manager.search_orders()
        
        if len(existing_orders) > 0:
            print(f"✅ Database already has {len(existing_orders)} order(s). Skipping seeding.")
            return
        
        # Seed the database
        print(f"🌱 Database is empty. Seeding {min(count, len(SAMPLE_ORDERS))} sample orders...")
        
        seeded_count = 0
        for i, order_data in enumerate(SAMPLE_ORDERS[:count]):
            try:
                manager.create_order(**order_data)
                seeded_count += 1
            except Exception as e:
                print(f"⚠️  Warning: Failed to seed order {i+1}: {str(e)}")
        
        print(f"✅ Successfully seeded {seeded_count} order(s)")
        
        # Verify seeding
        total_orders = len(manager.search_orders())
        print(f"📊 Total orders in database: {total_orders}")
        
    except Exception as e:
        print(f"❌ Error during database seeding: {str(e)}")
        raise
