"""
Complaint Management MCP Server
Main entry point for the FastMCP server
"""

import sys
import signal
import logging
from typing import Dict, Any, Optional
from mcp.server.fastmcp import FastMCP
from colorama import init, Fore, Back, Style

# Initialize colorama for cross-platform colored output
init(autoreset=True)

# Import complaint manager modules
from complaint_manager.database import db
from complaint_manager.config import config
from complaint_manager import tools
from complaint_manager.seed_data import run_seed_if_enabled

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP(
    name=config.SERVER_NAME,
    instructions="MCP server for managing customer complaints related to orders. Supports creating, updating, retrieving, filtering, and deleting complaints.",
    host=config.SERVER_HOST,
    port=config.SERVER_PORT,
)

# Shutdown event flag
shutdown_requested = False


# ============================================================================
# Display Functions
# ============================================================================

def print_banner():
    """Display colorful startup banner"""
    banner = f"""
{Fore.CYAN}{Style.BRIGHT}╔════════════════════════════════════════════════════════════════════════╗
║                                                                        ║
║            {Fore.YELLOW}🚀 COMPLAINT MANAGEMENT MCP SERVER 🚀{Fore.CYAN}                      ║
║                                                                        ║
╚════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
    print(banner)


def print_configuration():
    """Display server configuration in a colorful format"""
    print(f"\n{Fore.GREEN}{Style.BRIGHT}📋 SERVER CONFIGURATION{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'─' * 74}{Style.RESET_ALL}")
    
    config_items = [
        ("Server Name", config.SERVER_NAME, Fore.YELLOW),
        ("Version", config.SERVER_VERSION, Fore.YELLOW),
        ("Host", config.SERVER_HOST, Fore.MAGENTA),
        ("Port", str(config.SERVER_PORT), Fore.MAGENTA),
        ("Endpoint", f"http://{config.SERVER_HOST}:{config.SERVER_PORT}{config.MCP_MOUNT_PATH}", Fore.GREEN),
        ("Database", str(config.get_db_path()), Fore.BLUE),
        ("Auto-Seed Data", "Enabled ✓" if config.SEED_DATABASE else "Disabled ✗", 
         Fore.GREEN if config.SEED_DATABASE else Fore.RED),
    ]
    
    for label, value, color in config_items:
        print(f"  {Fore.WHITE}{label:<20}{Style.RESET_ALL}: {color}{value}{Style.RESET_ALL}")
    
    print(f"{Fore.CYAN}{'─' * 74}{Style.RESET_ALL}")


def print_features():
    """Display available MCP tools and features"""
    print(f"\n{Fore.GREEN}{Style.BRIGHT}✨ AVAILABLE MCP TOOLS{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'─' * 74}{Style.RESET_ALL}")
    
    tools = [
        ("create_complaint", "Create new customer complaints", "🆕"),
        ("get_complaint", "Retrieve complaint by ID", "🔍"),
        ("update_complaint", "Update complaint details", "✏️"),
        ("list_complaints", "List all complaints", "📋"),
        ("filter_complaints", "Filter by status/priority/customer/order", "🔎"),
        ("delete_complaint", "Delete complaint permanently", "🗑️"),
    ]
    
    for name, description, icon in tools:
        print(f"  {icon}  {Fore.YELLOW}{name:<22}{Style.RESET_ALL} → {Fore.WHITE}{description}{Style.RESET_ALL}")
    
    print(f"{Fore.CYAN}{'─' * 74}{Style.RESET_ALL}")


def print_data_model():
    """Display complaint data model and validation rules"""
    print(f"\n{Fore.GREEN}{Style.BRIGHT}📊 DATA MODEL & VALIDATION{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'─' * 74}{Style.RESET_ALL}")
    
    print(f"\n  {Fore.YELLOW}{Style.BRIGHT}Valid Priorities:{Style.RESET_ALL}")
    priorities = {
        "Low": Fore.GREEN,
        "Medium": Fore.YELLOW,
        "High": Fore.LIGHTYELLOW_EX,
        "Critical": Fore.RED
    }
    for priority, color in priorities.items():
        print(f"    • {color}{priority}{Style.RESET_ALL}")
    
    print(f"\n  {Fore.YELLOW}{Style.BRIGHT}Valid Statuses:{Style.RESET_ALL}")
    statuses = {
        "New": Fore.CYAN,
        "Open": Fore.BLUE,
        "In Progress": Fore.YELLOW,
        "Resolved": Fore.GREEN,
        "Closed": Fore.WHITE
    }
    for status, color in statuses.items():
        print(f"    • {color}{status}{Style.RESET_ALL}")
    
    print(f"\n{Fore.CYAN}{'─' * 74}{Style.RESET_ALL}")


def print_startup_complete():
    """Display startup complete message"""
    print(f"\n{Fore.GREEN}{Style.BRIGHT}✅ SERVER STARTED SUCCESSFULLY!{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'─' * 74}{Style.RESET_ALL}")
    print(f"\n  {Fore.WHITE}Press {Fore.RED}{Style.BRIGHT}Ctrl+C{Style.RESET_ALL}{Fore.WHITE} to stop the server gracefully{Style.RESET_ALL}\n")


# ============================================================================
# MCP Tool Definitions
# ============================================================================

@mcp.tool(
    name="create_complaint",
    description="Create a new customer complaint. Automatically sets status to 'New' and records registration timestamp.",
    structured_output=True,
)
def create_complaint_tool(
    description: str,
    customer_name: str,
    order_id: str,
    priority: str = "Medium",
    remarks: str = None
) -> Dict[str, Any]:
    """
    Create a new complaint with automatic ID generation and timestamp
    
    Args:
        description: Detailed description of the complaint
        customer_name: Name of the customer
        order_id: Order ID associated with the complaint
        priority: Priority level - Low, Medium, High, or Critical (default: Medium)
        remarks: Optional additional remarks or notes
    """
    return tools.create_complaint(
        description=description,
        customer_name=customer_name,
        order_id=order_id,
        priority=priority,
        remarks=remarks
    )


@mcp.tool(
    name="get_complaint",
    description="Retrieve a specific complaint by its ID",
    structured_output=True,
)
def get_complaint_tool(complaint_id: int) -> Dict[str, Any]:
    """
    Get detailed information about a specific complaint
    
    Args:
        complaint_id: The unique complaint ID to retrieve
    """
    return tools.get_complaint(complaint_id=complaint_id)


@mcp.tool(
    name="update_complaint",
    description="Update an existing complaint. Can update status, priority, remarks, or description. Automatically updates the 'updated_at' timestamp.",
    structured_output=True,
)
def update_complaint_tool(
    complaint_id: int,
    status: str = None,
    priority: str = None,
    remarks: str = None,
    description: str = None
) -> Dict[str, Any]:
    """
    Update one or more fields of an existing complaint
    
    Args:
        complaint_id: The complaint ID to update
        status: New status - New, Open, In Progress, Resolved, or Closed
        priority: New priority - Low, Medium, High, or Critical
        remarks: Updated remarks or notes
        description: Updated complaint description
    """
    return tools.update_complaint(
        complaint_id=complaint_id,
        status=status,
        priority=priority,
        remarks=remarks,
        description=description
    )


@mcp.tool(
    name="list_complaints",
    description="List all complaints ordered by registration date (newest first)",
    structured_output=True,
)
def list_complaints_tool(limit: int = 100) -> Dict[str, Any]:
    """
    Get a list of all complaints
    
    Args:
        limit: Maximum number of complaints to return (default: 100)
    """
    return tools.list_complaints(limit=limit)


@mcp.tool(
    name="filter_complaints",
    description="Filter complaints by status, priority, customer name, or order ID. Supports multiple filter criteria simultaneously.",
    structured_output=True,
)
def filter_complaints_tool(
    status: str = None,
    priority: str = None,
    customer_name: str = None,
    order_id: str = None,
    limit: int = 100
) -> Dict[str, Any]:
    """
    Filter complaints based on various criteria
    
    Args:
        status: Filter by status - New, Open, In Progress, Resolved, or Closed
        priority: Filter by priority - Low, Medium, High, or Critical
        customer_name: Filter by customer name (partial match supported)
        order_id: Filter by specific order ID
        limit: Maximum number of results to return (default: 100)
    """
    return tools.filter_complaints(
        status=status,
        priority=priority,
        customer_name=customer_name,
        order_id=order_id,
        limit=limit
    )


@mcp.tool(
    name="delete_complaint",
    description="Delete a complaint by its ID. This action cannot be undone.",
    structured_output=True,
)
def delete_complaint_tool(complaint_id: int) -> Dict[str, Any]:
    """
    Permanently delete a complaint
    
    Args:
        complaint_id: The complaint ID to delete
    """
    return tools.delete_complaint(complaint_id=complaint_id)


# ============================================================================
# Signal Handlers
# ============================================================================

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully"""
    global shutdown_requested
    signal_name = signal.Signals(signum).name
    print(f"\n\n{Fore.YELLOW}⚠️  Received {signal_name} signal. Initiating graceful shutdown...{Style.RESET_ALL}")
    shutdown_requested = True
    sys.exit(0)



# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)   # Handle Ctrl+C
    signal.signal(signal.SIGTERM, signal_handler)  # Handle termination signal
    
    try:
        # Display startup banner
        print_banner()
        
        # Initialize database
        logger.info(f"{Fore.YELLOW}⚙️  Initializing database...{Style.RESET_ALL}")
        db.initialize()
        logger.info(f"{Fore.GREEN}✓ Database initialized successfully{Style.RESET_ALL}")
        
        # Seed database if enabled
        logger.info(f"{Fore.YELLOW}⚙️  Checking database seeding configuration...{Style.RESET_ALL}")
        seed_result = run_seed_if_enabled(config.SEED_DATABASE)
        if seed_result.get("seeded"):
            logger.info(f"{Fore.GREEN}✓ {seed_result.get('message')}{Style.RESET_ALL}")
        else:
            logger.info(f"{Fore.BLUE}• {seed_result.get('message')}{Style.RESET_ALL}")
        
        # Display configuration and features
        print_configuration()
        print_features()
        print_data_model()
        print_startup_complete()
        
        # Start the MCP server
        mcp.run(transport="streamable-http", mount_path=config.MCP_MOUNT_PATH)
        
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}⚠️  Keyboard interrupt received. Shutting down gracefully...{Style.RESET_ALL}")
    except Exception as e:
        logger.error(f"{Fore.RED}❌ Server error: {e}{Style.RESET_ALL}", exc_info=True)
        raise
    finally:
        print(f"{Fore.CYAN}👋 Server shutdown complete. Goodbye!{Style.RESET_ALL}\n")