"""Seed data: 25 orders with Indian customers & Microsoft IT products, 4-5 complaints each."""

import logging
from datetime import datetime, timedelta
import random

from models.order import Order
from models.complaint import Complaint
from database.connection import db

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Reference data
# ---------------------------------------------------------------------------

CUSTOMERS = [
    ("Ramesh Kumar", "12, MG Road, Bengaluru, Karnataka 560001"),
    ("Priya Sharma", "45, Connaught Place, New Delhi 110001"),
    ("Amit Patel", "78, SG Highway, Ahmedabad, Gujarat 380015"),
    ("Sneha Iyer", "23, Anna Salai, Chennai, Tamil Nadu 600002"),
    ("Vikram Singh", "56, Civil Lines, Jaipur, Rajasthan 302006"),
    ("Ananya Reddy", "89, Banjara Hills, Hyderabad, Telangana 500034"),
    ("Rajesh Nair", "34, Marine Drive, Kochi, Kerala 682031"),
    ("Kavitha Menon", "67, Park Street, Kolkata, West Bengal 700016"),
    ("Suresh Gupta", "11, Hazratganj, Lucknow, Uttar Pradesh 226001"),
    ("Deepika Joshi", "90, FC Road, Pune, Maharashtra 411004"),
    ("Arjun Deshmukh", "15, Laxmi Road, Pune, Maharashtra 411030"),
    ("Meera Krishnan", "22, Residency Road, Bengaluru, Karnataka 560025"),
    ("Sanjay Verma", "38, Sector 17, Chandigarh 160017"),
    ("Pooja Agarwal", "50, Camac Street, Kolkata, West Bengal 700017"),
    ("Nikhil Rao", "63, Jubilee Hills, Hyderabad, Telangana 500033"),
    ("Lakshmi Pillai", "7, Thiruvananthapuram, Kerala 695001"),
    ("Dhruv Mehta", "19, CG Road, Ahmedabad, Gujarat 380006"),
    ("Isha Banerjee", "41, Salt Lake, Kolkata, West Bengal 700091"),
    ("Karthik Sundaram", "55, T Nagar, Chennai, Tamil Nadu 600017"),
    ("Nandini Kulkarni", "28, Koregaon Park, Pune, Maharashtra 411001"),
    ("Rohan Malhotra", "73, Rajouri Garden, New Delhi 110027"),
    ("Swati Tiwari", "6, Arera Colony, Bhopal, Madhya Pradesh 462016"),
    ("Anil Saxena", "82, Gomti Nagar, Lucknow, Uttar Pradesh 226010"),
    ("Divya Hegde", "14, Mangalore, Karnataka 575001"),
    ("Manish Choudhary", "36, Vaishali Nagar, Jaipur, Rajasthan 302021"),
]

PRODUCTS = [
    ("MSSFPRO9", "Microsoft Surface Pro 9", 89990),
    ("MSXBXCTL", "Xbox Wireless Controller", 5490),
    ("MSKB600B", "Microsoft Bluetooth Keyboard 600", 2490),
    ("MSSRFGO3", "Microsoft Surface Go 3", 44999),
    ("MSARCEML", "Microsoft Arc Mouse - ELG", 5999),
    ("MSOFC365", "Microsoft 365 Personal (1 Yr)", 4899),
    ("MSSFLPT5", "Microsoft Surface Laptop 5", 109990),
    ("MSXBXSXC", "Xbox Series X Console", 49990),
    ("MSSFERGO", "Microsoft Ergonomic Keyboard", 6499),
    ("MSSFSTD2", "Microsoft Surface Studio 2+", 329990),
]

ORDER_STATUSES = ["Pending", "Processing", "Shipped", "Delivered", "Cancelled", "Returned"]

COMPLAINT_TEMPLATES = [
    ("Product arrived with physical damage on the outer casing.", "High"),
    ("Received wrong product SKU, expected a different item.", "High"),
    ("Order delivered to wrong address, need immediate reshipment.", "Critical"),
    ("Product not functioning on first use, suspected DOA.", "Critical"),
    ("Missing accessories in the package (charger/cable not included).", "Medium"),
    ("Billing amount charged is higher than the listed price.", "High"),
    ("Delayed shipping - order has not moved for over a week.", "Medium"),
    ("Packaging was poor, items were loosely placed inside the box.", "Low"),
    ("Product colour/variant does not match what was ordered.", "Medium"),
    ("Received a used/refurbished item instead of brand new.", "High"),
    ("Warranty card and invoice missing from the shipment.", "Low"),
    ("Screen has dead pixels, noticed upon unboxing.", "High"),
    ("Bluetooth connectivity issues - device not pairing.", "Medium"),
    ("Software license key is invalid or already redeemed.", "High"),
    ("Battery draining unusually fast within first 24 hours.", "Medium"),
    ("Keyboard keys are sticky and unresponsive.", "Medium"),
    ("Touchscreen not responding accurately to inputs.", "High"),
    ("Fan noise is excessively loud during normal operation.", "Medium"),
    ("USB ports not recognizing connected peripherals.", "Medium"),
    ("Device overheating during regular usage.", "High"),
    ("Tracking number provided is invalid, cannot track shipment.", "Low"),
    ("Return request submitted but no pickup scheduled yet.", "Medium"),
    ("Refund not processed after 15 business days.", "High"),
    ("Customer support unresponsive for over 48 hours.", "Medium"),
    ("Order was cancelled without notification or consent.", "Critical"),
]

COMPLAINT_STATUSES_SEED = ["Open", "In Progress", "Resolved", "Closed", "Escalated"]

ASSIGNED_EXECUTIVES = [
    "Unassigned",
    "Arun Kapoor",
    "Smita Desai",
    "Raghav Menon",
    "Neha Saxena",
    "Vijay Prakash",
]


def _next_order_id(start: int, index: int) -> str:
    return f"ORD{start + index}"


def _next_complaint_id(start: int, index: int) -> str:
    return f"COMP{start + index}"


def seed_database() -> None:
    """Populate the database with sample orders and complaints if tables are empty."""
    with db.get_session() as session:
        if session.query(Order).first() is not None:
            logger.info("Database already seeded — skipping.")
            return

    random.seed(42)  # Reproducible data
    base_date = datetime(2025, 1, 10, 9, 0, 0)

    orders: list[Order] = []
    complaints: list[Complaint] = []
    comp_counter = 0

    for idx in range(25):
        cust_name, cust_addr = CUSTOMERS[idx]
        sku, _prod_name, price = PRODUCTS[idx % len(PRODUCTS)]
        qty = random.randint(1, 5)
        status = random.choice(ORDER_STATUSES)
        order_date = base_date + timedelta(days=idx * 3, hours=random.randint(0, 12))

        order = Order(
            order_id=_next_order_id(10001, idx),
            order_date=order_date,
            customer_name=cust_name,
            product_sku=sku,
            billing_address=cust_addr,
            quantity=qty,
            unit_price=price,
            order_status=status,
            remarks=f"Order for {_prod_name}",
        )
        orders.append(order)

        # 4-5 complaints per order
        num_complaints = random.randint(4, 5)
        selected = random.sample(COMPLAINT_TEMPLATES, num_complaints)

        for j, (desc, priority) in enumerate(selected):
            comp_date = order_date + timedelta(days=random.randint(1, 10), hours=random.randint(0, 8))
            comp_status = random.choice(COMPLAINT_STATUSES_SEED)
            assigned = random.choice(ASSIGNED_EXECUTIVES)
            resolution = None
            if comp_status in ("Resolved", "Closed"):
                resolution = "Issue has been investigated and resolved as per SLA guidelines."

            complaint = Complaint(
                complaint_id=_next_complaint_id(10001, comp_counter),
                complaint_reg_date=comp_date,
                order_id=order.order_id,
                complaint_description=desc,
                priority=priority,
                assigned_to=assigned,
                complaint_status=comp_status,
                resolution_note=resolution,
            )
            complaints.append(complaint)
            comp_counter += 1

    # Bulk insert
    with db.get_session() as session:
        session.add_all(orders)
        session.flush()
        session.add_all(complaints)

    logger.info(f"Seeded {len(orders)} orders and {len(complaints)} complaints.")
