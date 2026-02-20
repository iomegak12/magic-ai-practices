"""
Startup and shutdown utilities with colored console output.
"""
from colorama import Fore, Style, init
from art import text2art
from app.config import settings

# Initialize colorama
init(autoreset=True)


def display_welcome_banner():
    """
    Display ASCII art welcome banner.
    """
    print("\n")
    # Create ASCII art for the service name
    ascii_art = text2art("MSAv15", font="small")
    
    # Print the ASCII art in cyan
    for line in ascii_art.split('\n'):
        print(Fore.CYAN + Style.BRIGHT + line.center(80) + Style.RESET_ALL)
    
    # Subtitle
    subtitle = "Customer Service Agent REST API"
    print(Fore.GREEN + Style.BRIGHT + subtitle.center(80) + Style.RESET_ALL)
    
    # Decorative line
    print(Fore.YELLOW + "─" * 80 + Style.RESET_ALL)
    print()


def display_startup_banner():
    """
    Display colorful startup banner with service information.
    """
    banner_width = 80
    
    print("\n" + Fore.CYAN + "=" * banner_width)
    print(Fore.GREEN + Style.BRIGHT + f"🚀 {settings.SERVICE_NAME} v{settings.SERVICE_VERSION}".center(banner_width))
    print(Fore.CYAN + "=" * banner_width + Style.RESET_ALL)
    
    # Configuration Information
    print(f"\n{Fore.YELLOW}📋 Configuration:{Style.RESET_ALL}")
    print(f"   {Fore.WHITE}├─ Service Name:{Style.RESET_ALL} {Fore.CYAN}{settings.SERVICE_NAME}{Style.RESET_ALL}")
    print(f"   {Fore.WHITE}├─ Version:{Style.RESET_ALL} {Fore.CYAN}{settings.SERVICE_VERSION}{Style.RESET_ALL}")
    print(f"   {Fore.WHITE}├─ Port:{Style.RESET_ALL} {Fore.CYAN}{settings.SERVICE_PORT}{Style.RESET_ALL}")
    print(f"   {Fore.WHITE}├─ Log Level:{Style.RESET_ALL} {Fore.CYAN}{settings.LOG_LEVEL}{Style.RESET_ALL}")
    print(f"   {Fore.WHITE}├─ CORS Origins:{Style.RESET_ALL} {Fore.CYAN}{settings.CORS_ALLOW_ORIGINS}{Style.RESET_ALL}")
    print(f"   {Fore.WHITE}└─ Database:{Style.RESET_ALL} {Fore.CYAN}{settings.ORDER_DB_PATH}{Style.RESET_ALL}")
    
    # Azure OpenAI Configuration
    print(f"\n{Fore.YELLOW}☁️  Azure OpenAI:{Style.RESET_ALL}")
    print(f"   {Fore.WHITE}├─ Endpoint:{Style.RESET_ALL} {Fore.CYAN}{settings.AZURE_AI_PROJECT_ENDPOINT}{Style.RESET_ALL}")
    print(f"   {Fore.WHITE}└─ Deployment:{Style.RESET_ALL} {Fore.CYAN}{settings.AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME}{Style.RESET_ALL}")
    
    # MCP Server Configuration
    print(f"\n{Fore.YELLOW}🔌 MCP Server:{Style.RESET_ALL}")
    print(f"   {Fore.WHITE}└─ URL:{Style.RESET_ALL} {Fore.CYAN}{settings.MCP_COMPLAINT_SERVER_URL}{Style.RESET_ALL}")
    
    # Rate Limiting Configuration
    if settings.RATE_LIMITING_ENABLED:
        print(f"\n{Fore.YELLOW}⚡ Rate Limiting:{Style.RESET_ALL}")
        print(f"   {Fore.WHITE}└─ Limit:{Style.RESET_ALL} {Fore.CYAN}{settings.RATE_LIMIT_REQUESTS_PER_MINUTE} requests/min{Style.RESET_ALL}")


def display_startup_complete():
    """
    Display service ready message with endpoints.
    """
    print(f"\n{Fore.GREEN}✅ {settings.SERVICE_NAME} is ready!{Style.RESET_ALL}")
    print(f"\n{Fore.YELLOW}📍 Endpoints:{Style.RESET_ALL}")
    print(f"   {Fore.WHITE}├─ Root:{Style.RESET_ALL} {Fore.BLUE}http://localhost:{settings.SERVICE_PORT}/{Style.RESET_ALL}")
    print(f"   {Fore.WHITE}├─ Health:{Style.RESET_ALL} {Fore.BLUE}http://localhost:{settings.SERVICE_PORT}/health{Style.RESET_ALL}")
    print(f"   {Fore.WHITE}├─ Chat:{Style.RESET_ALL} {Fore.BLUE}http://localhost:{settings.SERVICE_PORT}/chat{Style.RESET_ALL}")
    print(f"   {Fore.WHITE}├─ API Docs:{Style.RESET_ALL} {Fore.BLUE}http://localhost:{settings.SERVICE_PORT}/docs{Style.RESET_ALL}")
    print(f"   {Fore.WHITE}└─ ReDoc:{Style.RESET_ALL} {Fore.BLUE}http://localhost:{settings.SERVICE_PORT}/redoc{Style.RESET_ALL}")
    print(Fore.CYAN + "=" * 80 + Style.RESET_ALL + "\n")


def display_database_seeding_status(enabled: bool, count: int = 0):
    """
    Display database seeding status.
    
    Args:
        enabled: Whether database seeding is enabled
        count: Number of records seeded
    """
    if enabled:
        print(f"\n{Fore.GREEN}🌱 Database Seeding:{Style.RESET_ALL}")
        print(f"   {Fore.WHITE}└─ Seeded {Fore.CYAN}{count}{Fore.WHITE} sample orders{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.YELLOW}ℹ️  Database seeding is disabled{Style.RESET_ALL}")


def display_shutdown_message():
    """
    Display shutdown message.
    """
    print(f"\n{Fore.YELLOW}👋 Shutting down {settings.SERVICE_NAME}...{Style.RESET_ALL}")
    print(f"{Fore.GREEN}✨ Service stopped gracefully{Style.RESET_ALL}\n")
