"""
Helper Utilities

General-purpose utility functions used across the application.
"""

import uuid
from typing import Any, Optional
from datetime import datetime, timezone
import hashlib
import re


def generate_request_id() -> str:
    """
    Generate a unique request ID.
    
    Returns:
        str: Unique request ID (UUID4)
    """
    return str(uuid.uuid4())


def generate_session_id(prefix: str = "session") -> str:
    """
    Generate a unique session ID with optional prefix.
    
    Args:
        prefix: Prefix for session ID
        
    Returns:
        str: Session ID in format "prefix-uuid"
    """
    return f"{prefix}-{uuid.uuid4().hex[:16]}"


def get_utc_now() -> datetime:
    """
    Get current UTC datetime.
    
    Returns:
        datetime: Current UTC datetime with timezone info
    """
    return datetime.now(timezone.utc)


def format_timestamp(dt: datetime) -> str:
    """
    Format datetime as ISO 8601 string.
    
    Args:
        dt: Datetime to format
        
    Returns:
        str: ISO 8601 formatted string
    """
    return dt.isoformat()


def parse_timestamp(timestamp: str) -> datetime:
    """
    Parse ISO 8601 timestamp string.
    
    Args:
        timestamp: ISO 8601 formatted string
        
    Returns:
        datetime: Parsed datetime
    """
    return datetime.fromisoformat(timestamp)


def mask_sensitive_value(value: str, show_chars: int = 4) -> str:
    """
    Mask sensitive value showing only first and last N characters.
    
    Args:
        value: Value to mask
        show_chars: Number of characters to show at start/end
        
    Returns:
        str: Masked value
    """
    if not value:
        return "***"
    
    if len(value) <= show_chars * 2:
        return "***"
    
    return f"{value[:show_chars]}...{value[-show_chars:]}"


def compute_hash(value: str, algorithm: str = "sha256") -> str:
    """
    Compute hash of a string value.
    
    Args:
        value: Value to hash
        algorithm: Hash algorithm (md5, sha1, sha256, sha512)
        
    Returns:
        str: Hex digest of hash
    """
    hash_obj = hashlib.new(algorithm)
    hash_obj.update(value.encode("utf-8"))
    return hash_obj.hexdigest()


def sanitize_session_id(session_id: str) -> str:
    """
    Sanitize session ID to prevent injection attacks.
    
    Args:
        session_id: Raw session ID
        
    Returns:
        str: Sanitized session ID
        
    Raises:
        ValueError: If session ID is invalid
    """
    # Only allow alphanumeric, dash, underscore
    if not re.match(r"^[a-zA-Z0-9_-]+$", session_id):
        raise ValueError("Session ID contains invalid characters")
    
    # Limit length
    if len(session_id) > 255:
        raise ValueError("Session ID too long")
    
    return session_id


def sanitize_tenant_id(tenant_id: str) -> str:
    """
    Sanitize tenant ID to prevent injection attacks.
    
    Args:
        tenant_id: Raw tenant ID
        
    Returns:
        str: Sanitized tenant ID
        
    Raises:
        ValueError: If tenant ID is invalid
    """
    # Only allow alphanumeric, dash, underscore
    if not re.match(r"^[a-zA-Z0-9_-]+$", tenant_id):
        raise ValueError("Tenant ID contains invalid characters")
    
    # Limit length
    if len(tenant_id) > 255:
        raise ValueError("Tenant ID too long")
    
    return tenant_id


def truncate_string(value: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate string to maximum length.
    
    Args:
        value: String to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
        
    Returns:
        str: Truncated string
    """
    if len(value) <= max_length:
        return value
    
    return value[:max_length - len(suffix)] + suffix


def safe_get(obj: Any, key: str, default: Any = None) -> Any:
    """
    Safely get value from object/dict with fallback.
    
    Args:
        obj: Object or dict to get value from
        key: Key to access
        default: Default value if key doesn't exist
        
    Returns:
        Any: Value or default
    """
    try:
        if isinstance(obj, dict):
            return obj.get(key, default)
        else:
            return getattr(obj, key, default)
    except (AttributeError, KeyError, TypeError):
        return default


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        str: Formatted size (e.g., "1.5 MB")
    """
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} PB"


def merge_dicts(*dicts: dict, deep: bool = False) -> dict:
    """
    Merge multiple dictionaries.
    
    Args:
        *dicts: Dictionaries to merge
        deep: Perform deep merge (recursive)
        
    Returns:
        dict: Merged dictionary
    """
    if not deep:
        result = {}
        for d in dicts:
            result.update(d)
        return result
    
    # Deep merge
    result = {}
    for d in dicts:
        for key, value in d.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = merge_dicts(result[key], value, deep=True)
            else:
                result[key] = value
    return result


def parse_bool(value: Any) -> bool:
    """
    Parse various inputs as boolean.
    
    Args:
        value: Value to parse
        
    Returns:
        bool: Parsed boolean value
    """
    if isinstance(value, bool):
        return value
    
    if isinstance(value, str):
        return value.lower() in ("true", "yes", "1", "on", "enabled")
    
    if isinstance(value, (int, float)):
        return value != 0
    
    return bool(value)


def chunk_list(items: list, chunk_size: int) -> list[list]:
    """
    Split list into chunks of specified size.
    
    Args:
        items: List to chunk
        chunk_size: Size of each chunk
        
    Returns:
        list: List of chunks
    """
    return [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)]


def remove_none_values(data: dict) -> dict:
    """
    Remove None values from dictionary.
    
    Args:
        data: Dictionary to clean
        
    Returns:
        dict: Dictionary without None values
    """
    return {k: v for k, v in data.items() if v is not None}
