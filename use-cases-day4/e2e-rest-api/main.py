"""Enterprise E2E Use Case — REST API entry point."""

import logging
import signal
import sys

import uvicorn
from app.config import get_settings
from app.factory import create_app


def _handle_shutdown(signum, _frame):
    sig_name = signal.Signals(signum).name
    logging.getLogger("app").info("Received %s — initiating graceful shutdown", sig_name)
    sys.exit(0)


def main() -> None:
    settings = get_settings()

    logging.basicConfig(
        level=settings.LOG_LEVEL.upper(),
        format="%(asctime)s | %(name)-12s | %(levelname)-7s | %(message)s",
        datefmt="%H:%M:%S",
        force=True,
    )

    signal.signal(signal.SIGINT, _handle_shutdown)
    signal.signal(signal.SIGTERM, _handle_shutdown)

    app = create_app(settings)

    uvicorn.run(
        app,
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        log_level=settings.LOG_LEVEL.lower(),
    )


if __name__ == "__main__":
    main()
