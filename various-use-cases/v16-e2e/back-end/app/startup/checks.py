"""
Startup Checks

Pre-flight checks to ensure all dependencies and services are available.
"""

import logging
from typing import Optional
from pathlib import Path


def check_configuration(settings, logger: Optional[logging.Logger] = None) -> bool:
    """
    Validate configuration settings.
    
    Args:
        settings: Application settings instance
        logger: Logger instance
        
    Returns:
        bool: True if configuration is valid
    """
    if logger:
        logger.info("Checking configuration...")
    
    try:
        # Validate directories
        for path_attr in ["LOG_FILE_PATH", "ORDER_DB_PATH"]:
            path = getattr(settings, path_attr)
            parent_dir = Path(path).parent
            parent_dir.mkdir(parents=True, exist_ok=True)
            if logger:
                logger.debug(f"  ✓ Directory exists: {parent_dir}")
        
        # Validate required fields
        required_fields = [
            "AZURE_AI_PROJECT_ENDPOINT",
            "AZURE_OPENAI_API_KEY",
            "SMTP_SERVER",
            "SENDER_EMAIL",
            "SENDER_PASSWORD",
        ]
        
        for field in required_fields:
            value = getattr(settings, field, None)
            if not value:
                raise ValueError(f"Required field {field} is not set")
        
        if logger:
            logger.info("✓ Configuration valid")
        
        return True
    
    except Exception as e:
        if logger:
            logger.error(f"✗ Configuration check failed: {e}")
        return False


def check_azure_openai(settings, logger: Optional[logging.Logger] = None) -> bool:
    """
    Check Azure OpenAI connectivity.
    
    Args:
        settings: Application settings instance
        logger: Logger instance
        
    Returns:
        bool: True if Azure OpenAI is reachable
    """
    if logger:
        logger.info("Checking Azure OpenAI connectivity...")
    
    try:
        # Basic validation of endpoint format
        endpoint = settings.AZURE_AI_PROJECT_ENDPOINT
        if not endpoint.startswith(("http://", "https://")):
            raise ValueError("Invalid Azure OpenAI endpoint format")
        
        # Note: Actual connectivity check would require Azure SDK
        # For now, just validate configuration
        if logger:
            logger.info(f"  Endpoint: {endpoint}")
            logger.info(f"  Deployment: {settings.AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME}")
            logger.info("✓ Azure OpenAI configuration valid")
        
        return True
    
    except Exception as e:
        if logger:
            logger.warning(f"⚠ Azure OpenAI check incomplete: {e}")
        return False


def check_mcp_server(settings, logger: Optional[logging.Logger] = None) -> tuple[bool, Optional[str]]:
    """
    Check MCP server connectivity.
    
    Args:
        settings: Application settings instance
        logger: Logger instance
        
    Returns:
        tuple: (is_available, error_message)
    """
    if logger:
        logger.info("Checking MCP server connectivity...")
    
    try:
        import httpx
        
        response = httpx.get(
            f"{settings.MCP_SERVER_URL.rstrip('/')}/health",
            timeout=5.0
        )
        
        if response.status_code < 500:
            if logger:
                logger.info(f"✓ MCP server available at {settings.MCP_SERVER_URL}")
            return True, None
        else:
            error = f"MCP server returned status {response.status_code}"
            if logger:
                logger.warning(f"⚠ {error}")
            return False, error
    
    except ImportError:
        if logger:
            logger.warning("⚠ httpx not available, skipping MCP connectivity check")
        return True, None  # Don't fail if httpx not installed
    
    except Exception as e:
        error = f"MCP server unreachable: {str(e)}"
        if logger:
            if settings.MCP_SERVER_REQUIRED:
                logger.error(f"✗ {error}")
            else:
                logger.warning(f"⚠ {error} (service will start anyway)")
        return False, error


def check_database(settings, logger: Optional[logging.Logger] = None) -> bool:
    """
    Check database accessibility.
    
    Args:
        settings: Application settings instance
        logger: Logger instance
        
    Returns:
        bool: True if database is accessible
    """
    if logger:
        logger.info("Checking database...")
    
    try:
        db_path = Path(settings.ORDER_DB_PATH)
        
        # Ensure parent directory exists
        db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Check if database file exists
        if db_path.exists():
            if logger:
                logger.info(f"✓ Database exists: {db_path}")
        else:
            if logger:
                logger.info(f"  Database will be created: {db_path}")
        
        return True
    
    except Exception as e:
        if logger:
            logger.error(f"✗ Database check failed: {e}")
        return False


def check_smtp_configuration(settings, logger: Optional[logging.Logger] = None) -> bool:
    """
    Validate SMTP configuration.
    
    Args:
        settings: Application settings instance
        logger: Logger instance
        
    Returns:
        bool: True if SMTP configuration is valid
    """
    if logger:
        logger.info("Checking SMTP configuration...")
    
    try:
        # Validate SMTP settings
        if not settings.SMTP_SERVER:
            raise ValueError("SMTP_SERVER not configured")
        
        if not settings.SENDER_EMAIL:
            raise ValueError("SENDER_EMAIL not configured")
        
        if not settings.SENDER_PASSWORD:
            raise ValueError("SENDER_PASSWORD not configured")
        
        if logger:
            logger.info(f"  Server: {settings.SMTP_SERVER}:{settings.SMTP_PORT}")
            logger.info(f"  From: {settings.SENDER_NAME} <{settings.SENDER_EMAIL}>")
            logger.info("✓ SMTP configuration valid")
        
        # Note: Actual SMTP connectivity test would require
        # attempting to connect, which we skip for startup speed
        
        return True
    
    except Exception as e:
        if logger:
            logger.warning(f"⚠ SMTP configuration issue: {e}")
        return False


def run_all_checks(settings, logger: Optional[logging.Logger] = None) -> tuple[bool, list[str]]:
    """
    Run all startup checks.
    
    Args:
        settings: Application settings instance
        logger: Logger instance
        
    Returns:
        tuple: (all_passed, warnings)
    """
    warnings = []
    
    if logger:
        logger.info("Running startup checks...")
        logger.info("=" * 60)
    
    # Critical checks (must pass)
    critical_checks = [
        ("Configuration", lambda: check_configuration(settings, logger)),
        ("Database", lambda: check_database(settings, logger)),
    ]
    
    for name, check_func in critical_checks:
        if not check_func():
            return False, [f"Critical check failed: {name}"]
    
    # Non-critical checks (warnings only)
    non_critical_checks = [
        ("Azure OpenAI", lambda: check_azure_openai(settings, logger)),
        ("SMTP Configuration", lambda: check_smtp_configuration(settings, logger)),
    ]
    
    for name, check_func in non_critical_checks:
        if not check_func():
            warnings.append(f"{name} check failed (non-critical)")
    
    # MCP server check (special handling)
    mcp_available, mcp_error = check_mcp_server(settings, logger)
    if not mcp_available:
        if settings.MCP_SERVER_REQUIRED:
            return False, [f"MCP server required but unavailable: {mcp_error}"]
        else:
            warnings.append(f"MCP server unavailable: {mcp_error}")
    
    if logger:
        logger.info("=" * 60)
        if warnings:
            logger.warning(f"Startup checks completed with {len(warnings)} warning(s)")
        else:
            logger.info("✓ All startup checks passed")
    
    return True, warnings
