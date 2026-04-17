"""Seed script — populates 15 Indian customers, 4-5 IT complaints each, and profile preferences.

Run with:  python -m customers_complaints.seed
"""

import random
from datetime import datetime, timedelta

from .database import get_session, init_db
from .models import Complaint, Customer, CustomerProfilePreference

# ---------------------------------------------------------------------------
# Seed data
# ---------------------------------------------------------------------------

SEED_CUSTOMERS = [
    {
        "customer_id": "CUST10001",
        "customer_name": "Shweta Iyer",
        "address": "42, MG Road, Indiranagar, Bangalore 560038",
        "email": "shweta.iyer@email.in",
        "phone": "+91-80-98765432",
        "active_status": "active",
        "remarks": "Key enterprise account",
    },
    {
        "customer_id": "CUST10002",
        "customer_name": "Rajesh Sharma",
        "address": "15, Connaught Place, New Delhi 110001",
        "email": "rajesh.sharma@email.in",
        "phone": "+91-11-23456789",
        "active_status": "active",
        "remarks": None,
    },
    {
        "customer_id": "CUST10003",
        "customer_name": "Priya Nair",
        "address": "7, Marine Drive, Mumbai 400020",
        "email": "priya.nair@email.in",
        "phone": "+91-22-87654321",
        "active_status": "active",
        "remarks": "Prefers email communication",
    },
    {
        "customer_id": "CUST10004",
        "customer_name": "Arun Mehta",
        "address": "23, Anna Salai, T. Nagar, Chennai 600017",
        "email": "arun.mehta@email.in",
        "phone": "+91-44-34567890",
        "active_status": "active",
        "remarks": None,
    },
    {
        "customer_id": "CUST10005",
        "customer_name": "Deepika Reddy",
        "address": "88, Banjara Hills, Road No. 12, Hyderabad 500034",
        "email": "deepika.reddy@email.in",
        "phone": "+91-40-45678901",
        "active_status": "active",
        "remarks": "VPN access issues reported frequently",
    },
    {
        "customer_id": "CUST10006",
        "customer_name": "Vikram Joshi",
        "address": "3, FC Road, Shivajinagar, Pune 411005",
        "email": "vikram.joshi@email.in",
        "phone": "+91-20-56789012",
        "active_status": "inactive",
        "remarks": "Account under review",
    },
    {
        "customer_id": "CUST10007",
        "customer_name": "Ananya Gupta",
        "address": "56, Park Street, Kolkata 700016",
        "email": "ananya.gupta@email.in",
        "phone": "+91-33-67890123",
        "active_status": "active",
        "remarks": None,
    },
    {
        "customer_id": "CUST10008",
        "customer_name": "Karthik Sundaram",
        "address": "12, 100 Feet Road, Koramangala, Bangalore 560034",
        "email": "karthik.sundaram@email.in",
        "phone": "+91-80-78901234",
        "active_status": "active",
        "remarks": "Recently upgraded hardware",
    },
    {
        "customer_id": "CUST10009",
        "customer_name": "Meera Pillai",
        "address": "9, MG Road, Ernakulam, Kochi 682011",
        "email": "meera.pillai@email.in",
        "phone": "+91-484-89012345",
        "active_status": "active",
        "remarks": None,
    },
    {
        "customer_id": "CUST10010",
        "customer_name": "Suresh Patel",
        "address": "34, SG Highway, Ahmedabad 380015",
        "email": "suresh.patel@email.in",
        "phone": "+91-79-90123456",
        "active_status": "active",
        "remarks": "Remote worker — needs stable VPN",
    },
    {
        "customer_id": "CUST10011",
        "customer_name": "Neha Singh",
        "address": "67, Hazratganj, Lucknow 226001",
        "email": "neha.singh@email.in",
        "phone": "+91-522-01234567",
        "active_status": "active",
        "remarks": None,
    },
    {
        "customer_id": "CUST10012",
        "customer_name": "Rohit Banerjee",
        "address": "21, Salt Lake, Sector V, Kolkata 700091",
        "email": "rohit.banerjee@email.in",
        "phone": "+91-33-12345098",
        "active_status": "inactive",
        "remarks": "Left organisation",
    },
    {
        "customer_id": "CUST10013",
        "customer_name": "Kavitha Rangan",
        "address": "5, Cathedral Road, Gopalapuram, Chennai 600086",
        "email": "kavitha.rangan@email.in",
        "phone": "+91-44-23456701",
        "active_status": "active",
        "remarks": "Team lead — IT procurement",
    },
    {
        "customer_id": "CUST10014",
        "customer_name": "Amit Deshmukh",
        "address": "78, Fergusson College Road, Pune 411004",
        "email": "amit.deshmukh@email.in",
        "phone": "+91-20-34567802",
        "active_status": "active",
        "remarks": None,
    },
    {
        "customer_id": "CUST10015",
        "customer_name": "Pooja Bhat",
        "address": "11, Residency Road, Ashok Nagar, Bangalore 560025",
        "email": "pooja.bhat@email.in",
        "phone": "+91-80-45678903",
        "active_status": "active",
        "remarks": "Frequent software installation requests",
    },
]

# Profile types — Shweta is platinum
SEED_PROFILES = {
    "CUST10001": "platinum",  # Shweta
    "CUST10002": "gold",
    "CUST10003": "silver",
    "CUST10004": "general",
    "CUST10005": "gold",
    "CUST10006": "general",
    "CUST10007": "silver",
    "CUST10008": "gold",
    "CUST10009": "general",
    "CUST10010": "silver",
    "CUST10011": "gold",
    "CUST10012": "general",
    "CUST10013": "platinum",
    "CUST10014": "silver",
    "CUST10015": "gold",
}

# IT complaint templates
COMPLAINT_TEMPLATES = [
    ("Laptop not booting after Windows update", "High"),
    ("Unable to connect to corporate VPN from home", "High"),
    ("Outlook keeps crashing when opening attachments", "Medium"),
    ("Printer on 3rd floor not responding to print jobs", "Low"),
    ("Request for additional monitor for workstation", "Low"),
    ("Microsoft Teams screen sharing not working", "Medium"),
    ("Password reset required — account locked out", "Critical"),
    ("Software license expired for Adobe Creative Suite", "Medium"),
    ("Wi-Fi connectivity drops every 15 minutes", "High"),
    ("Cannot access shared network drive \\\\fileserver\\projects", "Medium"),
    ("New laptop setup and data migration request", "Low"),
    ("Email not syncing on mobile device", "Medium"),
    ("Blue screen error (BSOD) occurring daily", "Critical"),
    ("Slow internet speed affecting video conferencing", "High"),
    ("Request to install Python 3.12 and VS Code", "Low"),
    ("Two-factor authentication app not generating codes", "High"),
    ("USB ports not working on docking station", "Medium"),
    ("SharePoint site access permission denied", "Medium"),
    ("Zoom audio echo during conference calls", "Low"),
    ("Hard drive running out of space — need cleanup", "Medium"),
    ("Antivirus scan flagging internal tool as threat", "High"),
    ("Cannot connect to database server from IDE", "High"),
    ("Mouse and keyboard lag on remote desktop session", "Medium"),
    ("Need VPN access for new project environment", "Medium"),
    ("Webcam not detected after driver update", "Low"),
]

STATUSES = ["Open", "In Progress", "Resolved", "Closed", "Reopened"]


def _random_date() -> datetime:
    """Generate a random datetime in the past 90 days."""
    days_ago = random.randint(1, 90)
    hours = random.randint(8, 18)
    minutes = random.randint(0, 59)
    return datetime.now() - timedelta(days=days_ago, hours=hours, minutes=minutes)


def seed() -> None:
    """Seed the database with sample data."""
    init_db()

    with get_session() as session:
        # Check if already seeded
        if session.query(Customer).count() > 0:
            print("Database already contains data — skipping seed.")
            return

        # --- Customers ---
        for data in SEED_CUSTOMERS:
            session.add(Customer(**data))

        # --- Profile Preferences ---
        for cust_id, cust_type in SEED_PROFILES.items():
            session.add(
                CustomerProfilePreference(customer_id=cust_id, customer_type=cust_type)
            )

        # --- Complaints (4-5 per customer) ---
        complaint_counter = 10001
        for cust in SEED_CUSTOMERS:
            num_complaints = random.randint(4, 5)
            chosen = random.sample(COMPLAINT_TEMPLATES, num_complaints)
            for description, default_priority in chosen:
                # Platinum customers get High if the template priority would be Medium or Low
                profile_type = SEED_PROFILES[cust["customer_id"]]
                if profile_type == "platinum" and default_priority in ("Medium", "Low"):
                    priority = "High"
                else:
                    priority = default_priority

                session.add(
                    Complaint(
                        complaint_id=f"COMP{complaint_counter}",
                        complaint_date=_random_date(),
                        customer_id=cust["customer_id"],
                        complaint_description=description,
                        priority=priority,
                        status=random.choice(STATUSES),
                    )
                )
                complaint_counter += 1

        session.commit()

    print("Seed complete — 15 customers, profile preferences, and complaints inserted.")


if __name__ == "__main__":
    seed()
