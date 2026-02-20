"""
Database configuration and session management for order management system.
"""
import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Get database path from environment or use default
# This will be overridden by the application settings
DATABASE_PATH = os.getenv('ORDER_DB_PATH', './data/orders.db')

# Create database URL
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# Create SQLAlchemy engine
engine = None
SessionLocal = None
Base = declarative_base()


def _get_engine():
    """Get or create SQLAlchemy engine"""
    global engine
    if engine is None:
        # Ensure the database directory exists
        db_path = Path(DATABASE_PATH)
        db_path.parent.mkdir(parents=True, exist_ok=True)
        
        engine = create_engine(
            DATABASE_URL,
            echo=False,  # Set to True for SQL query logging
            connect_args={"check_same_thread": False}  # Needed for SQLite
        )
    return engine


def _get_session_local():
    """Get or create session factory"""
    global SessionLocal
    if SessionLocal is None:
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_get_engine())
    return SessionLocal


def init_db():
    """
    Initialize the database by creating all tables.
    Should be called once when setting up the library.
    """
    Base.metadata.create_all(bind=_get_engine())


def get_db_session():
    """
    Get a database session.
    
    Returns:
        Session: SQLAlchemy database session
        
    Usage:
        session = get_db_session()
        try:
            # Use session
            pass
        finally:
            session.close()
    """
    return _get_session_local()()


def get_database_path():
    """
    Get the current database path.
    
    Returns:
        str: Path to the SQLite database file
    """
    return DATABASE_PATH


def set_database_path(path: str):
    """
    Set the database path (must be called before init_db).
    
    Args:
        path: Path to the SQLite database file
    """
    global DATABASE_PATH, DATABASE_URL, engine, SessionLocal
    DATABASE_PATH = path
    DATABASE_URL = f"sqlite:///{DATABASE_PATH}"
    # Reset engine and session to force recreation with new path
    engine = None
    SessionLocal = None
