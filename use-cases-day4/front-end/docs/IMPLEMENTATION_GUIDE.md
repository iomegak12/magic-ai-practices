# clonescript.ai — Frontend Implementation Guide

**Stack:** React 18 + Vite · JavaScript · Tailwind CSS v3  
**API Base URL:** `http://localhost:8800`

---

## Table of Contents

1. [Tech Stack Recommendations](#1-tech-stack-recommendations)
2. [Design System & Style Guide](#2-design-system--style-guide)
3. [Project Structure](#3-project-structure)
4. [Core Architecture — Context + useReducer](#4-core-architecture--context--usereducer)
5. [Component Breakdown](#5-component-breakdown)
6. [API Integration Layer](#6-api-integration-layer)
7. [SSE Streaming Implementation](#7-sse-streaming-implementation)
8. [Session Management](#8-session-management)
9. [Routing](#9-routing)
10. [Error Handling Strategy](#10-error-handling-strategy)
11. [Environment Configuration](#11-environment-configuration)
12. [Implementation Checklist](#12-implementation-checklist)

---

## 1. Tech Stack Recommendations

### CSS Framework — **Tailwind CSS v3**

Recommended over alternatives for the following reasons:

| Concern | Reason |
|---|---|
| Design fidelity | The UI uses a soft, glassmorphism aesthetic with custom gradients, blur effects, and layered cards — Tailwind's utility classes map directly to these without fighting a component library's opinions |
| Bundle size | PurgeCSS/tree-shaking is built-in; only used classes are shipped |
| No style conflicts | Unlike Ant Design or MUI, Tailwind has no base component styles to override |
| Speed | Utility-first means no context-switching between files for simple spacing/color tweaks |

**Additional libraries:**

| Package | Purpose |
|---|---|
| `tailwindcss` + `@tailwindcss/typography` | Base styling + prose formatting for AI responses |
| `react-markdown` + `rehype-highlight` | Render markdown in chat responses with code highlighting |
| `react-router-dom v6` | Client-side routing (sidebar nav, settings page) |
| `uuid` | Generate temporary client-side session IDs |
| `date-fns` | Format chat timestamps in sidebar |

---

## 2. Design System & Style Guide

> **Important:** All design decisions below are derived directly from the attached UI screenshot. Developers must not deviate from these specs without approval. This section is the single source of truth for visual implementation.

---

### 2.1 Overall Aesthetic

The UI follows a **soft glassmorphism** design language — translucent frosted panels layered over a blurred pastel gradient background. Key characteristics:

- Light theme only (no dark mode in v1)
- Blurred, multi-colour gradient fills the full viewport background
- All panels/cards are white or near-white with low opacity and subtle border + shadow
- No sharp or high-contrast borders — everything uses soft, feathered edges
- Rounded corners throughout, consistently large radius

---

### 2.2 Colour Palette

Define all colours as CSS custom properties in `src/index.css`.

```css
:root {
  /* Background gradient — full page */
  --color-bg-gradient-start: #f0e6ff;   /* soft lavender */
  --color-bg-gradient-mid:   #fce4ec;   /* blush pink */
  --color-bg-gradient-end:   #e8f0fe;   /* sky blue */

  /* Panels / Cards */
  --color-panel-bg:          rgba(255, 255, 255, 0.72);  /* frosted white */
  --color-panel-border:      rgba(255, 255, 255, 0.60);
  --color-card-bg:           rgba(255, 255, 255, 0.85);
  --color-card-border:       rgba(220, 220, 235, 0.60);

  /* Text */
  --color-text-primary:      #1a1a2e;   /* near-black, slightly cool */
  --color-text-secondary:    #6b7280;   /* medium grey */
  --color-text-muted:        #9ca3af;   /* light grey — timestamps, placeholders */
  --color-text-link:         #6d6de8;   /* muted indigo — nav active state */

  /* Interactive */
  --color-send-btn:          #1a1a2e;   /* dark filled circle for send button */
  --color-send-btn-hover:    #2d2d4e;
  --color-upgrade-btn-bg:    #ffffff;
  --color-upgrade-btn-border:#1a1a2e;

  /* Input */
  --color-input-bg:          rgba(255, 255, 255, 0.90);
  --color-input-border:      rgba(200, 200, 220, 0.50);
  --color-placeholder:       #9ca3af;

  /* Action bar pills */
  --color-pill-bg:           rgba(255, 255, 255, 0.80);
  --color-pill-border:       rgba(200, 200, 220, 0.55);
  --color-pill-text:         #374151;

  /* Divider */
  --color-divider:           rgba(200, 200, 220, 0.40);

  /* Upgrade card */
  --color-upgrade-card-bg:   rgba(255, 255, 255, 0.95);
  --color-upgrade-card-shadow: rgba(0, 0, 0, 0.08);
}
```

**Tailwind config** — extend with these tokens:

```js
// tailwind.config.js
export default {
  theme: {
    extend: {
      colors: {
        panel:   'rgba(255,255,255,0.72)',
        card:    'rgba(255,255,255,0.85)',
        'text-primary':   '#1a1a2e',
        'text-secondary': '#6b7280',
        'text-muted':     '#9ca3af',
        'send-btn':       '#1a1a2e',
      },
      backdropBlur: {
        panel: '16px',
        bg:    '40px',
      },
      borderRadius: {
        panel: '20px',
        card:  '14px',
        input: '16px',
        pill:  '999px',
      },
    },
  },
};
```

---

### 2.3 Typography

| Element | Font Family | Weight | Size | Notes |
|---|---|---|---|---|
| Logo (`clonescript.ai`) | `'DM Serif Display', serif` | 700 | `28px` | Bold, black, no letter spacing |
| Welcome heading | `'DM Serif Display', serif` | 400 | `36px` | Two-line centered, `line-height: 1.2` |
| Welcome subtext | `'Inter', sans-serif` | 400 | `14px` | Centered, `--color-text-secondary` |
| Nav items | `'Inter', sans-serif` | 400 | `15px` | `--color-text-secondary` |
| Chat group headers ("Yesterday") | `'Inter', sans-serif` | 700 | `13px` | All-caps optional, `--color-text-primary` |
| Chat list items | `'Inter', sans-serif` | 400 | `13px` | Truncated with ellipsis, `--color-text-secondary` |
| Section label ("BEGIN WITH THE EXAMPLE BELOW") | `'Inter', sans-serif` | 500 | `11px` | Uppercase, heavy letter-spacing `0.1em`, `--color-text-muted` |
| Example card text | `'Inter', sans-serif` | 400 | `13px` | `--color-text-primary` |
| Input placeholder | `'Inter', sans-serif` | 400 | `15px` | `--color-placeholder` |
| Action pill labels | `'Inter', sans-serif` | 400 | `13px` | `--color-pill-text` |
| Upgrade card title | `'Inter', sans-serif` | 700 | `15px` | `--color-text-primary` |
| Upgrade card body | `'Inter', sans-serif` | 400 | `13px` | `--color-text-secondary` |
| User name (top-right) | `'Inter', sans-serif` | 600 | `14px` | |
| User email (top-right) | `'Inter', sans-serif` | 400 | `12px` | `--color-text-muted` |

**Google Fonts import** (add to `index.html` `<head>`):

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
```

---

### 2.4 Page Background

The entire viewport background is a blurred multi-stop gradient, not a solid colour.

```css
/* index.css */
body {
  min-height: 100vh;
  background: linear-gradient(
    135deg,
    #e8d5f5 0%,    /* lavender top-left */
    #fce4ec 35%,   /* blush pink centre-left */
    #fde8f0 55%,   /* light rose */
    #e8eeff 80%,   /* periwinkle blue */
    #dde8ff 100%   /* light blue bottom-right */
  );
  background-attachment: fixed;
}
```

The diffuse blurred blobs visible at the corners of the screenshot are achieved with absolutely positioned `<div>` elements using large `border-radius: 50%` and `filter: blur(60px)` with low opacity:

```jsx
// In App.jsx or a BackgroundBlobs component
<div className="fixed inset-0 -z-10 overflow-hidden pointer-events-none">
  <div style={{
    position: 'absolute', top: '-10%', left: '-10%',
    width: '45vw', height: '45vw', borderRadius: '50%',
    background: 'rgba(180, 140, 240, 0.35)', filter: 'blur(70px)'
  }} />
  <div style={{
    position: 'absolute', bottom: '-10%', right: '-5%',
    width: '40vw', height: '40vw', borderRadius: '50%',
    background: 'rgba(140, 180, 255, 0.30)', filter: 'blur(70px)'
  }} />
</div>
```

---

### 2.5 Layout & Spacing

```
┌─────────────────────────────────────────────────────┐
│                  App (100vw × 100vh)                 │
│  ┌──────────────────────────────────────────────┐   │
│  │  Outer wrapper — max-w-[1200px], mx-auto,    │   │
│  │  my-6, px-4, h-[calc(100vh-48px)]            │   │
│  │  ┌────────────┐  ┌──────────────────────┐    │   │
│  │  │  Sidebar   │  │     Main Panel       │    │   │
│  │  │  w-[280px] │  │     flex-1           │    │   │
│  │  │  shrink-0  │  │                      │    │   │
│  │  └────────────┘  └──────────────────────┘    │   │
│  └──────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

| Element | Value |
|---|---|
| Outer wrapper max-width | `1200px` |
| Outer wrapper vertical margin | `24px` top and bottom |
| Gap between sidebar and main panel | `16px` |
| Sidebar width | `280px` (fixed) |
| Sidebar inner padding | `24px` horizontal, `28px` vertical |
| Sidebar border-radius | `20px` |
| Main panel border-radius | `20px` |
| Main panel inner padding | `24px` |
| Example card grid | `4 columns`, `gap: 12px` |
| Example card padding | `16px` |
| Example card border-radius | `14px` |
| Input bar border-radius | `16px` |
| Input bar padding | `14px 16px` |
| Nav item gap | `8px` between icon and label` |
| Nav item vertical padding | `10px` |
| Section divider (below nav) | `1px solid var(--color-divider)`, `my-4` |

---

### 2.6 Glassmorphism Panel Effect

Apply this class pattern to both the Sidebar and Main Panel:

```css
/* In index.css — reusable utility */
.glass-panel {
  background: rgba(255, 255, 255, 0.72);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.60);
  box-shadow:
    0 4px 24px rgba(0, 0, 0, 0.06),
    0 1px 4px rgba(0, 0, 0, 0.04);
}
```

Cards (example cards, upgrade card, input bar) use a slightly more opaque variant:

```css
.glass-card {
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  border: 1px solid rgba(220, 220, 235, 0.60);
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
}
```

---

### 2.7 Component-Level Visual Specs

#### Sidebar

- Background: `glass-panel`
- Logo: `DM Serif Display`, bold, `#1a1a2e`, top of sidebar, no icon
- Nav items: icon (16px, stroke-based, `--color-text-secondary`) + label side-by-side
- Active nav item: `--color-text-link` colour, subtle left border or background tint
- Horizontal divider: below nav links, above "Chat List" label
- "Chat List ∨" label: small caps dropdown indicator, `--color-text-secondary`
- Group headers ("Yesterday", "5 Days Ago"): bold `13px`, `--color-text-primary`
- Chat list items: single line, truncated at `~35 chars`, `--color-text-secondary`
- Upgrade card: sits at the very bottom of the sidebar, `glass-card` style, white background, close (×) button top-right, orb avatar, bold title, body text, outlined CTA button

#### Main Panel Header (top-right)

- User avatar: `36px` circular image
- Name: `14px` semibold
- Email: `12px` muted, below name
- Contained in a small white rounded card `(border-radius: 12px, padding: 8px 12px)`
- Positioned: `absolute top-4 right-4` within the main panel

#### Welcome Screen

- Orb: `80px × 80px` circular, centered — use a `<img>` of a metallic/holographic sphere; if no asset available, replicate with CSS radial gradient: `radial-gradient(circle at 35% 35%, #c084fc, #818cf8, #312e81)`
- Heading: two lines, centered, `DM Serif Display 36px`
- Subtext: centered, `14px`, `--color-text-secondary`, max-width `480px`, `mx-auto`
- Section label: uppercase, `11px`, `0.1em` letter-spacing, `--color-text-muted`, `mt-8 mb-3`
- Example cards: 4-column grid (2×2 on narrow screens), each card is `glass-card`, has a short text label at the top and a stroke icon at the bottom-left

#### Example Cards — Icon Mapping

| Card | Icon (use Lucide React) |
|---|---|
| Write a to-do list for a personal project | `User` |
| Generate an email to reply to a job offer | `Mail` |
| Summarize this article in one paragraph | `MessageSquare` |
| How does AI work in a technical capacity | `Code2` |

#### Input Bar

- Full-width, `glass-card` style
- Placeholder: `"✦ Ask Anything...."` — include the sparkle character (✦ U+2726)
- Below the textarea, within the same card: `Attach` button (📎 icon + label) and `Writing Style ∨` dropdown — both are ghost/pill styled, `12px` text
- Send button: `40px` dark circle (`--color-send-btn`), white arrow-up icon, `absolute right-3 bottom-3`

#### Action Bar (below input card)

Pills: `Create Images`, `Study`, `Build`, `Deep Research`, `Learn`

Each pill:
- `glass-card` style with `border-radius: 999px`
- `padding: 6px 14px`
- Small icon (`14px`) to the left of the label
- `13px` text, `--color-pill-text`
- Hover: subtle shadow increase

#### Bottom Branding

- `clonescript.ai` text — bottom-right of the main panel, `12px`, `--color-text-muted`

---

### 2.8 Tailwind Utility Reference

Common patterns the team should use consistently:

| Purpose | Tailwind classes |
|---|---|
| Glass panel | `bg-white/70 backdrop-blur-xl border border-white/60 shadow-sm rounded-[20px]` |
| Glass card | `bg-white/85 backdrop-blur-md border border-gray-200/60 shadow-sm rounded-[14px]` |
| Pill button | `bg-white/80 border border-gray-200/55 rounded-full px-3.5 py-1.5 text-sm text-gray-700` |
| Send button | `bg-[#1a1a2e] text-white rounded-full w-10 h-10 flex items-center justify-center` |
| Muted label | `text-[11px] uppercase tracking-widest text-gray-400` |
| Nav item | `flex items-center gap-2.5 px-2 py-2.5 text-[15px] text-gray-500 rounded-lg hover:bg-white/40` |
| Truncated text | `truncate overflow-hidden whitespace-nowrap` |

---

### 2.9 Responsive Behaviour

The design is desktop-first. Apply these breakpoints:

| Breakpoint | Behaviour |
|---|---|
| `lg` (1024px+) | Full two-panel layout as designed |
| `md` (768–1023px) | Sidebar collapses to icon-only strip `(56px wide)` |
| `sm` (< 768px) | Sidebar hidden, accessible via hamburger menu overlay |

---

## 3. Project Structure

```
src/
├── api/
│   ├── chat.js              # POST /chat and POST /chat/stream fetch wrappers
│   └── health.js            # GET /health and GET /health/readiness
│
├── context/
│   ├── ChatContext.jsx      # Global chat state — conversations, sessions, streaming flag
│   └── chatReducer.js       # All state transitions as pure functions
│
├── components/
│   ├── layout/
│   │   ├── Sidebar.jsx      # Left panel: logo, nav, chat list, upgrade card
│   │   └── MainPanel.jsx    # Right panel: header, chat area, input bar
│   │
│   ├── sidebar/
│   │   ├── NavItem.jsx      # New Chat / Library / Settings / Help links
│   │   ├── ChatListGroup.jsx # "Yesterday" / "5 Days Ago" grouped list
│   │   ├── ChatListItem.jsx  # Single chat history row
│   │   └── UpgradeCard.jsx  # "Upgrade to Pro" dismissible card
│   │
│   ├── chat/
│   │   ├── WelcomeScreen.jsx # Greeting + example prompt cards (shown when no messages)
│   │   ├── MessageList.jsx   # Scrollable list of all messages
│   │   ├── MessageBubble.jsx # User or assistant message with markdown rendering
│   │   ├── StreamingIndicator.jsx # Animated dots shown while tokens stream in
│   │   ├── ToolCallBadge.jsx # Shows which tools were used after response
│   │   └── ExampleCard.jsx   # Clickable prompt suggestion cards
│   │
│   ├── input/
│   │   ├── InputBar.jsx      # Textarea, Attach, Writing Style, Send button
│   │   ├── StreamToggle.jsx  # Toggle between streaming / non-streaming mode
│   │   └── ActionBar.jsx     # Bottom row: Create Images, Study, Build, etc.
│   │
│   └── common/
│       ├── Avatar.jsx        # User avatar (top-right corner)
│       ├── ErrorBanner.jsx   # Inline error display
│       └── LoadingDots.jsx   # Reusable animated dots
│
├── hooks/
│   ├── useChat.js           # Convenience hook — consumes ChatContext
│   ├── useStreamingChat.js  # Manages SSE connection lifecycle
│   └── useHealthCheck.js    # Polls /health/readiness on app load
│
├── pages/
│   ├── ChatPage.jsx         # Main chat page (Sidebar + MainPanel)
│   ├── LibraryPage.jsx      # Placeholder / future
│   └── SettingsPage.jsx     # Placeholder / future
│
├── utils/
│   ├── groupChatsByDate.js  # Groups sessions into "Yesterday", "5 Days Ago", etc.
│   └── parseSSE.js          # Parses raw SSE text lines into structured events
│
├── App.jsx                  # Router setup
├── main.jsx                 # React 18 createRoot entry point
└── index.css                # Tailwind directives + custom CSS variables
```

---

## 4. Core Architecture — Context + useReducer

All chat state lives in a single context. Components read from it via a custom hook.

### State Shape

```js
// context/chatReducer.js

const initialState = {
  // All sessions keyed by session_id
  sessions: {},
  // { [session_id]: { session_id, title, messages: [], createdAt, updatedAt } }

  // The currently active session ID (null = welcome screen)
  activeSessionId: null,

  // Whether the app is waiting for a response
  isLoading: false,

  // Whether SSE streaming mode is active
  streamingEnabled: true,

  // The text being streamed in the current response (partial)
  streamingContent: '',

  // Tools used in the most recent response
  toolsUsed: [],

  // Application-level error message
  error: null,
};
```

### Actions

```js
// All action types
const ACTIONS = {
  NEW_SESSION:          'NEW_SESSION',
  SET_ACTIVE_SESSION:   'SET_ACTIVE_SESSION',
  ADD_USER_MESSAGE:     'ADD_USER_MESSAGE',
  SET_LOADING:          'SET_LOADING',
  APPEND_STREAM_CHUNK:  'APPEND_STREAM_CHUNK',
  COMMIT_STREAM:        'COMMIT_STREAM',       // Finalizes streaming content into a message
  ADD_ASSISTANT_MESSAGE:'ADD_ASSISTANT_MESSAGE', // For non-streaming responses
  SET_ERROR:            'SET_ERROR',
  CLEAR_ERROR:          'CLEAR_ERROR',
  TOGGLE_STREAMING:     'TOGGLE_STREAMING',
  DISMISS_ERROR:        'DISMISS_ERROR',
};
```

### Provider Setup

```jsx
// context/ChatContext.jsx
import { createContext, useContext, useReducer } from 'react';
import { chatReducer, initialState } from './chatReducer';

const ChatContext = createContext(null);

export function ChatProvider({ children }) {
  const [state, dispatch] = useReducer(chatReducer, initialState);
  return (
    <ChatContext.Provider value={{ state, dispatch }}>
      {children}
    </ChatContext.Provider>
  );
}

export const useChatContext = () => useContext(ChatContext);
```

---

## 5. Component Breakdown

### `WelcomeScreen.jsx`

Displayed when `activeSessionId` is null or the active session has no messages.

- Renders the 3D orb image at the top (use an `<img>` or CSS radial gradient sphere)
- Shows `"Good Afternoon, {username}"` — derive time of day from `new Date().getHours()`
- Renders 4 `ExampleCard` components with hardcoded starter prompts
- Clicking an `ExampleCard` populates the `InputBar` textarea and auto-submits

### `MessageList.jsx`

- Maps over `sessions[activeSessionId].messages`
- Each message has a `role` (`'user'` | `'assistant'`) and `content` string
- Auto-scrolls to the bottom when new messages arrive — use a `ref` on a sentinel `<div>` at the bottom and call `ref.current.scrollIntoView({ behavior: 'smooth' })` inside a `useEffect` triggered by message count changes
- While `isLoading` is true, renders a `StreamingIndicator` after the last message

### `MessageBubble.jsx`

```jsx
// User messages: right-aligned, filled background
// Assistant messages: left-aligned, transparent/subtle background

// Assistant message content must be rendered as markdown:
import ReactMarkdown from 'react-markdown';
import rehypeHighlight from 'rehype-highlight';

<ReactMarkdown rehypePlugins={[rehypeHighlight]}>
  {message.content}
</ReactMarkdown>
```

After each assistant message, render `<ToolCallBadge tools={message.toolsUsed} />` if the array is non-empty.

### `InputBar.jsx`

- Controlled `<textarea>` that grows vertically (use CSS `field-sizing: content` or a JS resize approach)
- `Enter` to submit, `Shift+Enter` for newline
- Disable input and send button while `isLoading` is true
- The `StreamToggle` sits inside or beside the input bar — a small pill toggle between `Stream` and `Instant` mode

### `Sidebar.jsx`

- Logo (`clonescript.ai`) and nav links at the top
- Chat list grouped by relative date using `groupChatsByDate.js`
- Each `ChatListItem` shows a truncated title and triggers `SET_ACTIVE_SESSION` on click
- `UpgradeCard` is dismissible — track dismissed state in `localStorage` so it stays gone on reload

---

## 6. API Integration Layer

Centralize all fetch logic in `src/api/`. Never call `fetch` directly from components.

```js
// api/chat.js

const BASE_URL = import.meta.env.VITE_API_BASE_URL;

/**
 * Non-streaming: POST /chat
 * Returns the full response JSON.
 */
export async function sendMessage({ message, session_id = null }) {
  const res = await fetch(`${BASE_URL}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, session_id }),
  });

  if (!res.ok) {
    const err = await res.json();
    throw err; // Throw the full error envelope for consistent handling
  }

  return res.json();
  // Returns: { session_id, response, tools_used, duration_seconds, timestamp, status }
}

/**
 * Streaming: POST /chat/stream
 * Returns a ReadableStream reader for SSE consumption.
 */
export async function sendMessageStream({ message, session_id = null }) {
  const res = await fetch(`${BASE_URL}/chat/stream`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, session_id }),
  });

  if (!res.ok) {
    const err = await res.json();
    throw err;
  }

  return res.body.getReader(); // Caller is responsible for reading and closing
}
```

```js
// api/health.js

export async function checkReadiness() {
  const res = await fetch(`${BASE_URL}/health/readiness`);
  return res.json();
  // Returns: { ready, status, checks }
}
```

---

## 7. SSE Streaming Implementation

Use a custom hook to manage the full SSE lifecycle. **Do not use `EventSource`** — the API requires a `POST` body, and `EventSource` only supports `GET`. Use `fetch` with a `ReadableStream` reader instead.

```js
// hooks/useStreamingChat.js
import { useCallback } from 'react';
import { useChatContext } from '../context/ChatContext';
import { sendMessageStream } from '../api/chat';
import { ACTIONS } from '../context/chatReducer';

export function useStreamingChat() {
  const { dispatch } = useChatContext();

  const sendStreaming = useCallback(async ({ message, session_id }) => {
    dispatch({ type: ACTIONS.SET_LOADING, payload: true });
    dispatch({ type: ACTIONS.ADD_USER_MESSAGE, payload: { content: message } });

    let reader;
    try {
      reader = await sendMessageStream({ message, session_id });
      const decoder = new TextDecoder();
      let buffer = '';
      let isMetadataNext = false;

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop(); // Keep incomplete last line in buffer

        for (const line of lines) {
          if (line.startsWith('event: metadata')) {
            isMetadataNext = true;
          } else if (line.startsWith('event: error')) {
            isMetadataNext = false;
            // Next data line will be the error message
          } else if (line.startsWith('data: ')) {
            const data = line.slice(6); // Strip "data: " prefix

            if (data === '[DONE]') {
              dispatch({ type: ACTIONS.COMMIT_STREAM });
              break;
            }

            if (isMetadataNext) {
              const meta = JSON.parse(data);
              dispatch({ type: ACTIONS.COMMIT_STREAM, payload: meta });
              isMetadataNext = false;
            } else {
              dispatch({ type: ACTIONS.APPEND_STREAM_CHUNK, payload: data });
            }
          }
        }
      }
    } catch (err) {
      dispatch({ type: ACTIONS.SET_ERROR, payload: err.message || 'Stream failed' });
    } finally {
      reader?.cancel();
      dispatch({ type: ACTIONS.SET_LOADING, payload: false });
    }
  }, [dispatch]);

  return { sendStreaming };
}
```

### Reducer Handling for Streaming

```js
// In chatReducer.js

case ACTIONS.APPEND_STREAM_CHUNK:
  return { ...state, streamingContent: state.streamingContent + action.payload };

case ACTIONS.COMMIT_STREAM: {
  const meta = action.payload || {};
  const finalMessage = {
    role: 'assistant',
    content: state.streamingContent,
    toolsUsed: meta.tools_used || [],
    timestamp: meta.timestamp,
  };
  const sessionId = meta.session_id || state.activeSessionId;
  // Append finalMessage to the session's messages array
  // Update activeSessionId if this was a new session
  return {
    ...state,
    activeSessionId: sessionId,
    streamingContent: '',
    sessions: appendMessageToSession(state.sessions, sessionId, finalMessage),
  };
}
```

---

## 8. Session Management

The session ID comes from the API — never invent your own except as a UI-only temporary key before the first response.

```
Start new chat
  └─> User types message
      └─> Send with session_id: null
          └─> API returns session_id: "uuid-abc"
              └─> Store in context, persist to localStorage
                  └─> All future messages in this chat send session_id: "uuid-abc"
```

**Persistence strategy:**

- On `COMMIT_STREAM` or `ADD_ASSISTANT_MESSAGE`, save the entire `sessions` map to `localStorage` under the key `clonescript_sessions`
- On app load (`ChatProvider` mount), rehydrate from `localStorage`
- This gives the user their history back after a browser refresh, matching what the sidebar displays

**localStorage schema:**

```json
{
  "clonescript_sessions": {
    "uuid-abc": {
      "session_id": "uuid-abc",
      "title": "Write a to-do list for a personal...",
      "messages": [],
      "createdAt": "2026-04-16T10:00:00Z",
      "updatedAt": "2026-04-16T10:05:00Z"
    }
  }
}
```

The `title` is auto-generated from the first 40 characters of the user's first message.

---

## 9. Routing

```jsx
// App.jsx
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';

<BrowserRouter>
  <Routes>
    <Route path="/" element={<ChatPage />} />
    <Route path="/chat/:sessionId" element={<ChatPage />} />
    <Route path="/library" element={<LibraryPage />} />
    <Route path="/settings" element={<SettingsPage />} />
    <Route path="*" element={<Navigate to="/" />} />
  </Routes>
</BrowserRouter>
```

When a user clicks a chat from the sidebar, navigate to `/chat/:sessionId`. The `ChatPage` reads the param and dispatches `SET_ACTIVE_SESSION`.

---

## 10. Error Handling Strategy

All API errors follow the same envelope shape from the backend:

```json
{
  "error": "rate_limit_exceeded",
  "message": "Too many requests.",
  "status_code": 429,
  "timestamp": "...",
  "request_id": "...",
  "details": null
}
```

Handle them uniformly:

| Status | UX Behavior |
|---|---|
| `422` | Show inline field validation message near input |
| `429` | Show `ErrorBanner` with countdown using `Retry-After` header value |
| `500` | Show `ErrorBanner`: "Something went wrong. Try again." |
| `502` | Show `ErrorBanner`: "The agent encountered an error." |
| `503` | Show `ErrorBanner`: "Service is starting up. Please wait…" + auto-retry after 3s |

**`useHealthCheck` hook:** On app mount, call `GET /health/readiness`. If `ready` is `false`, show a top banner warning and disable the input. Poll every 5 seconds until ready, then remove the banner.

---

## 11. Environment Configuration

```bash
# .env.local (never commit this file)
VITE_API_BASE_URL=http://localhost:8800
```

Access in code:
```js
const BASE_URL = import.meta.env.VITE_API_BASE_URL;
```

For production deployments, update this variable per environment in CI/CD.

---

## 12. Implementation Checklist

Use this to track progress sprint by sprint.

### Phase 1 — Foundation
- [ ] Scaffold project: `npm create vite@latest . -- --template react`
- [ ] Install Tailwind CSS v3 and configure `tailwind.config.js`
- [ ] Install `react-router-dom`, `react-markdown`, `rehype-highlight`, `uuid`, `date-fns`
- [ ] Create folder structure as defined in Section 2
- [ ] Implement `ChatContext` + `chatReducer` with all action types
- [ ] Set up `.env.local` with `VITE_API_BASE_URL`

### Phase 2 — Layout & Static UI
- [ ] Build `Sidebar` with logo, nav items, chat list groups, and upgrade card
- [ ] Build `MainPanel` shell with header and scrollable content area
- [ ] Build `WelcomeScreen` with orb, greeting, and 4 example cards
- [ ] Build `InputBar` with textarea auto-resize, Attach, Writing Style dropdown, Send button
- [ ] Build `StreamToggle` pill component
- [ ] Build `ActionBar` (Create Images, Study, Build, Deep Research, Learn)
- [ ] Match visual design: glassmorphism sidebar, soft gradient background, card styles

### Phase 3 — API Integration
- [ ] Implement `api/chat.js` — non-streaming `sendMessage`
- [ ] Implement `api/chat.js` — streaming `sendMessageStream`
- [ ] Implement `api/health.js` — `checkReadiness`
- [ ] Implement `useHealthCheck` hook with polling and banner
- [ ] Implement `useChat` convenience hook

### Phase 4 — Chat Features
- [ ] Implement `MessageList` with auto-scroll
- [ ] Implement `MessageBubble` with markdown + code highlighting
- [ ] Implement `useStreamingChat` hook
- [ ] Wire up non-streaming path through `useChat`
- [ ] Implement `StreamToggle` switching logic in context
- [ ] Implement `ToolCallBadge` display
- [ ] Implement `StreamingIndicator` animated dots

### Phase 5 — Session & History
- [ ] Auto-generate session titles from first message
- [ ] Persist sessions to `localStorage` on each update
- [ ] Rehydrate sessions from `localStorage` on app load
- [ ] Wire sidebar chat list to real session data
- [ ] Wire `/chat/:sessionId` route to restore active session

### Phase 6 — Error Handling & Polish
- [ ] Implement `ErrorBanner` component
- [ ] Handle all 5 error status codes per strategy in Section 9
- [ ] Implement `429` retry countdown
- [ ] Implement `503` auto-retry logic
- [ ] Accessibility: keyboard navigation, ARIA labels on interactive elements
- [ ] Test on mobile viewport (responsive sidebar collapse)
