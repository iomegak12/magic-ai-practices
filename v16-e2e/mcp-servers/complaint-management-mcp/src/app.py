"""
App Factory
===========
Creates and returns the configured FastMCP application instance
with all 6 complaint-management tools registered.

Keeping this separate from the entry point means the ``mcp`` object
can be imported cleanly by tests, worker processes, or ASGI servers
without triggering the ``__main__`` startup sequence.
"""

from mcp.server.fastmcp import FastMCP

from src.config import load_config
from src.tools import register_all_tools
from src.utils.logger import get_logger

logger = get_logger(__name__)


def create_app() -> FastMCP:
    """
    Build and return a fully configured :class:`FastMCP` instance.

    Steps:
    1. Load & validate configuration from environment / .env file.
    2. Instantiate :class:`FastMCP` with server metadata and network settings.
    3. Register all 6 MCP tools via :func:`register_all_tools`.

    Returns:
        A ready-to-run :class:`FastMCP` application.
    """
    config = load_config()

    logger.info(
        "Creating FastMCP app — name=%s host=%s port=%s",
        config.server_name, config.host, config.port,
    )

    mcp = FastMCP(
        name=config.server_name,
        instructions=(
            "You are a complaint management assistant. "
            "Use the available tools to register, retrieve, search, resolve, "
            "update, and archive customer complaints related to orders."
        ),
        host=config.host,
        port=config.port,
    )

    register_all_tools(mcp)
    logger.info("All 6 tools registered on FastMCP instance.")

    return mcp
