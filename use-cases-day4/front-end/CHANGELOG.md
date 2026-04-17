# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [1.0.0] - 2026-04-17

### Added

- React 18 + Vite + Tailwind CSS v3 chat interface
- Glassmorphism UI with soft gradient background and frosted panels
- `POST /chat` integration — non-streaming chat with full response metadata
- `POST /chat/stream` integration — SSE streaming with real-time token rendering
- `GET /health/readiness` polling with status banner
- Context + useReducer state management (11 action types)
- Session persistence to `localStorage` with auto-rehydration
- Sidebar with grouped chat history (Today, Yesterday, Previous 7 Days, Older)
- Welcome screen with orb graphic, time-based greeting, and example prompt cards
- Markdown rendering with syntax highlighting (`react-markdown` + `rehype-highlight`)
- Tool usage badges showing MCP tool names and durations
- Stream / Instant toggle for switching between response modes
- Auto-resizing textarea with Enter to submit / Shift+Enter for newline
- Error banner with dismiss functionality
- Health check polling — disables input until API is ready
- Responsive layout — collapsible sidebar on smaller viewports
- Multi-stage Docker build (node:22-alpine → nginx:alpine-slim)
- Nginx SPA config with gzip and static asset caching
- Docker Compose configuration (port 3000:80)
- Roboto font, 15px base font size
