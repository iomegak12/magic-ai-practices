"""
Configuration Validation Utilities

Additional validation functions for configuration settings.
"""

import os
from pathlib import Path
from typing import Optional


def validate_file_path(path: str, create_if_missing: bool = True) -> bool:
    """
    Validate file path and optionally create parent directory.
    
    Args:
        path: File path to validate
        create_if_missing: Create parent directory if it doesn't exist
        
    Returns:
        bool: True if path is valid
        
    Raises:
        ValueError: If path is invalid
    """
    try:
        file_path = Path(path)
        parent_dir = file_path.parent
        
        if not parent_dir.exists():
            if create_if_missing:
                parent_dir.mkdir(parents=True, exist_ok=True)
            else:
                raise ValueError(f"Parent directory does not exist: {parent_dir}")
        
        # Check if parent directory is writable
        if not os.access(parent_dir, os.W_OK):
            raise ValueError(f"Parent directory is not writable: {parent_dir}")
        
        return True
    except Exception as e:
        raise ValueError(f"Invalid file path '{path}': {str(e)}")


def validate_directory(path: str, create_if_missing: bool = True) -> bool:
    """
    Validate directory path and optionally create it.
    
    Args:
        path: Directory path to validate
        create_if_missing: Create directory if it doesn't exist
        
    Returns:
        bool: True if directory is valid
        
    Raises:
        ValueError: If directory is invalid
    """
    try:
        dir_path = Path(path)
        
        if not dir_path.exists():
            if create_if_missing:
                dir_path.mkdir(parents=True, exist_ok=True)
            else:
                raise ValueError(f"Directory does not exist: {dir_path}")
        
        # Check if directory is writable
        if not os.access(dir_path, os.W_OK):
            raise ValueError(f"Directory is not writable: {dir_path}")
        
        return True
    except Exception as e:
        raise ValueError(f"Invalid directory '{path}': {str(e)}")


def validate_port(port: int) -> bool:
    """
    Validate port number.
    
    Args:
        port: Port number to validate
        
    Returns:
        bool: True if port is valid
        
    Raises:
        ValueError: If port is invalid
    """
    if not isinstance(port, int):
        raise ValueError(f"Port must be an integer, got {type(port)}")
    
    if port < 1024 or port > 65535:
        raise ValueError(f"Port must be between 1024 and 65535, got {port}")
    
    return True


def validate_url_reachable(url: str, timeout: float = 5.0) -> tuple[bool, Optional[str]]:
    """
    Check if a URL is reachable (optional, requires httpx).
    
    Args:
        url: URL to check
        timeout: Request timeout in seconds
        
    Returns:
        tuple: (is_reachable, error_message)
    """
    try:
        import httpx
        response = httpx.get(url, timeout=timeout)
        if response.status_code < 500:
            return True, None
        return False, f"Server returned status {response.status_code}"
    except ImportError:
        # httpx not available, skip check
        return True, None
    except Exception as e:
        return False, str(e)


def validate_environment(settings) -> list[str]:
    """
    Validate complete environment configuration.
    
    Args:
        settings: Settings instance to validate
        
    Returns:
        list: List of warning messages (empty if all OK)
    """
    warnings = []
    
    # Validate directories
    try:
        validate_directory(Path(settings.LOG_FILE_PATH).parent, create_if_missing=True)
    except ValueError as e:
        warnings.append(f"Log directory issue: {e}")
    
    try:
        validate_directory(Path(settings.ORDER_DB_PATH).parent, create_if_missing=True)
    except ValueError as e:
        warnings.append(f"Database directory issue: {e}")
    
    # Check MCP server (if required)
    if settings.MCP_SERVER_REQUIRED:
        reachable, error = validate_url_reachable(settings.MCP_SERVER_URL)
        if not reachable:
            warnings.append(f"MCP server unreachable: {error}")
    
    # Validate rate limiting settings
    if settings.ENABLE_RATE_LIMITING and settings.RATE_LIMIT_PER_MINUTE < 10:
        warnings.append("Rate limit is very restrictive (< 10 requests/min)")
    
    # Check log file size settings
    if settings.LOG_MAX_SIZE_MB < 10:
        warnings.append("Log file size is very small (< 10 MB)")
    
    return warnings
