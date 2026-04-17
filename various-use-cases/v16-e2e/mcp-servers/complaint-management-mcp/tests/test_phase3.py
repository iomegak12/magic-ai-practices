"""
Test script to verify Phase 3 implementation.

Tests:
- Validators (title, description, customer_name, order_number)
- Logger (creation, handler counts)
- Seed data (20 records inserted, distributions, idempotency)
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.validators import (
    validate_title,
    validate_description,
    validate_customer_name,
    validate_order_number,
)
from src.utils.logger import get_logger
from src.utils.seed_data import seed_database
from src.database import init_database, get_db
from src.enums import Priority, Status


# ---------------------------------------------------------------------------
# Validators
# ---------------------------------------------------------------------------

def test_validate_title():
    print("Testing validate_title...")

    # Valid cases
    assert validate_title("Short bug") == "Short bug"
    assert validate_title("  Trimmed  ") == "Trimmed"
    assert validate_title("Order-123, issue.") == "Order-123, issue."

    # Too short
    try:
        validate_title("Hi")
        assert False, "Should have raised"
    except ValueError as e:
        assert "at least 5" in str(e)

    # Too long
    try:
        validate_title("A" * 201)
        assert False, "Should have raised"
    except ValueError as e:
        assert "not exceed 200" in str(e)

    # Invalid characters
    try:
        validate_title("Title with @special# chars!")
        assert False, "Should have raised"
    except ValueError as e:
        assert "invalid characters" in str(e)

    print("✓ validate_title passed")


def test_validate_description():
    print("\nTesting validate_description...")

    # Valid
    valid = "This is a valid complaint description."
    assert validate_description(valid) == valid

    # Too short
    try:
        validate_description("Too short")
        assert False, "Should have raised"
    except ValueError as e:
        assert "at least 10" in str(e)

    # Too long
    try:
        validate_description("A" * 2001)
        assert False, "Should have raised"
    except ValueError as e:
        assert "not exceed 2000" in str(e)

    print("✓ validate_description passed")


def test_validate_customer_name():
    print("\nTesting validate_customer_name...")

    assert validate_customer_name("John Doe") == "John Doe"
    assert validate_customer_name("  Alice  ") == "Alice"

    # Contains digits
    try:
        validate_customer_name("John123")
        assert False, "Should have raised"
    except ValueError as e:
        assert "invalid characters" in str(e)

    # Too short
    try:
        validate_customer_name("A")
        assert False, "Should have raised"
    except ValueError as e:
        assert "at least 2" in str(e)

    print("✓ validate_customer_name passed")


def test_validate_order_number():
    print("\nTesting validate_order_number...")

    assert validate_order_number("ORD-10001") == "ORD-10001"
    assert validate_order_number("ORD-999999") == "ORD-999999"
    assert validate_order_number("  ORD-10001  ") == "ORD-10001"

    # Wrong prefix
    try:
        validate_order_number("OD-10001")
        assert False, "Should have raised"
    except ValueError as e:
        assert "invalid" in str(e).lower()

    # Too few digits
    try:
        validate_order_number("ORD-1234")
        assert False, "Should have raised"
    except ValueError as e:
        assert "invalid" in str(e).lower()

    # Letters in numeric part
    try:
        validate_order_number("ORD-ABCDE")
        assert False, "Should have raised"
    except ValueError as e:
        assert "invalid" in str(e).lower()

    print("✓ validate_order_number passed")


# ---------------------------------------------------------------------------
# Logger
# ---------------------------------------------------------------------------

def test_logger():
    print("\nTesting Logger...")

    logger = get_logger("test-complaint-mcp")
    assert logger is not None
    assert len(logger.handlers) >= 1  # at least console handler

    # Idempotency: calling again should not add duplicate handlers
    logger2 = get_logger("test-complaint-mcp")
    assert len(logger.handlers) == len(logger2.handlers)

    logger.info("Logger test message — this should appear in logs.")
    print(f"  Handlers: {[type(h).__name__ for h in logger.handlers]}")
    print("✓ Logger passed")


# ---------------------------------------------------------------------------
# Seed data
# ---------------------------------------------------------------------------

def test_seed_data():
    print("\nTesting Seed Data...")

    # Re-init DB to ensure clean state for this test run
    init_database()

    with get_db() as session:
        inserted = seed_database(session)

    print(f"  Inserted: {inserted} records")
    assert inserted == 20, f"Expected 20, got {inserted}"

    # Verify records in DB
    with get_db() as session:
        from src.models import Complaint
        complaints = session.query(Complaint).all()
        total = len(complaints)
        assert total == 20, f"Expected 20 in DB, got {total}"

        # Status distribution
        statuses = [c.status for c in complaints]
        open_count = statuses.count(Status.OPEN)
        in_progress_count = statuses.count(Status.IN_PROGRESS)
        resolved_count = statuses.count(Status.RESOLVED)
        closed_count = statuses.count(Status.CLOSED)

        print(f"  Status  → OPEN:{open_count} IN_PROGRESS:{in_progress_count} "
              f"RESOLVED:{resolved_count} CLOSED:{closed_count}")
        assert open_count == 8,         f"Expected 8 OPEN, got {open_count}"
        assert in_progress_count == 6,  f"Expected 6 IN_PROGRESS, got {in_progress_count}"
        assert resolved_count == 4,     f"Expected 4 RESOLVED, got {resolved_count}"
        assert closed_count == 2,       f"Expected 2 CLOSED, got {closed_count}"

        # Priority distribution
        priorities = [c.priority for c in complaints]
        low_count = priorities.count(Priority.LOW)
        medium_count = priorities.count(Priority.MEDIUM)
        high_count = priorities.count(Priority.HIGH)
        critical_count = priorities.count(Priority.CRITICAL)

        print(f"  Priority → LOW:{low_count} MEDIUM:{medium_count} "
              f"HIGH:{high_count} CRITICAL:{critical_count}")
        assert low_count == 6,      f"Expected 6 LOW, got {low_count}"
        assert medium_count == 8,   f"Expected 8 MEDIUM, got {medium_count}"
        assert high_count == 4,     f"Expected 4 HIGH, got {high_count}"
        assert critical_count == 2, f"Expected 2 CRITICAL, got {critical_count}"

        # Archived count (10% = 2 out of 20)
        archived = [c for c in complaints if c.is_archived]
        print(f"  Archived: {len(archived)}")
        assert len(archived) == 2, f"Expected 2 archived, got {len(archived)}"

        # Resolution dates for RESOLVED / CLOSED
        for c in complaints:
            if c.status in (Status.RESOLVED, Status.CLOSED):
                assert c.resolution_date is not None, \
                    f"Complaint {c.complaint_id} is {c.status} but has no resolution_date"

    # Idempotency: second call should insert 0 records
    with get_db() as session:
        second_run = seed_database(session)
    assert second_run == 0, f"Idempotency check failed: expected 0, got {second_run}"
    print("  Idempotency: ✓ (0 records inserted on second run)")

    print("✓ Seed data passed")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=" * 60)
    print("Phase 3: Utilities & Supporting Services - Verification Tests")
    print("=" * 60)

    try:
        test_validate_title()
        test_validate_description()
        test_validate_customer_name()
        test_validate_order_number()
        test_logger()
        test_seed_data()

        print("\n" + "=" * 60)
        print("✅ Phase 3: Utilities - ALL TESTS PASSED")
        print("=" * 60)
        print("\nUtility Components Ready:")
        print("  ✓ validate_title")
        print("  ✓ validate_description")
        print("  ✓ validate_customer_name")
        print("  ✓ validate_order_number")
        print("  ✓ get_logger")
        print("  ✓ seed_database (20 records, correct distribution, idempotent)")
        print("\nReady for Phase 4: MCP Tools Implementation")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
