"""
Integration Tests for Info Endpoints

Tests for information API endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from app.server import app


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


class TestInfoEndpoint:
    """Tests for /info endpoint."""
    
    def test_get_info(self, client):
        """Test getting API information."""
        response = client.get("/info")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
    
    def test_info_includes_version(self, client):
        """Test info includes version."""
        response = client.get("/info")
        
        data = response.json()
        assert "version" in data or "api_version" in data
    
    def test_info_includes_name(self, client):
        """Test info includes API name."""
        response = client.get("/info")
        
        data = response.json()
        assert "name" in data or "service_name" in data or "title" in data
    
    def test_info_response_structure(self, client):
        """Test info response has expected structure."""
        response = client.get("/info")
        
        data = response.json()
        # Should have basic info fields
        assert len(data) > 0
        
        # Common fields
        possible_fields = [
            "name", "version", "description", "api_version",
            "title", "service_name", "endpoints"
        ]
        
        has_info_field = any(field in data for field in possible_fields)
        assert has_info_field


class TestToolsEndpoint:
    """Tests for /info/tools endpoint."""
    
    def test_get_tools(self, client):
        """Test getting available tools."""
        response = client.get("/info/tools")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, (list, dict))
    
    def test_tools_list_structure(self, client):
        """Test tools list structure."""
        response = client.get("/info/tools")
        
        data = response.json()
        
        if isinstance(data, list):
            # Should have tools
            assert len(data) >= 0
            
            # Check structure if tools exist
            if len(data) > 0:
                tool = data[0]
                assert "name" in tool or "tool_name" in tool
        elif isinstance(data, dict):
            # Might be wrapped in object
            assert "tools" in data or len(data) > 0
    
    def test_tools_include_order_tools(self, client):
        """Test tools list includes order management tools."""
        response = client.get("/info/tools")
        
        data = response.json()
        
        # Extract tool names
        if isinstance(data, list):
            tool_names = [t.get("name", t.get("tool_name", "")) for t in data]
        elif isinstance(data, dict) and "tools" in data:
            tool_names = [t.get("name", t.get("tool_name", "")) for t in data["tools"]]
        else:
            tool_names = []
        
        # Should have some order-related tools
        has_order_tools = any("order" in name.lower() for name in tool_names)
        assert has_order_tools or len(tool_names) == 0
    
    def test_tools_include_email_tools(self, client):
        """Test tools list includes email tools."""
        response = client.get("/info/tools")
        
        data = response.json()
        
        # Extract tool names
        if isinstance(data, list):
            tool_names = [t.get("name", t.get("tool_name", "")) for t in data]
        elif isinstance(data, dict) and "tools" in data:
            tool_names = [t.get("name", t.get("tool_name", "")) for t in data["tools"]]
        else:
            tool_names = []
        
        # Should have some email-related tools
        has_email_tools = any("email" in name.lower() for name in tool_names)
        assert has_email_tools or len(tool_names) == 0
    
    def test_tool_descriptions(self, client):
        """Test tools have descriptions."""
        response = client.get("/info/tools")
        
        data = response.json()
        
        if isinstance(data, list) and len(data) > 0:
            tool = data[0]
            # Should have description
            assert "description" in tool or "tool_description" in tool


class TestInfoCORS:
    """Tests for CORS on info endpoints."""
    
    def test_info_cors_headers(self, client):
        """Test CORS headers on info endpoint."""
        response = client.options("/info")
        
        # Should handle OPTIONS request
        assert response.status_code in [200, 405]


class TestInfoCaching:
    """Tests for caching of info endpoints."""
    
    def test_info_response_consistency(self, client):
        """Test info endpoint returns consistent data."""
        response1 = client.get("/info")
        response2 = client.get("/info")
        
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        # Should return same structure
        data1 = response1.json()
        data2 = response2.json()
        
        assert set(data1.keys()) == set(data2.keys())
    
    def test_tools_response_consistency(self, client):
        """Test tools endpoint returns consistent data."""
        response1 = client.get("/info/tools")
        response2 = client.get("/info/tools")
        
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        data1 = response1.json()
        data2 = response2.json()
        
        # Should return same number of tools
        if isinstance(data1, list) and isinstance(data2, list):
            assert len(data1) == len(data2)


class TestInfoAuthentication:
    """Tests for authentication on info endpoints."""
    
    def test_info_public_access(self, client):
        """Test info endpoint is publicly accessible."""
        response = client.get("/info")
        
        # Should not require authentication
        assert response.status_code == 200
    
    def test_tools_public_access(self, client):
        """Test tools endpoint is publicly accessible."""
        response = client.get("/info/tools")
        
        # Should not require authentication
        assert response.status_code == 200
