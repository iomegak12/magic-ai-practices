# Front-End Integration Guide

**Base URL:** `http://localhost:8800`

**Interactive API Docs:** [Swagger UI](http://localhost:8800/docs) · [ReDoc](http://localhost:8800/redoc)

---

## Table of Contents

1. [Chat — Non-Streaming](#1-chat--non-streaming)
2. [Chat — SSE Streaming](#2-chat--sse-streaming)
3. [Health — Liveness Probe](#3-health--liveness-probe)
4. [Health — Readiness Probe](#4-health--readiness-probe)
5. [Session Management](#5-session-management)
6. [SSE Stream Protocol](#6-sse-stream-protocol)
7. [Error Handling](#7-error-handling)
8. [Rate Limiting](#8-rate-limiting)
9. [Response Headers](#9-response-headers)

---

## 1. Chat — Non-Streaming

Send a message and receive the complete agent response in a single JSON payload.

| | |
|---|---|
| **Method** | `POST` |
| **Path** | `/chat` |
| **Content-Type** | `application/json` |

### Request Body

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `message` | `string` | Yes | 1–10,000 chars | The user message to send to the agent |
| `session_id` | `string \| null` | No | UUID format | Session ID to resume an existing conversation. Omit to create a new session |

### Response Body — `200 OK`

| Field | Type | Description |
|-------|------|-------------|
| `session_id` | `string` | Session ID for this conversation (use this to continue the conversation) |
| `response` | `string` | The agent's full response text |
| `tools_used` | `ToolCallInfo[]` | Array of tools invoked during the agent run (see below) |
| `duration_seconds` | `number` | Total wall-clock time for the agent run (seconds) |
| `timestamp` | `string` | ISO-8601 UTC timestamp of the response |
| `status` | `string` | Always `"success"` for successful responses |

### `ToolCallInfo` Object

| Field | Type | Description |
|-------|------|-------------|
| `name` | `string` | Name of the tool that was called |
| `arguments` | `object` | Key-value arguments passed to the tool |
| `duration_seconds` | `number` | Execution time for this tool call (seconds) |
| `result_preview` | `string \| null` | Truncated preview of the tool result (max 200 chars) |

### Example

```bash
curl -X POST http://localhost:8800/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Get all orders for Priya Sharma"
  }'
```

```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "response": "Here are the orders for Priya Sharma:\n\n1. **ORD-1001** — Wireless Mouse (SKU: TECH-001) — Delivered\n2. **ORD-1002** — USB-C Hub (SKU: TECH-042) — Shipped",
  "tools_used": [
    {
      "name": "get_orders_by_customer",
      "arguments": { "customer_name": "Priya Sharma" },
      "duration_seconds": 0.45,
      "result_preview": "[{\"order_id\": \"ORD-1001\", \"customer\": \"Priya Sharma\", ..."
    }
  ],
  "duration_seconds": 3.21,
  "timestamp": "2026-04-17T10:00:00.000000+00:00",
  "status": "success"
}
```

---

## 2. Chat — SSE Streaming

Send a message and receive the agent's response as a **Server-Sent Events** stream. Tokens arrive incrementally, followed by a metadata event with tool usage details.

| | |
|---|---|
| **Method** | `POST` |
| **Path** | `/chat/stream` |
| **Content-Type** (request) | `application/json` |
| **Content-Type** (response) | `text/event-stream` |

### Request Body

Identical to the non-streaming endpoint (see [Section 1](#1-chat--non-streaming)).

### SSE Event Protocol

The stream emits three types of events in this order:

| Event Type | Format | Description |
|------------|--------|-------------|
| **Text chunks** | `data: <text>\n\n` | Incremental response tokens. Concatenate all `data:` values to build the full response |
| **Metadata** | `event: metadata\ndata: <json>\n\n` | Single JSON event with session/tool/timing metadata (see below) |
| **Done sentinel** | `data: [DONE]\n\n` | Signals the end of the stream. Close the connection after receiving this |
| **Error** (if applicable) | `event: error\ndata: <message>\n\n` | Emitted on agent failure, followed by `[DONE]` |

### Metadata Event Payload

| Field | Type | Description |
|-------|------|-------------|
| `session_id` | `string` | Session ID for this conversation |
| `tools_used` | `ToolCallInfo[]` | Array of tools invoked (same structure as non-streaming) |
| `duration_seconds` | `number` | Total wall-clock time (seconds) |
| `timestamp` | `string` | ISO-8601 UTC timestamp |

### Example

```bash
curl -N -X POST http://localhost:8800/chat/stream \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is the weather in Mumbai?",
    "session_id": "550e8400-e29b-41d4-a716-446655440000"
  }'
```

```
data: The

data:  weather

data:  in Mumbai

data:  is sunny

data:  with a high

data:  of 35°C.

event: metadata
data: {"session_id":"550e8400-...","tools_used":[{"name":"get_weather","arguments":{"location":"Mumbai"},"duration_seconds":0.02,"result_preview":"The weather in Mumbai is sunny with a high of 35°C."}],"duration_seconds":2.10,"timestamp":"2026-04-17T10:01:00.000000+00:00"}

data: [DONE]
```

---

## 3. Health — Liveness Probe

Lightweight check confirming the server process is alive.

| | |
|---|---|
| **Method** | `GET` |
| **Path** | `/health` |

### Response Body — `200 OK`

| Field | Type | Description |
|-------|------|-------------|
| `status` | `string` | Always `"healthy"` |
| `timestamp` | `string` | ISO-8601 UTC timestamp |
| `version` | `string` | Application version (e.g., `"1.0.0"`) |
| `uptime_seconds` | `number` | Server uptime in seconds |

### Example

```bash
curl http://localhost:8800/health
```

```json
{
  "status": "healthy",
  "timestamp": "2026-04-17T10:00:00.000000+00:00",
  "version": "1.0.0",
  "uptime_seconds": 3600.42
}
```

---

## 4. Health — Readiness Probe

Checks whether the agent and database are operational. Use this before sending chat requests.

| | |
|---|---|
| **Method** | `GET` |
| **Path** | `/health/readiness` |

### Response Body — `200 OK`

| Field | Type | Description |
|-------|------|-------------|
| `ready` | `boolean` | `true` if all components are operational |
| `status` | `string` | `"ready"` or `"degraded"` |
| `timestamp` | `string` | ISO-8601 UTC timestamp |
| `checks` | `object` | Component-level check results (see below) |

### `checks` Object

Each key is a component name (`"agent"`, `"database"`), and each value has:

| Field | Type | Description |
|-------|------|-------------|
| `status` | `string` | `"ok"`, `"degraded"`, or `"fail"` |
| `detail` | `string \| null` | Human-readable status description |

### Example

```bash
curl http://localhost:8800/health/readiness
```

```json
{
  "ready": true,
  "status": "ready",
  "timestamp": "2026-04-17T10:00:00.000000+00:00",
  "checks": {
    "agent": { "status": "ok", "detail": "Agent is initialized" },
    "database": { "status": "ok", "detail": "SQLite accessible" }
  }
}
```

---

## 5. Session Management

Sessions enable **multi-turn conversations** where the agent remembers prior context.

| Scenario | What to send |
|----------|-------------|
| **Start a new conversation** | Omit `session_id` (or set to `null`) |
| **Continue an existing conversation** | Pass the `session_id` from a previous response |

- Every response (both streaming metadata and non-streaming) includes a `session_id`.
- Store this value on the front-end and pass it back in subsequent requests to maintain conversation continuity.
- Sessions persist server-side. Conversation history is stored in SQLite, so sessions survive server restarts.

---

## 6. SSE Stream Protocol

Detailed rules for consuming the streaming endpoint:

1. **Open the connection** as a `POST` request with `Content-Type: application/json`. The response is `text/event-stream`.
2. **Read `data:` lines** — each carries a text fragment. Concatenate them to build the full response.
3. **Watch for `event: metadata`** — the next `data:` line after this contains a JSON object with `session_id`, `tools_used`, `duration_seconds`, and `timestamp`.
4. **Watch for `event: error`** — if the agent fails mid-stream, an error event is emitted with a human-readable message. The stream still ends with `[DONE]`.
5. **Close on `data: [DONE]`** — this sentinel signals the stream is complete. Close the EventSource / reader.

### Important Notes

- The SSE response includes these headers: `Cache-Control: no-cache`, `Connection: keep-alive`, `X-Accel-Buffering: no`.
- If using a reverse proxy (e.g., Nginx), disable response buffering for `/chat/stream`.
- The `[DONE]` value is a literal string, not JSON.

---

## 7. Error Handling

All errors use a **consistent JSON envelope**:

| Field | Type | Description |
|-------|------|-------------|
| `error` | `string` | Short error type identifier |
| `message` | `string` | Human-readable error description |
| `status_code` | `number` | HTTP status code |
| `timestamp` | `string` | ISO-8601 UTC timestamp |
| `request_id` | `string \| null` | Correlation ID (from `X-Request-ID` header) |
| `details` | `ErrorDetail[] \| null` | Field-level validation errors (only for 422) |

### `ErrorDetail` Object (422 responses only)

| Field | Type | Description |
|-------|------|-------------|
| `code` | `string` | Always `"validation_error"` |
| `message` | `string` | What's wrong |
| `field` | `string \| null` | Dot-separated field path (e.g., `"body.message"`) |

### HTTP Status Codes

| Code | Error Type | Meaning |
|------|-----------|---------|
| `422` | `validation_error` | Request body failed validation (missing/invalid fields) |
| `429` | `rate_limit_exceeded` | Too many requests — check `Retry-After` header |
| `500` | `internal_error` | Unexpected server error |
| `502` | `agent_execution_error` | Agent encountered an error during processing |
| `503` | `agent_not_initialized` | Server is starting up — agent not ready yet |

### Example — Validation Error (422)

```bash
curl -X POST http://localhost:8800/chat \
  -H "Content-Type: application/json" \
  -d '{}'
```

```json
{
  "error": "validation_error",
  "message": "Request validation failed.",
  "status_code": 422,
  "timestamp": "2026-04-17T10:00:00.000000+00:00",
  "request_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "details": [
    {
      "code": "validation_error",
      "message": "Field required",
      "field": "body.message"
    }
  ]
}
```

### Example — Agent Not Ready (503)

```json
{
  "error": "agent_not_initialized",
  "message": "The agent has not been initialized yet. Please try again shortly.",
  "status_code": 503,
  "timestamp": "2026-04-17T10:00:00.000000+00:00",
  "request_id": null,
  "details": null
}
```

---

## 8. Rate Limiting

When rate limiting is enabled on the server, the following applies:

| Header | Description |
|--------|-------------|
| `X-RateLimit-Limit` | Maximum requests allowed per window |
| `X-RateLimit-Remaining` | Requests remaining in the current window |
| `X-RateLimit-Reset` | Seconds until the rate limit window resets |
| `Retry-After` | (429 only) Seconds to wait before retrying |

- Rate limiting is **per IP address** with a sliding window.
- Paths excluded from rate limiting: `/health`, `/health/readiness`, `/docs`, `/redoc`, `/openapi.json`.
- If you receive a `429`, wait for the number of seconds in the `Retry-After` header before retrying.

---

## 9. Response Headers

Every response includes these custom headers:

| Header | Description |
|--------|-------------|
| `X-Request-ID` | Unique UUID for request correlation / debugging |
| `X-Response-Time` | Server-side processing time (e.g., `"1.234s"`) |

- Pass the `X-Request-ID` value when reporting issues to the back-end team.
- CORS is enabled for all origins by default.

---

## Quick Reference

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/chat` | `POST` | Non-streaming chat |
| `/chat/stream` | `POST` | SSE streaming chat |
| `/health` | `GET` | Liveness probe |
| `/health/readiness` | `GET` | Readiness probe |
| `/docs` | `GET` | Swagger UI |
| `/redoc` | `GET` | ReDoc documentation |
| `/openapi.json` | `GET` | OpenAPI spec (machine-readable) |
