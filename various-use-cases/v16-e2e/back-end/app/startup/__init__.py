"""Startup and Shutdown Handlers"""

from .banner import (
    display_banner,
    display_ready_message,
    display_shutdown_message,
    display_error_banner,
)

from .checks import (
    check_configuration,
    check_azure_openai,
    check_mcp_server,
    check_database,
    check_smtp_configuration,
    run_all_checks,
)

from .shutdown import (
    ShutdownHandler,
    create_shutdown_handler,
    cleanup_sessions,
    close_database_connections,
    stop_background_tasks,
    flush_logs,
)

__all__ = [
    # Banner
    "display_banner",
    "display_ready_message",
    "display_shutdown_message",
    "display_error_banner",
    # Checks
    "check_configuration",
    "check_azure_openai",
    "check_mcp_server",
    "check_database",
    "check_smtp_configuration",
    "run_all_checks",
    # Shutdown
    "ShutdownHandler",
    "create_shutdown_handler",
    "cleanup_sessions",
    "close_database_connections",
    "stop_background_tasks",
    "flush_logs",
]
