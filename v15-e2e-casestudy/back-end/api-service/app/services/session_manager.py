"""
Session Manager - In-memory session storage for multi-turn conversations.
"""
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import uuid


class SessionManager:
    """
    Manages agent sessions for multi-turn conversations.
    Sessions are stored in-memory with automatic expiration.
    """
    
    def __init__(self, ttl_minutes: int = 60):
        """
        Initialize the session manager.
        
        Args:
            ttl_minutes: Session time-to-live in minutes (default: 60)
        """
        self._sessions: Dict[str, Dict[str, Any]] = {}
        self._ttl_minutes = ttl_minutes
    
    def get_or_create_session(self, session_id: Optional[str] = None):
        """
        Get an existing session or create a new one.
        
        Args:
            session_id: Optional session ID. If None, generates a new UUID.
            
        Returns:
            tuple: (session_id, agent_session)
        """
        if session_id is None:
            session_id = str(uuid.uuid4())
        
        if session_id not in self._sessions:
            # Import here to avoid circular dependency
            from .agent_service import get_agent_service
            agent_service = get_agent_service()
            session = agent_service.create_session()
            
            self._sessions[session_id] = {
                "session": session,
                "created_at": datetime.now(),
                "last_accessed": datetime.now(),
                "turn_count": 0
            }
            print(f"✅ Created new session: {session_id}")
        else:
            self._sessions[session_id]["last_accessed"] = datetime.now()
        
        return session_id, self._sessions[session_id]["session"]
    
    def increment_turn(self, session_id: str):
        """Increment the turn count for a session."""
        if session_id in self._sessions:
            self._sessions[session_id]["turn_count"] += 1
    
    def get_turn_count(self, session_id: str) -> int:
        """Get the turn count for a session."""
        return self._sessions.get(session_id, {}).get("turn_count", 0)
    
    def get_session_info(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session metadata."""
        if session_id not in self._sessions:
            return None
        
        data = self._sessions[session_id]
        return {
            "session_id": session_id,
            "created_at": data["created_at"],
            "last_accessed": data["last_accessed"],
            "turn_count": data["turn_count"]
        }
    
    def cleanup_expired_sessions(self):
        """Remove sessions older than TTL."""
        now = datetime.now()
        expired = [
            sid for sid, data in self._sessions.items()
            if (now - data["last_accessed"]) > timedelta(minutes=self._ttl_minutes)
        ]
        for sid in expired:
            del self._sessions[sid]
            print(f"🗑️  Removed expired session: {sid}")
        
        if expired:
            print(f"✅ Cleaned up {len(expired)} expired session(s)")
    
    def get_active_session_count(self) -> int:
        """Get the number of active sessions."""
        return len(self._sessions)


# Singleton instance
_session_manager: Optional[SessionManager] = None


def get_session_manager() -> SessionManager:
    """Get the singleton SessionManager instance."""
    global _session_manager
    if _session_manager is None:
        _session_manager = SessionManager()
    return _session_manager
