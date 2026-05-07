"""MAGIC-v22-MCP server entry point."""

from __future__ import annotations

import logging
import sys

from fastmcp import FastMCP

from magic_v22_mcp.auth import build_auth_provider
from magic_v22_mcp.config import get_settings
from magic_v22_mcp.console import print_startup_banner
from magic_v22_mcp.db import init_db
from magic_v22_mcp.mcp.prompts import register_prompts
from magic_v22_mcp.mcp.resources import register_resources
from magic_v22_mcp.mcp.tools import register_tools
from magic_v22_mcp.seed import run_seed


def _configure_logging(level: str) -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s  %(levelname)-8s  %(name)s — %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        stream=sys.stdout,
        force=True,
    )


def main() -> None:
    settings = get_settings()

    # Logging — console only, no JSON, no file
    _configure_logging(settings.log_level)
    logger = logging.getLogger(__name__)

    # Database bootstrap + seed
    logger.info("Initialising database at %s …", settings.db_path)
    init_db()
    run_seed()

    # Build FastMCP server
    auth = build_auth_provider() if settings.require_auth else None
    if not settings.require_auth:
        logger.warning("Auth is DISABLED (REQUIRE_AUTH=false). Do not expose this server publicly.")
    mcp = FastMCP(
        name=settings.server_name,
        instructions=settings.description,
        auth=auth,
    )

    # Register MCP surface
    register_tools(mcp)
    register_resources(mcp)
    register_prompts(mcp)

    # Startup banner (printed before blocking mcp.run())
    print_startup_banner(settings)

    # Run the server — catch Ctrl+C for a clean exit
    try:
        mcp.run(
            transport="http",
            host=settings.mcp_host,
            port=settings.mcp_port,
            path="/mcp",
        )
    except KeyboardInterrupt:
        logger.info("Server stopped.")


if __name__ == "__main__":
    main()
