"""
MSAv15Service - Customer Service Agent REST API

Main application entry point for the FastAPI service.
Simple entry point that creates the app and starts the uvicorn server.
"""
import uvicorn

from app.config import settings
from app.core import create_app

# Create FastAPI application
app = create_app()


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.SERVICE_PORT,
        reload=True,
        log_level=settings.LOG_LEVEL.lower()
    )
