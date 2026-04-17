"""
Startup & Signal Handling
=========================
Encapsulates everything that must happen *before* the MCP server
starts accepting requests:

  - OS signal registration (SIGINT, SIGTERM)
  - Database initialisation
  - Optional auto-seeding of sample data

These concerns are isolated here so ``server.py`` remains a
minimal orchestration entry point.
"""

import signal
import sys

from src.config import load_config
from src.database import get_db, init_database
from src.utils.logger import get_logger
from src.utils.seed_data import seed_database

logger = get_logger(__name__)


# ---------------------------------------------------------------------------
# Signal handling
# ---------------------------------------------------------------------------

def _signal_handler(signum, frame) -> None:
    """Handle SIGINT / SIGTERM — log then exit cleanly."""
    signal_name = signal.Signals(signum).name
    logger.info("Received %s — shutting down gracefully.", signal_name)
    sys.exit(0)


def register_signal_handlers() -> None:
    """Register OS-level signal handlers for graceful shutdown."""
    signal.signal(signal.SIGINT, _signal_handler)
    signal.signal(signal.SIGTERM, _signal_handler)
    logger.debug("Signal handlers registered (SIGINT, SIGTERM).")


# ---------------------------------------------------------------------------
# Database / seed startup
# ---------------------------------------------------------------------------

def run_startup() -> None:
    """
    Prepare the application before the server starts listening.

    Actions (in order):
    1. Initialise the SQLite database and create tables if absent.
    2. If ``AUTO_SEED_DATABASE=true``, seed the database with 20 sample
       complaints — skipped silently when data already exists.
    """
    config = load_config()

    logger.info("Initialising database at: %s", config.database_path)
    init_database()
    logger.info("Database ready.")

    if config.auto_seed:
        with get_db() as session:
            inserted = seed_database(session)
        if inserted:
            logger.info("Auto-seeded %d sample complaints.", inserted)
        else:
            logger.info("Auto-seed skipped (database already contains data).")
    else:
        logger.info("Auto-seed disabled.")
