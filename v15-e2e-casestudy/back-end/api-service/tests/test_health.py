"""
Tests for health endpoint
"""
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_check_returns_200():
    """Test that health check returns 200 OK."""
    response = client.get("/health")
    assert response.status_code == 200


def test_health_check_has_required_fields():
    """Test that health check response has all required fields."""
    response = client.get("/health")
    data = response.json()
    
    assert "status" in data
    assert "service" in data
    assert "version" in data
    assert "timestamp" in data
    assert "dependencies" in data


def test_health_check_service_name():
    """Test that health check returns correct service name."""
    response = client.get("/health")
    data = response.json()
    
    assert data["service"] == "MSAv15Service"
    assert data["version"] == "0.1.0"


def test_health_check_dependencies():
    """Test that health check includes dependency status."""
    response = client.get("/health")
    data = response.json()
    
    assert "database" in data["dependencies"]
    assert "mcp_server" in data["dependencies"]


def test_health_check_status_values():
    """Test that status is one of expected values."""
    response = client.get("/health")
    data = response.json()
    
    assert data["status"] in ["healthy", "degraded"]
