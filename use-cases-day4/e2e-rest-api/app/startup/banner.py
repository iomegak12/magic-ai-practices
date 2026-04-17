"""Colorama-based startup banner displaying server configuration."""

from colorama import Fore, Style, init

from app.config import Settings

init(autoreset=True)

_BANNER = r"""
  ╔══════════════════════════════════════════════════════════════╗
  ║           Enterprise E2E Use Case — REST API                ║
  ║         Microsoft Agent Framework · FastAPI · MCP           ║
  ╚══════════════════════════════════════════════════════════════╝
"""


def _status(enabled: bool) -> str:
    """Return a coloured Enabled/Disabled label."""
    if enabled:
        return f"{Fore.GREEN}Enabled{Style.RESET_ALL}"
    return f"{Fore.RED}Disabled{Style.RESET_ALL}"


def _masked(value: str, visible: int = 8) -> str:
    """Mask a secret, showing only the first `visible` characters."""
    if not value:
        return f"{Fore.RED}(not set){Style.RESET_ALL}"
    if len(value) <= visible:
        return value
    return value[:visible] + "****"


def print_startup_banner(settings: Settings) -> None:
    """Print the server configuration banner to the console."""
    print(f"{Fore.CYAN}{Style.BRIGHT}{_BANNER}{Style.RESET_ALL}")

    print(f"  {Fore.YELLOW}{Style.BRIGHT}Server{Style.RESET_ALL}")
    print(f"    Host            : {Fore.WHITE}{settings.SERVER_HOST}{Style.RESET_ALL}")
    print(f"    Port            : {Fore.WHITE}{settings.SERVER_PORT}{Style.RESET_ALL}")
    print(f"    Log Level       : {Fore.WHITE}{settings.LOG_LEVEL}{Style.RESET_ALL}")
    print(f"    Version         : {Fore.WHITE}{settings.APP_VERSION}{Style.RESET_ALL}")
    print()

    print(f"  {Fore.YELLOW}{Style.BRIGHT}Azure OpenAI{Style.RESET_ALL}")
    print(f"    Endpoint        : {Fore.WHITE}{settings.AZURE_OPENAI_ENDPOINT or '(not set)'}{Style.RESET_ALL}")
    print(f"    Deployment      : {Fore.WHITE}{settings.AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME or '(not set)'}{Style.RESET_ALL}")
    print(f"    API Key         : {Fore.WHITE}{_masked(settings.AZURE_OPENAI_API_KEY)}{Style.RESET_ALL}")
    print(f"    Auth Method     : {Fore.WHITE}{settings.AZURE_AUTH_METHOD}{Style.RESET_ALL}")
    print()

    print(f"  {Fore.YELLOW}{Style.BRIGHT}MCP Servers{Style.RESET_ALL}")
    print(f"    Orders & Comp.  : {Fore.WHITE}{settings.MCP_ORDERS_URL}{Style.RESET_ALL}")
    print(f"    Microsoft Learn : {Fore.WHITE}{settings.MCP_LEARN_URL}{Style.RESET_ALL}")
    print()

    print(f"  {Fore.YELLOW}{Style.BRIGHT}Features{Style.RESET_ALL}")
    print(f"    CORS            : {_status(settings.ENABLE_CORS)}")
    print(f"    Rate Limiting   : {_status(settings.ENABLE_RATE_LIMITING)}", end="")
    if settings.ENABLE_RATE_LIMITING:
        print(f"  ({settings.RATE_LIMIT_PER_MINUTE} req/min)")
    else:
        print()
    print(f"    Observability   : {_status(settings.ENABLE_OBSERVABILITY)}")
    print()

    print(f"  {Fore.YELLOW}{Style.BRIGHT}Storage{Style.RESET_ALL}")
    print(f"    SQLite DB       : {Fore.WHITE}{settings.DB_PATH}{Style.RESET_ALL}")
    print()

    print(
        f"  {Fore.GREEN}{Style.BRIGHT}Swagger UI  →  "
        f"http://{settings.SERVER_HOST}:{settings.SERVER_PORT}/docs{Style.RESET_ALL}"
    )
    print(
        f"  {Fore.GREEN}{Style.BRIGHT}ReDoc       →  "
        f"http://{settings.SERVER_HOST}:{settings.SERVER_PORT}/redoc{Style.RESET_ALL}"
    )
    print()
