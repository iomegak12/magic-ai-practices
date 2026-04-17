"""
FastAPI application factory.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.routers import health, chat
from app.services.seeding_service import seed_database
from .startup import (
    display_welcome_banner,
    display_startup_banner,
    display_startup_complete,
    display_database_seeding_status,
    display_shutdown_message
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    Handles startup and shutdown events.
    """
    # Startup - Display welcome banner first
    display_welcome_banner()
    display_startup_banner()
    
    # Seed database if enabled
    if settings.ORDER_DB_SEEDING_ENABLED:
        seed_database(settings.ORDER_DB_PATH, settings.ORDER_DB_SEED_COUNT)
        display_database_seeding_status(True, settings.ORDER_DB_SEED_COUNT)
    else:
        display_database_seeding_status(False)
    
    display_startup_complete()
    
    yield
    
    # Shutdown
    display_shutdown_message()


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    Returns:
        FastAPI: Configured FastAPI application instance
    """
    # Create FastAPI application
    app = FastAPI(
        title=settings.SERVICE_NAME,
        description="Customer Service Agent REST API - Multi-turn conversational AI for order and complaint management",
        version=settings.SERVICE_VERSION,
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        contact={
            "name": "Ramkumar",
            "email": "ram@example.com"
        },
        license_info={
            "name": "MIT License",
            "url": "https://opensource.org/licenses/MIT"
        }
    )
    
    # CORS Middleware
    origins = settings.CORS_ALLOW_ORIGINS.split(",")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins if origins != ["*"] else ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(health.router, tags=["Health"])
    app.include_router(chat.router, tags=["Chat"])
    
    # Root endpoint
    @app.get("/", tags=["Root"])
    async def root():
        """Root endpoint with service information."""
        return {
            "service": settings.SERVICE_NAME,
            "version": settings.SERVICE_VERSION,
            "status": "running",
            "documentation": f"http://localhost:{settings.SERVICE_PORT}/docs",
            "health": f"http://localhost:{settings.SERVICE_PORT}/health"
        }
    
    return app
