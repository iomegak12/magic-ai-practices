# Enterprise E2E Use Case — REST API

Production-grade FastAPI service wrapping a **Microsoft Agent Framework** agent with MCP tools, LLM guardrails, SQLite conversation history, and OpenTelemetry observability.

## Architecture

```
Client Request
  │
  ├── FastAPI (Uvicorn on 0.0.0.0:8800)
  │     ├── CORS Middleware
  │     ├── Rate Limit Middleware (optional)
  │     └── Request Logging Middleware
  │
  ├── POST /chat              → Non-streaming response
  ├── POST /chat/stream       → SSE streaming response
  ├── GET  /health            → Liveness probe
  └── GET  /health/readiness  → Readiness probe
        │
        └── AgentManager
              │
              ├── LLMInputGuardrailMiddleware   (blocks PII / toxic / injection / off-topic)
              ├── ExceptionHandlingMiddleware    (catch-all → polished error)
              ├── LLMOutputGuardrailMiddleware   (validates agent response)
              ├── TrackingFunctionMiddleware     (logs + captures tool metadata)
              │
              ├── [Agent Core]
              │     ├── MCP: Microsoft Learn         (learn.microsoft.com/api/mcp)
              │     ├── MCP: Orders & Complaints     (localhost:8700/mcp)
              │     ├── Local: get_weather
              │     ├── Local: get_current_time
              │     └── Local: get_location_info
              │
              └── SQLiteHistoryProvider         (persists conversation to SQLite)
```

## Quick Start

### 1. Environment Setup

```bash
cp .env.example .env
# Edit .env with your Azure OpenAI credentials
```

### 2. Start the MCP Server (dependency)

```bash
cd ../mcp && python main.py
```

### 3. Run the API

```bash
pip install -r requirements.txt
python main.py
```

The server starts on `http://0.0.0.0:8800`. Open `http://localhost:8800/docs` for Swagger UI.

### 4. Docker

```bash
docker compose build
docker compose up -d
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/chat` | Send a message, get complete response with tool usage |
| `POST` | `/chat/stream` | Send a message, receive SSE stream with metadata event |
| `GET` | `/health` | Liveness probe |
| `GET` | `/health/readiness` | Readiness probe (agent + DB checks) |
| `GET` | `/docs` | Swagger UI |
| `GET` | `/redoc` | ReDoc documentation |

### Example: Non-Streaming

```bash
curl -X POST http://localhost:8800/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Get all orders for Priya Sharma"}'
```

Response:
```json
{
  "session_id": "abc-123",
  "response": "Here are the orders for Priya Sharma...",
  "tools_used": [
    {
      "name": "get_orders_by_customer",
      "arguments": {"customer_name": "Priya Sharma"},
      "duration_seconds": 0.45,
      "result_preview": "..."
    }
  ],
  "duration_seconds": 3.21,
  "timestamp": "2026-04-17T10:00:00Z",
  "status": "success"
}
```

### Example: SSE Streaming

```bash
curl -X POST http://localhost:8800/chat/stream \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the weather in Mumbai?"}'
```

SSE events:
```
data: Here
data:  is
data:  the weather
...
event: metadata
data: {"session_id":"abc-123","tools_used":[...],"duration_seconds":2.1,"timestamp":"..."}
data: [DONE]
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `SERVER_HOST` | `0.0.0.0` | Bind address |
| `SERVER_PORT` | `8800` | Listen port |
| `LOG_LEVEL` | `INFO` | Logging level |
| `AZURE_OPENAI_ENDPOINT` | — | Azure OpenAI endpoint URL |
| `AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME` | — | Model deployment name |
| `AZURE_OPENAI_API_KEY` | — | API key (required for guardrails; optional if `AZURE_AUTH_METHOD=cli`) |
| `AZURE_AUTH_METHOD` | `cli` | `cli` (AzureCliCredential) or `api_key` |
| `MCP_ORDERS_URL` | `http://localhost:8700/mcp` | Orders & Complaints MCP server |
| `MCP_LEARN_URL` | `https://learn.microsoft.com/api/mcp` | Microsoft Learn MCP server |
| `ENABLE_RATE_LIMITING` | `false` | Enable per-IP rate limiting |
| `RATE_LIMIT_PER_MINUTE` | `60` | Max requests per IP per minute |
| `ENABLE_CORS` | `true` | Enable CORS (all origins) |
| `ENABLE_OBSERVABILITY` | `false` | Enable OpenTelemetry tracing |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | `http://localhost:4317` | OTLP collector endpoint |
| `DB_PATH` | `./data/conversation_history.db` | SQLite database path |

## Prerequisites

- **Python 3.13+**
- **Orders & Complaints MCP server** running on port 8700
- **Azure OpenAI** resource with a deployed model
- **Jaeger** (optional, for observability)

## License

[MIT](LICENSE)
