"""
Database configuration and session management for order management system.
"""
import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database path from environment or use default
DATABASE_PATH = os.getenv('DATABASE_PATH', 'orders.db')

# Create database URL
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Set to True for SQL query logging
    connect_args={"check_same_thread": False}  # Needed for SQLite
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create declarative base for models
Base = declarative_base()


def init_db():
    """
    Initialize the database by creating all tables.
    Should be called once when setting up the library.
    """
    Base.metadata.create_all(bind=engine)


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
    return SessionLocal()


def get_database_path():
    """
    Get the current database path.
    
    Returns:
        str: Path to the SQLite database file
    """
    return DATABASE_PATH
