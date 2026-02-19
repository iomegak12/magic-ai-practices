"""
Banner Module
=============
Renders the colourful startup banner to stdout using ``colorama`` (ANSI colours)
and ``art`` (ASCII text art).

Public API
----------
    print_banner(config) -> None
"""

from art import text2art
from colorama import Fore, Style, init as colorama_init

colorama_init(autoreset=True)

# ---------------------------------------------------------------------------
# Colour palette
# ---------------------------------------------------------------------------

_BORDER   = Fore.CYAN   + Style.BRIGHT
_TITLE    = Fore.CYAN   + Style.BRIGHT
_LABEL    = Fore.YELLOW + Style.BRIGHT
_VALUE    = Fore.GREEN  + Style.BRIGHT
_DIM      = Fore.WHITE  + Style.DIM
_ACCENT   = Fore.MAGENTA + Style.BRIGHT
_RESET    = Style.RESET_ALL

_WIDTH = 62


def _line(char: str = "─") -> str:
    return _BORDER + char * _WIDTH + _RESET


def _row(label: str, value: str) -> str:
    label_col = f"{_LABEL}{label:<18}{_RESET}"
    value_col = f"{_VALUE}{value}{_RESET}"
    return f"  {label_col} {value_col}"


# ---------------------------------------------------------------------------
# Public
# ---------------------------------------------------------------------------

def print_banner(config) -> None:
    """
    Print the colourful startup banner to stdout.

    Args:
        config: A :class:`src.config.Config` instance.
    """
    # ASCII art — "COMPLAINTS" rendered in block font, coloured cyan
    art_text = text2art("MSEv16", )
    coloured_art = "\n".join(
        _TITLE + line + _RESET for line in art_text.splitlines()
    )

    endpoint = f"http://{config.host}:{config.port}{config.mount_path}"

    print()
    print(_line("═"))
    print(coloured_art)
    print()
    print(
        f"  {_ACCENT}{'Complaint Management MCP Server':^{_WIDTH - 4}}{_RESET}"
    )
    print(
        f"  {_DIM}{'MCP · Streamable HTTP · SQLite · FastMCP':^{_WIDTH - 4}}{_RESET}"
    )
    print()
    print(_line())
    print()
    print(_row("Server Name",   config.server_name))
    print(_row("Version",       config.server_version))
    print(_row("Transport",     "Streamable HTTP"))
    print(_row("Host",          config.host))
    print(_row("Port",          str(config.port)))
    print(_row("MCP Endpoint",  endpoint))
    print()
    print(_line())
    print()
    print(_row("Database",      config.database_path))
    print(_row("Auto-Seed",     f"{'Yes' if config.auto_seed else 'No'} ({config.seed_count} records)"))
    print(_row("Log Level",     config.log_level))
    print()
    print(_line("═"))
    print(
        f"  {_DIM}Press Ctrl+C to stop the server.{_RESET}"
    )
    print()
