"""
Unit Tests for Exception Classes

Tests for app/utils/exceptions.py exception hierarchy.
"""
import pytest
from app.utils.exceptions import (
    # Base
    APIException,
    AgentException,
    ToolException,
    SessionException,
    # API Exceptions
    ValidationError,
    RateLimitError,
    ResourceNotFoundError,
    AuthenticationError,
    AuthorizationError,
    # Agent Exceptions
    AgentInitializationError,
    AgentExecutionError,
    AgentTimeoutError,
    # Tool Exceptions
    MCPConnectionError,
    MCPServerUnavailableError,
    OrderManagementError,
    EmailSendError,
    # Session Exceptions
    SessionNotFoundError,
    SessionExpiredError,
    SessionStorageError,
    # Utility functions
    format_exception_details,
    get_http_status_code,
    should_retry
)


class TestAPIExceptions:
    """Tests for API exception classes."""
    
    def test_validation_error(self):
        """Test ValidationError exception."""
        error = ValidationError("Invalid input")
        
        assert isinstance(error, APIException)
        assert str(error) == "Invalid input"
        assert error.status_code == 400
    
    def test_rate_limit_error(self):
        """Test RateLimitError exception."""
        error = RateLimitError("Rate limit exceeded")
        
        assert isinstance(error, APIException)
        assert error.status_code == 429
    
    def test_resource_not_found_error(self):
        """Test ResourceNotFoundError exception."""
        error = ResourceNotFoundError("Resource not found")
        
        assert isinstance(error, APIException)
        assert error.status_code == 404
    
    def test_authentication_error(self):
        """Test AuthenticationError exception."""
        error = AuthenticationError("Authentication failed")
        
        assert isinstance(error, APIException)
        assert error.status_code == 401
    
    def test_authorization_error(self):
        """Test AuthorizationError exception."""
        error = AuthorizationError("Access denied")
        
        assert isinstance(error, APIException)
        assert error.status_code == 403


class TestAgentExceptions:
    """Tests for agent exception classes."""
    
    def test_agent_initialization_error(self):
        """Test AgentInitializationError exception."""
        error = AgentInitializationError("Failed to initialize")
        
        assert isinstance(error, AgentException)
        assert str(error) == "Failed to initialize"
    
    def test_agent_execution_error(self):
        """Test AgentExecutionError exception."""
        error = AgentExecutionError("Execution failed")
        
        assert isinstance(error, AgentException)
        assert str(error) == "Execution failed"
    
    def test_agent_timeout_error(self):
        """Test AgentTimeoutError exception."""
        error = AgentTimeoutError("Operation timed out")
        
        assert isinstance(error, AgentException)
        assert str(error) == "Operation timed out"


class TestToolExceptions:
    """Tests for tool exception classes."""
    
    def test_mcp_connection_error(self):
        """Test MCPConnectionError exception."""
        error = MCPConnectionError("Connection failed")
        
        assert isinstance(error, ToolException)
        assert str(error) == "Connection failed"
    
    def test_mcp_server_unavailable_error(self):
        """Test MCPServerUnavailableError exception."""
        error = MCPServerUnavailableError("Server unavailable")
        
        assert isinstance(error, ToolException)
        assert str(error) == "Server unavailable"
    
    def test_order_management_error(self):
        """Test OrderManagementError exception."""
        error = OrderManagementError("Order operation failed")
        
        assert isinstance(error, ToolException)
        assert str(error) == "Order operation failed"
    
    def test_email_send_error(self):
        """Test EmailSendError exception."""
        error = EmailSendError("Email sending failed")
        
        assert isinstance(error, ToolException)
        assert str(error) == "Email sending failed"


class TestSessionExceptions:
    """Tests for session exception classes."""
    
    def test_session_not_found_error(self):
        """Test SessionNotFoundError exception."""
        error = SessionNotFoundError("Session not found")
        
        assert isinstance(error, SessionException)
        assert str(error) == "Session not found"
    
    def test_session_expired_error(self):
        """Test SessionExpiredError exception."""
        error = SessionExpiredError("Session expired")
        
        assert isinstance(error, SessionException)
        assert str(error) == "Session expired"
    
    def test_session_storage_error(self):
        """Test SessionStorageError exception."""
        error = SessionStorageError("Storage error")
        
        assert isinstance(error, SessionException)
        assert str(error) == "Storage error"


class TestExceptionUtilities:
    """Tests for exception utility functions."""
    
    def test_format_exception_details_simple(self):
        """Test formatting simple exception."""
        try:
            raise ValueError("Test error")
        except ValueError as e:
            details = format_exception_details(e)
            
            assert isinstance(details, dict)
            assert "type" in details
            assert "message" in details
            assert details["type"] == "ValueError"
            assert details["message"] == "Test error"
    
    def test_format_exception_details_with_traceback(self):
        """Test formatting exception with traceback."""
        try:
            raise RuntimeError("Test error")
        except RuntimeError as e:
            details = format_exception_details(e, include_traceback=True)
            
            assert "traceback" in details
            assert isinstance(details["traceback"], str)
    
    def test_get_http_status_code_api_exception(self):
        """Test getting status code from API exception."""
        error = ValidationError("Invalid")
        status_code = get_http_status_code(error)
        
        assert status_code == 400
    
    def test_get_http_status_code_standard_exception(self):
        """Test getting status code from standard exception."""
        error = ValueError("Invalid")
        status_code = get_http_status_code(error)
        
        assert status_code == 500  # Default for unknown exceptions
    
    def test_should_retry_transient_errors(self):
        """Test retry logic for transient errors."""
        # Timeout errors should be retryable
        assert should_retry(AgentTimeoutError("Timeout"))
        
        # Connection errors should be retryable
        assert should_retry(MCPConnectionError("Connection failed"))
    
    def test_should_retry_permanent_errors(self):
        """Test retry logic for permanent errors."""
        # Validation errors should not be retryable
        assert not should_retry(ValidationError("Invalid input"))
        
        # Authentication errors should not be retryable
        assert not should_retry(AuthenticationError("Auth failed"))
    
    def test_should_retry_max_attempts(self):
        """Test retry respects max attempts."""
        error = AgentTimeoutError("Timeout")
        
        # Should retry within max attempts
        assert should_retry(error, attempt=1, max_attempts=3)
        assert should_retry(error, attempt=2, max_attempts=3)
        
        # Should not retry after max attempts
        assert not should_retry(error, attempt=3, max_attempts=3)
        assert not should_retry(error, attempt=4, max_attempts=3)


class TestExceptionInheritance:
    """Tests for exception inheritance hierarchy."""
    
    def test_api_exception_inheritance(self):
        """Test API exceptions inherit from APIException."""
        assert issubclass(ValidationError, APIException)
        assert issubclass(RateLimitError, APIException)
        assert issubclass(ResourceNotFoundError, APIException)
    
    def test_agent_exception_inheritance(self):
        """Test Agent exceptions inherit from AgentException."""
        assert issubclass(AgentInitializationError, AgentException)
        assert issubclass(AgentExecutionError, AgentException)
        assert issubclass(AgentTimeoutError, AgentException)
    
    def test_tool_exception_inheritance(self):
        """Test Tool exceptions inherit from ToolException."""
        assert issubclass(MCPConnectionError, ToolException)
        assert issubclass(OrderManagementError, ToolException)
        assert issubclass(EmailSendError, ToolException)
    
    def test_session_exception_inheritance(self):
        """Test Session exceptions inherit from SessionException."""
        assert issubclass(SessionNotFoundError, SessionException)
        assert issubclass(SessionExpiredError, SessionException)
        assert issubclass(SessionStorageError, SessionException)
    
    def test_all_inherit_from_exception(self):
        """Test all custom exceptions inherit from base Exception."""
        assert issubclass(APIException, Exception)
        assert issubclass(AgentException, Exception)
        assert issubclass(ToolException, Exception)
        assert issubclass(SessionException, Exception)
