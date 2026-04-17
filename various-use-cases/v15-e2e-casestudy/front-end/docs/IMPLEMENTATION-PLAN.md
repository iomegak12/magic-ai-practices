# MSAv15 Customer Service Portal — Phased Implementation Plan

**Team:** MSAv15FE  
**Lead:** Ramkumar  
**Date:** February 20, 2026  
**Document Type:** Implementation Plan  

---

## Table of Contents

1. [Phase 1 — Project Scaffolding & Setup](#phase-1--project-scaffolding--setup)
2. [Phase 2 — Core Infrastructure (Service Layer + Contexts)](#phase-2--core-infrastructure-service-layer--contexts)
3. [Phase 3 — Global Layout & Navigation](#phase-3--global-layout--navigation)
4. [Phase 4 — Static Pages (Home, About, Contact)](#phase-4--static-pages-home-about-contact)
5. [Phase 5 — Support Page & Chat Interface](#phase-5--support-page--chat-interface)
6. [Phase 6 — API Integration & Streaming](#phase-6--api-integration--streaming)
7. [Phase 7 — Error Handling & UX Polish](#phase-7--error-handling--ux-polish)
8. [Phase 8 — Documentation](#phase-8--documentation)
9. [Phase 9 — Docker & Deployment](#phase-9--docker--deployment)
10. [Phase 10 — Final Review & Handoff](#phase-10--final-review--handoff)
11. [Summary Timeline View](#summary-timeline-view)
12. [API Contract Drift Notes](#api-contract-drift-notes)

---

## Phase 1 — Project Scaffolding & Setup

**Goal:** Get a working skeleton running on port 9090

| Task | Details |
|------|---------|
| Initialize Vite + React 18 project | `npm create vite@latest` with React template |
| Install dependencies | `react-router-dom`, `axios` |
| Configure Tabler Admin via CDN | Add CSS, Icons, JS links to `index.html` |
| Set up folder structure | `components/`, `pages/`, `context/`, `services/`, `hooks/`, `utils/` |
| Create `.env.example` | `PORT=9090`, `API_BASE_URL=http://localhost:9080` |
| Set up `.gitignore` | Per spec |
| Configure `vite.config.js` | Port 9090, proxy `/chat` and `/health` to 9080 for dev |
| Verify app runs | `npm run dev` → `http://localhost:9090` |

**Exit Criteria:** Blank React app with Tabler CSS loaded, running on port 9090.

---

## Phase 2 — Core Infrastructure (Service Layer + Contexts)

**Goal:** Build the API and state management foundation — no UI yet

| Task | Details |
|------|---------|
| `src/services/api.js` | Axios instance, base URL, interceptors, 30s timeout |
| `src/services/healthService.js` | `checkHealth()` → `GET /health` |
| `src/services/chatService.js` | `sendMessage()` (non-streaming) + `sendStreamingMessage()` (SSE) |
| `src/utils/constants.js` | `MAX_SESSIONS=10`, `HEALTH_POLL_INTERVAL=30000`, etc. |
| `src/utils/dateFormatter.js` | Timestamp formatting helpers |
| `src/utils/sessionStorage.js` | `localStorage` read/write helpers (`msav15_sessions`, `msav15_messages_*`) |
| `src/context/SessionContext.jsx` | `sessions[]`, `activeSessionId`, `createSession()`, `switchSession()`, `deleteSession()`, localStorage sync |
| `src/context/ChatContext.jsx` | `messages[]`, `isLoading`, `error`, `streamingEnabled`, all chat methods |
| `src/hooks/useSessionManager.js` | Wraps SessionContext for clean component access |
| `src/hooks/useChatStream.js` | SSE connection management, `startStream()`, `stopStream()`, `isStreaming` |

**Exit Criteria:** All services and contexts unit-testable in isolation; localStorage persistence working.

---

## Phase 3 — Global Layout & Navigation

**Goal:** Shell of the app with routing and shared components

| Task | Details |
|------|---------|
| `src/App.jsx` | Wrap with `SessionContext` + `ChatContext` providers |
| `src/routes.jsx` | Routes: `/`, `/about`, `/contact`, `/support` |
| `src/components/common/Header.jsx` | Branding "MSAv15 Portal", health status indicator (green/yellow/red), version badge |
| `src/components/common/Sidebar.jsx` | Menu: Home, About Us, Contact Us, Support; highlight active route |
| `src/components/common/Footer.jsx` | Copyright, "Team CAP", backend version |
| `src/components/common/Loader.jsx` | Reusable loading spinner |
| Health polling in Header | `setInterval` every 30s calling `healthService.checkHealth()` |
| React Router `<Outlet>` layout | Header + Sidebar + Footer wrapping all pages |

**Exit Criteria:** All 4 routes navigable, sidebar highlights active page, health dot visible in header.

---

## Phase 4 — Static Pages (Home, About, Contact)

**Goal:** Complete the three informational pages

| Task | Details |
|------|---------|
| `src/pages/HomePage.jsx` | Hero section, 3 feature cards (AI Agent, Session Mgmt, Real-time), CTA → `/support` |
| `src/pages/AboutPage.jsx` | App overview, team info (Ramkumar PM, CAP dev), tech stack table, version badge |
| `src/pages/ContactPage.jsx` | Contact cards, support channels, link to `/support` and backend docs |

**Exit Criteria:** All three pages render correctly with Tabler styling, CTA buttons navigate properly.

---

## Phase 5 — Support Page & Chat Interface

**Goal:** The core feature — fully functional chat UI

### 5a — Session Panel

| Task | Details |
|------|---------|
| `src/components/sessions/CreateSessionButton.jsx` | Generates UUID, adds to SessionContext, clears chat |
| `src/components/sessions/SessionItem.jsx` | Shows short session ID, turn count, relative timestamp, active highlight |
| `src/components/sessions/SessionList.jsx` | Renders list + create button; click to switch, delete on hover |

### 5b — Chat Window

| Task | Details |
|------|---------|
| `src/components/chat/ChatMessage.jsx` | User (right, blue), Agent (left, gray), System (centered, subtle) message types |
| `src/components/chat/TypingIndicator.jsx` | "Agent is typing..." animation, shown when `isLoading` |
| `src/components/chat/ChatWindow.jsx` | Scrollable message list, auto-scroll to bottom, error message display with retry |

### 5c — Chat Input

| Task | Details |
|------|---------|
| `src/components/chat/StreamingToggle.jsx` | Tabler toggle switch, tooltip, updates `streamingEnabled` in context |
| `src/components/chat/ChatInput.jsx` | Textarea (auto-expand up to 150px), Enter=send, Shift+Enter=newline, disabled during loading |

### 5d — Support Page Assembly

| Task | Details |
|------|---------|
| `src/pages/SupportPage.jsx` | Two-column layout: SessionList (left) + ChatWindow + ChatInput (right) |

**Exit Criteria:** Full chat flow works end-to-end (non-streaming); sessions create/switch/delete correctly.

---

## Phase 6 — API Integration & Streaming

**Goal:** Connect all UI to live backend, validate both modes

| Task | Details |
|------|---------|
| Wire `sendMessage()` to ChatInput | Non-streaming POST `/chat`, render full response |
| Wire `sendStreamingMessage()` to ChatInput | SSE connection, append chunks in real-time |
| Session continuity | Pass `session_id` in every subsequent message within a session |
| Handle new session from backend | Store returned `session_id` in SessionContext on first turn |
| Health check → header indicator | Live status dot updates on poll and on startup |
| Defensive `metadata` handling | Null-guard all `metadata?.turn_count`, `metadata?.streaming` accesses |
| `session_id` as opaque string | No UUID assumption — treat as plain string per OpenAPI drift finding |

**Exit Criteria:** Both streaming and non-streaming modes work correctly against live backend on port 9080.

---

## Phase 7 — Error Handling & UX Polish

**Goal:** Production-grade resilience and user experience

| Task | Details |
|------|---------|
| `ErrorBoundary` component | Catches render errors, shows fallback UI |
| Network error handling | "Service Unavailable" banner with retry when backend is offline |
| 500 / error response display | User-friendly message in chat window, Retry button |
| Streaming connection loss | Detect EventSource error, show "Connection lost", offer retry |
| 422 validation error display | Parse `HTTPValidationError` detail array from backend |
| Loading states everywhere | Buttons disabled, spinner shown during all async operations |
| Auto-scroll reliability | Scroll to bottom on every new message/chunk |
| Keyboard shortcuts | Enter to send, Shift+Enter for newline, focus management |
| Tooltips | Streaming toggle tooltip, session action tooltips |
| Session limit enforcement | Auto-remove oldest when >10 sessions in localStorage |

**Exit Criteria:** App handles all error scenarios gracefully without crashing; no raw technical errors shown to user.

---

## Phase 8 — Documentation

**Goal:** Complete all required project documentation

| Task | Details |
|------|---------|
| `README.md` | Full spec per PM guide: overview, features, prerequisites, install, Docker, env vars, scripts |
| `CONTRIBUTING.md` | Dev setup, code style, branching strategy, conventional commits, PR checklist |
| `LICENSE` | MIT License — "2026 MSAv15 Service - Team CAP" |
| `.gitignore` | Per spec |
| `.env.example` | Template with all env vars |
| `docs/API_INTEGRATION.md` | SSE implementation notes, drift resolutions, usage examples |

**Exit Criteria:** A new developer can clone and run the app using only the README.

---

## Phase 9 — Docker & Deployment

**Goal:** Containerized, production-ready deployment

| Task | Details |
|------|---------|
| `server/server.js` | Express server, serves `dist/`, catch-all for React Router, port 9090 |
| `Dockerfile` | Node 22 Alpine, `npm ci --only=production`, `npm run build`, `EXPOSE 9090` |
| `docker-compose.yml` | No version field, frontend + api-service, shared `msav15-network`, `restart: unless-stopped` |
| `.dockerignore` | Per spec — exclude `node_modules`, `dist`, `.env`, etc. |
| Local Docker test | Build image, `docker run`, verify at `http://localhost:9090` |
| Docker Compose test | `docker-compose up -d`, verify inter-service communication |

**Exit Criteria:** `docker-compose up -d` brings up the full stack; app fully functional in container.

---

## Phase 10 — Final Review & Handoff

**Goal:** Quality gate before stakeholder handoff

| Task | Details |
|------|---------|
| Manual end-to-end testing | All 4 pages, both chat modes, session CRUD, error scenarios |
| Cross-browser testing | Chrome, Firefox, Edge, Safari |
| Responsive design check | Desktop, tablet (collapsed sidebar), mobile (320px min) |
| Accessibility review | ARIA labels, keyboard navigation, WCAG AA contrast |
| Security review | No secrets in client code, no sensitive data in localStorage |
| Performance check | Lazy loading routes, no unnecessary re-renders |
| Stakeholder demo | Demo to Ramkumar (PM) and team |

**Exit Criteria:** All checklist items pass; application signed off by PM.

---

## Summary Timeline View

```
Phase 1  ████░░░░░░░░░░░░░░░░  Scaffolding
Phase 2  ░░████░░░░░░░░░░░░░░  Services & Context
Phase 3  ░░░░████░░░░░░░░░░░░  Layout & Routing
Phase 4  ░░░░░░██░░░░░░░░░░░░  Static Pages
Phase 5  ░░░░░░░░██████░░░░░░  Chat UI (core)
Phase 6  ░░░░░░░░░░░░████░░░░  API Integration
Phase 7  ░░░░░░░░░░░░░░████░░  Error Handling & Polish
Phase 8  ░░░░░░░░░░░░░░░░██░░  Documentation
Phase 9  ░░░░░░░░░░░░░░░░░░██  Docker & Deployment
Phase 10 ░░░░░░░░░░░░░░░░░░░█  Review & Handoff
```

---

## API Contract Drift Notes

These items were identified during analysis of the backend OpenAPI spec vs the PM specification guide.
Clarifications have been requested from the backend team. Handle defensively in code until confirmed.

| # | Area | Issue | Frontend Mitigation |
|---|------|-------|---------------------|
| 1 | Streaming/SSE format | SSE contract not in OpenAPI spec at all | Build against PM spec; confirm with backend team before shipping |
| 2 | `session_id` format | PM says UUID; OpenAPI example uses `"customer-123"` | Treat as opaque string — no UUID format assumption |
| 3 | `metadata` field | Not in `required` array; `metadata.streaming` sub-field missing | Null-guard all `metadata?.` accesses |
| 4 | Error schemas (400/500) | Only 422 formally defined | Handle all non-2xx codes with generic user-friendly fallback |

---

## Document Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-02-20 | Ramkumar | Initial implementation plan |

---

**Contact:** Ramkumar — ram@example.com  
**Team:** MSAv15FE (MSAv15 Front-End)
