"""
Session Manager

High-level session management operations.
"""
from typing import Optional, List
from datetime import datetime, timedelta
from .models import SessionData, SessionSummary
from .store import SessionStore, get_session_store
from ..utils.helpers import generate_session_id, sanitize_session_id, sanitize_tenant_id
from ..utils.exceptions import SessionNotFoundError, SessionExpiredError
from ..utils.logger import get_logger

logger = get_logger(__name__)


class SessionManager:
    """
    Manages session lifecycle and operations.
    
    Provides high-level interface for session CRUD operations,
    message management, and session cleanup.
    """
    
    def __init__(self, store: Optional[SessionStore] = None, session_ttl_hours: int = 24):
        """
        Initialize session manager.
        
        Args:
            store: Session store instance (creates default if None)
            session_ttl_hours: Session time-to-live in hours
        """
        self.store = store or get_session_store()
        self.session_ttl = timedelta(hours=session_ttl_hours)
    
    async def create_session(
        self,
        session_id: Optional[str] = None,
        tenant_id: str = "default",
        metadata: Optional[dict] = None
    ) -> SessionData:
        """
        Create a new session.
        
        Args:
            session_id: Session identifier (generates if None)
            tenant_id: Tenant identifier
            metadata: Optional metadata
        
        Returns:
            SessionData: The created session
        """
        if session_id is None:
            session_id = generate_session_id()
        else:
            session_id = sanitize_session_id(session_id)
        
        tenant_id = sanitize_tenant_id(tenant_id)
        
        # Check if session already exists
        existing = self.store.get(tenant_id, session_id)
        if existing:
            logger.warning(
                f"Session already exists: {session_id} (tenant: {tenant_id})",
                extra={"session_id": session_id, "tenant_id": tenant_id}
            )
            return existing
        
        # Create new session
        session = SessionData(
            session_id=session_id,
            tenant_id=tenant_id,
            messages=[],
            created_at=datetime.utcnow(),
            last_activity=datetime.utcnow(),
            metadata=metadata or {}
        )
        
        self.store.set(session)
        
        logger.info(
            f"Session created: {session_id} (tenant: {tenant_id})",
            extra={"session_id": session_id, "tenant_id": tenant_id}
        )
        
        return session
    
    async def get_session(
        self,
        session_id: str,
        tenant_id: str = "default",
        check_expiry: bool = True
    ) -> SessionData:
        """
        Get an existing session.
        
        Args:
            session_id: Session identifier
            tenant_id: Tenant identifier
            check_expiry: Whether to check session expiry
        
        Returns:
            SessionData: The session
        
        Raises:
            SessionNotFoundError: If session doesn't exist
            SessionExpiredError: If session has expired
        """
        session_id = sanitize_session_id(session_id)
        tenant_id = sanitize_tenant_id(tenant_id)
        
        session = self.store.get(tenant_id, session_id)
        
        if not session:
            raise SessionNotFoundError(
                f"Session not found: {session_id} (tenant: {tenant_id})"
            )
        
        # Check expiry
        if check_expiry:
            age = datetime.utcnow() - session.last_activity
            if age > self.session_ttl:
                # Delete expired session
                self.store.delete(tenant_id, session_id)
                raise SessionExpiredError(
                    f"Session expired: {session_id} (age: {age.total_seconds():.0f}s)"
                )
        
        return session
    
    async def get_or_create_session(
        self,
        session_id: str,
        tenant_id: str = "default",
        metadata: Optional[dict] = None
    ) -> SessionData:
        """
        Get existing session or create new one if it doesn't exist.
        
        Args:
            session_id: Session identifier
            tenant_id: Tenant identifier
            metadata: Optional metadata for new session
        
        Returns:
            SessionData: The session
        """
        try:
            return await self.get_session(session_id, tenant_id)
        except (SessionNotFoundError, SessionExpiredError):
            return await self.create_session(session_id, tenant_id, metadata)
    
    async def add_message(
        self,
        session_id: str,
        tenant_id: str,
        role: str,
        content: str,
        tool_calls: Optional[List[dict]] = None
    ):
        """
        Add a message to a session.
        
        Args:
            session_id: Session identifier
            tenant_id: Tenant identifier
            role: Message role (user, assistant, system)
            content: Message content
            tool_calls: Optional tool call information
        """
        session = await self.get_session(session_id, tenant_id)
        session.add_message(role, content, tool_calls)
        self.store.set(session)
        
        logger.debug(
            f"Message added to session {session_id}: {role}",
            extra={
                "session_id": session_id,
                "tenant_id": tenant_id,
                "role": role,
                "message_length": len(content)
            }
        )
    
    async def update_metadata(
        self,
        session_id: str,
        tenant_id: str,
        metadata: dict
    ):
        """
        Update session metadata.
        
        Args:
            session_id: Session identifier
            tenant_id: Tenant identifier
            metadata: Metadata to merge
        """
        session = await self.get_session(session_id, tenant_id)
        session.metadata.update(metadata)
        session.last_activity = datetime.utcnow()
        self.store.set(session)
    
    async def delete_session(
        self,
        session_id: str,
        tenant_id: str = "default"
    ) -> bool:
        """
        Delete a session.
        
        Args:
            session_id: Session identifier
            tenant_id: Tenant identifier
        
        Returns:
            bool: True if deleted, False if not found
        """
        session_id = sanitize_session_id(session_id)
        tenant_id = sanitize_tenant_id(tenant_id)
        
        deleted = self.store.delete(tenant_id, session_id)
        
        if deleted:
            logger.info(
                f"Session deleted: {session_id} (tenant: {tenant_id})",
                extra={"session_id": session_id, "tenant_id": tenant_id}
            )
        else:
            logger.warning(
                f"Session not found for deletion: {session_id} (tenant: {tenant_id})",
                extra={"session_id": session_id, "tenant_id": tenant_id}
            )
        
        return deleted
    
    async def list_sessions(
        self,
        tenant_id: str = "default",
        limit: int = 50,
        offset: int = 0
    ) -> List[SessionSummary]:
        """
        List sessions for a tenant.
        
        Args:
            tenant_id: Tenant identifier
            limit: Maximum number of sessions to return
            offset: Number of sessions to skip
        
        Returns:
            List of SessionSummary objects
        """
        tenant_id = sanitize_tenant_id(tenant_id)
        sessions = self.store.list_by_tenant(tenant_id)
        
        # Sort by last activity (most recent first)
        sessions.sort(key=lambda s: s.last_activity, reverse=True)
        
        # Apply pagination
        paginated = sessions[offset:offset + limit]
        
        # Convert to summaries
        summaries = [
            SessionSummary(
                session_id=s.session_id,
                tenant_id=s.tenant_id,
                message_count=len(s.messages),
                created_at=s.created_at,
                last_activity=s.last_activity
            )
            for s in paginated
        ]
        
        return summaries
    
    async def cleanup_expired_sessions(self) -> int:
        """
        Clean up expired sessions across all tenants.
        
        Returns:
            int: Number of sessions deleted
        """
        logger.info("Starting session cleanup")
        
        deleted_count = 0
        current_time = datetime.utcnow()
        
        # Get all sessions from store (need direct access)
        with self.store._lock:
            expired_keys = []
            for key, session in self.store._sessions.items():
                age = current_time - session.last_activity
                if age > self.session_ttl:
                    expired_keys.append(key)
                    tenant_id, session_id = key.split(":", 1)
                    logger.debug(
                        f"Marking session for deletion: {session_id} "
                        f"(age: {age.total_seconds():.0f}s)",
                        extra={"session_id": session_id, "tenant_id": tenant_id}
                    )
            
            # Delete expired sessions
            for key in expired_keys:
                del self.store._sessions[key]
                deleted_count += 1
        
        if deleted_count > 0:
            logger.info(f"Cleaned up {deleted_count} expired sessions")
        
        return deleted_count
    
    def get_stats(self) -> dict:
        """
        Get session statistics.
        
        Returns:
            dict: Statistics including total sessions, by tenant, etc.
        """
        return {
            "total_sessions": self.store.count(),
            "timestamp": datetime.utcnow().isoformat()
        }


# Global session manager instance
_session_manager: Optional[SessionManager] = None


def get_session_manager() -> SessionManager:
    """
    Get the global session manager instance.
    
    Returns:
        SessionManager: The global session manager
    """
    global _session_manager
    if _session_manager is None:
        _session_manager = SessionManager()
    return _session_manager


def reset_session_manager():
    """Reset the global session manager (for testing)."""
    global _session_manager
    _session_manager = None
