"""Rich startup banner for the MAGIC-v22-MCP server."""

from __future__ import annotations

from rich import box
from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from magic_v22_mcp.config import Settings

console = Console()


def print_startup_banner(settings: Settings) -> None:
    """Print a colorful startup banner with server info, config, and endpoints."""

    # ── Header ────────────────────────────────────────────────────────────────
    title = Text()
    title.append("⚡ ", style="bold yellow")
    title.append(settings.server_name, style="bold cyan")
    title.append(f"  v{settings.version}", style="dim white")

    subtitle = Text(settings.description, style="italic bright_white")

    header_panel = Panel(
        Text.assemble(title, "\n", subtitle),
        box=box.DOUBLE_EDGE,
        style="bold blue",
        padding=(0, 2),
    )
    console.print(header_panel)

    # ── Configuration table ───────────────────────────────────────────────────
    cfg_table = Table(
        show_header=True,
        header_style="bold magenta",
        box=box.SIMPLE_HEAVY,
        padding=(0, 1),
        title="[bold white]Configuration[/bold white]",
        title_style="bold white",
    )
    cfg_table.add_column("Setting", style="cyan", no_wrap=True)
    cfg_table.add_column("Value", style="bright_white")

    mcp_url = f"http://{settings.mcp_host}:{settings.mcp_port}/mcp"
    cfg_table.add_row("Transport", "Streamable HTTP")
    cfg_table.add_row("Host", settings.mcp_host)
    cfg_table.add_row("Port", str(settings.mcp_port))
    cfg_table.add_row("MCP Endpoint", f"[link={mcp_url}]{mcp_url}[/link]")
    auth_label = "[bold red]DISABLED[/bold red]" if not settings.require_auth else "API Key Bearer"
    cfg_table.add_row("Auth", auth_label)
    cfg_table.add_row("Database", settings.db_path)
    cfg_table.add_row("Log Level", settings.log_level)

    console.print(cfg_table)

    # ── Components table ──────────────────────────────────────────────────────
    comp_table = Table(
        show_header=True,
        header_style="bold magenta",
        box=box.SIMPLE_HEAVY,
        padding=(0, 1),
        title="[bold white]Registered Components[/bold white]",
        title_style="bold white",
    )
    comp_table.add_column("Type", style="yellow", no_wrap=True)
    comp_table.add_column("Name / URI", style="bright_white")
    comp_table.add_column("Description", style="dim white")

    _tools = [
        ("make_order", "Create a new customer order"),
        ("query_orders", "Search orders by customer / SKU"),
        ("get_order_details", "Get order by id"),
        ("register_complaint", "Register a complaint for an order"),
        ("get_complaint_details", "Get complaint by id"),
        ("search_complaints", "Search complaints by multiple filters"),
        ("resolve_complaint", "Resolve a complaint"),
        ("close_complaint", "Close a resolved complaint"),
    ]
    _resources = [
        ("stats://orders-summary", "Aggregated order stats"),
        ("stats://complaints-summary", "Aggregated complaint stats"),
        ("catalog://{kind}", "Enum catalog (4 kinds)"),
        ("complaints://open", "All active complaints"),
    ]
    _prompts = [
        ("complaint_triage", "Triage priority + team for an order's complaints"),
        ("customer_order_summary", "Summarise a customer's order history"),
        ("complaint_resolution_drafter", "Draft a professional resolution note"),
        ("escalation_decision", "Decide whether to escalate / reassign a complaint"),
    ]

    for name, desc in _tools:
        comp_table.add_row("🔧 Tool", name, desc)
    for uri, desc in _resources:
        comp_table.add_row("📦 Resource", uri, desc)
    for name, desc in _prompts:
        comp_table.add_row("💬 Prompt", name, desc)

    console.print(comp_table)

    # ── Connect snippet ───────────────────────────────────────────────────────
    snippet = (
        f"[bold green]# Connect with FastMCP client (Python)[/bold green]\n"
        f"[bright_white]from fastmcp import Client\n"
        f'async with Client("{mcp_url}", headers={{"Authorization": "Bearer <YOUR_JWT>"}}) as c:\n'
        f"    tools = await c.list_tools()"
    )
    console.print(
        Panel(snippet, title="[bold green]Connect Snippet[/bold green]", box=box.ROUNDED, style="green", padding=(0, 2))
    )

    console.print(
        f"\n[bold green]✓ Server is ready.[/bold green]  "
        f"Listening on [bold cyan]{mcp_url}[/bold cyan]\n"
    )
