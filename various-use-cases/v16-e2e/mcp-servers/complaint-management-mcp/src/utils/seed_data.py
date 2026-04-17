"""
Seed Data Module

Seeds the database with 20 realistic sample complaints using Faker.

Distribution:
  Status  - OPEN: 40%, IN_PROGRESS: 30%, RESOLVED: 20%, CLOSED: 10%
  Priority - LOW: 30%, MEDIUM: 40%, HIGH: 20%, CRITICAL: 10%
  Archived - 10% of records are soft-deleted

The seeder is idempotent: it only runs when the complaints table is empty.
"""

import random
from datetime import datetime, timedelta, timezone

from faker import Faker

from src.enums import Priority, Status
from src.models import Complaint
from src.utils.logger import get_logger

logger = get_logger(__name__)
fake = Faker()
Faker.seed(42)
random.seed(42)


# ---------------------------------------------------------------------------
# Distribution pools
# ---------------------------------------------------------------------------

_STATUS_POOL: list[Status] = (
    [Status.OPEN] * 8
    + [Status.IN_PROGRESS] * 6
    + [Status.RESOLVED] * 4
    + [Status.CLOSED] * 2
)  # total 20 — exact target distribution

_PRIORITY_POOL: list[Priority] = (
    [Priority.LOW] * 6
    + [Priority.MEDIUM] * 8
    + [Priority.HIGH] * 4
    + [Priority.CRITICAL] * 2
)  # total 20 — exact target distribution


# ---------------------------------------------------------------------------
# Sample text templates (realistic complaint content)
# ---------------------------------------------------------------------------

_TITLES = [
    "Item received in damaged condition",
    "Wrong product delivered for order",
    "Order delayed beyond promised date",
    "Missing items from shipment",
    "Billing charged twice for same order",
    "Product quality does not match description",
    "Package arrived with broken seal",
    "Delivery attempted but no notification sent",
    "Incorrect size/variant shipped",
    "Refund not processed after return",
    "Order cancelled without prior notice",
    "Tracking number not updating",
    "Product malfunctioned on first use",
    "Received expired product",
    "Partial order delivered - remainder missing",
    "Order shipped to wrong address",
    "Promotional discount not applied",
    "Item out of stock after order confirmed",
    "Courier left package with wrong neighbour",
    "Invoice total does not match cart total",
]

_DESCRIPTIONS = [
    "The outer packaging was visibly crushed and the contents were broken on arrival. "
    "I have photos to support this claim.",
    "I ordered the blue variant (size M) but received a red variant (size L) instead. "
    "Please arrange a replacement.",
    "The estimated delivery date was {date} but the order has still not arrived. "
    "No updates have been provided.",
    "Only 2 of the 4 ordered items were included in the shipment. "
    "The packing slip shows all 4 items.",
    "My credit card statement shows two identical charges of the same amount for this order. "
    "Please investigate and refund the duplicate.",
    "The product images on the website showed a premium finish, but the delivered item "
    "appears to be a lower-grade material.",
    "When I opened the box the tamper-evident seal was already broken. "
    "I am concerned about product integrity.",
    "The courier marked the delivery as attempted but I was home all day and received "
    "no knock or notification.",
    "I specifically selected size XL during checkout but received size S. "
    "Please send a pre-paid return label.",
    "My return was received by your warehouse 14 days ago but the refund has not "
    "appeared on my account.",
    "I received a cancellation email with no explanation. "
    "The item was listed as in stock at the time of purchase.",
    "The tracking page has shown 'In Transit' for 8 days with no further updates. "
    "Please check with the courier.",
    "The device stopped charging after fewer than 10 uses. "
    "This appears to be a manufacturing defect.",
    "The 'best before' date printed on the product is two weeks in the past. "
    "This is unacceptable for a food item.",
    "The shipping confirmation email listed 5 items but only 3 were in the box. "
    "The missing items are still showing as 'delivered'.",
    "The package was delivered to a different street entirely. "
    "I had to retrieve it from a neighbour two blocks away.",
    "I used the promotional code at checkout and it was accepted, but the final invoice "
    "does not reflect the discount.",
    "I received an 'order confirmed' email but was later told the item is out of stock. "
    "I need a timeline for fulfillment.",
    "A card was left saying my parcel was left with a neighbour, but none of my neighbours "
    "have received it.",
    "The checkout total was $48.99 but the invoice emailed to me shows $56.99. "
    "Please clarify the discrepancy.",
]

_REMARKS = [
    "Customer contacted via email; awaiting response.",
    "Replacement dispatched with tracking reference.",
    "Escalated to logistics team for investigation.",
    "Refund approved and submitted to finance.",
    "Customer requested callback — scheduled for tomorrow.",
    "Warehouse team confirmed stock discrepancy.",
    "Photos reviewed; damage confirmed by QA team.",
    "Courier contacted for investigation.",
    None,  # Some records have no remarks
    None,
]


# ---------------------------------------------------------------------------
# Helper builders
# ---------------------------------------------------------------------------

def _random_past_datetime(days_back_max: int = 90) -> datetime:
    """Return a random UTC datetime within the past N days."""
    offset = random.randint(0, days_back_max * 24 * 60)  # minutes
    return datetime.now(timezone.utc) - timedelta(minutes=offset)


def _build_complaint(index: int, status: Status, priority: Priority) -> Complaint:
    """Construct a single Complaint instance with realistic data."""
    created_at = _random_past_datetime(days_back_max=90)

    # Resolution date only makes sense for RESOLVED / CLOSED
    resolution_date: datetime | None = None
    if status in (Status.RESOLVED, Status.CLOSED):
        resolution_date = created_at + timedelta(days=random.randint(1, 14))

    # 10% chance of being archived (soft-deleted)
    is_archived = index % 10 == 9  # indices 9, 19, 29 … → exactly 10%

    # Format descriptions with a plausible missed-delivery date where applicable
    description_template = _DESCRIPTIONS[index % len(_DESCRIPTIONS)]
    missed_date = (created_at + timedelta(days=random.randint(2, 7))).strftime("%d %b %Y")
    description = description_template.replace("{date}", missed_date)

    remark = _REMARKS[index % len(_REMARKS)]

    return Complaint(
        title=_TITLES[index % len(_TITLES)],
        description=description,
        customer_name=fake.name(),
        order_number=f"ORD-{10000 + index + 1:05d}",
        priority=priority,
        status=status,
        remarks=remark,
        is_archived=is_archived,
        resolution_date=resolution_date,
        created_at=created_at,
        updated_at=created_at,
    )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def seed_database(session) -> int:
    """
    Seed the database with 20 sample complaints.

    This function is idempotent: it only inserts records when the table is empty.

    Args:
        session: An active SQLAlchemy :class:`Session`.

    Returns:
        Number of records inserted (0 if the table was already populated).
    """
    from src.database import check_database_empty  # avoid circular at module level

    if not check_database_empty():
        logger.info("Database already contains data — skipping seed.")
        return 0

    logger.info("Seeding database with %d sample complaints...", len(_STATUS_POOL))

    # Shuffle pools to avoid predictable ordering
    status_pool = _STATUS_POOL.copy()
    priority_pool = _PRIORITY_POOL.copy()
    random.shuffle(status_pool)
    random.shuffle(priority_pool)

    complaints: list[Complaint] = []
    for i in range(20):
        complaint = _build_complaint(i, status_pool[i], priority_pool[i])
        complaints.append(complaint)

    session.add_all(complaints)
    session.commit()

    logger.info("Seeded %d complaints successfully.", len(complaints))
    return len(complaints)
