# Plan: E2E REST API for MAF Agent

Wrap the end-to-end MAF agent from the notebook into a production-grade FastAPI service at `use-cases-day4/e2e-rest-api/`, with streaming/non-streaming chat endpoints, full tool usage tracking, guardrails, SQLite history, and Docker infrastructure.

## Project Structure

```
use-cases-day4/e2e-rest-api/
├── main.py                        # Minimal: ~20 lines, uvicorn.run + signal handlers
├── app/
│   ├── __init__.py
│   ├── factory.py                 # create_app() — FastAPI factory, lifespan, routers
│   ├── agent/
│   │   ├── __init__.py
│   │   ├── builder.py            # build_agent() — assembles full agent from config
│   │   ├── manager.py            # Singleton AgentManager (execute, execute_stream)
│   │   ├── instructions.py       # AGENT_INSTRUCTIONS constant
│   │   └── tools.py              # get_weather, get_current_time, get_location_info
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── chat.py           # POST /chat + POST /chat/stream (SSE)
│   │   │   └── health.py         # GET /health + GET /health/readiness
│   │   ├── models.py             # ChatRequest, ChatResponse, ToolCallInfo, ErrorResponse
│   │   └── errors.py             # Exception classes + handlers
│   ├── middleware/
│   │   ├── __init__.py           # setup_middleware() — CORS, rate limit, request logging
│   │   ├── guardrails.py         # Input/Output guardrail (from notebook)
│   │   ├── exception_handler.py  # ExceptionHandlingMiddleware
│   │   ├── function_logger.py    # TrackingFunctionMiddleware (captures tool metadata via contextvars)
│   │   └── rate_limit.py         # Sliding window per-IP (disabled by default)
│   ├── history/
│   │   └── sqlite_provider.py    # SQLiteHistoryProvider
│   ├── config/
│   │   └── settings.py           # Pydantic BaseSettings, all .env vars
│   └── startup/
│       └── banner.py             # Colorama server config display
├── .env.example / .gitignore / .dockerignore
├── Dockerfile                     # Multi-stage Alpine (python:3.13-alpine)
├── docker-compose.yml             # iomega\end-to-end-rest-service
├── requirements.txt
├── README.md / TROUBLESHOOTING.md / CONTRIBUTING.md / CHANGELOG.md
└── LICENSE                        # MIT
```

## Steps

### Phase 1: Foundation *(parallel)*

1. `config/settings.py` — Pydantic `BaseSettings` with all env vars: server host/port, Azure OpenAI config, `AZURE_AUTH_METHOD` (cli|api_key), MCP URLs, rate limiting toggle, observability toggle, DB path, log level
2. `startup/banner.py` — Colorama-based display of server config (title, host:port, Azure endpoint, MCP URLs, auth method, feature flags)
3. `.env.example` — Template of all env vars

### Phase 2: Agent Layer *(depends on Phase 1)*

4. `agent/instructions.py` — Extract system prompt from notebook
5. `agent/tools.py` — Port 3 local `@tool` functions from notebook
6. `middleware/guardrails.py` — Port guardrail prompts, classifier, `LLMInputGuardrailMiddleware`, `LLMOutputGuardrailMiddleware`
7. `middleware/exception_handler.py` — Port `ExceptionHandlingMiddleware`
8. `middleware/function_logger.py` — **Extended** `TrackingFunctionMiddleware`: uses `contextvars.ContextVar[list[dict]]` to collect `{name, arguments, duration_seconds, result_preview}` per request, exports `get_tool_calls()` / `reset_tool_calls()` for endpoint consumption
9. `history/sqlite_provider.py` — Port `SQLiteHistoryProvider`
10. `agent/builder.py` — `build_agent(settings)`: creates client (cli or API key auth), MCP tools, history provider, guardrail classifier, middleware pipeline, returns assembled agent
11. `agent/manager.py` — Singleton `AgentManager` with `execute()` (returns response + tool metadata + duration) and `execute_stream()` (yields SSE chunks, then metadata event)

### Phase 3: API Layer *(depends on Phase 2)*

12. `api/models.py` — `ChatRequest(message, session_id?)`, `ChatResponse(session_id, response, tools_used: list[ToolCallInfo], duration_seconds, timestamp)`, `HealthResponse`, `ReadinessResponse`, `ErrorResponse(error, message, status_code, timestamp, request_id, details)`
13. `api/errors.py` — Custom exceptions + `setup_exception_handlers(app)` for validation errors, agent errors, catch-all
14. `api/routes/chat.py` — `POST /chat` (non-streaming, returns `ChatResponse`), `POST /chat/stream` (SSE with `data:` text chunks → `event: metadata` with tool info → `data: [DONE]`)
15. `api/routes/health.py` — Liveness + readiness (checks agent, MCP, DB)
16. `middleware/__init__.py` — Wire CORS, rate limiter, request logging (`X-Request-ID`, `X-Response-Time`)
17. `middleware/rate_limit.py` — Sliding window per-IP, 429 with `Retry-After`, skips health/docs paths

### Phase 4: App Assembly *(depends on Phase 3)*

18. `factory.py` — `create_app()` with `FastAPI(title="Enterprise E2E Use Case")`, async lifespan (startup: banner + init agent, shutdown: cleanup), include routers, wire middleware
19. `main.py` — Minimal: import factory, register SIGINT/SIGTERM for graceful shutdown, `uvicorn.run()` on 0.0.0.0:8800

### Phase 5: Infrastructure *(parallel with Phase 3-4)*

20. `requirements.txt` — agent-framework, fastapi, uvicorn, pydantic-settings, colorama, openai, azure-identity
21. `Dockerfile` — Multi-stage: builder (install deps) → runtime (python:3.13-alpine, non-root user, expose 8800)
22. `docker-compose.yml` — No `version:` key, image `iomega/end-to-end-rest-service`, port 8800, env_file, healthcheck
23. `.gitignore`, `.dockerignore` — Standard Python + .env, *.db, data/
24. `LICENSE` — MIT
25. `README.md` — Overview, architecture, setup, endpoints, env vars, Docker, examples
26. `TROUBLESHOOTING.md` — MCP down, auth failures, port conflicts, rate limiting
27. `CONTRIBUTING.md` — Code style, PR process
28. `CHANGELOG.md` — v1.0.0 entry

## Key Design Decisions

- **Tool tracking**: `contextvars.ContextVar` in `TrackingFunctionMiddleware` collects tool call metadata per-request, consumed by the endpoint after `agent.run()` completes. For streaming, tool info is sent as a final `event: metadata` SSE event before `[DONE]`
- **Sessions**: Optional `session_id` in `ChatRequest` — if provided, the manager resumes that session; if omitted, a new session is auto-created and its ID returned in the response
- **Auth flexibility**: `AZURE_AUTH_METHOD=cli` uses `AzureCliCredential` (dev), `api_key` uses API key (production/Docker)
- **Guardrails use a separate sync client** (API key auth, `temperature=0.0`, JSON mode) — same as notebook
- **Observability is opt-in**: When `ENABLE_OBSERVABILITY=false`, `configure_otel_providers()` is skipped entirely

## Verification

1. `python main.py` — colorama banner displays, agent initializes, server on 0.0.0.0:8800
2. `http://localhost:8800/docs` — Swagger UI shows all endpoints with models
3. `POST /chat` with `{"message": "Get all orders for Priya Sharma"}` — response includes `tools_used`, `duration_seconds`
4. `POST /chat/stream` — SSE chunks flow, metadata event with tools, `[DONE]` sentinel
5. Two requests with same `session_id` — second recalls first conversation
6. PII/off-topic/injection messages — blocked by guardrails with refusal
7. Enable rate limiting → rapid requests → 429 after limit
8. `GET /health` → 200, `GET /health/readiness` → checks components
9. Malformed request → structured `ErrorResponse`
10. `docker compose build && docker compose up` → container serves endpoints
11. Ctrl+C → clean shutdown logs

## Further Considerations

1. **MCP server dependency** — If the Orders & Complaints MCP server (port 8700) is down, the agent still starts but those tools fail at runtime. The readiness endpoint reflects this.
2. **Observability toggle** — When disabled, no OTel dependency needed at runtime. The agent works without Jaeger.
