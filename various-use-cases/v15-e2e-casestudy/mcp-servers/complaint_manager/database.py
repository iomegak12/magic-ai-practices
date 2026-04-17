"""
Database connection and session management
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
import logging

from .models import Base
from .config import config

logger = logging.getLogger(__name__)


class Database:
    """Database manager for SQLite with SQLAlchemy"""
    
    def __init__(self):
        self.db_path = config.get_db_path()
        self.engine = None
        self.SessionLocal = None
        self._initialized = False
    
    def initialize(self):
        """Initialize database engine and create tables"""
        if self._initialized:
            return
        
        try:
            # Create SQLite engine
            db_url = f"sqlite:///{self.db_path}"
            self.engine = create_engine(
                db_url,
                echo=False,
                connect_args={"check_same_thread": False}
            )
            
            # Create session factory
            self.SessionLocal = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine
            )
            
            # Create all tables
            Base.metadata.create_all(bind=self.engine)
            
            self._initialized = True
            logger.info(f"Database initialized at: {self.db_path}")
            
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise
    
    @contextmanager
    def get_session(self) -> Session:
        """
        Context manager for database sessions
        Ensures proper session cleanup
        """
        if not self._initialized:
            self.initialize()
        
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Database session error: {e}")
            raise
        finally:
            session.close()


# Global database instance
db = Database()
