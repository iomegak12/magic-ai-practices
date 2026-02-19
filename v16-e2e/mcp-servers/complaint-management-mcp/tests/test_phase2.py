"""
Test script to verify Phase 2 implementation.

This script tests that all core infrastructure components work correctly:
- Enums
- Configuration
- Models
- Database
- Schemas
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.enums import Priority, Status
from src.config import load_config
from src.database import init_database, check_database_empty
from src.models import Complaint
from src.schemas import ComplaintCreate, ErrorResponse


def test_enums():
    """Test enum definitions."""
    print("Testing Enums...")
    assert Priority.LOW == "LOW"
    assert Priority.MEDIUM == "MEDIUM"
    assert Priority.HIGH == "HIGH"
    assert Priority.CRITICAL == "CRITICAL"

    assert Status.OPEN == "OPEN"
    assert Status.IN_PROGRESS == "IN_PROGRESS"
    assert Status.RESOLVED == "RESOLVED"
    assert Status.CLOSED == "CLOSED"
    print("✓ Enums working correctly")


def test_config():
    """Test configuration loading."""
    print("\nTesting Configuration...")
    config = load_config()
    print(f"  Server: {config.server_name}")
    print(f"  Host: {config.host}:{config.port}")
    print(f"  Database: {config.database_path}")
    print(f"  Auto-seed: {config.auto_seed} ({config.seed_count} records)")
    print(f"✓ Configuration loaded successfully")
    return config


def test_database():
    """Test database initialization."""
    print("\nTesting Database...")
    init_database()
    is_empty = check_database_empty()
    print(f"  Database initialized")
    print(f"  Database empty: {is_empty}")
    print(f"✓ Database working correctly")


def test_schemas():
    """Test Pydantic schemas."""
    print("\nTesting Schemas...")

    # Test valid complaint creation
    complaint_data = ComplaintCreate(
        title="Test complaint",
        description="This is a test complaint description",
        customer_name="John Doe",
        order_number="ORD-10001",
        priority=Priority.HIGH
    )
    print(f"  Created schema: {complaint_data.title}")

    # Test error response
    error = ErrorResponse.create(
        code="TEST_ERROR",
        message="This is a test error"
    )
    print(f"  Error response: {error['error']['code']}")
    print(f"✓ Schemas working correctly")


def test_model():
    """Test Complaint model."""
    print("\nTesting Model...")

    complaint = Complaint(
        title="Test Model Complaint",
        description="Testing the complaint model",
        customer_name="Jane Smith",
        order_number="ORD-20001",
        priority=Priority.MEDIUM,
        status=Status.OPEN
    )

    complaint_dict = complaint.to_dict()
    print(f"  Model to_dict: {complaint_dict['title']}")
    print(f"  Model repr: {complaint}")
    print(f"✓ Model working correctly")


def main():
    """Run all tests."""
    print("=" * 60)
    print("Phase 2: Core Infrastructure - Verification Tests")
    print("=" * 60)

    try:
        test_enums()
        config = test_config()
        test_database()
        test_schemas()
        test_model()

        print("\n" + "=" * 60)
        print("✅ Phase 2: Core Infrastructure - ALL TESTS PASSED")
        print("=" * 60)
        print("\nCore Components Ready:")
        print("  ✓ Enums (Priority, Status)")
        print("  ✓ Configuration Management")
        print("  ✓ Database Connection & Models")
        print("  ✓ Pydantic Schemas")
        print("\nReady for Phase 3: Utilities & Supporting Services")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
