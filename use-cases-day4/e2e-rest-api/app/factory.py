"""FastAPI application factory with async lifespan management."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.agent.manager import initialize_manager, shutdown_manager
from app.api.errors import setup_exception_handlers
from app.api.routes.chat import router as chat_router
from app.api.routes.health import router as health_router
from app.config import Settings, get_settings
from app.middleware import setup_middleware
from app.startup import print_startup_banner

logger = logging.getLogger("app")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: print banner, initialise agent.  Shutdown: clean up."""
    settings: Settings = app.state.settings

    print_startup_banner(settings)

    logger.info("Initializing agent …")
    await initialize_manager(settings)
    logger.info("Agent ready — accepting requests")

    yield

    logger.info("Shutting down …")
    await shutdown_manager()
    logger.info("Shutdown complete")


def create_app(settings: Settings | None = None) -> FastAPI:
    """Build and return the configured FastAPI application."""
    settings = settings or get_settings()

    app = FastAPI(
        title=settings.APP_TITLE,
        version=settings.APP_VERSION,
        description=settings.APP_DESCRIPTION,
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        openapi_tags=[
            {"name": "Chat", "description": "Agent chat endpoints (streaming and non-streaming)"},
            {"name": "Health", "description": "Liveness and readiness probes"},
        ],
        contact={
            "name": "Enterprise E2E Team",
        },
        license_info={
            "name": "MIT",
            "url": "https://opensource.org/licenses/MIT",
        },
    )

    # Stash settings on app state for lifespan access
    app.state.settings = settings

    # --- Middleware ---
    setup_middleware(app, settings)

    # --- Exception handlers ---
    setup_exception_handlers(app)

    # --- Routers ---
    app.include_router(chat_router)
    app.include_router(health_router)

    @app.get("/", include_in_schema=False)
    async def root():
        return {
            "name": settings.APP_TITLE,
            "version": settings.APP_VERSION,
            "docs": "/docs",
        }

    return app
