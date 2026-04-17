# Frontend Implementation Plan

**Version:** 1.0.0  
**Last Updated:** February 20, 2026  
**Stack:** React 18 + JavaScript, Vite, Tabler (CDN), Axios, Docker/nginx  
**Backend:** FastAPI @ `localhost:9080` (ready)  
**Timeline:** 1–2 weeks, solo developer

---

## Table of Contents

- [Overview](#overview)
- [Tech Stack Decisions](#tech-stack-decisions)
- [Phase 1 — Project Foundation](#phase-1--project-foundation)
- [Phase 2 — Core Infrastructure](#phase-2--core-infrastructure)
- [Phase 3 — Chat Feature](#phase-3--chat-feature)
- [Phase 4 — Session Management](#phase-4--session-management)
- [Phase 5 — Streaming SSE](#phase-5--streaming-sse)
- [Phase 6 — Multi-Tenancy](#phase-6--multi-tenancy)
- [Phase 7 — Health Dashboard](#phase-7--health-dashboard)
- [Phase 8 — Polish and Docker](#phase-8--polish-and-docker)
- [Summary Table](#summary-table)
- [Reference Documents](#reference-documents)

---

## Overview

This document describes the phased implementation plan for building the Customer Service Agent Web UI. The frontend is a React-based single-page application that consumes the FastAPI backend REST APIs.

### Key Requirements

- **Framework:** React 18 with JavaScript (not TypeScript)
- **Build Tool:** Vite
- **UI Framework:** Tabler Admin Template (CDN, Free Edition)
- **API Communication:** Direct to FastAPI backend via Axios
- **Streaming:** Server-Sent Events (SSE) via EventSource
- **Multi-Tenancy:** Tenant context via React Context API + localStorage
- **Deployment:** Docker with nginx:alpine serving static build

---

## Tech Stack Decisions

| Concern | Choice | Rationale |
|---|---|---|
| Language | JavaScript (ES2022+) | Developer preference, avoids TS overhead |
| Framework | React 18 | Specified in architecture docs |
| Build Tool | Vite | Fast HMR, simple config, env var support |
| UI Library | Tabler (CDN) | Pre-built components, Bootstrap 5 base, dark mode |
| HTTP Client | Axios | Interceptor support for retry, tenant injection |
| Routing | React Router v6 | Standard SPA routing |
| State | React Context API | Lightweight, sufficient for app scope |
| SSE Streaming | Native EventSource | No extra dependency needed |
| Containerization | Docker (nginx:alpine) | Multi-stage build, small image |

---

## Phase 1 — Project Foundation

**Duration:** Day 1 (~4 hours)  
**Goal:** Scaffold the project and get a working skeleton with routing.

### Tasks

- [ ] `npm create vite@latest` → React + JavaScript template
- [ ] Install dependencies: `axios`, `react-router-dom`
- [ ] Set up feature-based folder structure (see [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md))
- [ ] Add Tabler CSS/JS via CDN in `index.html`
- [ ] Configure Vite proxy: `/api` → `http://localhost:9080` for local CORS bypass
- [ ] Create `src/core/config/env.js` — environment variable loader (`VITE_API_BASE_URL`, etc.)
- [ ] Create `.env.example` from [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) template
- [ ] Scaffold `App.jsx` with React Router routes:
  - `/` → `HomePage` (stub)
  - `/support` → `SupportPage` (stub)
  - `/settings` → `SettingsPage` (stub)
  - `/about` → `AboutPage` (stub)
- [ ] Create `MainLayout.jsx` — TopNavbar shell + Footer + `<Outlet />`
- [ ] Create `TopNavbar.jsx` — logo, nav links, placeholder for theme toggle and tenant selector

### Deliverable

App boots at `localhost:5173`, shows navbar, all routes render without errors.

---

## Phase 2 — Core Infrastructure

**Duration:** Day 1–2 (~4 hours)  
**Goal:** API client with resilience patterns, theme context, tenant context.

### Tasks

#### API Client (`src/core/api/`)

- [ ] `client.js` — Axios instance with `baseURL`, `timeout`, default headers
- [ ] `interceptors.js` — Request interceptors: inject `X-Request-ID`, log in dev mode
- [ ] `interceptors.js` — Response interceptors: log response time, extract data
- [ ] `errors.js` — Error classification (network, timeout, 4xx, 5xx) and transform to `APIError`
- [ ] `retry.js` — Retry logic: exponential backoff, max 3 attempts, skip POST by default

#### Theme (`src/features/theme/`)

- [ ] `ThemeContext.jsx` + `ThemeProvider.jsx`
- [ ] `useTheme.js` hook — toggles `data-bs-theme` attribute on `<html>`, persists to localStorage
- [ ] `ThemeToggle.jsx` — sun/moon icon button in TopNavbar

#### Tenant (`src/features/tenant/`)

- [ ] `TenantContext.jsx` + `TenantProvider.jsx`
- [ ] `useTenant.js` hook — `currentTenant`, `switchTenant()`, `addTenant()`
- [ ] Persist `current_tenant_id` and `tenant_list` to localStorage
- [ ] Default tenant: `{ id: 'default', displayName: 'Personal Workspace' }`

### Deliverable

Theme toggle works. Tenant state initialises from localStorage. API client is importable and configured.

---

## Phase 3 — Chat Feature

**Duration:** Day 2–4 (~8 hours)  
**Goal:** Full non-streaming chat working end-to-end with the backend.

### Tasks

#### Context & State

- [ ] `ChatContext.jsx` + `ChatProvider.jsx`
  - State: `currentSession`, `messages`, `isLoading`, `error`
- [ ] `useChat.js` hook — exposes state and actions to components

#### Session Creation

- [ ] `chatService.js` — `createSession()` via POST `/api/v1/agent/sessions`
- [ ] Auto-create session on first message if none exists

#### Message Sending

- [ ] `useSendMessage.js` — POST `/api/v1/agent/messages` with `{ session_id, message }`
- [ ] Optimistically add user message to list before response
- [ ] Handle error: show error message in chat

#### UI Components (`src/features/chat/components/`)

- [ ] `ChatView.jsx` — layout: header, scrollable message list, sticky input
- [ ] `MessageList.jsx` — renders list, auto-scrolls to bottom on new message
- [ ] `MessageItem.jsx` — user bubble (right, indigo bg) + assistant bubble (left, gray bg)
- [ ] `MessageInput.jsx` — auto-resize textarea, Enter = send, Shift+Enter = newline
- [ ] `TypingIndicator.jsx` — three animated dots shown while `isLoading === true`

### API Calls

```
POST /api/v1/agent/sessions         → create session
POST /api/v1/agent/messages         → send message, get response
```

### Deliverable

User can type a message, send it, see it in the chat, and get an assistant response. Loading state shown while waiting.

---

## Phase 4 — Session Management

**Duration:** Day 4–5 (~6 hours)  
**Goal:** Users can browse, switch between, and delete past sessions.

### Tasks

- [ ] `sessionService.js` — `listSessions()`, `deleteSession()`, `getSessionHistory()`
- [ ] `useSessions.js` hook — fetch sessions list with `tenant_id` param
- [ ] `useSessionHistory.js` hook — load message history for a session
- [ ] `SessionSelector.jsx` — grouped list: Today / Yesterday / Last 7 Days
  - Each item: preview text, relative timestamp, message count badge
  - Hover actions: delete
- [ ] `SessionFilter.jsx` — time range dropdown, sort order
- [ ] `Pagination.jsx` shared component — page controls
- [ ] `SessionStats.jsx` — cards: total sessions, avg messages per session

### API Calls

```
GET    /api/v1/sessions/?tenant_id=...              → list sessions
GET    /api/v1/sessions/{id}/history?tenant_id=...  → load history
DELETE /api/v1/sessions/{id}?tenant_id=...          → delete session
GET    /api/v1/sessions/stats                        → stats data
```

### Deliverable

Support page shows session list sidebar. Clicking a session loads its history. Sessions can be deleted.

---

## Phase 5 — Streaming SSE

**Duration:** Day 5–6 (~6 hours)  
**Goal:** Assistant responses stream in real-time with tool call visibility.

### Tasks

- [ ] `StreamingClient.js` — `EventSource` wrapper class
  - Manages connection lifecycle: `connect()`, `disconnect()`
  - Parses event types: `start`, `chunk`, `tool_call`, `tool_result`, `end`, `error`
- [ ] `useStreamingMessage.js` hook — integrates `StreamingClient` into React state
  - Accumulates chunks into a single message string
  - Updates message list progressively
- [ ] `StreamToggle.jsx` — toggle switch in `MessageInput` to switch streaming on/off
- [ ] `ToolCallBadge.jsx` — inline badge: `🔧 Using tool: [tool name]...`
- [ ] Update `useSendMessage.js` to route to streaming or non-streaming based on toggle
- [ ] Show `TypingIndicator` during streaming, swap to full message on `end` event

### Stream Event Handling

| Event Type | Action |
|---|---|
| `start` | Show typing indicator, set `isStreaming = true` |
| `chunk` | Append text chunk to assistant message bubble |
| `tool_call` | Show `ToolCallBadge` with tool name |
| `tool_result` | Update badge to show result status |
| `end` | Remove typing indicator, set `isStreaming = false` |
| `error` | Show error message in chat |

### Deliverable

Streaming toggle in input area. When enabled, assistant response appears word-by-word. Tool executions shown inline.

---

## Phase 6 — Multi-Tenancy

**Duration:** Day 6–7 (~4 hours)  
**Goal:** Full tenant switching UI with isolated data per tenant.

### Tasks

- [ ] `TenantSelector.jsx` — dropdown in TopNavbar (top-right)
  - Shows current tenant name
  - Lists all saved tenants with active checkmark
  - "Add Tenant" option at bottom
- [ ] `AddTenantModal.jsx` — form: Tenant ID (slug validation) + Display Name
- [ ] Wire Axios interceptor to auto-inject `tenant_id` query param from `TenantContext`
- [ ] `clearTenantData(tenantId)` utility — clears all `tenant_${id}_*` localStorage keys
- [ ] On tenant switch: clear cached sessions, re-fetch for new tenant
- [ ] `TenantIndicator.jsx` — small badge in navbar showing current tenant name

### LocalStorage Keys

```
current_tenant_id                   → active tenant ID
tenant_list                         → JSON array of tenant objects
tenant_${tenantId}_sessions         → cached session list
tenant_${tenantId}_settings         → per-tenant UI settings
tenant_${tenantId}_drafts           → unsent message drafts
```

### Deliverable

User can add tenants, switch between them. Session data and history are isolated per tenant. Tenant persists between page refreshes.

---

## Phase 7 — Health Dashboard

**Duration:** Day 7 (~3 hours)  
**Goal:** Visible backend system health on a dedicated page or navbar indicator.

### Tasks

- [ ] `healthService.js` — `checkHealth()` via GET `/health` and GET `/health/detailed`
- [ ] `useHealth.js` hook — polls every 30 seconds, exposes `status`, `latency`, `components`
- [ ] `HealthIndicator.jsx` — small coloured dot in TopNavbar (green/yellow/red)
- [ ] `HealthDashboard.jsx` — cards per component with status + latency
  - Overall status card
  - AI Agent status
  - MCP Tools status
  - Response time trend (last 10 polls)

### Status Colour Mapping

| Status | Colour | Meaning |
|---|---|---|
| `healthy` | Green | All systems operational |
| `degraded` | Orange/Yellow | Partial issues |
| `unhealthy` | Red | Critical failure |
| No response | Gray | Backend unreachable |

### API Calls

```
GET /health           → basic status
GET /health/detailed  → per-component breakdown
```

### Deliverable

Health dot in navbar. Detailed health dashboard accessible from Settings or nav.

---

## Phase 8 — Polish and Docker

**Duration:** Day 8–9 (~6 hours)  
**Goal:** Production-ready, containerized, accessible application.

### Error Handling & UX Polish

- [ ] `ErrorBoundary.jsx` — catches render errors, shows `ErrorFallback.jsx`
- [ ] `Toast.jsx` — notification system for API errors, success actions
- [ ] `EmptyState.jsx` — shown when session list or message list is empty
- [ ] `SkeletonLoader.jsx` — shown while sessions/history load
- [ ] `ConnectionIndicator.jsx` — offline/online banner using `navigator.onLine`
- [ ] Save message drafts to localStorage, restore on revisit

### Docker

- [ ] `Dockerfile` — multi-stage: `node:22-alpine` builder → `nginx:alpine` production
- [ ] `nginx.conf` — SPA fallback (`try_files $uri /index.html`), gzip, MIME types
- [ ] `docker-compose.yml` — `frontend-ui` service (port 3000→80) on shared `app-network`
- [ ] `.dockerignore` — exclude `node_modules`, `dist`, `.env`, test files
- [ ] `.env.example` — document all `VITE_*` variables

### Accessibility

- [ ] All interactive elements have `aria-label`
- [ ] Focus management on modal open/close
- [ ] Keyboard navigation: Tab order, Enter/Escape on modals
- [ ] Colour contrast meets WCAG AA

### Deliverable

```bash
docker compose up -d
# → frontend at http://localhost:3000
# → proxies API calls to backend at http://localhost:9080
```

---

## Summary Table

| Phase | Focus | Day | Est. Hours |
|---|---|---|---|
| 1 | Project scaffold, routing, layout | 1 | 4h |
| 2 | API client, theme, tenant contexts | 1–2 | 4h |
| 3 | Chat interface (non-streaming) | 2–4 | 8h |
| 4 | Session management | 4–5 | 6h |
| 5 | SSE streaming + tool call badges | 5–6 | 6h |
| 6 | Multi-tenancy UI | 6–7 | 4h |
| 7 | Health dashboard | 7 | 3h |
| 8 | Polish, error handling, Docker | 8–9 | 6h |
| **Total** | | **~9 days** | **~41h** |

---

## Reference Documents

| Document | Purpose |
|---|---|
| [API_SPECIFICATION.md](API_SPECIFICATION.md) | All backend endpoints, request/response schemas |
| [FRONTEND_ARCHITECTURE.md](FRONTEND_ARCHITECTURE.md) | Layered architecture, component hierarchy, state patterns |
| [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) | Folder layout, naming conventions, import patterns |
| [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md) | Retry, circuit breaker, rate limit, streaming patterns |
| [TENANT_MULTI_TENANCY.md](TENANT_MULTI_TENANCY.md) | Tenant model, context management, API injection |
| [UI_COMPONENT_GUIDE.md](UI_COMPONENT_GUIDE.md) | Tabler component usage, colour palette, chat UI patterns |
| [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) | Dockerfile, nginx.conf, docker-compose, env vars |
