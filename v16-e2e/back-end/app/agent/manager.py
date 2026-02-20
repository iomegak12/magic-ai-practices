"""
Agent manager for handling agent lifecycle and execution.

This module manages agent instances, sessions, and conversation execution.
"""
import logging
from typing import Optional, Dict, Any
from agent_framework.azure import AzureOpenAIResponsesClient
from azure.identity import AzureCliCredential

from ..config.settings import get_settings
from .factory import AgentFactory
from ..utils.exceptions import (
    AgentInitializationError,
    AgentExecutionError,
    SessionNotFoundError
)
from ..utils.helpers import generate_session_id

logger = logging.getLogger(__name__)


class AgentManager:
    """Manager for AI agent lifecycle and execution."""
    
    def __init__(self):
        """Initialize agent manager."""
        self._client: Optional[AzureOpenAIResponsesClient] = None
        self._agent = None  # Agent instance from agent_framework
        self._sessions: Dict[str, Any] = {}  # session_id -> AgentSession
        self._initialized = False
    
    def initialize(self) -> bool:
        """
        Initialize the agent manager and create default agent.
        
        Returns:
            bool: True if initialization successful
            
        Raises:
            AgentInitializationError: If initialization fails
        """
        if self._initialized:
            logger.debug("Agent manager already initialized")
            return True
        
        try:
            logger.info("Initializing agent manager...")
            
            # Create Azure OpenAI client
            self._client = AgentFactory.create_client()
            logger.debug("Azure OpenAI client created")
            
            # Create default agent using factory
            self._agent = AgentFactory.create_agent(self._client)
            
            self._initialized = True
            logger.info("Agent manager initialized successfully")
            return True
            
        except Exception as e:
            error_msg = f"Agent manager initialization failed: {str(e)}"
            logger.error(error_msg)
            raise AgentInitializationError(error_msg)
    
    def is_initialized(self) -> bool:
        """
        Check if agent manager is initialized.
        
        Returns:
            bool: True if initialized, False otherwise
        """
        return self._initialized
    
    def get_agent(self):
        """
        Get the current agent instance.
        
        Returns:
            Agent instance from agent_framework
            
        Raises:
            AgentInitializationError: If manager not initialized
        """
        if not self._initialized or not self._agent:
            raise AgentInitializationError("Agent manager not initialized")
        return self._agent
    
    def create_session(self, session_id: Optional[str] = None) -> str:
        """
        Create a new conversation session.
        
        Args:
            session_id: Optional session ID (generated if not provided)
            
        Returns:
            str: Session ID
            
        Raises:
            AgentInitializationError: If manager not initialized
        """
        if not self._initialized:
            raise AgentInitializationError("Agent manager not initialized")
        
        try:
            # Generate session ID if not provided
            if session_id is None:
                session_id = generate_session_id()
            
            logger.info(f"Creating new session: {session_id}")
            
            # Create agent session
            agent_session = self._agent.create_session()
            
            # Store session
            self._sessions[session_id] = agent_session
            
            logger.info(f"Session created: {session_id}")
            return session_id
            
        except Exception as e:
            error_msg = f"Failed to create session: {str(e)}"
            logger.error(error_msg)
            raise AgentExecutionError(error_msg)
    
    def get_session(self, session_id: str):
        """
        Get an existing session.
        
        Args:
            session_id: Session identifier
            
        Returns:
            AgentSession: Session instance
            
        Raises:
            SessionNotFoundError: If session doesn't exist
        """
        if session_id not in self._sessions:
            raise SessionNotFoundError(f"Session not found: {session_id}")
        return self._sessions[session_id]
    
    def delete_session(self, session_id: str) -> bool:
        """
        Delete a conversation session.
        
        Args:
            session_id: Session identifier
            
        Returns:
            bool: True if deleted, False if not found
        """
        if session_id in self._sessions:
            logger.info(f"Deleting session: {session_id}")
            
            # Remove from local sessions
            del self._sessions[session_id]
            logger.info(f"Session deleted: {session_id}")
            return True
        
        return False
    
    async def execute(
        self,
        session_id: str,
        message: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Execute agent with a message in a session.
        
        Args:
            session_id: Session identifier
            message: User message
            **kwargs: Additional execution parameters
            
        Returns:
            dict: Execution result with response and metadata
            
        Raises:
            SessionNotFoundError: If session doesn't exist
            AgentExecutionError: If execution fails
        """
        try:
            # Get session
            session = self.get_session(session_id)
            
            logger.info(f"Executing agent for session: {session_id}")
            logger.debug(f"User message: {message}")
            
            # Run agent (this is async in agent_framework)
            result = await self._agent.run(message, session=session)
            
            logger.info(f"Agent execution successful for session: {session_id}")
            
            return {
                "session_id": session_id,
                "response": str(result),
                "status": "success"
            }
            
        except SessionNotFoundError:
            raise
        except Exception as e:
            error_msg = f"Agent execution failed: {str(e)}"
            logger.error(error_msg)
            raise AgentExecutionError(error_msg)
    
    async def execute_stream(
        self,
        session_id: str,
        message: str,
        **kwargs
    ):
        """
        Execute agent with streaming response.
        
        Args:
            session_id: Session identifier
            message: User message
            **kwargs: Additional execution parameters
            
        Yields:
            str: Text chunks from agent response
            
        Raises:
            SessionNotFoundError: If session doesn't exist
            AgentExecutionError: If execution fails
        """
        try:
            # Get session
            session = self.get_session(session_id)
            
            logger.info(f"Executing agent (streaming) for session: {session_id}")
            logger.debug(f"User message: {message}")
            
            # Run agent with streaming enabled
            stream = self._agent.run(message, session=session, stream=True)
            
            # Yield text chunks as they arrive
            try:
                async for update in stream:
                    if update.text:
                        yield update.text
            except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError):
                # Client disconnected - exit gracefully
                logger.debug(f"Client disconnected during streaming for session: {session_id}")
                return
            
            logger.info(f"Agent streaming execution complete for session: {session_id}")
            
        except SessionNotFoundError:
            raise
        except Exception as e:
            error_msg = f"Agent streaming execution failed: {str(e)}"
            logger.error(error_msg)
            raise AgentExecutionError(error_msg)
    
    def get_session_count(self) -> int:
        """
        Get the number of active sessions.
        
        Returns:
            int: Number of active sessions
        """
        return len(self._sessions)
    
    def list_sessions(self) -> list:
        """
        List all active session IDs.
        
        Returns:
            list: List of session IDs
        """
        return list(self._sessions.keys())
    
    def cleanup_sessions(self):
        """Cleanup all active sessions."""
        logger.info(f"Cleaning up {len(self._sessions)} sessions...")
        
        session_ids = list(self._sessions.keys())
        for session_id in session_ids:
            try:
                self.delete_session(session_id)
            except Exception as e:
                logger.error(f"Error cleaning up session {session_id}: {str(e)}")
        
        logger.info("Session cleanup complete")
    
    def shutdown(self):
        """Shutdown agent manager and cleanup resources."""
        logger.info("Shutting down agent manager...")
        
        # Cleanup sessions
        self.cleanup_sessions()
        
        # Clear references
        self._agent = None
        self._client = None
        self._initialized = False
        
        logger.info("Agent manager shutdown complete")
    
    def __repr__(self):
        status = "initialized" if self._initialized else "not initialized"
        return f"<AgentManager(status={status}, sessions={len(self._sessions)})>"


# Global agent manager instance
_agent_manager: Optional[AgentManager] = None


def initialize_agent_manager() -> AgentManager:
    """
    Initialize and get the global agent manager instance.
    
    Returns:
        AgentManager: Initialized agent manager
        
    Raises:
        AgentInitializationError: If initialization fails
    """
    global _agent_manager
    
    if _agent_manager is None:
        _agent_manager = AgentManager()
    
    if not _agent_manager.is_initialized():
        _agent_manager.initialize()
    
    return _agent_manager


def get_agent_manager() -> Optional[AgentManager]:
    """
    Get the global agent manager instance.
    
    Returns:
        AgentManager: Agent manager if initialized, None otherwise
    """
    return _agent_manager


def shutdown_agent_manager():
    """Shutdown the global agent manager."""
    global _agent_manager
    
    if _agent_manager:
        _agent_manager.shutdown()
        _agent_manager = None


# Export public API
__all__ = [
    "AgentManager",
    "initialize_agent_manager",
    "get_agent_manager",
    "shutdown_agent_manager",
]
