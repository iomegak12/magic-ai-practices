"""
Logging System Configuration

This module provides comprehensive logging setup with console and file handlers,
structured formatting, and log rotation support.
"""

import logging
import sys
from pathlib import Path
from typing import Optional
from logging.handlers import RotatingFileHandler
from datetime import datetime


# ANSI color codes for console output
class LogColors:
    """ANSI color codes for terminal output"""
    RESET = "\033[0m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    BOLD = "\033[1m"
    DIM = "\033[2m"


class ColoredFormatter(logging.Formatter):
    """Custom formatter with color support for console output"""
    
    LEVEL_COLORS = {
        logging.DEBUG: LogColors.CYAN,
        logging.INFO: LogColors.GREEN,
        logging.WARNING: LogColors.YELLOW,
        logging.ERROR: LogColors.RED,
        logging.CRITICAL: LogColors.RED + LogColors.BOLD,
    }
    
    def __init__(self, include_timestamp: bool = True):
        self.include_timestamp = include_timestamp
        super().__init__()
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record with colors"""
        # Get color for level
        level_color = self.LEVEL_COLORS.get(record.levelno, LogColors.WHITE)
        
        # Format timestamp
        timestamp = ""
        if self.include_timestamp:
            timestamp = f"{LogColors.DIM}[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]{LogColors.RESET} "
        
        # Format level
        level = f"{level_color}[{record.levelname:8}]{LogColors.RESET}"
        
        # Format module/function
        location = f"{LogColors.DIM}[{record.name}]{LogColors.RESET}"
        
        # Format message
        message = record.getMessage()
        
        # Combine
        formatted = f"{timestamp}{level} {location} {message}"
        
        # Add exception info if present
        if record.exc_info:
            formatted += "\n" + self.formatException(record.exc_info)
        
        return formatted


class StructuredFormatter(logging.Formatter):
    """Structured formatter for file output (JSON-like)"""
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as structured text"""
        timestamp = datetime.fromtimestamp(record.created).isoformat()
        
        log_data = {
            "timestamp": timestamp,
            "level": record.levelname,
            "module": record.name,
            "function": record.funcName,
            "line": record.lineno,
            "message": record.getMessage(),
        }
        
        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        # Add extra fields if present
        if hasattr(record, "session_id"):
            log_data["session_id"] = record.session_id
        if hasattr(record, "tenant_id"):
            log_data["tenant_id"] = record.tenant_id
        if hasattr(record, "request_id"):
            log_data["request_id"] = record.request_id
        
        # Format as key=value pairs
        parts = [f"{k}={repr(v)}" for k, v in log_data.items()]
        return " | ".join(parts)


def setup_logger(
    name: str,
    level: str = "INFO",
    log_file: Optional[str] = None,
    max_bytes: int = 100 * 1024 * 1024,  # 100 MB
    backup_count: int = 5,
    enable_console: bool = True,
    enable_file: bool = True,
) -> logging.Logger:
    """
    Setup logger with console and/or file handlers.
    
    Args:
        name: Logger name
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to log file (required if enable_file is True)
        max_bytes: Maximum log file size before rotation
        backup_count: Number of backup files to keep
        enable_console: Enable console output
        enable_file: Enable file output
        
    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    # Remove existing handlers to avoid duplicates
    logger.handlers.clear()
    
    # Console handler
    if enable_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(ColoredFormatter(include_timestamp=True))
        logger.addHandler(console_handler)
    
    # File handler with rotation
    if enable_file and log_file:
        # Ensure log directory exists
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8"
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(StructuredFormatter())
        logger.addHandler(file_handler)
    
    # Prevent propagation to root logger
    logger.propagate = False
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance by name.
    
    Args:
        name: Logger name (typically __name__)
        
    Returns:
        logging.Logger: Logger instance
    """
    return logging.getLogger(name)


def add_context_to_logger(logger: logging.Logger, **context) -> logging.LoggerAdapter:
    """
    Add context fields to logger (session_id, tenant_id, etc.).
    
    Args:
        logger: Logger instance
        **context: Context fields to add
        
    Returns:
        logging.LoggerAdapter: Logger adapter with context
    """
    return logging.LoggerAdapter(logger, context)


def test_logger(logger: logging.Logger) -> None:
    """
    Test logger with all log levels.
    
    Args:
        logger: Logger instance to test
    """
    logger.debug("This is a DEBUG message")
    logger.info("This is an INFO message")
    logger.warning("This is a WARNING message")
    logger.error("This is an ERROR message")
    logger.critical("This is a CRITICAL message")
    
    try:
        raise ValueError("Test exception")
    except ValueError:
        logger.exception("This is an exception with traceback")


# Default logger configuration
def configure_default_logger(settings) -> logging.Logger:
    """
    Configure the default application logger from settings.
    
    Args:
        settings: Application settings instance
        
    Returns:
        logging.Logger: Configured logger
    """
    return setup_logger(
        name="msev15e2e",
        level=settings.LOG_LEVEL,
        log_file=settings.LOG_FILE_PATH if settings.LOG_TO_FILE else None,
        max_bytes=settings.log_max_bytes,
        backup_count=settings.LOG_BACKUP_COUNT,
        enable_console=True,
        enable_file=settings.LOG_TO_FILE,
    )
