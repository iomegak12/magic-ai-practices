"""
Custom Exception Classes

Application-specific exceptions for better error handling and reporting.
"""


class MSEv15E2EException(Exception):
    """Base exception for all application errors"""
    
    def __init__(self, message: str, details: dict = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


# ============================================
# API Layer Exceptions
# ============================================

class APIException(MSEv15E2EException):
    """Base exception for API layer errors"""
    status_code = 500


class ValidationError(APIException):
    """Request validation failed"""
    status_code = 400


class RateLimitError(APIException):
    """Rate limit exceeded"""
    status_code = 429


class AuthenticationError(APIException):
    """Authentication failed"""
    status_code = 401


class AuthorizationError(APIException):
    """Authorization failed"""
    status_code = 403


class ResourceNotFoundError(APIException):
    """Requested resource not found"""
    status_code = 404


# ============================================
# Agent Layer Exceptions
# ============================================

class AgentException(MSEv15E2EException):
    """Base exception for agent errors"""
    pass


class AgentInitializationError(AgentException):
    """Agent failed to initialize"""
    pass


class AgentExecutionError(AgentException):
    """Agent execution failed"""
    pass


class AgentTimeoutError(AgentException):
    """Agent execution timed out"""
    pass


# ============================================
# Tool Layer Exceptions
# ============================================

class ToolException(MSEv15E2EException):
    """Base exception for tool errors"""
    pass


class ToolExecutionError(ToolException):
    """Tool execution failed"""
    pass


class MCPConnectionError(ToolException):
    """MCP server connection failed"""
    pass


class MCPServerUnavailableError(ToolException):
    """MCP server is unavailable"""
    pass


class OrderManagementError(ToolException):
    """Order management operation failed"""
    pass


class EmailSendError(ToolException):
    """Email sending failed"""
    pass


# ============================================
# Session Layer Exceptions
# ============================================

class SessionException(MSEv15E2EException):
    """Base exception for session errors"""
    pass


class SessionNotFoundError(SessionException):
    """Session does not exist"""
    pass


class SessionExpiredError(SessionException):
    """Session has expired"""
    pass


class SessionStorageError(SessionException):
    """Session storage operation failed"""
    pass


# ============================================
# Configuration Exceptions
# ============================================

class ConfigurationError(MSEv15E2EException):
    """Configuration is invalid or missing"""
    pass


class DependencyError(MSEv15E2EException):
    """Required dependency is missing or unavailable"""
    pass


# ============================================
# Helper Functions
# ============================================

def format_exception_details(exc: Exception) -> dict:
    """
    Format exception details for logging or API responses.
    
    Args:
        exc: Exception instance
        
    Returns:
        dict: Formatted exception details
    """
    details = {
        "type": exc.__class__.__name__,
        "message": str(exc),
    }
    
    # Add custom details if available
    if isinstance(exc, MSEv15E2EException) and exc.details:
        details["details"] = exc.details
    
    # Add status code for API exceptions
    if isinstance(exc, APIException):
        details["status_code"] = exc.status_code
    
    return details


def get_http_status_code(exc: Exception) -> int:
    """
    Get HTTP status code for an exception.
    
    Args:
        exc: Exception instance
        
    Returns:
        int: HTTP status code
    """
    if isinstance(exc, APIException):
        return exc.status_code
    
    # Default to 500 for unexpected errors
    return 500


def should_retry(exc: Exception) -> bool:
    """
    Determine if an operation should be retried based on exception type.
    
    Args:
        exc: Exception instance
        
    Returns:
        bool: True if operation should be retried
    """
    # Retry on transient errors
    retryable_exceptions = (
        MCPConnectionError,
        AgentTimeoutError,
        SessionStorageError,
    )
    
    # Don't retry validation or not found errors
    non_retryable_exceptions = (
        ValidationError,
        ResourceNotFoundError,
        AuthenticationError,
        AuthorizationError,
        ConfigurationError,
    )
    
    if isinstance(exc, non_retryable_exceptions):
        return False
    
    if isinstance(exc, retryable_exceptions):
        return True
    
    # Default: retry on generic exceptions (network errors, etc.)
    return not isinstance(exc, MSEv15E2EException)
