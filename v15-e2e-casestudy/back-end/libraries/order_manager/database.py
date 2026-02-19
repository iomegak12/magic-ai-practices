"""
Database connection and session management for the Order Manager library.

This module handles SQLite database initialization and provides
context-managed database sessions.
"""

from contextlib import contextmanager
from pathlib import Path
from typing import Generator
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session
from .models import Base
from .exceptions import DatabaseException


# Enable foreign key support for SQLite
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_conn, connection_record):
    """Enable foreign key constraints in SQLite."""
    cursor = dbapi_conn.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


class Database:
    """
    Database manager for SQLite with SQLAlchemy.
    
    Handles database initialization, connection management, and provides
    context-managed sessions for transactions.
    """
    
    def __init__(self, db_path: str):
        """
        Initialize the database manager.
        
        Args:
            db_path: Path to the SQLite database file
            
        Raises:
            DatabaseException: If database initialization fails
        """
        self.db_path = db_path
        self._engine = None
        self._session_factory = None
        
        try:
            # Create parent directories if they don't exist
            db_file = Path(db_path)
            db_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Create database engine
            database_url = f"sqlite:///{db_path}"
            self._engine = create_engine(
                database_url,
                echo=False,
                future=True,
                connect_args={"check_same_thread": False}
            )
            
            # Create session factory
            self._session_factory = sessionmaker(
                bind=self._engine,
                expire_on_commit=False
            )
            
            # Initialize database tables
            self.initialize()
            
        except Exception as e:
            raise DatabaseException(
                f"Failed to initialize database at {db_path}: {str(e)}",
                original_exception=e
            )
    
    def initialize(self) -> None:
        """
        Initialize database tables.
        
        Creates all tables defined in the models if they don't exist.
        
        Raises:
            DatabaseException: If table creation fails
        """
        try:
            Base.metadata.create_all(self._engine)
        except Exception as e:
            raise DatabaseException(
                f"Failed to create database tables: {str(e)}",
                original_exception=e
            )
    
    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        """
        Provide a transactional scope for database operations.
        
        Yields:
            SQLAlchemy Session object
            
        Example:
            with db.get_session() as session:
                order = session.query(Order).first()
                
        Note:
            The session will automatically commit on success or rollback on error.
        """
        from .exceptions import OrderManagerException
        
        session = self._session_factory()
        try:
            yield session
            session.commit()
        except OrderManagerException:
            # Re-raise our custom exceptions without wrapping
            session.rollback()
            raise
        except Exception as e:
            session.rollback()
            raise DatabaseException(
                f"Database operation failed: {str(e)}",
                original_exception=e
            )
        finally:
            session.close()
    
    def close(self) -> None:
        """
        Close the database connection.
        
        Should be called when the database is no longer needed.
        """
        if self._engine:
            self._engine.dispose()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - closes database connection."""
        self.close()
