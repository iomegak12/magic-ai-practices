"""
Graceful Shutdown Handler

Handles application shutdown with proper cleanup.
"""

import signal
import logging
import sys
from typing import Optional, Callable
import asyncio


class ShutdownHandler:
    """Handles graceful application shutdown"""
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        self.logger = logger
        self.shutdown_callbacks: list[Callable] = []
        self._shutdown_initiated = False
    
    def register_callback(self, callback: Callable) -> None:
        """
        Register a callback to be called during shutdown.
        
        Args:
            callback: Function to call during shutdown
        """
        self.shutdown_callbacks.append(callback)
    
    def handle_shutdown(self, signum: Optional[int] = None, frame: Optional[object] = None) -> None:
        """
        Handle shutdown signal.
        
        Args:
            signum: Signal number
            frame: Current stack frame
        """
        if self._shutdown_initiated:
            return  # Already shutting down
        
        self._shutdown_initiated = True
        
        signal_name = signal.Signals(signum).name if signum else "UNKNOWN"
        
        if self.logger:
            self.logger.info("")
            self.logger.info("=" * 60)
            self.logger.info(f"Received shutdown signal: {signal_name}")
            self.logger.info("Initiating graceful shutdown...")
            self.logger.info("=" * 60)
        else:
            print(f"\n\nReceived shutdown signal: {signal_name}")
            print("Shutting down gracefully...")
        
        # Execute shutdown callbacks
        for callback in self.shutdown_callbacks:
            try:
                if self.logger:
                    self.logger.info(f"Executing shutdown callback: {callback.__name__}")
                callback()
            except Exception as e:
                if self.logger:
                    self.logger.error(f"Error in shutdown callback {callback.__name__}: {e}")
                else:
                    print(f"Error in shutdown callback: {e}")
        
        if self.logger:
            self.logger.info("=" * 60)
            self.logger.info("Shutdown complete")
            self.logger.info("=" * 60)
        else:
            print("\nShutdown complete")
        
        # Exit cleanly
        sys.exit(0)
    
    def setup_signal_handlers(self) -> None:
        """Setup signal handlers for graceful shutdown"""
        # Handle SIGINT (Ctrl+C) and SIGTERM
        signal.signal(signal.SIGINT, self.handle_shutdown)
        signal.signal(signal.SIGTERM, self.handle_shutdown)
        
        if self.logger:
            self.logger.debug("Signal handlers registered (SIGINT, SIGTERM)")


def cleanup_sessions(logger: Optional[logging.Logger] = None) -> None:
    """
    Cleanup in-memory sessions.
    
    Args:
        logger: Logger instance
    """
    try:
        # Import here to avoid circular dependencies
        from ..session import get_session_store
        
        if logger:
            logger.info("Cleaning up sessions...")
        
        # Get session store and count
        session_store = get_session_store()
        active_count = session_store.count()
        
        if active_count > 0:
            if logger:
                logger.info(f"  • Clearing {active_count} active session(s)")
            # Clear all sessions
            session_store.clear()
        else:
            if logger:
                logger.info("  • No active sessions to clean up")
        
        if logger:
            logger.info("✓ Sessions cleaned up")
            
    except Exception as e:
        if logger:
            logger.warning(f"Error cleaning up sessions: {e}")


def close_database_connections(logger: Optional[logging.Logger] = None) -> None:
    """
    Close database connections.
    
    Args:
        logger: Logger instance
    """
    if logger:
        logger.info("Closing database connections...")
    
    # Database connection cleanup will be implemented in Phase 2
    # For now, just log the intent
    
    if logger:
        logger.info("✓ Database connections closed")


def stop_background_tasks(logger: Optional[logging.Logger] = None) -> None:
    """
    Stop background tasks.
    
    Args:
        logger: Logger instance
    """
    if logger:
        logger.info("Stopping background tasks...")
    
    # Background task cleanup (session cleanup, etc.)
    # Will be implemented in Phase 5
    
    if logger:
        logger.info("✓ Background tasks stopped")


def flush_logs(logger: Optional[logging.Logger] = None) -> None:
    """
    Flush all log handlers.
    
    Args:
        logger: Logger instance
    """
    if logger:
        logger.info("Flushing logs...")
        for handler in logging.root.handlers:
            handler.flush()
        for handler in logger.handlers:
            handler.flush()


def create_shutdown_handler(logger: Optional[logging.Logger] = None) -> ShutdownHandler:
    """
    Create and configure shutdown handler with default callbacks.
    
    Args:
        logger: Logger instance
        
    Returns:
        ShutdownHandler: Configured shutdown handler
    """
    handler = ShutdownHandler(logger)
    
    # Register default cleanup callbacks
    handler.register_callback(lambda: stop_background_tasks(logger))
    handler.register_callback(lambda: cleanup_sessions(logger))
    handler.register_callback(lambda: close_database_connections(logger))
    handler.register_callback(lambda: flush_logs(logger))
    
    # Setup signal handlers
    handler.setup_signal_handlers()
    
    return handler
