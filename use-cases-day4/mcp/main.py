"""
Orders & Complaints MCP Server
Main entry point — minimal bootstrap.
"""

import sys
import logging
from pathlib import Path

# Ensure project root is on sys.path
sys.path.insert(0, str(Path(__file__).parent))

from fastmcp import FastMCP
from colorama import init, Fore, Style

from config.settings import settings
from database.connection import init_db
from database.seed import seed_database
from tools import register_tools
from resources import register_resources
from prompts import register_prompts
from middleware.rate_limiter import RateLimiterMiddleware

# Colorama init
init(autoreset=True)

# Console logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


# ── Banner ───────────────────────────────────────────────────────────────

def print_banner():
    banner = f"""
{Fore.CYAN}{Style.BRIGHT}╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║       {Fore.YELLOW}🚀  ORDERS & COMPLAINTS  MCP SERVER  🚀{Fore.CYAN}                      ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
    print(banner)

    config_items = [
        ("Server Name", settings.SERVER_NAME, Fore.YELLOW),
        ("Host", settings.SERVER_HOST, Fore.MAGENTA),
        ("Port", str(settings.SERVER_PORT), Fore.MAGENTA),
        ("Endpoint", f"http://{settings.SERVER_HOST}:{settings.SERVER_PORT}/mcp", Fore.GREEN),
        ("Database", str(settings.get_db_path()), Fore.BLUE),
        ("Auto-Seed", "Enabled ✓" if settings.SEED_ON_STARTUP else "Disabled ✗",
         Fore.GREEN if settings.SEED_ON_STARTUP else Fore.RED),
        ("Rate Limiting", "Enabled ✓" if settings.RATE_LIMIT_ENABLED else "Disabled ✗",
         Fore.GREEN if settings.RATE_LIMIT_ENABLED else Fore.RED),
    ]

    if settings.RATE_LIMIT_ENABLED:
        config_items.append(
            ("  └─ Limit", f"{settings.RATE_LIMIT_MAX_REQUESTS} req / {settings.RATE_LIMIT_WINDOW_SECONDS}s per IP", Fore.CYAN)
        )

    print(f"{Fore.GREEN}{Style.BRIGHT}📋 SERVER CONFIGURATION{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'─' * 70}{Style.RESET_ALL}")
    for label, value, color in config_items:
        print(f"  {Fore.WHITE}{label:<20}{Style.RESET_ALL}: {color}{value}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'─' * 70}{Style.RESET_ALL}")

    tools_list = [
        ("get_orders_by_customer", "Search orders by customer name", "🔍"),
        ("search_orders_by_sku", "Search orders by product SKU", "🔍"),
        ("search_orders_by_status", "Search orders by status", "🔍"),
        ("get_complaints_by_order", "Get complaints for an order", "🔍"),
        ("get_complaints_by_customer", "Get complaints for a customer", "🔍"),
        ("register_complaint", "Register a new complaint", "🆕"),
        ("resolve_complaint", "Resolve a complaint", "✅"),
    ]

    print(f"\n{Fore.GREEN}{Style.BRIGHT}🛠️  REGISTERED TOOLS{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'─' * 70}{Style.RESET_ALL}")
    for name, desc, icon in tools_list:
        print(f"  {icon}  {Fore.YELLOW}{name:<30}{Style.RESET_ALL} → {Fore.WHITE}{desc}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'─' * 70}{Style.RESET_ALL}")

    resources_list = [
        ("orders://summary", "Order totals by status"),
        ("complaints://summary", "Complaint totals by status & priority"),
        ("config://statuses", "All valid system enums"),
        ("orders://recent", "Last 10 orders"),
        ("complaints://unresolved", "Open / In-Progress complaints"),
    ]

    print(f"\n{Fore.GREEN}{Style.BRIGHT}📦 REGISTERED RESOURCES{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'─' * 70}{Style.RESET_ALL}")
    for uri, desc in resources_list:
        print(f"  📄 {Fore.MAGENTA}{uri:<30}{Style.RESET_ALL} → {Fore.WHITE}{desc}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'─' * 70}{Style.RESET_ALL}")

    prompts_list = [
        ("analyze_customer_orders", "Analyze a customer's order history"),
        ("complaint_resolution_guide", "Resolution steps for a complaint"),
        ("escalation_review", "Review high-priority unresolved complaints"),
        ("order_status_inquiry", "Help customer with order statuses"),
    ]

    print(f"\n{Fore.GREEN}{Style.BRIGHT}💬 REGISTERED PROMPTS{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'─' * 70}{Style.RESET_ALL}")
    for name, desc in prompts_list:
        print(f"  💬 {Fore.CYAN}{name:<30}{Style.RESET_ALL} → {Fore.WHITE}{desc}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'─' * 70}{Style.RESET_ALL}\n")


# ── Server setup ─────────────────────────────────────────────────────────

mcp = FastMCP(
    name=settings.SERVER_NAME,
    instructions=(
        "MCP server for managing customer eCommerce orders and their complaints. "
        "Supports querying orders, searching complaints, registering new complaints, "
        "and resolving existing ones."
    ),
)

# Register components
register_tools(mcp)
register_resources(mcp)
register_prompts(mcp)

# Database init & seed
init_db()
if settings.SEED_ON_STARTUP:
    seed_database()


# ── Entry point ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    print_banner()
    logger.info("Starting MCP server …")

    # Apply rate-limiter middleware if enabled
    if settings.RATE_LIMIT_ENABLED:
        original_app = mcp.get_app()
        rate_limited_app = RateLimiterMiddleware(
            original_app,
            enabled=settings.RATE_LIMIT_ENABLED,
            max_requests=settings.RATE_LIMIT_MAX_REQUESTS,
            window_seconds=settings.RATE_LIMIT_WINDOW_SECONDS,
        )
        mcp._app = rate_limited_app

    try:
        mcp.run(
            transport="streamable-http",
            host=settings.SERVER_HOST,
            port=settings.SERVER_PORT,
        )
    except KeyboardInterrupt:
        logger.info("Received shutdown signal — MCP server stopped")
