"""
Database Connection and Session Management

This module handles database initialization, connection, and session management.

Functions:
    - init_database: Initialize database and create tables
    - get_session: Get database session
    - get_db: Database session dependency (context manager)
"""

from contextlib import contextmanager
from typing import Generator
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.engine import Engine
from .config import get_config
from .models import Base


# Global engine and session factory
_engine: Engine = None
_SessionLocal: sessionmaker = None


def get_engine() -> Engine:
    """
    Get or create the SQLAlchemy engine.
    
    Returns:
        SQLAlchemy Engine instance
    """
    global _engine
    if _engine is None:
        config = get_config()
        database_url = config.get_database_url()
        
        _engine = create_engine(
            database_url,
            echo=config.database_echo,
            connect_args={"check_same_thread": False}  # Needed for SQLite
        )
        
        # Enable foreign keys for SQLite
        @event.listens_for(_engine, "connect")
        def set_sqlite_pragma(dbapi_conn, connection_record):
            cursor = dbapi_conn.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()
    
    return _engine


def get_session_factory() -> sessionmaker:
    """
    Get or create the session factory.
    
    Returns:
        SQLAlchemy sessionmaker instance
    """
    global _SessionLocal
    if _SessionLocal is None:
        engine = get_engine()
        _SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=engine
        )
    return _SessionLocal


def init_database() -> None:
    """
    Initialize database and create all tables.
    
    This function creates all tables defined in the models if they don't exist.
    Should be called on application startup.
    """
    engine = get_engine()
    Base.metadata.create_all(bind=engine)


def get_session() -> Session:
    """
    Get a new database session.
    
    Returns:
        SQLAlchemy Session instance
        
    Note:
        The caller is responsible for closing the session.
    """
    SessionLocal = get_session_factory()
    return SessionLocal()


@contextmanager
def get_db() -> Generator[Session, None, None]:
    """
    Get database session with automatic cleanup (context manager).
    
    Yields:
        SQLAlchemy Session instance
        
    Example:
        with get_db() as db:
            complaint = db.query(Complaint).first()
    """
    session = get_session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_complaint_count() -> int:
    """
    Get the total count of complaints in the database.
    
    Returns:
        Number of complaints in database
    """
    from .models import Complaint
    
    with get_db() as db:
        count = db.query(Complaint).count()
    
    return count


def check_database_empty() -> bool:
    """
    Check if the complaints table is empty.
    
    Returns:
        True if database is empty, False otherwise
    """
    return get_complaint_count() == 0
