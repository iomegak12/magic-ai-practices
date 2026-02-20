# MSEv15E2E Product Specification Guide

**Product Name:** MSEv15E2E (Microsoft Europe v15 End-to-End)  
**Version:** 0.1.0  
**Date:** February 19, 2026  
**Product Manager:** Hemanth Shah  
**Development Team:** Ramkumar, Rahul  

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Product Overview](#product-overview)
3. [Core Features](#core-features)
4. [API Specifications](#api-specifications)
5. [Configuration Management](#configuration-management)
6. [Security & Rate Limiting](#security--rate-limiting)
7. [Multi-tenancy Support](#multi-tenancy-support)
8. [Error Handling](#error-handling)
9. [Deployment & Operations](#deployment--operations)
10. [Documentation Requirements](#documentation-requirements)
11. [Non-Functional Requirements](#non-functional-requirements)

---

## Executive Summary

MSEv15E2E is a REST API service that exposes an intelligent customer service agent capable of managing complaints, orders, and email communications through a unified conversational interface. The system integrates with external MCP (Model Context Protocol) servers and provides local order management and email sending capabilities.

**Key Value Propositions:**
- Unified AI-powered customer service agent accessible via REST API
- Multi-turn conversational support with session management
- Streaming HTTP responses for real-time interaction
- Multi-tenant architecture for enterprise deployment
- Production-ready with rate limiting, logging, and health monitoring

---

## Product Overview

### Purpose
Provide a scalable, containerized REST API that enables customer service applications to interact with an AI agent that can:
- Register and manage customer complaints via MCP server integration
- Access and manipulate customer orders
- Send email notifications
- Maintain conversation context across multiple interactions

### Target Users
- Enterprise customer service platforms
- Customer support applications
- Internal business tools requiring AI-assisted workflows
- Multi-tenant SaaS platforms

### Technology Stack
- **Framework:** FastAPI (Python)
- **Server:** Uvicorn
- **AI Framework:** Azure OpenAI with Agent Framework
- **Containerization:** Docker (Alpine-based, multi-stage build)
- **Orchestration:** Docker Compose

---

## Core Features

### 1. Conversational AI Agent

**Fixed Configuration:**
- **Agent Name:** CustomerServiceAgent
- **Capabilities:**
  - Complaint management (via external MCP server)
  - Order management (local tools)
  - Email sending (local tools)

**Tools Available:**

**MCP Server Tools (Complaints Management):**
- Register complaint
- Get complaint by ID
- Search complaints
- Update complaint
- Resolve complaint
- Archive complaint

**Local Order Management Tools:**
- `create_order` - Create new customer orders
- `get_order_by_id` - Retrieve specific order details
- `get_orders_by_customer` - Get all orders for a customer
- `search_orders` - Search by SKU, address, or status
- `update_order_status` - Update order status
- `get_all_orders` - List all orders with optional limit

**Local Email Sender Tools:**
- `send_email` - Send email with full options (CC, BCC, HTML)
- `send_text_email` - Send simple text email
- `send_html_email` - Send HTML formatted email
- `send_email_with_attachments` - Send email with file attachments
- `test_connection` - Test SMTP connectivity

### 2. Session Management

**Architecture:**
- In-memory storage (stateless, per-instance)
- Client-provided session IDs
- Server-side conversation history maintenance
- Multi-tenant session isolation

**Session Lifecycle:**
- Created implicitly on first message with session_id
- Maintained in memory during server runtime
- Can be explicitly deleted by client
- Automatic cleanup on server restart

### 3. Streaming Support

**Protocol:** Streaming HTTP (SSE-compatible)
- Real-time token streaming from AI agent
- Compatible with `agent.run(stream=True)`
- Maintains conversation history during streaming

### 4. Health Monitoring

**Endpoints:**
- `/health` - Basic health check
- `/health/readiness` - Readiness probe (checks dependencies)
- `/health/liveness` - Liveness probe (server status)

**Health Check Components:**
- API server status
- MCP server connectivity (non-blocking)
- Azure OpenAI endpoint availability
- SMTP configuration validation

---

## API Specifications

### Base Configuration
```
Base URL: http://localhost:9080
Content-Type: application/json
```

### Endpoints

#### 1. Chat Endpoint (Non-Streaming)

**Request:**
```http
POST /api/v1/chat
Content-Type: application/json

{
  "session_id": "string (required, client-provided)",
  "message": "string (required, user message)",
  "tenant_id": "string (optional, for multi-tenancy)"
}
```

**Response (200 OK):**
```json
{
  "session_id": "abc-123-def",
  "message": "Assistant response text",
  "timestamp": "2026-02-19T10:30:00Z",
  "message_count": 4,
  "tenant_id": "tenant-001"
}
```

**Response (429 Rate Limit Exceeded):**
```json
{
  "error": "Rate limit exceeded",
  "message": "Maximum 100 requests per minute per IP address",
  "retry_after": 30
}
```

#### 2. Chat Endpoint (Streaming)

**Request:**
```http
POST /api/v1/chat/stream
Content-Type: application/json

{
  "session_id": "string (required)",
  "message": "string (required)",
  "tenant_id": "string (optional)"
}
```

**Response (200 OK - Server-Sent Events):**
```
Content-Type: text/event-stream

data: {"type": "token", "content": "Hello", "session_id": "abc-123"}

data: {"type": "token", "content": " there!", "session_id": "abc-123"}

data: {"type": "done", "session_id": "abc-123", "message_count": 4}
```

#### 3. Get Conversation History

**Request:**
```http
GET /api/v1/sessions/{session_id}/history?tenant_id=tenant-001
```

**Response (200 OK):**
```json
{
  "session_id": "abc-123-def",
  "tenant_id": "tenant-001",
  "message_count": 6,
  "created_at": "2026-02-19T09:00:00Z",
  "last_activity": "2026-02-19T10:30:00Z",
  "messages": [
    {
      "role": "user",
      "content": "Hi, I need help with my order",
      "timestamp": "2026-02-19T09:00:00Z"
    },
    {
      "role": "assistant",
      "content": "I'd be happy to help! What's your order number?",
      "timestamp": "2026-02-19T09:00:05Z"
    }
  ]
}
```

**Response (404 Not Found):**
```json
{
  "error": "Session not found",
  "session_id": "abc-123-def"
}
```

#### 4. Delete Session

**Request:**
```http
DELETE /api/v1/sessions/{session_id}?tenant_id=tenant-001
```

**Response (200 OK):**
```json
{
  "message": "Session deleted successfully",
  "session_id": "abc-123-def",
  "messages_deleted": 6
}
```

#### 5. List Sessions

**Request:**
```http
GET /api/v1/sessions?tenant_id=tenant-001&limit=50&offset=0
```

**Response (200 OK):**
```json
{
  "tenant_id": "tenant-001",
  "total": 3,
  "limit": 50,
  "offset": 0,
  "sessions": [
    {
      "session_id": "abc-123",
      "message_count": 6,
      "created_at": "2026-02-19T09:00:00Z",
      "last_activity": "2026-02-19T10:30:00Z"
    }
  ]
}
```

#### 6. Health Endpoints

**Basic Health:**
```http
GET /health

Response: {"status": "healthy", "timestamp": "2026-02-19T10:30:00Z"}
```

**Readiness Check:**
```http
GET /health/readiness

Response: {
  "status": "ready",
  "checks": {
    "api": "healthy",
    "mcp_server": "unavailable",
    "azure_openai": "healthy",
    "smtp": "configured"
  },
  "warnings": ["MCP server not reachable at http://localhost:8000/mcp"]
}
```

**Liveness Check:**
```http
GET /health/liveness

Response: {"status": "alive", "uptime_seconds": 3600}
```

#### 7. API Documentation

```http
GET /docs         # Swagger UI
GET /redoc        # ReDoc UI
GET /openapi.json # OpenAPI specification
```

---

## Configuration Management

### Environment Variables (.env)

```ini
# Server Configuration
SERVER_HOST=0.0.0.0
SERVER_PORT=9080
LOG_LEVEL=INFO
ENABLE_CORS=true
CORS_ORIGINS=*

# Rate Limiting
ENABLE_RATE_LIMITING=false
RATE_LIMIT_PER_MINUTE=100

# Azure OpenAI Configuration
AZURE_AI_PROJECT_ENDPOINT=https://your-project.services.ai.azure.com/api/projects/your-project
AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME=gpt-4o
AZURE_OPENAI_ENDPOINT=https://your-resource.cognitiveservices.azure.com
AZURE_OPENAI_API_KEY=your-api-key

# MCP Server Configuration
MCP_SERVER_URL=http://localhost:8000/mcp
MCP_SERVER_REQUIRED=false

# Order Management Database
ORDER_DB_PATH=./data/orders.db

# Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-password
SENDER_NAME=Customer Service

# Logging Configuration
LOG_TO_FILE=true
LOG_FILE_PATH=./logs/app.log
LOG_MAX_SIZE_MB=100
LOG_BACKUP_COUNT=5
```

### Docker Environment (.env.docker)

Same structure as `.env` but optimized for containerized deployment:
- Paths adjusted for container filesystem
- Network endpoints configured for Docker networking
- Container-specific optimizations

---

## Security & Rate Limiting

### Rate Limiting

**When Enabled (`ENABLE_RATE_LIMITING=true`):**
- **Scope:** Per IP address
- **Limit:** 100 requests per minute (configurable)
- **Algorithm:** Sliding window
- **Response:** HTTP 429 with retry-after header
- **Bypass:** Health endpoints excluded from rate limiting

**Rate Limit Headers:**
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1708340400
```

### CORS Configuration

**Default Settings:**
- **Enabled:** Yes (`ENABLE_CORS=true`)
- **Origins:** `*` (all origins)
- **Methods:** GET, POST, DELETE, OPTIONS
- **Headers:** `*`
- **Credentials:** Allowed

**Production Recommendations:**
- Restrict origins to specific domains
- Review allowed methods based on requirements

### Authentication & Authorization

**Current Version (0.1.0):**
- No authentication required
- Placeholder in architecture for future implementation

**Future Considerations:**
- API Key authentication
- JWT token validation
- Role-based access control (RBAC)

---

## Multi-tenancy Support

### Design Principles

**Tenant Isolation:**
- Session data isolated by `tenant_id`
- Optional tenant context in all requests
- Cross-tenant data access prevented

**Implementation:**
- `tenant_id` field in session management
- In-memory tenant-specific session stores
- Tenant-aware logging and metrics

**Tenant Identification:**
```json
{
  "session_id": "user-123",
  "tenant_id": "company-A",
  "message": "Hello"
}
```

**Without tenant_id:** Defaults to "default" tenant

---

## Error Handling

### Standard Error Response Format

```json
{
  "error": "string (error type)",
  "message": "string (human-readable description)",
  "detail": "string (optional technical details)",
  "request_id": "string (for tracking)",
  "timestamp": "ISO-8601 timestamp"
}
```

### HTTP Status Codes

| Code | Meaning | Usage |
|------|---------|-------|
| 200 | OK | Successful request |
| 400 | Bad Request | Invalid input data |
| 404 | Not Found | Session/resource not found |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Unexpected server error |
| 503 | Service Unavailable | Critical dependency failure |

### Error Categories

**Client Errors (4xx):**
- Missing required fields
- Invalid session_id format
- Malformed JSON
- Rate limit exceeded

**Server Errors (5xx):**
- Agent initialization failure
- Azure OpenAI API errors
- MCP server critical failures (if required)
- Database write failures

**Graceful Degradation:**
- MCP server unavailable: Log warning, continue without complaint tools
- SMTP configuration invalid: Log error, disable email tools
- Non-critical failures don't prevent API startup

---

## Deployment & Operations

### Docker Configuration

**Base Image:** Alpine Linux (multi-stage build)
- Stage 1: Build dependencies
- Stage 2: Runtime environment (minimal)

**Image Name:** `msev15-e2e-service`

**Health Check:** Disabled (as requested)

**Port Exposure:** 9080

### Docker Compose

**Service Definition:**
```yaml
services:
  api:
    image: msev15-e2e-service
    env_file:
      - .env.docker
    ports:
      - "9080:9080"
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
```

**Note:** MCP server NOT included in docker-compose

### Startup Behavior

**Welcome Message:**
```
╔══════════════════════════════════════════════════════════════╗
║                    MSEv15E2E Service                         ║
║                       Version 0.1.0                          ║
╚══════════════════════════════════════════════════════════════╝

Server Configuration:
  • Host: 0.0.0.0
  • Port: 9080
  • Log Level: INFO
  • CORS: Enabled (*)
  • Rate Limiting: Disabled

Agent Configuration:
  • Model: gpt-4o
  • Tools: 12 (MCP + Local)
  • MCP Server: http://localhost:8000/mcp [⚠ Unavailable]

Logging:
  • File: ./logs/app.log (Enabled)
  • Max Size: 100MB
  • Backups: 5

Starting server... ✓
API Documentation: http://localhost:9080/docs
```

**Warnings Display:**
- MCP server unreachable
- SMTP configuration issues
- Missing optional dependencies

### Graceful Shutdown

**CTRL+C Behavior:**
```
^C Shutdown signal received...
  • Closing active sessions... [3 sessions]
  • Flushing logs...
  • Closing database connections...
  • Cleanup complete.
Server stopped gracefully. Goodbye!
```

### Logging

**Log Targets:**
- File system (default enabled)
- Console output (always enabled)

**Log Levels:** DEBUG, INFO, WARNING, ERROR, CRITICAL

**Log Format:**
```
2026-02-19 10:30:45 | INFO | api.chat | session=abc-123 | tenant=company-A | User message received
```

**Log Rotation:**
- Max size: 100MB
- Backup count: 5
- Automatic rotation

---

## Documentation Requirements

### Repository Documentation

1. **README.md**
   - Project overview
   - Quick start guide
   - Installation instructions
   - API usage examples
   - Configuration reference
   - Development setup
   - Contributing guidelines link

2. **CONTRIBUTING.md**
   - Team structure (Hemanth Shah, Ramkumar, Rahul)
   - Development workflow
   - Code standards
   - Pull request process
   - Testing requirements

3. **CHANGELOG.md**
   - Version history
   - v0.1.0 features and changes
   - Release notes

4. **LICENSE** (MIT)

5. **.gitignore**
   - Python artifacts
   - Environment files
   - Logs and data
   - IDE configurations

6. **.dockerignore**
   - Development files
   - Documentation
   - Tests
   - Git metadata

### API Documentation

**OpenAPI/Swagger:**
- Comprehensive endpoint documentation
- Request/response schemas
- Example requests
- Authentication (placeholder)
- Error responses

**Interactive Docs:**
- Swagger UI at `/docs`
- ReDoc at `/redoc`

---

## Non-Functional Requirements

### Performance

**Response Times:**
- Health endpoints: < 100ms
- Non-streaming chat: < 5s (depends on AI model)
- Streaming chat: First token < 2s
- History retrieval: < 500ms

**Throughput:**
- Support 100 concurrent sessions per instance
- Rate limiting: 100 req/min per IP (configurable)

### Reliability

**Uptime Target:** 99.5% (excluding maintenance)

**Error Recovery:**
- Automatic retry for transient failures
- Graceful degradation when dependencies unavailable
- No data loss on graceful shutdown

### Scalability

**Horizontal Scaling:**
- Stateless design (in-memory sessions are instance-specific)
- Multiple instances behind load balancer
- Session affinity required (if reusing session_ids)

**Vertical Scaling:**
- Configurable thread pool for async operations
- Memory-efficient session storage

### Maintainability

**Code Quality:**
- Modular architecture
- Type hints throughout
- Comprehensive docstrings
- Unit test coverage > 80%

**Monitoring:**
- Structured logging
- Request tracing with request_id
- Performance metrics (future)

### Security

**Data Protection:**
- No sensitive data in logs (API keys masked)
- Secure credential management via environment variables
- HTTPS ready (TLS termination at proxy)

**Input Validation:**
- All inputs validated and sanitized
- SQL injection prevention (parameterized queries)
- XSS prevention in responses

---

## Appendix

### Glossary

- **MCP:** Model Context Protocol - Standard for exposing tools to AI agents
- **Session:** Conversation context maintained across multiple messages
- **Tenant:** Isolated customer/organization in multi-tenant setup
- **Tool:** Function callable by AI agent to perform actions
- **Streaming:** Real-time response delivery token-by-token

### References

- FastAPI Documentation: https://fastapi.tiangolo.com/
- Azure OpenAI Agent Framework
- Model Context Protocol Specification
- Docker Best Practices

### Version History

| Version | Date | Changes |
|---------|------|---------|
| 0.1.0 | 2026-02-19 | Initial specification release |

---

**Document Status:** Draft for Implementation  
**Next Review Date:** Post Phase 1 Implementation  
**Approvers:** Hemanth Shah (Product Manager)

