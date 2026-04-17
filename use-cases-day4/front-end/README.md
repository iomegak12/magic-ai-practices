# clonescript.ai — Frontend

React 18 chat interface for the Enterprise E2E agent. Glassmorphism design, SSE streaming, session history, and tool usage badges.

## Architecture

```
Browser (port 3000)
  │
  ├── React 18 + Vite + Tailwind CSS v3
  │
  ├── POST /chat              → Non-streaming request
  ├── POST /chat/stream       → SSE streaming request
  ├── GET  /health/readiness  → Health polling
  │
  └── REST API (port 8800)
        └── MCP Agent + Guardrails + History
```

## Quick Start

### 1. Environment Setup

```bash
cp .env.example .env.local
# Edit VITE_API_BASE_URL if the API runs on a different host/port
```

### 2. Install & Run

```bash
npm install
npm run dev
```

Open `http://localhost:3000` in your browser.

### 3. Docker

```bash
docker compose build
docker compose up -d
```

The container serves the app on port `3000` via Nginx.

## Project Structure

```
src/
├── api/           # fetch wrappers (chat, health)
├── context/       # ChatContext + chatReducer (global state)
├── components/
│   ├── layout/    # Sidebar, MainPanel
│   ├── sidebar/   # NavItem, ChatListGroup, ChatListItem, UpgradeCard
│   ├── chat/      # WelcomeScreen, MessageList, MessageBubble, etc.
│   ├── input/     # InputBar, StreamToggle, ActionBar
│   └── common/    # Avatar, ErrorBanner, LoadingDots
├── hooks/         # useChat, useStreamingChat, useHealthCheck
├── pages/         # ChatPage, LibraryPage, SettingsPage
├── utils/         # groupChatsByDate, parseSSE
├── App.jsx        # Router setup + background blobs
├── main.jsx       # React 18 createRoot entry
└── index.css      # Tailwind directives + CSS variables
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `VITE_API_BASE_URL` | `http://localhost:8800` | REST API base URL |

## Key Features

- **SSE Streaming** — real-time token-by-token rendering via `fetch` + `ReadableStream`
- **Session Persistence** — conversations saved to `localStorage`, restored on reload
- **Tool Usage Badges** — shows which MCP tools were invoked + duration
- **Health Polling** — checks API readiness every 5s, disables input until ready
- **Glassmorphism UI** — frosted glass panels, pastel gradient background
- **Stream Toggle** — switch between streaming and instant response modes

## Prerequisites

- **Node.js 22+**
- **REST API** running on port 8800 (see `../e2e-rest-api/`)
- **MCP Server** running on port 8700 (see `../mcp/`)

## Scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Start Vite dev server on port 3000 |
| `npm run build` | Production build to `dist/` |
| `npm run preview` | Preview production build locally |

## License

[MIT](LICENSE)
