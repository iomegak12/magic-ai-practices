"""
Test script to verify Phase 4 implementation.

Tests all 6 MCP tools against a freshly seeded database:
  - register_complaint
  - get_complaint
  - search_complaints
  - resolve_complaint
  - update_complaint
  - archive_complaint
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.database import init_database, get_db
from src.models import Complaint
from src.utils.seed_data import seed_database
from src.tools import (
    register_complaint,
    get_complaint,
    search_complaints,
    resolve_complaint,
    update_complaint,
    archive_complaint,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def assert_success(result: dict, label: str) -> dict:
    assert result.get("success") is True, (
        f"[{label}] Expected success=True, got: {result}"
    )
    return result


def assert_error(result: dict, code: str, label: str) -> dict:
    assert result.get("success") is False, (
        f"[{label}] Expected success=False, got: {result}"
    )
    assert result["error"]["code"] == code, (
        f"[{label}] Expected error code '{code}', got '{result['error']['code']}'"
    )
    return result


# ---------------------------------------------------------------------------
# Tool tests
# ---------------------------------------------------------------------------

async def test_register_complaint():
    print("Testing register_complaint...")

    # Valid registration
    r = await register_complaint(
        title="Damaged item on delivery",
        description="The product arrived with a cracked casing and scratches on the surface.",
        customer_name="Alice Johnson",
        order_number="ORD-99001",
        priority="HIGH",
        remarks="Customer requested urgent replacement.",
    )
    assert_success(r, "register valid")
    cid = r["data"]["complaint_id"]
    assert r["data"]["status"] == "OPEN"
    assert r["data"]["priority"] == "HIGH"
    assert r["data"]["is_archived"] is False
    print(f"  Registered complaint #{cid}")

    # Invalid title (too short)
    r2 = await register_complaint(
        title="Bad",
        description="This is a valid description for testing purposes.",
        customer_name="Bob Smith",
        order_number="ORD-99002",
    )
    assert_error(r2, "VALIDATION_ERROR", "register short title")

    # Invalid order number format
    r3 = await register_complaint(
        title="Valid title here",
        description="This is a valid description for testing purposes.",
        customer_name="Bob Smith",
        order_number="OD-1234",
    )
    assert_error(r3, "VALIDATION_ERROR", "register bad order number")

    # Invalid priority
    r4 = await register_complaint(
        title="Valid title here",
        description="This is a valid description for testing purposes.",
        customer_name="Bob Smith",
        order_number="ORD-99003",
        priority="EXTREME",
    )
    assert_error(r4, "INVALID_PRIORITY", "register bad priority")

    # Customer name with digits
    r5 = await register_complaint(
        title="Valid title here",
        description="This is a valid description for testing purposes.",
        customer_name="John123",
        order_number="ORD-99004",
    )
    assert_error(r5, "VALIDATION_ERROR", "register bad customer name")

    print("✓ register_complaint passed")
    return cid


async def test_get_complaint(existing_id: int):
    print("\nTesting get_complaint...")

    # Found
    r = await get_complaint(existing_id)
    assert_success(r, "get existing")
    assert r["data"]["complaint_id"] == existing_id
    print(f"  Retrieved complaint #{existing_id}: {r['data']['title'][:40]}")

    # Not found
    r2 = await get_complaint(999999)
    assert_error(r2, "NOT_FOUND", "get missing")

    # Invalid ID (zero)
    r3 = await get_complaint(0)
    assert_error(r3, "INVALID_ID", "get id=0")

    print("✓ get_complaint passed")


async def test_search_complaints():
    print("\nTesting search_complaints...")

    # By customer name (partial) — seeded data has real Faker names
    r = await search_complaints(customer_name="a")  # 'a' should appear in many names
    assert_success(r, "search by name")
    print(f"  search customer_name='a' → {r['count']} result(s)")

    # By order number prefix
    r2 = await search_complaints(order_number="ORD-1")
    assert_success(r2, "search by order")
    print(f"  search order_number='ORD-1' → {r2['count']} result(s)")

    # By status only
    r3 = await search_complaints(status="OPEN")
    assert_success(r3, "search by status")
    assert all(c["status"] == "OPEN" for c in r3["data"])
    print(f"  search status=OPEN → {r3['count']} result(s)")

    # OR-logic: customer name OR title
    r4 = await search_complaints(customer_name="John", title="damaged")
    assert_success(r4, "search OR logic")
    print(f"  search OR(customer=John, title=damaged) → {r4['count']} result(s)")

    # Include archived
    r5 = await search_complaints(order_number="ORD-", include_archived=True)
    assert_success(r5, "search include archived")
    r6 = await search_complaints(order_number="ORD-", include_archived=False)
    assert r5["count"] >= r6["count"], "include_archived=True should return >= results"
    print(f"  archived=True:{r5['count']} vs archived=False:{r6['count']}")

    # No criteria
    r7 = await search_complaints()
    assert_error(r7, "NO_CRITERIA", "search no criteria")

    # Invalid status
    r8 = await search_complaints(status="PENDING")
    assert_error(r8, "INVALID_STATUS", "search bad status")

    print("✓ search_complaints passed")


async def test_search_zero_result_hints():
    """
    Regression test for: search_complaints returning 0 results with no
    explanation when the matching record is archived or has a different status.

    Seed data: ORD-10010 = index 9 → is_archived=True, status=IN_PROGRESS
    """
    print("\nTesting search_complaints zero-result diagnostic hints...")

    # --- Hint 1: archived record ---
    # ORD-10010 is archived; default include_archived=False should hint
    r = await search_complaints(order_number="ORD-10010")
    assert_success(r, "archived hint: success=True even with 0 results")
    assert r["count"] == 0, "ORD-10010 is archived, expect 0 with include_archived=False"
    assert "archived" in r["message"].lower(), (
        f"Expected hint about archived records, got: {r['message']}"
    )
    assert "include_archived=true" in r["message"].lower(), (
        f"Expected 'include_archived=true' in hint, got: {r['message']}"
    )
    print(f"  Archived hint: '{r['message']}'")

    # Resolves with include_archived=True
    r2 = await search_complaints(order_number="ORD-10010", include_archived=True)
    assert_success(r2, "archived resolved")
    assert r2["count"] == 1, "ORD-10010 should be found when include_archived=True"
    print(f"  Resolved with include_archived=True → {r2['count']} result(s)")

    # --- Hint 2: status mismatch ---
    # Register a known OPEN complaint, then search it with status=RESOLVED
    reg = await register_complaint(
        title="Status hint regression test complaint",
        description="Created to verify status-mismatch diagnostic hint in search.",
        customer_name="Eve Turner",
        order_number="ORD-55001",
    )
    reg_id = reg["data"]["complaint_id"]

    r3 = await search_complaints(order_number="ORD-55001", status="RESOLVED")
    assert_success(r3, "status hint: success=True")
    assert r3["count"] == 0, "Status=RESOLVED should not match the OPEN complaint"
    assert "different status" in r3["message"].lower(), (
        f"Expected status-mismatch hint, got: {r3['message']}"
    )
    print(f"  Status-mismatch hint: '{r3['message']}'")

    # Resolves with correct status
    r4 = await search_complaints(order_number="ORD-55001", status="OPEN")
    assert_success(r4, "status resolved")
    assert r4["count"] == 1
    assert r4["data"][0]["complaint_id"] == reg_id
    print(f"  Resolved with correct status → {r4['count']} result(s)")

    print("✓ search_complaints zero-result hints passed")


async def test_resolve_complaint(complaint_id: int):
    print("\nTesting resolve_complaint...")

    # Resolve successfully
    r = await resolve_complaint(complaint_id, remarks="Issue confirmed and resolved by support team.")
    assert_success(r, "resolve valid")
    assert r["data"]["status"] == "RESOLVED"
    assert r["data"]["resolution_date"] is not None
    print(f"  Resolved complaint #{complaint_id}")

    # Cannot resolve again
    r2 = await resolve_complaint(complaint_id)
    assert_error(r2, "ALREADY_RESOLVED", "resolve already resolved")

    # Not found
    r3 = await resolve_complaint(999999)
    assert_error(r3, "NOT_FOUND", "resolve missing")

    print("✓ resolve_complaint passed")


async def test_update_complaint():
    print("\nTesting update_complaint...")

    # Register a fresh complaint to update
    reg = await register_complaint(
        title="Update test complaint",
        description="Original description for the update test scenario.",
        customer_name="Carol White",
        order_number="ORD-88001",
    )
    cid = reg["data"]["complaint_id"]

    # Update title only
    r = await update_complaint(cid, title="Updated title for the complaint")
    assert_success(r, "update title")
    assert r["data"]["title"] == "Updated title for the complaint"

    # Update description and remarks together
    r2 = await update_complaint(
        cid,
        description="Revised and more detailed description of the problem encountered.",
        remarks="Follow-up call scheduled for next Monday.",
    )
    assert_success(r2, "update desc+remarks")
    assert "revised" in r2["data"]["description"].lower()
    print(f"  Updated complaint #{cid}")

    # No fields provided
    r3 = await update_complaint(cid)
    assert_error(r3, "NO_UPDATES", "update no fields")

    # Archive it then fail to update
    await archive_complaint(cid)
    r4 = await update_complaint(cid, title="Should not work")
    assert_error(r4, "COMPLAINT_ARCHIVED", "update archived")

    # Not found
    r5 = await update_complaint(999999, title="Valid title for test")
    assert_error(r5, "NOT_FOUND", "update missing")

    print("✓ update_complaint passed")


async def test_archive_complaint():
    print("\nTesting archive_complaint...")

    # Register fresh complaint
    reg = await register_complaint(
        title="Archive test complaint",
        description="This complaint will be archived as part of the test suite.",
        customer_name="David Brown",
        order_number="ORD-77001",
    )
    cid = reg["data"]["complaint_id"]

    # Archive it
    r = await archive_complaint(cid)
    assert_success(r, "archive valid")
    assert r["data"]["is_archived"] is True
    print(f"  Archived complaint #{cid}")

    # Cannot archive again
    r2 = await archive_complaint(cid)
    assert_error(r2, "ALREADY_ARCHIVED", "archive twice")

    # Archived record not in default search
    r3 = await search_complaints(order_number="ORD-77001", include_archived=False)
    assert r3["count"] == 0, "Archived complaint should not appear in default search"

    # Archived record visible with flag
    r4 = await search_complaints(order_number="ORD-77001", include_archived=True)
    assert r4["count"] == 1, "Archived complaint should appear with include_archived=True"

    # Resolve an archived complaint → should fail
    r5 = await resolve_complaint(cid)
    assert_error(r5, "COMPLAINT_ARCHIVED", "resolve archived")

    # Not found
    r6 = await archive_complaint(999999)
    assert_error(r6, "NOT_FOUND", "archive missing")

    print("✓ archive_complaint passed")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

async def main():
    print("=" * 60)
    print("Phase 4: MCP Tools - Verification Tests")
    print("=" * 60)

    # Fresh DB state for tools tests
    init_database()
    with get_db() as session:
        # Drop all rows so seed runs fresh each time
        session.query(Complaint).delete()
        session.commit()
    with get_db() as session:
        seed_database(session)

    try:
        new_id = await test_register_complaint()
        await test_get_complaint(new_id)
        await test_search_complaints()
        await test_search_zero_result_hints()
        await test_resolve_complaint(new_id)
        await test_update_complaint()
        await test_archive_complaint()

        print("\n" + "=" * 60)
        print("✅ Phase 4: MCP Tools - ALL TESTS PASSED")
        print("=" * 60)
        print("\nTools Ready:")
        print("  ✓ register_complaint")
        print("  ✓ get_complaint")
        print("  ✓ search_complaints  (OR-logic + zero-result hints)")
        print("  ✓ resolve_complaint")
        print("  ✓ update_complaint")
        print("  ✓ archive_complaint  (soft-delete)")
        print("\nReady for Phase 5: Server Setup & Integration")

    except AssertionError as exc:
        print(f"\n❌ Assertion failed: {exc}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    except Exception as exc:
        print(f"\n❌ Unexpected error: {exc}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
