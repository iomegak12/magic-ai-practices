"""
Startup Banner Display

Displays an informative startup banner with configuration and service status.
"""

import logging
from typing import Optional


def display_banner(
    version: str,
    settings,
    logger: Optional[logging.Logger] = None
) -> None:
    """
    Display startup banner with application info.
    
    Args:
        version: Application version
        settings: Application settings instance
        logger: Logger instance (optional)
    """
    banner_lines = [
        "",
        "=" * 80,
        "  __  __  ____  _____       __ ____  ______ ___  ______ ",
        " |  \\/  |/ ___|| ____|_   _/_ | ___||  ____/ _ \\|  ____|",
        " | |\\/| |\\___ \\|  _| \\ \\ / / |___ \\| |__ | | | | |__   ",
        " | |  | | ___) | |___ \\ V /  |___) |  __|| |_| |  __|  ",
        " |_|  |_||____/|_____|  \\_/  |____/|_____\\___/|_____|  ",
        "",
        "  Customer Service Agent REST API",
        "=" * 80,
        "",
        f"  Version:        {version}",
        f"  Server:         {settings.SERVER_HOST}:{settings.SERVER_PORT}",
        f"  Log Level:      {settings.LOG_LEVEL}",
        "",
        "  🤖 AI Agent Configuration:",
        f"    • Model:            {settings.AGENT_MODEL}",
        f"    • Max Turns:        {settings.AGENT_MAX_TURNS}",
        f"    • Timeout:          {settings.AGENT_TIMEOUT_SECONDS}s",
        "",
        "  🔧 Feature Flags:",
        f"    • CORS:             {'✓ Enabled' if settings.ENABLE_CORS else '✗ Disabled'}",
        f"    • Rate Limiting:    {'✓ Enabled' if settings.ENABLE_RATE_LIMITING else '✗ Disabled'}",
    ]
    
    # Add rate limiting details if enabled
    if settings.ENABLE_RATE_LIMITING:
        banner_lines.append(f"      ├─ Limit:         {settings.RATE_LIMIT_PER_MINUTE} requests/minute")
    
    banner_lines.extend([
        f"    • File Logging:     {'✓ Enabled' if settings.LOG_TO_FILE else '✗ Disabled'}",
    ])
    
    # Add log file path if enabled
    if settings.LOG_TO_FILE:
        banner_lines.append(f"      ├─ Log File:      {settings.LOG_FILE_PATH}")
    
    banner_lines.extend([
        f"    • Session Cleanup:  {'✓ Enabled' if settings.SESSION_CLEANUP_ENABLED else '✗ Disabled'}",
    ])
    
    # Add session cleanup interval if enabled
    if settings.SESSION_CLEANUP_ENABLED:
        banner_lines.append(f"      ├─ Interval:      {settings.SESSION_CLEANUP_INTERVAL_MINUTES}m")
        banner_lines.append(f"      └─ Max Age:       {settings.SESSION_MAX_AGE_HOURS}h")
    
    banner_lines.extend([
        "",
        "  🔗 External Services:",
        f"    • Azure OpenAI:     {settings.AZURE_AI_PROJECT_ENDPOINT}",
        f"    • MCP Server:       {settings.MCP_SERVER_URL}",
        f"    • SMTP Server:      {settings.SMTP_SERVER}:{settings.SMTP_PORT}",
        "",
        "  📡 API Endpoints:",
        f"    • Documentation:    http://{settings.SERVER_HOST}:{settings.SERVER_PORT}/docs",
        f"    • ReDoc:            http://{settings.SERVER_HOST}:{settings.SERVER_PORT}/redoc",
        f"    • Health Check:     http://{settings.SERVER_HOST}:{settings.SERVER_PORT}/health",
        f"    • Chat API:         http://{settings.SERVER_HOST}:{settings.SERVER_PORT}/api/v1/chat",
        f"    • Sessions API:     http://{settings.SERVER_HOST}:{settings.SERVER_PORT}/api/v1/sessions",
        "",
        "=" * 80,
        "  Status: Starting up...",
        "=" * 80,
        "",
    ])
    
    banner_text = "\n".join(banner_lines)
    
    if logger:
        for line in banner_lines:
            if line:  # Don't log empty lines
                logger.info(line)
    else:
        print(banner_text)


def display_ready_message(
    settings,
    warnings: list[str] = None,
    logger: Optional[logging.Logger] = None
) -> None:
    """
    Display ready message after successful startup.
    
    Args:
        settings: Application settings instance
        warnings: List of warning messages
        logger: Logger instance (optional)
    """
    messages = [
        "",
        "=" * 80,
        "  🚀 SERVER READY AND LISTENING",
        "=" * 80,
        f"  Base URL:      http://{settings.SERVER_HOST}:{settings.SERVER_PORT}",
        f"  Docs (Swagger): http://{settings.SERVER_HOST}:{settings.SERVER_PORT}/docs",
        f"  Docs (ReDoc):  http://{settings.SERVER_HOST}:{settings.SERVER_PORT}/redoc",
        "",
    ]
    
    if warnings:
        messages.append("  ⚠️  WARNINGS:")
        for warning in warnings:
            messages.append(f"    • {warning}")
        messages.append("")
    else:
        messages.append("  ✓ All systems operational")
        messages.append("")
    
    messages.extend([
        "  💡 Quick Start:",
        "    1. Visit /docs for interactive API documentation",
        "    2. Check /health for service health status",
        "    3. Use /api/v1/chat to interact with the agent",
        "",
        "  🛑 To stop server: Press CTRL+C",
        "=" * 80,
        "",
    ])
    
    if logger:
        for msg in messages:
            if msg:
                logger.info(msg)
    else:
        print("\n".join(messages))


def display_shutdown_message(logger: Optional[logging.Logger] = None) -> None:
    """
    Display shutdown message.
    
    Args:
        logger: Logger instance (optional)
    """
    messages = [
        "",
        "=" * 80,
        "  Shutting down gracefully...",
        "=" * 80,
        "",
    ]
    
    if logger:
        for msg in messages:
            if msg:
                logger.info(msg)
    else:
        print("\n".join(messages))


def display_error_banner(error: str, logger: Optional[logging.Logger] = None) -> None:
    """
    Display error banner for startup failures.
    
    Args:
        error: Error message
        logger: Logger instance (optional)
    """
    messages = [
        "",
        "=" * 80,
        "  ❌ STARTUP FAILED",
        "=" * 80,
        f"  Error: {error}",
        "",
        "  Please check your configuration and try again.",
        "=" * 80,
        "",
    ]
    
    if logger:
        for msg in messages:
            if msg:
                logger.error(msg)
    else:
        print("\n".join(messages))
