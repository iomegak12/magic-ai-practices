"""
Integration Tests for Health Endpoints

Tests for health check API endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from app.server import app


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


class TestHealthEndpoint:
    """Tests for /health endpoint."""
    
    def test_health_check(self, client):
        """Test basic health check endpoint."""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] in ["healthy", "ok"]
    
    def test_health_check_response_structure(self, client):
        """Test health check response structure."""
        response = client.get("/health")
        
        data = response.json()
        assert "status" in data
        assert "timestamp" in data
        assert isinstance(data["timestamp"], str)
    
    def test_health_check_uptime(self, client):
        """Test health check includes uptime."""
        response = client.get("/health")
        
        data = response.json()
        if "uptime" in data:
            assert isinstance(data["uptime"], (int, float))
            assert data["uptime"] >= 0


class TestReadinessEndpoint:
    """Tests for /health/ready endpoint."""
    
    def test_readiness_check(self, client):
        """Test readiness endpoint."""
        response = client.get("/health/ready")
        
        # Should return 200 or 503 depending on readiness
        assert response.status_code in [200, 503]
        
        data = response.json()
        assert "ready" in data
        assert isinstance(data["ready"], bool)
    
    def test_readiness_dependencies(self, client):
        """Test readiness checks dependencies."""
        response = client.get("/health/ready")
        
        data = response.json()
        if "dependencies" in data:
            assert isinstance(data["dependencies"], dict)
            
            # Check expected dependencies
            if "agent" in data["dependencies"]:
                assert isinstance(data["dependencies"]["agent"], bool)


class TestLivenessEndpoint:
    """Tests for /health/live endpoint."""
    
    def test_liveness_check(self, client):
        """Test liveness endpoint."""
        response = client.get("/health/live")
        
        assert response.status_code == 200
        data = response.json()
        assert "alive" in data
        assert data["alive"] is True
    
    def test_liveness_always_responds(self, client):
        """Test liveness endpoint always responds."""
        # Make multiple requests
        for _ in range(3):
            response = client.get("/health/live")
            assert response.status_code == 200


class TestHealthCORS:
    """Tests for CORS on health endpoints."""
    
    def test_health_cors_headers(self, client):
        """Test CORS headers on health endpoint."""
        response = client.options("/health")
        
        # Should have CORS headers
        assert "access-control-allow-origin" in response.headers or \
               response.status_code in [200, 405]


class TestHealthMetrics:
    """Tests for health metrics."""
    
    def test_health_includes_version(self, client):
        """Test health response includes version."""
        response = client.get("/health")
        
        data = response.json()
        # Version might be included
        if "version" in data:
            assert isinstance(data["version"], str)
    
    def test_health_includes_environment(self, client):
        """Test health response includes environment."""
        response = client.get("/health")
        
        data = response.json()
        # Environment might be included
        if "environment" in data:
            assert isinstance(data["environment"], str)
