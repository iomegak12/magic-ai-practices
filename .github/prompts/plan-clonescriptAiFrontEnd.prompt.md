# Plan: clonescript.ai Front-End — Full Implementation

## TL;DR
Implement a React 18 + Vite + Tailwind CSS v3 chat front-end at `use-cases-day4/front-end/` consuming the REST API at `localhost:8800`. Covers project scaffold, source skeleton with all components/hooks/context/API layer, infrastructure files (Docker, nginx, .env, docs), ready for `npm install && npm run dev`.

## Confirmed Decisions
- Port: **3000** (dev server + Docker container)
- Docker: **Nginx alpine-slim** serving static build
- Image: `iomega/end-to-end-front-end`
- Location: `use-cases-day4/front-end/`
- No version key in docker-compose.yml
- Font: **Roboto** (single font family — replaces DM Serif Display + Inter from design guide)
- Base font size: **15px**

---

## Phase 1: Project Scaffold (5 files)

1. **`package.json`** — React 18, Vite, all deps from IMPLEMENTATION_GUIDE:
   - Dependencies: `react`, `react-dom`, `react-router-dom@6`, `react-markdown`, `rehype-highlight`, `uuid`, `date-fns`
   - Dev deps: `vite`, `@vitejs/plugin-react`, `tailwindcss@3`, `@tailwindcss/typography`, `postcss`, `autoprefixer`
   - Scripts: `dev` (port 3000), `build`, `preview`, `lint`

2. **`vite.config.js`** — dev server on port 3000, proxy `/chat` and `/health` → `http://localhost:8800`

3. **`tailwind.config.js`** — content paths for `./index.html` + `./src/**/*.{js,jsx}`, typography plugin, extend `fontFamily.sans` to `['Roboto', 'sans-serif']`

4. **`postcss.config.js`** — tailwindcss + autoprefixer

5. **`index.html`** — Vite SPA entry with `<div id="root">`, links `src/main.jsx`, Google Fonts: `Roboto:wght@400;500;600;700`

*All 5 are independent — can create in parallel.*

---

## Phase 2: Source Entry Points (3 files)

6. **`src/main.jsx`** — React 18 `createRoot`, wraps `<App />` in `<BrowserRouter>` and `<ChatProvider>`

7. **`src/App.jsx`** — Router with routes: `/` → ChatPage, `/chat/:sessionId` → ChatPage, `/library` → LibraryPage, `/settings` → SettingsPage, `*` → redirect to `/`

8. **`src/index.css`** — Tailwind directives (`@tailwind base/components/utilities`) + CSS variables for glassmorphism theme + body `font-family: 'Roboto', sans-serif; font-size: 15px`

*Depends on Phase 1 (tailwind config must exist for directives).*

---

## Phase 3: State Management (2 files)

9. **`src/context/chatReducer.js`** — `initialState` and `chatReducer` pure function with all action types: `NEW_SESSION`, `SET_ACTIVE_SESSION`, `ADD_USER_MESSAGE`, `SET_LOADING`, `APPEND_STREAM_CHUNK`, `COMMIT_STREAM`, `ADD_ASSISTANT_MESSAGE`, `SET_ERROR`, `CLEAR_ERROR`, `TOGGLE_STREAMING`, `DISMISS_ERROR`. Helper `appendMessageToSession()`.

10. **`src/context/ChatContext.jsx`** — `ChatProvider` with `useReducer`, `useChatContext` hook. Rehydrates sessions from `localStorage` on mount, persists on updates.

*Independent of Phase 2.*

---

## Phase 4: API Layer (2 files)

11. **`src/api/chat.js`** — `sendMessage({ message, session_id })` for `POST /chat`, `sendMessageStream({ message, session_id })` for `POST /chat/stream` returning `ReadableStream` reader. Uses `import.meta.env.VITE_API_BASE_URL`.

12. **`src/api/health.js`** — `checkReadiness()` for `GET /health/readiness`.

*Independent of Phase 3.*

---

## Phase 5: Custom Hooks (3 files)

13. **`src/hooks/useChat.js`** — Convenience hook consuming `ChatContext`. Exposes `sendMessage(text)` that dispatches user message, calls API (streaming or non-streaming based on `streamingEnabled`), dispatches result. Handles new session creation.

14. **`src/hooks/useStreamingChat.js`** — Full SSE lifecycle: fetch → ReadableStream reader → parse `data:` lines → dispatch `APPEND_STREAM_CHUNK` → parse `event: metadata` → dispatch `COMMIT_STREAM` → handle `[DONE]` / `event: error`. Uses `TextDecoder` with line buffer.

15. **`src/hooks/useHealthCheck.js`** — On mount, polls `GET /health/readiness` every 5s. Exposes `{ ready, status, checks }`. Stops polling once ready.

*Depends on Phase 3 (context) and Phase 4 (API layer).*

---

## Phase 6: Utilities (2 files)

16. **`src/utils/groupChatsByDate.js`** — Groups session list into date buckets ("Today", "Yesterday", "Previous 7 Days", "Older") using `date-fns`.

17. **`src/utils/parseSSE.js`** — Parses raw SSE text into structured events: `{ type: 'text'|'metadata'|'error'|'done', data }`.

*Independent.*

---

## Phase 7: Layout Components (2 files)

18. **`src/components/layout/Sidebar.jsx`** — Left panel: logo (`clonescript.ai`), nav items (New Chat, Library, Settings, Help), chat list grouped by date, upgrade card. Collapsible on mobile.

19. **`src/components/layout/MainPanel.jsx`** — Right panel: header bar with model selector + avatar, scrollable chat area (renders `WelcomeScreen` or `MessageList`), `InputBar` at bottom.

*Depends on Phase 3 (context reads).*

---

## Phase 8: Sidebar Sub-Components (4 files)

20. **`src/components/sidebar/NavItem.jsx`** — Icon + label link, active state highlight.
21. **`src/components/sidebar/ChatListGroup.jsx`** — Date header + list of `ChatListItem`.
22. **`src/components/sidebar/ChatListItem.jsx`** — Truncated title, click → `SET_ACTIVE_SESSION`.
23. **`src/components/sidebar/UpgradeCard.jsx`** — Dismissible card, persists dismiss to `localStorage`.

*All 4 independent, depend on Phase 3.*

---

## Phase 9: Chat Components (6 files)

24. **`src/components/chat/WelcomeScreen.jsx`** — Orb graphic, time-based greeting, 4 `ExampleCard` components with starter prompts.
25. **`src/components/chat/MessageList.jsx`** — Maps messages, auto-scrolls to bottom via ref + `useEffect`.
26. **`src/components/chat/MessageBubble.jsx`** — User (right-aligned) or assistant (left-aligned) with `react-markdown` + `rehype-highlight`. Shows `ToolCallBadge` for assistant messages.
27. **`src/components/chat/StreamingIndicator.jsx`** — Animated dots while streaming.
28. **`src/components/chat/ToolCallBadge.jsx`** — Pill badges showing tool names + duration.
29. **`src/components/chat/ExampleCard.jsx`** — Clickable prompt card, triggers input population + auto-submit.

*Depends on Phase 3 + Phase 5.*

---

## Phase 10: Input Components (3 files)

30. **`src/components/input/InputBar.jsx`** — Auto-resizing textarea, Enter to submit / Shift+Enter for newline, disabled while loading.
31. **`src/components/input/StreamToggle.jsx`** — Pill toggle between "Stream" / "Instant", dispatches `TOGGLE_STREAMING`.
32. **`src/components/input/ActionBar.jsx`** — Bottom quick-action row (Create Images, Study, Build, Deep Research, Learn).

*Depends on Phase 3.*

---

## Phase 11: Common Components (3 files)

33. **`src/components/common/Avatar.jsx`** — User avatar circle (top-right).
34. **`src/components/common/ErrorBanner.jsx`** — Dismissible inline error with status-specific messaging and retry countdown for 429.
35. **`src/components/common/LoadingDots.jsx`** — Reusable animated dots.

*Independent.*

---

## Phase 12: Pages (3 files)

36. **`src/pages/ChatPage.jsx`** — Composes `Sidebar` + `MainPanel`. Reads `:sessionId` route param → dispatches `SET_ACTIVE_SESSION`.
37. **`src/pages/LibraryPage.jsx`** — Placeholder page.
38. **`src/pages/SettingsPage.jsx`** — Placeholder page.

*Depends on Phases 7–11.*

---

## Phase 13: Infrastructure Files (11 files)

39. **`.env.example`** — `VITE_API_BASE_URL=http://localhost:8800`
40. **`.gitignore`** — node_modules, dist, .env, .env.local, .vscode, .DS_Store, coverage, *.log
41. **`.dockerignore`** — node_modules, dist, .env, .git, docs, *.md (except index.html), coverage
42. **`nginx.conf`** — SPA fallback (`try_files $uri /index.html`), gzip, cache static assets (js/css/images)
43. **`Dockerfile`** — Multi-stage: `node:22-alpine` builder → `npm ci && npm run build` → `nginx:alpine-slim` runtime, COPY build output to `/usr/share/nginx/html`, COPY `nginx.conf`, expose 80, healthcheck on `/`
44. **`docker-compose.yml`** — service `e2e-front-end`, image `iomega/end-to-end-front-end`, port `3000:80`, no version key, restart unless-stopped, healthcheck
45. **`LICENSE`** — MIT, 2026 Enterprise E2E Team
46. **`README.md`** — Project overview, architecture diagram, quick start (npm + Docker), project structure, env vars, API integration notes
47. **`TROUBLESHOOTING.md`** — CORS blocked, API unreachable, blank page after build, Docker networking, port conflicts, HMR not working
48. **`CONTRIBUTING.md`** — Code style (ESLint, Prettier), component conventions, PR process
49. **`CHANGELOG.md`** — v1.0.0 entry

*All 11 independent — can create in parallel.*

---

## Verification

1. `npm install` completes without errors
2. `npm run dev` starts Vite on port 3000
3. Browser at `http://localhost:3000` renders the app shell
4. `npm run build` produces `dist/` with index.html + assets
5. `docker compose build` succeeds
6. `docker compose up` serves the app on port 3000
7. API proxy: `/chat` requests from dev server reach `localhost:8800`
8. SSE streaming works end-to-end with the REST API running

## Scope
- **Included**: Full React source code, all components, hooks, context, API layer, utilities, infrastructure
- **Excluded**: Unit tests, E2E tests, CI/CD pipeline, production deployment config
