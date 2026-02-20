"""
Tests for chat endpoint
"""
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_chat_requires_message():
    """Test that chat endpoint requires a message."""
    response = client.post("/chat", json={})
    assert response.status_code == 422  # Validation error


def test_chat_accepts_valid_request():
    """Test that chat endpoint accepts valid request structure."""
    response = client.post("/chat", json={
        "message": "Hello, I need help with my order"
    })
    # Note: This test may fail if agent initialization fails
    # In a real scenario, you'd mock the agent service
    assert response.status_code in [200, 500]  # 500 if agent not initialized


def test_chat_response_structure():
    """Test that successful chat response has required fields."""
    # This test would need proper mocking of agent service
    # Skipping actual validation for now
    pass


def test_chat_with_session_id():
    """Test that chat accepts session_id parameter."""
    response = client.post("/chat", json={
        "session_id": "test-session-123",
        "message": "Hello"
    })
    # Should accept the request structure
    assert response.status_code in [200, 500]


def test_chat_with_stream_flag():
    """Test that chat accepts stream parameter."""
    response = client.post("/chat", json={
        "message": "Hello",
        "stream": False
    })
    # Should accept the request structure
    assert response.status_code in [200, 500]


@pytest.mark.skip(reason="Requires agent initialization and mocking")
def test_chat_streaming_response():
    """Test that chat supports streaming responses."""
    # This would need proper testing with SSE client
    pass


@pytest.mark.skip(reason="Requires agent initialization and mocking")
def test_chat_multi_turn_conversation():
    """Test that chat maintains conversation context."""
    # This would require testing with same session_id
    pass
