"""
Session Store

Thread-safe in-memory storage for session data.
"""
from typing import Dict, Optional, List
from threading import Lock
from .models import SessionData


class SessionStore:
    """
    Thread-safe in-memory session storage.
    
    Sessions are keyed by "tenant_id:session_id" for multi-tenant isolation.
    """
    
    def __init__(self):
        self._sessions: Dict[str, SessionData] = {}
        self._lock = Lock()
    
    def _make_key(self, tenant_id: str, session_id: str) -> str:
        """Create composite key for session storage."""
        return f"{tenant_id}:{session_id}"
    
    def get(self, tenant_id: str, session_id: str) -> Optional[SessionData]:
        """
        Get session by tenant_id and session_id.
        
        Args:
            tenant_id: Tenant identifier
            session_id: Session identifier
        
        Returns:
            SessionData if found, None otherwise
        """
        key = self._make_key(tenant_id, session_id)
        with self._lock:
            return self._sessions.get(key)
    
    def set(self, session_data: SessionData):
        """
        Store session data.
        
        Args:
            session_data: Session data to store
        """
        key = self._make_key(session_data.tenant_id, session_data.session_id)
        with self._lock:
            self._sessions[key] = session_data
    
    def delete(self, tenant_id: str, session_id: str) -> bool:
        """
        Delete a session.
        
        Args:
            tenant_id: Tenant identifier
            session_id: Session identifier
        
        Returns:
            True if session was deleted, False if not found
        """
        key = self._make_key(tenant_id, session_id)
        with self._lock:
            if key in self._sessions:
                del self._sessions[key]
                return True
            return False
    
    def list_by_tenant(self, tenant_id: str) -> List[SessionData]:
        """
        List all sessions for a tenant.
        
        Args:
            tenant_id: Tenant identifier
        
        Returns:
            List of SessionData for the tenant
        """
        with self._lock:
            return [
                session for key, session in self._sessions.items()
                if session.tenant_id == tenant_id
            ]
    
    def count(self) -> int:
        """Get total number of sessions across all tenants."""
        with self._lock:
            return len(self._sessions)
    
    def count_by_tenant(self, tenant_id: str) -> int:
        """Get number of sessions for a specific tenant."""
        with self._lock:
            return sum(
                1 for session in self._sessions.values()
                if session.tenant_id == tenant_id
            )
    
    def clear(self):
        """Clear all sessions (for testing purposes)."""
        with self._lock:
            self._sessions.clear()


# Global session store instance
_session_store: Optional[SessionStore] = None


def get_session_store() -> SessionStore:
    """
    Get the global session store instance.
    
    Returns:
        SessionStore: The global session store
    """
    global _session_store
    if _session_store is None:
        _session_store = SessionStore()
    return _session_store


def reset_session_store():
    """Reset the global session store (for testing)."""
    global _session_store
    _session_store = None
