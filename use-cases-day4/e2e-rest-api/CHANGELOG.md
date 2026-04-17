# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [1.0.0] - 2026-04-17

### Added

- FastAPI REST API with Uvicorn server on `0.0.0.0:8800`
- `POST /chat` — non-streaming chat endpoint with full response metadata
- `POST /chat/stream` — SSE streaming endpoint with metadata event
- `GET /health` — liveness probe
- `GET /health/readiness` — readiness probe (agent, database checks)
- Microsoft Agent Framework agent with:
  - 2 MCP tools (Microsoft Learn, Orders & Complaints)
  - 3 local tools (weather, time, location)
  - 4-layer middleware pipeline (input guardrail, exception handler, output guardrail, function tracker)
  - SQLite-backed conversation history provider
- LLM-based input/output guardrails (PII, toxic, injection, off-topic detection)
- Tool usage tracking via `contextvars` — response includes tool names, arguments, durations
- Optional session resumption via `session_id` parameter
- Configurable Azure auth (`AZURE_AUTH_METHOD=cli|api_key`)
- CORS support (all origins, enabled by default)
- Per-IP sliding window rate limiting (disabled by default, configurable via `.env`)
- Request logging with `X-Request-ID` and `X-Response-Time` headers
- OpenTelemetry observability (opt-in via `ENABLE_OBSERVABILITY`)
- Colorama-based startup banner displaying server configuration
- Graceful shutdown on SIGINT/SIGTERM
- Standardized `ErrorResponse` model for all error types
- Multi-stage Alpine Docker build
- Docker Compose configuration
- OpenAPI/Swagger documentation at `/docs` and `/redoc`
