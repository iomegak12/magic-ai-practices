"""
Complaint Management MCP Server — Entry Point
=============================================
Thin orchestration layer. All heavy lifting lives in:

  src/app.py     — FastMCP app factory (create_app)
  src/startup.py — DB init, seeding, signal handlers

Transport : Streamable HTTP
Endpoint  : http://<host>:<port>/mcp

Author  : Ramkumar and Team (Chandini, Priya, Ashok)
Version : 1.0.0
Date    : February 19, 2026
"""

from src.app import create_app
from src.banner import print_banner
from src.config import load_config
from src.startup import register_signal_handlers, run_startup
from src.utils.logger import get_logger

logger = get_logger("complaint-mcp-server")

# Build the FastMCP app (and make it importable by tests / ASGI hosts)
mcp = create_app()
config = load_config()


if __name__ == "__main__":
    register_signal_handlers()

    print_banner(config)

    run_startup()

    logger.info("Server starting — press Ctrl+C to stop.")

    try:
        mcp.run(transport="streamable-http", mount_path=config.mount_path)
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received. Shutting down gracefully.")
    except Exception as exc:
        logger.exception("Unexpected server error: %s", exc)
        raise
    finally:
        logger.info("Server shutdown complete.")
