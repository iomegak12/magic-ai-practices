"""
Unit Tests for Helper Utilities

Tests for app/utils/helpers.py functions.
"""
import pytest
from datetime import datetime
from app.utils.helpers import (
    generate_request_id,
    generate_session_id,
    mask_sensitive_value,
    sanitize_session_id,
    sanitize_tenant_id,
    format_timestamp,
    compute_hash,
    truncate_string,
    merge_dicts,
    chunk_list
)


class TestIDGeneration:
    """Tests for ID generation functions."""
    
    def test_generate_request_id_format(self):
        """Test request ID has correct format."""
        request_id = generate_request_id()
        
        assert isinstance(request_id, str)
        assert request_id.startswith("REQ-")
        assert len(request_id) > 10  # REQ- + timestamp + random
    
    def test_generate_request_id_uniqueness(self):
        """Test that consecutive request IDs are unique."""
        id1 = generate_request_id()
        id2 = generate_request_id()
        
        assert id1 != id2
    
    def test_generate_session_id_format(self):
        """Test session ID has correct format."""
        session_id = generate_session_id()
        
        assert isinstance(session_id, str)
        assert session_id.startswith("SES-")
        assert len(session_id) > 10
    
    def test_generate_session_id_uniqueness(self):
        """Test that consecutive session IDs are unique."""
        id1 = generate_session_id()
        id2 = generate_session_id()
        
        assert id1 != id2


class TestSensitiveDataMasking:
    """Tests for sensitive data masking."""
    
    def test_mask_short_string(self):
        """Test masking of short strings shows partial content."""
        result = mask_sensitive_value("1234")
        assert len(result) == 4
        assert "*" in result
    
    def test_mask_long_string(self):
        """Test masking of long strings."""
        result = mask_sensitive_value("1234567890abcdef")
        assert result.startswith("1234")
        assert result.endswith("cdef")
        assert "..." in result
    
    def test_mask_empty_string(self):
        """Test masking empty string."""
        result = mask_sensitive_value("")
        assert result == "****"
    
    def test_mask_none_value(self):
        """Test masking None value."""
        result = mask_sensitive_value(None)
        assert result == "****"


class TestSanitization:
    """Tests for input sanitization."""
    
    def test_sanitize_session_id_valid(self):
        """Test sanitizing valid session ID."""
        result = sanitize_session_id("SES-123-ABC")
        assert result == "SES-123-ABC"
    
    def test_sanitize_session_id_with_spaces(self):
        """Test sanitizing session ID with spaces."""
        result = sanitize_session_id("  SES-123  ")
        assert result == "SES-123"
    
    def test_sanitize_session_id_invalid_chars(self):
        """Test sanitizing session ID with invalid characters."""
        result = sanitize_session_id("SES-123!@#$")
        assert "!" not in result
        assert "@" not in result
    
    def test_sanitize_tenant_id(self):
        """Test sanitizing tenant ID."""
        result = sanitize_tenant_id("  tenant-123  ")
        assert result == "tenant-123"


class TestTimestampFormatting:
    """Tests for timestamp formatting."""
    
    def test_format_timestamp_default(self):
        """Test default timestamp formatting."""
        result = format_timestamp(datetime.now())
        
        assert isinstance(result, str)
        # Should match ISO 8601 format
        datetime.fromisoformat(result)  # Should not raise
    
    def test_format_timestamp_custom_dt(self):
        """Test formatting specific datetime."""
        dt = datetime(2024, 1, 15, 10, 30, 0)
        result = format_timestamp(dt)
        
        assert "2024-01-15" in result
        assert "10:30:00" in result


class TestHashing:
    """Tests for hashing functions."""
    
    def test_compute_hash_string(self):
        """Test hashing a string."""
        result = compute_hash("test")
        
        assert isinstance(result, str)
        assert len(result) == 64  # SHA256 produces 64 char hex string
    
    def test_compute_hash_consistency(self):
        """Test that same input produces same hash."""
        hash1 = compute_hash("test")
        hash2 = compute_hash("test")
        
        assert hash1 == hash2
    
    def test_compute_hash_different_inputs(self):
        """Test that different inputs produce different hashes."""
        hash1 = compute_hash("test1")
        hash2 = compute_hash("test2")
        
        assert hash1 != hash2


class TestStringManipulation:
    """Tests for string manipulation functions."""
    
    def test_truncate_string_short(self):
        """Test truncating string shorter than max length."""
        result = truncate_string("hello", max_length=10)
        assert result == "hello"
    
    def test_truncate_string_long(self):
        """Test truncating long string."""
        result = truncate_string("hello world this is a test", max_length=15)
        assert len(result) <= 15
        assert result.endswith("...")
    
    def test_truncate_string_exact_length(self):
        """Test truncating string at exact max length."""
        result = truncate_string("hello", max_length=5)
        assert result == "hello"


class TestDictionaryOperations:
    """Tests for dictionary operations."""
    
    def test_merge_dicts_simple(self):
        """Test merging two simple dictionaries."""
        dict1 = {"a": 1, "b": 2}
        dict2 = {"c": 3, "d": 4}
        
        result = merge_dicts(dict1, dict2)
        
        assert result == {"a": 1, "b": 2, "c": 3, "d": 4}
    
    def test_merge_dicts_override(self):
        """Test that second dict overrides first."""
        dict1 = {"a": 1, "b": 2}
        dict2 = {"b": 3, "c": 4}
        
        result = merge_dicts(dict1, dict2)
        
        assert result["b"] == 3  # dict2 value wins
    
    def test_merge_dicts_nested(self):
        """Test merging dictionaries with nested values."""
        dict1 = {"a": {"x": 1}, "b": 2}
        dict2 = {"a": {"y": 2}, "c": 3}
        
        result = merge_dicts(dict1, dict2)
        
        assert "a" in result
        assert "b" in result
        assert "c" in result


class TestListOperations:
    """Tests for list operations."""
    
    def test_chunk_list_even_division(self):
        """Test chunking list with even division."""
        items = [1, 2, 3, 4, 5, 6]
        chunks = chunk_list(items, chunk_size=2)
        
        assert len(chunks) == 3
        assert chunks[0] == [1, 2]
        assert chunks[1] == [3, 4]
        assert chunks[2] == [5, 6]
    
    def test_chunk_list_uneven_division(self):
        """Test chunking list with uneven division."""
        items = [1, 2, 3, 4, 5]
        chunks = chunk_list(items, chunk_size=2)
        
        assert len(chunks) == 3
        assert chunks[0] == [1, 2]
        assert chunks[1] == [3, 4]
        assert chunks[2] == [5]
    
    def test_chunk_list_empty(self):
        """Test chunking empty list."""
        items = []
        chunks = chunk_list(items, chunk_size=2)
        
        assert chunks == []
    
    def test_chunk_list_single_chunk(self):
        """Test chunking list into single chunk."""
        items = [1, 2, 3]
        chunks = chunk_list(items, chunk_size=10)
        
        assert len(chunks) == 1
        assert chunks[0] == [1, 2, 3]
