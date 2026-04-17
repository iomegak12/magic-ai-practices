# API Specification

**Version:** 0.1.0  
**Base URL:** `http://localhost:9080`  
**Last Updated:** February 20, 2026 *(reconciled with backend-openapi.json)*

## Table of Contents

- [Overview](#overview)
- [Base URL Configuration](#base-url-configuration)
- [Headers](#headers)
- [Response Format](#response-format)
- [Error Handling](#error-handling)
- [Rate Limiting](#rate-limiting)
- [Endpoints](#endpoints)
  - [Root](#root)
  - [Health Checks](#health-checks)
  - [Agent Operations](#agent-operations)
  - [Session Management](#session-management)
  - [API Information](#api-information)

---

## Overview

The Customer Service Agent API provides an AI-powered conversational interface with capabilities for:
- Multi-turn conversations with session management
- Order management (search, track, modify)
- Email communication
- Complaint tracking via MCP integration

## Base URL Configuration

**Development:** `http://localhost:9080`  
**Production:** Configure via environment variable

All endpoints are relative to the base URL.

## Headers

### Standard Request Headers

```http
Content-Type: application/json
Accept: application/json
X-Request-ID: <optional-uuid>  # For request tracing
X-Tenant-ID: <optional-tenant-id>  # For multi-tenancy (default: "default")
```

### Standard Response Headers

```http
Content-Type: application/json
X-Request-ID: <uuid>  # Request correlation ID
X-Response-Time: <duration>ms  # Request processing time
X-RateLimit-Limit: <number>  # Max requests per minute (if rate limiting enabled)
X-RateLimit-Remaining: <number>  # Remaining requests
X-RateLimit-Reset: <unix-timestamp>  # Rate limit reset time
```

## Response Format

### Success Response

```json
{
  "status": "success",
  "data": { ... },
  "message": "Optional success message",
  "timestamp": "2026-02-20T10:30:00Z"
}
```

### Error Response

```json
{
  "error": "Error Type",
  "detail": "Detailed error message",
  "timestamp": "2026-02-20T10:30:00Z",
  "path": "/api/v1/endpoint",
  "request_id": "uuid-here"
}
```

## Error Handling

### HTTP Status Codes

| Status Code | Meaning | Action |
|------------|---------|--------|
| 200 | Success | Process response |
| 201 | Created | Resource created successfully |
| 400 | Bad Request | Fix request payload |
| 404 | Not Found | Resource doesn't exist |
| 410 | Gone | Resource expired (session) |
| 429 | Too Many Requests | Implement backoff, check Retry-After header |
| 500 | Internal Server Error | Retry with exponential backoff |
| 503 | Service Unavailable | Service temporarily down, retry later |

### Error Types

```typescript
type ErrorType = 
  | "Validation Error"          // 400 - Invalid request data
  | "Session Not Found"         // 404 - Session doesn't exist
  | "Session Expired"           // 410 - Session TTL exceeded
  | "Resource Not Found"        // 404 - General not found
  | "Rate Limit Exceeded"       // 429 - Too many requests
  | "Service Error"             // 500 - Agent/tool errors
  | "Internal Server Error";    // 500 - Unknown errors
```

## Rate Limiting

When rate limiting is enabled (check `/` endpoint for configuration):

**429 Response:**
```json
{
  "error": "Rate Limit Exceeded",
  "detail": "Too many requests. Try again in 45 seconds.",
  "retry_after": 45,
  "request_id": "uuid"
}
```

**Headers:**
- `Retry-After`: Seconds to wait before retrying
- `X-RateLimit-Limit`: Requests per minute limit
- `X-RateLimit-Remaining`: 0
- `X-RateLimit-Reset`: Unix timestamp when limit resets

**Client Handling:**
1. Check `X-RateLimit-Remaining` header
2. If 0, wait for `X-RateLimit-Reset` time
3. Implement exponential backoff on 429 errors

---

## Endpoints

## Root

### Get API Information

**Endpoint:** `GET /`

**Description:** Returns basic API metadata and documentation links.

**Request:**
```http
GET / HTTP/1.1
Host: localhost:9080
```

**Response:** `200 OK`
```json
{
  "name": "Customer Service Agent API",
  "version": "0.1.0",
  "status": "operational",
  "documentation": "/docs",
  "health": "/health",
  "openapi": "/openapi.json"
}
```

---

## Health Checks

### Health Check

**Endpoint:** `GET /health`

**Description:** Basic health check for load balancers.

**Request:**
```http
GET /health HTTP/1.1
Host: localhost:9080
```

**Response:** `200 OK`
```json
{
  "status": "healthy",
  "timestamp": "2026-02-20T10:30:00.123456Z",
  "version": "0.1.0",
  "uptime_seconds": 3600.5,
  "checks": {
    "agent_manager": true,
    "database": true,
    "mcp_server": false
  }
}
```

**Response Schema:**
```typescript
interface HealthCheckResponse {
  status: string;                      // "healthy" | "degraded" | "unhealthy"
  timestamp: string;                   // ISO 8601 timestamp
  version: string;                     // API version
  uptime_seconds: number;              // Server uptime in seconds
  checks: Record<string, boolean>;     // Component health: true = healthy
}
```

### Readiness Check

**Endpoint:** `GET /health/ready`

**Description:** Checks if service is ready to accept traffic (dependencies available).

**Request:**
```http
GET /health/ready HTTP/1.1
Host: localhost:9080
```

**Response:** `200 OK`
```json
{
  "ready": true,
  "status": "ready",
  "timestamp": "2026-02-20T10:30:00.123456Z",
  "components": {
    "agent_manager": true,
    "database": true,
    "mcp_server": false
  }
}
```

**Response (Not Ready):** `503 Service Unavailable`
```json
{
  "ready": false,
  "status": "not_ready",
  "timestamp": "2026-02-20T10:30:00.123456Z",
  "components": {
    "agent_manager": false,
    "database": false
  }
}
```

**Response Schema:**
```typescript
interface ReadinessCheckResponse {
  ready: boolean;                       // Whether the service is ready
  status: string;                       // "ready" or "not_ready"
  timestamp: string;                    // ISO 8601 timestamp
  components: Record<string, boolean>;  // Component readiness: true = ready
}
```

### Liveness Check

**Endpoint:** `GET /health/live`

**Description:** Checks if the service is alive (for restart detection).

**Request:**
```http
GET /health/live HTTP/1.1
Host: localhost:9080
```

**Response:** `200 OK`
```json
{
  "status": "alive",
  "timestamp": "2026-02-20T10:30:00.123456Z"
}
```

---

## Agent Operations

### Create Session

**Endpoint:** `POST /agent/sessions`

**Description:** Create a new conversation session with the agent.

**Request:**
```http
POST /agent/sessions HTTP/1.1
Host: localhost:9080
Content-Type: application/json

{
  "session_id": "optional-custom-id",
  "tenant_id": "default",
  "metadata": {
    "user_name": "John Doe",
    "channel": "web",
    "custom_field": "value"
  }
}
```

**Request Schema:**
```typescript
interface CreateSessionRequest {
  session_id?: string;            // Optional custom session ID (generated if omitted)
  tenant_id?: string;             // Optional tenant identifier (default: "default")
  metadata?: Record<string, any>; // Optional metadata
}
```

**Response:** `201 Created`
```json
{
  "session_id": "sess_abc123xyz",
  "status": "created",
  "message": "Session created successfully",
  "created_at": "2026-02-20T10:30:00.123456Z",
  "metadata": {
    "user_name": "John Doe",
    "channel": "web",
    "custom_field": "value"
  }
}
```

**Response Schema:**
```typescript
interface CreateSessionResponse {
  session_id: string;
  status: "created";
  message: string;
  created_at: string;  // ISO 8601 timestamp
  metadata?: Record<string, any>;
}
```

**Error Responses:**
- `400 Bad Request` - Invalid request format
- `500 Internal Server Error` - Session creation failed

---

### Send Message

**Endpoint:** `POST /agent/messages`

**Description:** Send a message to the agent in an existing session.

**Request:**
```http
POST /agent/messages HTTP/1.1
Host: localhost:9080
Content-Type: application/json

{
  "session_id": "sess_abc123xyz",
  "message": "What's the status of my order ORD-10001?",
  "tenant_id": "default",
  "stream": false
}
```

**Request Schema:**
```typescript
interface SendMessageRequest {
  session_id: string;   // Required session ID
  message: string;      // User message content (max 10,000 chars)
  tenant_id?: string;   // Optional tenant identifier (default: "default")
  stream?: boolean;     // Stream the response — not yet implemented (default: false)
}
```

**Response:** `200 OK`
```json
{
  "session_id": "sess_abc123xyz",
  "response": "Your order ORD-10001 is currently in transit and expected to arrive on February 25, 2026.",
  "status": "success",
  "timestamp": "2026-02-20T10:30:05.789Z",
  "metadata": {
    "request_id": "req_xyz789",
    "tool_calls": ["search_orders"],
    "processing_time_ms": 1234
  }
}
```

**Response Schema:**
```typescript
interface SendMessageResponse {
  session_id: string;
  response: string;           // Agent's response message
  status: "success";
  timestamp: string;          // ISO 8601 timestamp
  metadata: {
    request_id: string;
    tool_calls?: string[];    // Tools the agent used
    processing_time_ms?: number;
  };
}
```

**Error Responses:**
- `400 Bad Request` - Invalid message format
- `404 Not Found` - Session doesn't exist
- `500 Internal Server Error` - Agent execution failed
- `503 Service Unavailable` - Agent service not initialized

**Notes:**
- If session doesn't exist, it will be automatically created with the provided session_id
- Long messages may take longer to process; implement timeout handling (recommended: 60s)

---

### List Sessions

**Endpoint:** `GET /agent/sessions`

**Description:** List all active conversation sessions.

**Request:**
```http
GET /agent/sessions HTTP/1.1
Host: localhost:9080
```

**Response:** `200 OK`
```json
{
  "sessions": [
    {
      "session_id": "sess_abc123xyz",
      "created_at": "2026-02-20T10:00:00Z",
      "message_count": 5,
      "last_activity": "2026-02-20T10:30:00Z"
    },
    {
      "session_id": "sess_def456uvw",
      "created_at": "2026-02-20T09:45:00Z",
      "message_count": 12,
      "last_activity": "2026-02-20T10:25:00Z"
    }
  ],
  "total_count": 2,
  "status": "success"
}
```

**Response Schema:**
```typescript
interface SessionInfo {
  session_id: string;
  created_at: string;      // ISO 8601 timestamp
  message_count: number;
  last_activity: string;   // ISO 8601 timestamp
}

interface ListSessionsResponse {
  sessions: SessionInfo[];
  total_count: number;
  status: "success";
}
```

**Error Responses:**
- `500 Internal Server Error` - Failed to retrieve sessions
- `503 Service Unavailable` - Agent service not initialized

---

### Delete Session

**Endpoint:** `DELETE /agent/sessions/{session_id}`

**Description:** Delete a conversation session and its history.

**Request:**
```http
DELETE /agent/sessions/sess_abc123xyz HTTP/1.1
Host: localhost:9080
```

**Path Parameters:**
- `session_id` (string, required) - Session ID to delete

**Response:** `200 OK`
```json
{
  "session_id": "sess_abc123xyz",
  "status": "deleted",
  "message": "Session deleted successfully"
}
```

**Response Schema:**
```typescript
interface DeleteSessionResponse {
  session_id: string;
  status: "deleted";
  message: string;
}
```

**Error Responses:**
- `404 Not Found` - Session doesn't exist
- `500 Internal Server Error` - Deletion failed
- `503 Service Unavailable` - Agent service not initialized

---

## Session Management

### Get Session History

**Endpoint:** `GET /api/v1/sessions/{session_id}/history`

**Description:** Retrieve the complete conversation history for a session.

**Request:**
```http
GET /api/v1/sessions/sess_abc123xyz/history?tenant_id=customer_acme HTTP/1.1
Host: localhost:9080
```

**Path Parameters:**
- `session_id` (string, required) - Session ID

**Query Parameters:**
- `tenant_id` (string, optional, default: "default") - Tenant identifier for multi-tenancy

**Response:** `200 OK`
```json
{
  "session_id": "sess_abc123xyz",
  "tenant_id": "customer_acme",
  "message_count": 4,
  "created_at": "2026-02-20T10:00:00.123456Z",
  "last_activity": "2026-02-20T10:30:00.789Z",
  "messages": [
    {
      "role": "user",
      "content": "Hello, I need help with my order",
      "timestamp": "2026-02-20T10:00:15.123456Z"
    },
    {
      "role": "assistant",
      "content": "Hello! I'd be happy to help you with your order. Could you please provide your order number?",
      "timestamp": "2026-02-20T10:00:18.456789Z",
      "tool_calls": null
    },
    {
      "role": "user",
      "content": "It's ORD-10001",
      "timestamp": "2026-02-20T10:00:45.123456Z"
    },
    {
      "role": "assistant",
      "content": "I found your order ORD-10001. It was placed on February 15, 2026, and is currently in transit.",
      "timestamp": "2026-02-20T10:00:50.789Z",
      "tool_calls": ["search_orders"]
    }
  ]
}
```

**Response Schema:**
```typescript
interface SessionMessage {
  role: "user" | "assistant" | "system";
  content: string;
  timestamp: string;  // ISO 8601 timestamp
  tool_calls?: string[] | null;  // Tools used by assistant
}

interface SessionHistoryResponse {
  session_id: string;
  tenant_id: string;
  message_count: number;
  created_at: string;
  last_activity: string;
  messages: SessionMessage[];
}
```

**Error Responses:**
- `404 Not Found` - Session doesn't exist
- `410 Gone` - Session expired (TTL exceeded)
- `500 Internal Server Error` - Failed to retrieve history

---

### Delete Session (Management)

**Endpoint:** `DELETE /api/v1/sessions/{session_id}`

**Description:** Delete a session by session ID and tenant ID.

**Request:**
```http
DELETE /api/v1/sessions/sess_abc123xyz?tenant_id=customer_acme HTTP/1.1
Host: localhost:9080
```

**Path Parameters:**
- `session_id` (string, required) - Session ID

**Query Parameters:**
- `tenant_id` (string, optional, default: "default") - Tenant identifier

**Response:** `200 OK`
```json
{
  "session_id": "sess_abc123xyz",
  "tenant_id": "customer_acme",
  "message": "Session deleted successfully"
}
```

**Response Schema:**
```typescript
interface DeleteSessionManagementResponse {
  session_id: string;
  tenant_id: string;
  message: string;
}
```

**Error Responses:**
- `404 Not Found` - Session doesn't exist
- `500 Internal Server Error` - Deletion failed

---

### List Sessions by Tenant

**Endpoint:** `GET /api/v1/sessions/`

**Description:** List all sessions for a specific tenant with pagination.

**Request:**
```http
GET /api/v1/sessions/?tenant_id=customer_acme&limit=20&offset=0 HTTP/1.1
Host: localhost:9080
```

**Query Parameters:**
- `tenant_id` (string, optional, default: "default") - Tenant identifier
- `limit` (integer, optional, default: 50, max: 100) - Number of sessions to return
- `offset` (integer, optional, default: 0) - Pagination offset

**Response:** `200 OK`
```json
{
  "sessions": [
    {
      "session_id": "sess_abc123xyz",
      "tenant_id": "customer_acme",
      "message_count": 5,
      "created_at": "2026-02-20T10:00:00Z",
      "last_activity": "2026-02-20T10:30:00Z"
    }
  ],
  "total": 1,
  "limit": 20,
  "offset": 0,
  "tenant_id": "customer_acme"
}
```

**Response Schema:**
```typescript
interface SessionSummary {
  session_id: string;
  tenant_id: string;
  message_count: number;
  created_at: string;
  last_activity: string;
}

interface SessionListResponse {
  sessions: SessionSummary[];
  total: number;        // Note: field is "total", not "total_count"
  limit: number;
  offset: number;
  tenant_id: string;
}
```

**Error Responses:**
- `400 Bad Request` - Invalid pagination parameters
- `500 Internal Server Error` - Failed to retrieve sessions

---

### Cleanup Expired Sessions

**Endpoint:** `POST /api/v1/sessions/{session_id}/cleanup`

**Description:** Manually trigger cleanup of expired sessions (if auto-cleanup is disabled).

**Request:**
```http
POST /api/v1/sessions/sess_abc123xyz/cleanup?tenant_id=customer_acme HTTP/1.1
Host: localhost:9080
```

**Path Parameters:**
- `session_id` (string, required) - Session ID

**Query Parameters:**
- `tenant_id` (string, optional, default: "default") - Tenant identifier

**Response:** `200 OK`
```json
{
  "cleaned_sessions": 3,
  "message": "Expired sessions cleaned up successfully"
}
```

**Response Schema:**
```typescript
interface CleanupResponse {
  cleaned_sessions: number;
  message: string;
}
```

**Error Responses:**
- `500 Internal Server Error` - Cleanup failed

---

### Get Session Statistics

**Endpoint:** `GET /api/v1/sessions/stats`

**Description:** Get statistics about sessions across all tenants.

**Request:**
```http
GET /api/v1/sessions/stats HTTP/1.1
Host: localhost:9080
```

**Response:** `200 OK`
```json
{
  "total_sessions": 125,
  "active_sessions": 45,
  "expired_sessions": 80,
  "sessions_by_tenant": {
    "default": 50,
    "customer_acme": 30,
    "customer_beta": 45
  },
  "oldest_session": "2026-02-19T08:00:00Z",
  "newest_session": "2026-02-20T10:35:00Z"
}
```

**Response Schema:**
```typescript
interface SessionStats {
  total_sessions: number;
  active_sessions: number;
  expired_sessions: number;
  sessions_by_tenant: Record<string, number>;
  oldest_session: string;
  newest_session: string;
}
```

**Error Responses:**
- `500 Internal Server Error` - Failed to retrieve statistics

---

## API Information

### Get API Info

**Endpoint:** `GET /info`

**Description:** Get API version and contact information.

**Request:**
```http
GET /info HTTP/1.1
Host: localhost:9080
```

**Response:** `200 OK`
```json
{
  "name": "Customer Service Agent API",
  "version": "0.1.0",
  "description": "REST API for AI-powered customer service agent with order management, email communication, and complaint tracking capabilities.",
  "documentation_url": "/docs",
  "contact": {
    "name": "API Support",
    "email": "support@example.com",
    "url": "https://github.com/yourusername/project"
  }
}
```

**Response Schema:**
```typescript
interface APIInfo {
  name: string;
  version: string;
  description: string;
  documentation_url: string;          // URL to interactive API documentation
  contact: Record<string, string>;    // Contact info (name, email, url)
}
```

---

### List Available Tools

**Endpoint:** `GET /info/tools`

**Description:** List all tools available to the agent.

**Request:**
```http
GET /info/tools HTTP/1.1
Host: localhost:9080
```

**Response:** `200 OK`
```json
{
  "tools": [
    {
      "name": "create_new_order",
      "description": "Create a new order for a customer",
      "category": "order",
      "available": true
    },
    {
      "name": "get_order",
      "description": "Get detailed information about a specific order",
      "category": "order",
      "available": true
    },
    {
      "name": "send_simple_email",
      "description": "Send a simple email to a customer",
      "category": "email",
      "available": true
    },
    {
      "name": "complaint_management",
      "description": "Manage customer complaints via MCP integration",
      "category": "complaint",
      "available": true
    }
  ],
  "total_count": 12,
  "categories": ["order", "email", "complaint"]
}
```

**Response Schema:**
```typescript
interface ToolInfo {
  name: string;
  description: string;
  category: "order" | "email" | "complaint";  // Note: not "order_management"/"communication"
  available: boolean;                          // Whether the tool is currently available
}

interface ListToolsResponse {
  tools: ToolInfo[];
  total_count: number;
  categories: string[];   // List of distinct tool categories present
}
```

---

## Streaming Support (Future)

**Note:** Streaming support is planned but not yet implemented. This section describes the intended behavior.

### Streaming Message Response

**Endpoint:** `POST /agent/messages/stream`

**Description:** Send a message and receive streaming response chunks.

**Request:**
```http
POST /agent/messages/stream HTTP/1.1
Host: localhost:9080
Content-Type: application/json
Accept: text/event-stream

{
  "session_id": "sess_abc123xyz",
  "message": "What's the status of my order ORD-10001?"
}
```

**Response:** `200 OK`
```http
Content-Type: text/event-stream
Cache-Control: no-cache
Connection: keep-alive

event: message
data: {"type": "start", "session_id": "sess_abc123xyz"}

event: message
data: {"type": "chunk", "content": "Your order ORD-10001"}

event: message
data: {"type": "chunk", "content": " is currently"}

event: message
data: {"type": "chunk", "content": " in transit."}

event: message
data: {"type": "tool_call", "tool": "search_orders", "status": "executing"}

event: message
data: {"type": "tool_result", "tool": "search_orders", "status": "completed"}

event: message
data: {"type": "end", "session_id": "sess_abc123xyz", "total_chunks": 3}
```

**Event Types:**
```typescript
type StreamEvent = 
  | { type: "start"; session_id: string; }
  | { type: "chunk"; content: string; }
  | { type: "tool_call"; tool: string; status: "executing"; }
  | { type: "tool_result"; tool: string; status: "completed" | "failed"; }
  | { type: "end"; session_id: string; total_chunks: number; }
  | { type: "error"; error: string; detail: string; };
```

**Client Implementation:**
- Use EventSource API or SSE client library
- Handle reconnection on connection loss
- Implement timeout (recommended: 120s for streaming)

---

## OpenAPI Specification

**Endpoint:** `GET /openapi.json`

**Description:** Get the complete OpenAPI 3.0 specification.

**Interactive Documentation:**
- Swagger UI: `http://localhost:9080/docs`
- ReDoc: `http://localhost:9080/redoc`

---

## Notes

1. **Session TTL:** Sessions expire after 24 hours of inactivity (configurable)
2. **Message History:** Complete message history is retained for active sessions
3. **Tenant Isolation:** Sessions are isolated by tenant_id
4. **Timestamps:** All timestamps are in ISO 8601 format (UTC)
5. **UUIDs:** Session IDs follow format: `sess_<random>` if auto-generated
6. **Content Type:** All requests/responses use `application/json`
7. **Tool Calls:** The agent automatically determines which tools to use based on user message
8. **Rate Limits:** Check response headers to monitor rate limit usage

---

## Changelog

**v0.1.0** (2026-02-20)
- Initial API specification
- Agent operations endpoints
- Session management endpoints
- Health check endpoints
- Multi-tenancy support
- Rate limiting documentation
