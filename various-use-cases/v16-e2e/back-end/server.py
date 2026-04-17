"""
MSEv15E2E - Customer Service Agent REST API
Entry Point

This is the entry point that initializes and starts the FastAPI application.
"""

import sys
import logging
import asyncio
from pathlib import Path
from contextlib import asynccontextmanager

# Ensure app directory is in path
sys.path.insert(0, str(Path(__file__).parent))

from fastapi import FastAPI
import uvicorn

from app.config import get_settings
from app.utils import configure_default_logger
from app.startup import (
    display_banner, 
    display_ready_message, 
    display_error_banner, 
    run_all_checks,
    create_shutdown_handler
)
from app.agent import initialize_agent_manager, shutdown_agent_manager
from app.tools.mcp_handler import initialize_mcp_handler, shutdown_mcp_handler
from app.tools.order_management import set_database_path
from app.api import (
    agent_router,
    health_router,
    info_router,
    sessions_router,
    setup_cors_middleware,
    setup_custom_middleware,
    setup_exception_handlers
)

__version__ = "0.1.0"

logger = logging.getLogger(__name__)


def setup_asyncio_exception_handler():
    """
    Setup custom asyncio exception handler to suppress harmless Windows connection errors.
    
    On Windows, when clients disconnect from streaming endpoints, asyncio can raise
    ConnectionResetError in the event loop callback. These are harmless and expected.
    """
    def handle_exception(loop, context):
        exception = context.get("exception")
        
        # Suppress Windows connection errors from streaming disconnects
        if isinstance(exception, (ConnectionResetError, ConnectionAbortedError, BrokenPipeError)):
            # Log at debug level instead of error
            logger.debug(f"Client connection closed: {context.get('message', '')}")
            return
        
        # For other exceptions, use default handling
        loop.default_exception_handler(context)
    
    # Get the current event loop and set the exception handler
    try:
        loop = asyncio.get_event_loop()
        loop.set_exception_handler(handle_exception)
        logger.debug("Custom asyncio exception handler installed")
    except RuntimeError:
        # No event loop in current thread - will be set up later
        pass


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager for startup and shutdown.
    
    Args:
        app: FastAPI application
    """
    # ===== STARTUP =====
    logger.info("=" * 80)
    logger.info("APPLICATION STARTUP")
    logger.info("=" * 80)
    
    # Setup asyncio exception handler for Windows streaming issues
    setup_asyncio_exception_handler()
    
    try:
        settings = get_settings()
        
        # Configure database path for order management
        logger.info(f"Configuring database path: {settings.database_path}")
        set_database_path(str(settings.database_path))
        
        # Initialize MCP handler
        logger.info("Initializing MCP handler...")
        try:
            initialize_mcp_handler()
            logger.info("✓ MCP handler initialized")
        except Exception as e:
            logger.warning(f"MCP initialization failed (continuing without MCP): {str(e)}")
        
        # Initialize agent manager
        logger.info("Initializing agent manager...")
        initialize_agent_manager()
        logger.info("✓ Agent manager initialized")
        
        logger.info("=" * 80)
        logger.info("APPLICATION READY")
        logger.info("=" * 80)
        
    except Exception as e:
        logger.error(f"Startup failed: {str(e)}", exc_info=True)
        raise
    
    # Application is running
    yield
    
    # ===== SHUTDOWN =====
    logger.info("=" * 80)
    logger.info("APPLICATION SHUTDOWN")
    logger.info("=" * 80)
    
    try:
        # Shutdown agent manager
        logger.info("Shutting down agent manager...")
        shutdown_agent_manager()
        logger.info("✓ Agent manager shutdown complete")
        
        # Shutdown MCP handler
        logger.info("Shutting down MCP handler...")
        shutdown_mcp_handler()
        logger.info("✓ MCP handler shutdown complete")
        
    except Exception as e:
        logger.error(f"Shutdown error: {str(e)}", exc_info=True)
    
    logger.info("=" * 80)
    logger.info("SHUTDOWN COMPLETE")
    logger.info("=" * 80)


def create_app() -> FastAPI:
    """
    Create and configure FastAPI application.
    
    Returns:
        FastAPI: Configured application instance
    """
    settings = get_settings()
    
    # Create FastAPI app with enhanced metadata
    app = FastAPI(
        title="Customer Service Agent API",
        description=(
            "## AI-Powered Customer Service REST API\n\n"
            "This API provides an intelligent customer service agent with:\n\n"
            "### 🤖 Core Features\n"
            "- **Conversational AI**: Natural language understanding powered by Azure OpenAI\n"
            "- **Multi-Turn Conversations**: Session-based dialogue management\n"
            "- **Order Management**: Query, track, and modify customer orders\n"
            "- **Email Communication**: Automated customer notifications\n"
            "- **Complaint Tracking**: MCP integration for complaint management\n\n"
            "### 🔧 Technical Capabilities\n"
            "- **Multi-Tenant**: Tenant isolation for session management\n"
            "- **Rate Limiting**: Configurable per-IP request throttling\n"
            "- **Request Tracing**: UUID-based request correlation\n"
            "- **Health Monitoring**: Liveness and readiness probes\n\n"
            "### 📚 Documentation\n"
            "- **Interactive Docs**: Available at `/docs` (Swagger UI)\n"
            "- **Alternative Docs**: Available at `/redoc` (ReDoc)\n"
            "- **OpenAPI Spec**: Available at `/openapi.json`\n\n"
            "### 🚀 Quick Start\n"
            "1. Check service health at `/health`\n"
            "2. Create a session at `/api/v1/agent/sessions`\n"
            "3. Send messages at `/api/v1/agent/messages`\n"
            "4. View session history at `/api/v1/sessions/{id}/history`\n"
        ),
        version=__version__,
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        openapi_tags=[
            {
                "name": "Root",
                "description": "Root endpoint with API information"
            },
            {
                "name": "Health",
                "description": "Health check endpoints for monitoring and orchestration"
            },
            {
                "name": "Agent",
                "description": "Agent conversation endpoints for session and message management"
            },
            {
                "name": "Sessions",
                "description": "Session management endpoints for history and cleanup"
            },
            {
                "name": "Info",
                "description": "API information and tool listing"
            }
        ],
        contact={
            "name": "API Support",
            "email": "support@example.com"
        },
        license_info={
            "name": "MIT License",
            "url": "https://opensource.org/licenses/MIT"
        }
    )
    
    # Setup CORS middleware
    setup_cors_middleware(app)
    
    # Setup custom middleware (rate limiting, logging, error handling)
    setup_custom_middleware(app)
    
    # Setup exception handlers
    setup_exception_handlers(app)
    
    # Register routers
    app.include_router(health_router)
    app.include_router(agent_router)
    app.include_router(info_router)
    app.include_router(sessions_router)
    
    # Root endpoint
    @app.get(
        "/",
        tags=["Root"],
        summary="API Information",
        description="Get basic API information including version and documentation links"
    )
    async def root():
        """
        Root endpoint with API information.
        
        Returns API metadata including:
        - Service name and version
        - Operational status
        - Documentation URL
        - Health check URL
        """
        return {
            "name": "Customer Service Agent API",
            "version": __version__,
            "status": "operational",
            "documentation": "/docs",
            "health": "/health",
            "openapi": "/openapi.json"
        }
    
    logger.info("FastAPI application created and configured")
    
    return app


def main():
    """Main entry point for the application."""
    
    # Load configuration
    try:
        settings = get_settings()
    except Exception as e:
        print(f"\n❌ Failed to load configuration: {e}")
        print("Please check your .env file and try again.\n")
        sys.exit(1)
    
    # Setup logging
    configure_default_logger(settings)
    
    # Setup asyncio exception handler for Windows
    setup_asyncio_exception_handler()
    
    # Setup signal handlers for graceful shutdown
    logger.info("Registering shutdown handlers...")
    shutdown_handler = create_shutdown_handler(logger)
    logger.info("✓ Shutdown handlers registered")
    
    # Display startup banner
    display_banner(__version__, settings, logger)
    
    # Run startup checks
    logger.info("Running startup checks...")
    checks_passed, warnings = run_all_checks(settings, logger)
    
    if not checks_passed:
        display_error_banner("Startup checks failed", logger)
        sys.exit(1)
    
    # Display ready message
    display_ready_message(settings, warnings if warnings else None, logger)
    
    # Create application
    app = create_app()
    
    # Start server
    logger.info(f"Starting Uvicorn server on {settings.api_host}:{settings.api_port}")
    logger.info("=" * 80)
    
    try:
        uvicorn.run(
            app,
            host=settings.api_host,
            port=settings.api_port,
            log_level=settings.log_level.lower(),
            access_log=True
        )
    except KeyboardInterrupt:
        logger.info("Received shutdown signal (CTRL+C)")
    except Exception as e:
        logger.error(f"Server error: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()


