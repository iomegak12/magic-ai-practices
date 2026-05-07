"""API key bearer authentication provider for FastMCP."""

from __future__ import annotations

from fastmcp.server.auth.providers.jwt import StaticTokenVerifier

from magic_v22_mcp.config import get_settings


def build_auth_provider() -> StaticTokenVerifier:
    """Return a FastMCP StaticTokenVerifier that accepts a single API key.

    Clients send:  Authorization: Bearer <API_KEY>
    The API_KEY value comes from the .env file.
    """
    settings = get_settings()
    return StaticTokenVerifier(
        tokens={
            settings.api_key: {
                "client_id": "api-client",
                "sub": "api-client",
            }
        }
    )
