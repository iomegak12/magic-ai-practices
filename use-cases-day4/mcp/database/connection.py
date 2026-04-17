"""Database connection and session management."""

import logging
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from config.settings import settings
from models.base import Base

logger = logging.getLogger(__name__)


class Database:
    """SQLite database manager with SQLAlchemy."""

    def __init__(self):
        self.db_path = settings.get_db_path()
        self.engine = None
        self.SessionLocal = None
        self._initialized = False

    def initialize(self):
        if self._initialized:
            return

        db_url = f"sqlite:///{self.db_path}"
        self.engine = create_engine(
            db_url,
            echo=False,
            connect_args={"check_same_thread": False},
        )
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine,
        )
        Base.metadata.create_all(bind=self.engine)
        self._initialized = True
        logger.info(f"Database initialized at: {self.db_path}")

    @contextmanager
    def get_session(self) -> Session:
        """Context manager that yields a session and handles commit/rollback."""
        if not self._initialized:
            self.initialize()

        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()


# Global database instance
db = Database()


def init_db():
    """Initialize the database (create tables)."""
    db.initialize()
