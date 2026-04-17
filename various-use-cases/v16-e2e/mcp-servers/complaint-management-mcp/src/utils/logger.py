"""
Logger Module

Provides a pre-configured logger for the complaint management MCP server.
Logs to both stdout (console) and a rotating file handler.
"""

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path


_LOG_DIR = Path(__file__).parent.parent.parent / "logs"
_LOG_FILE = _LOG_DIR / "complaint-management-mcp.log"
_LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
_MAX_BYTES = 5 * 1024 * 1024   # 5 MB
_BACKUP_COUNT = 3


def get_logger(name: str = "complaint-mcp", level: int = logging.INFO) -> logging.Logger:
    """
    Return a named logger configured with console and rotating file handlers.

    Handlers are only added once per logger name to avoid duplicate log entries
    when called multiple times.

    Args:
        name:  Logger name (default: "complaint-mcp").
        level: Logging level (default: logging.INFO).

    Returns:
        A configured :class:`logging.Logger` instance.
    """
    logger = logging.getLogger(name)

    # Guard: don't add handlers more than once
    if logger.handlers:
        return logger

    logger.setLevel(level)
    formatter = logging.Formatter(_LOG_FORMAT, datefmt=_DATE_FORMAT)

    # --- Console handler ---
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(level)
    logger.addHandler(console_handler)

    # --- Rotating file handler ---
    try:
        _LOG_DIR.mkdir(parents=True, exist_ok=True)
        file_handler = RotatingFileHandler(
            _LOG_FILE,
            maxBytes=_MAX_BYTES,
            backupCount=_BACKUP_COUNT,
            encoding="utf-8",
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(level)
        logger.addHandler(file_handler)
    except OSError as exc:
        # If we can't write log files (e.g. read-only filesystem) just warn
        logger.warning("Could not create file log handler: %s", exc)

    # Prevent propagation to root logger to avoid duplicate output
    logger.propagate = False

    return logger
