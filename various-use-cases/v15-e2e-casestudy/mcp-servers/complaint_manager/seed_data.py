"""
Seed database with sample complaint data
Only seeds if database is empty and SEED_DATABASE is enabled
"""

import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any

from .database import db
from .models import Complaint

logger = logging.getLogger(__name__)


def check_if_data_exists() -> bool:
    """Check if the database already has complaint data"""
    try:
        with db.get_session() as session:
            count = session.query(Complaint).count()
            return count > 0
    except Exception as e:
        logger.error(f"Error checking for existing data: {e}")
        return False


def generate_sample_complaints() -> List[Dict[str, Any]]:
    """Generate sample complaint data"""
    
    base_date = datetime.utcnow()
    
    sample_complaints = [
        {
            "description": "Product arrived damaged - screen has multiple cracks",
            "customer_name": "John Smith",
            "order_id": "ORD-10001",
            "priority": "High",
            "status": "In Progress",
            "remarks": "Replacement unit being prepared for shipment",
            "complaint_registration_date": base_date - timedelta(days=5)
        },
        {
            "description": "Wrong color delivered - ordered black, received white",
            "customer_name": "Sarah Johnson",
            "order_id": "ORD-10002",
            "priority": "Medium",
            "status": "Open",
            "remarks": "Customer requested return and reorder",
            "complaint_registration_date": base_date - timedelta(days=3)
        },
        {
            "description": "Missing accessories in the package",
            "customer_name": "Michael Brown",
            "order_id": "ORD-10003",
            "priority": "Low",
            "status": "Resolved",
            "remarks": "Missing items shipped separately and delivered",
            "complaint_registration_date": base_date - timedelta(days=10)
        },
        {
            "description": "Product not working - device won't power on",
            "customer_name": "Emily Davis",
            "order_id": "ORD-10004",
            "priority": "Critical",
            "status": "Open",
            "remarks": "Technical team investigating the issue",
            "complaint_registration_date": base_date - timedelta(days=1)
        },
        {
            "description": "Late delivery - 5 days past promised date",
            "customer_name": "David Wilson",
            "order_id": "ORD-10005",
            "priority": "High",
            "status": "Closed",
            "remarks": "Delivered with apology and discount coupon provided",
            "complaint_registration_date": base_date - timedelta(days=15)
        },
        {
            "description": "Product quality below expectations - material feels cheap",
            "customer_name": "Jessica Martinez",
            "order_id": "ORD-10006",
            "priority": "Medium",
            "status": "In Progress",
            "remarks": "Quality assurance team reviewing the product batch",
            "complaint_registration_date": base_date - timedelta(days=7)
        },
        {
            "description": "Incorrect product shipped - ordered laptop, received tablet",
            "customer_name": "Robert Taylor",
            "order_id": "ORD-10007",
            "priority": "Critical",
            "status": "In Progress",
            "remarks": "Return initiated, correct item being shipped expedited",
            "complaint_registration_date": base_date - timedelta(days=2)
        },
        {
            "description": "Package opened and resealed - suspected tampering",
            "customer_name": "Linda Anderson",
            "order_id": "ORD-10008",
            "priority": "High",
            "status": "Open",
            "remarks": "Security team investigating warehouse procedures",
            "complaint_registration_date": base_date - timedelta(days=4)
        },
        {
            "description": "Defective charger - not charging the device",
            "customer_name": "James Thomas",
            "order_id": "ORD-10009",
            "priority": "Medium",
            "status": "Resolved",
            "remarks": "Replacement charger sent and confirmed working",
            "complaint_registration_date": base_date - timedelta(days=12)
        },
        {
            "description": "Items missing from order - only received 2 of 3 items",
            "customer_name": "Patricia Jackson",
            "order_id": "ORD-10010",
            "priority": "High",
            "status": "Resolved",
            "remarks": "Missing item shipped with expedited delivery",
            "complaint_registration_date": base_date - timedelta(days=8)
        },
        {
            "description": "Product size mismatch - label says medium but fits like small",
            "customer_name": "Christopher White",
            "order_id": "ORD-10011",
            "priority": "Low",
            "status": "Open",
            "remarks": "Return label provided, replacement being processed",
            "complaint_registration_date": base_date - timedelta(days=6)
        },
        {
            "description": "Software/firmware issues - device keeps crashing",
            "customer_name": "Mary Harris",
            "order_id": "ORD-10012",
            "priority": "High",
            "status": "In Progress",
            "remarks": "Technical support working on firmware update solution",
            "complaint_registration_date": base_date - timedelta(days=3)
        },
        {
            "description": "Poor packaging - item not protected during shipping",
            "customer_name": "Daniel Martin",
            "order_id": "ORD-10013",
            "priority": "Medium",
            "status": "Closed",
            "remarks": "Customer satisfied with partial refund, improved packaging noted",
            "complaint_registration_date": base_date - timedelta(days=20)
        },
        {
            "description": "Battery drains too quickly - lasts only 2 hours",
            "customer_name": "Jennifer Thompson",
            "order_id": "ORD-10014",
            "priority": "Medium",
            "status": "Open",
            "remarks": "Diagnostics requested from customer",
            "complaint_registration_date": base_date - timedelta(days=5)
        },
        {
            "description": "Product description misleading - features not as advertised",
            "customer_name": "Matthew Garcia",
            "order_id": "ORD-10015",
            "priority": "Low",
            "status": "New",
            "remarks": "Product team reviewing description accuracy",
            "complaint_registration_date": base_date - timedelta(hours=12)
        }
    ]
    
    return sample_complaints


def seed_database() -> Dict[str, Any]:
    """
    Seed the database with sample complaints
    Returns operation result
    """
    try:
        # Check if data already exists
        if check_if_data_exists():
            logger.info("Database already contains data. Skipping seed operation.")
            return {
                "success": True,
                "message": "Database already seeded",
                "seeded": False,
                "count": 0
            }
        
        logger.info("Seeding database with sample complaint data...")
        
        # Generate sample data
        sample_complaints = generate_sample_complaints()
        
        # Insert data
        with db.get_session() as session:
            for complaint_data in sample_complaints:
                complaint = Complaint(**complaint_data)
                session.add(complaint)
            
            session.flush()
            count = len(sample_complaints)
        
        logger.info(f"Successfully seeded {count} sample complaints")
        
        return {
            "success": True,
            "message": f"Database seeded with {count} sample complaints",
            "seeded": True,
            "count": count
        }
    
    except Exception as e:
        logger.error(f"Error seeding database: {e}")
        return {
            "success": False,
            "message": f"Failed to seed database: {str(e)}",
            "seeded": False,
            "count": 0
        }


def run_seed_if_enabled(seed_enabled: bool = False) -> Dict[str, Any]:
    """
    Run seed operation if enabled in configuration
    
    Args:
        seed_enabled: Whether seeding is enabled
    
    Returns:
        Operation result dictionary
    """
    if not seed_enabled:
        logger.info("Database seeding is disabled in configuration")
        return {
            "success": True,
            "message": "Seeding disabled",
            "seeded": False,
            "count": 0
        }
    
    return seed_database()
