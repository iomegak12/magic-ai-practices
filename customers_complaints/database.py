"""Database configuration and session management."""

import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv()

DATABASE_PATH = os.getenv("DATABASE_PATH", "./data")
DATABASE_NAME = "customers_complaints.db"

# Ensure the directory exists
Path(DATABASE_PATH).mkdir(parents=True, exist_ok=True)

_db_url = f"sqlite:///{Path(DATABASE_PATH) / DATABASE_NAME}"
engine = create_engine(_db_url, echo=False)
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


def init_db() -> None:
    """Create all tables if they don't already exist."""
    from . import models as _models  # noqa: F401 — ensure models are registered

    Base.metadata.create_all(bind=engine)


def get_session():
    """Return a new database session."""
    return SessionLocal()
