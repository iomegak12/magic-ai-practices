# MSAv15 Customer Service Portal - Front-End Specification & Implementation Guide

**Version:** 1.0.0  
**Date:** February 20, 2026  
**Product Manager:** Ramkumar  
**Document Type:** Product Specification & Implementation Guide  
**Target Audience:** Front-End Development Team

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Product Overview](#2-product-overview)
3. [Technical Stack](#3-technical-stack)
4. [Project Structure](#4-project-structure)
5. [Architecture & Design Patterns](#5-architecture--design-patterns)
6. [REST API Integration](#6-rest-api-integration)
7. [UI/UX Specifications](#7-uiux-specifications)
8. [Feature Specifications](#8-feature-specifications)
9. [State Management](#9-state-management)
10. [Docker Configuration](#10-docker-configuration)
11. [Project Documentation](#11-project-documentation)
12. [Development Guidelines](#12-development-guidelines)
13. [Deployment Strategy](#13-deployment-strategy)

---

## 1. Executive Summary

### 1.1 Purpose
This document provides comprehensive specifications and implementation guidelines for building the MSAv15 Customer Service Portal - a React-based web application that provides support agents with an intuitive interface to interact with the AI-powered customer service agent.

### 1.2 Goals
- Enable support agents to assist customers through an AI-powered conversational interface
- Provide session management for handling multiple customer conversations
- Support both streaming and non-streaming response modes
- Deliver a professional, enterprise-grade user experience
- Ensure easy deployment via Docker containers

### 1.3 Target Users
- **Primary:** Customer support agents (internal tool)
- **Use Case:** Assisting customers with orders and complaints through AI agent
- **Access:** No authentication required (demo/internal access)

---

## 2. Product Overview

### 2.1 Application Description
The MSAv15 Customer Service Portal is a web-based internal tool that allows support agents to interact with an AI customer service agent via a conversational interface. The agent can handle order management and complaint resolution through natural language interactions.

### 2.2 Key Features
- **Multi-page Portal:** Home, About Us, Contact Us, and Support (Chat)
- **AI Chat Interface:** Real-time conversation with customer service agent
- **Session Management:** View, switch, and manage multiple conversation sessions
- **Streaming Toggle:** Switch between real-time streaming and complete responses
- **Professional UI:** Built with Tabler Admin Template for enterprise look-and-feel

### 2.3 Integration
- **Backend API:** MSAv15Service REST API (http://localhost:9080)
- **Communication:** HTTP/REST with optional Server-Sent Events (SSE) for streaming

---

## 3. Technical Stack

### 3.1 Core Technologies

```
Frontend Framework:      React 18+ (with Hooks and Functional Components)
Build Tool:             Vite or Create React App
Server:                 Node.js v22 + Express (for serving React app)
Templating:             Tabler Admin Template (Free Edition, CDN-based)
State Management:       React Context API
HTTP Client:            Axios or Fetch API
Styling:                Tabler CSS (via CDN)
Port:                   9090
```

### 3.2 Development Tools

```
Package Manager:        npm or yarn
Node Version:          v22 (Alpine in Docker)
Container:             Docker + Docker Compose
Version Control:       Git
License:               MIT
```

### 3.3 Key Libraries (Recommended)

```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.0",
    "axios": "^1.6.0",
    "express": "^4.18.0"
  },
  "devDependencies": {
    "vite": "^5.0.0",
    "@vitejs/plugin-react": "^4.2.0"
  }
}
```

---

## 4. Project Structure

### 4.1 Recommended Directory Structure

```
customer-service-portal/
│
├── public/                          # Static assets
│   ├── favicon.ico
│   └── index.html                  # HTML with Tabler CDN links
│
├── src/
│   ├── components/                 # Reusable React components
│   │   ├── common/                # Common UI components
│   │   │   ├── Header.jsx
│   │   │   ├── Footer.jsx
│   │   │   ├── Sidebar.jsx
│   │   │   └── Loader.jsx
│   │   │
│   │   ├── chat/                  # Chat-related components
│   │   │   ├── ChatWindow.jsx
│   │   │   ├── ChatMessage.jsx
│   │   │   ├── ChatInput.jsx
│   │   │   ├── StreamingToggle.jsx
│   │   │   └── TypingIndicator.jsx
│   │   │
│   │   └── sessions/              # Session management components
│   │       ├── SessionList.jsx
│   │       ├── SessionItem.jsx
│   │       └── CreateSessionButton.jsx
│   │
│   ├── pages/                     # Page components
│   │   ├── HomePage.jsx
│   │   ├── AboutPage.jsx
│   │   ├── ContactPage.jsx
│   │   └── SupportPage.jsx
│   │
│   ├── context/                   # React Context for state management
│   │   ├── ChatContext.jsx
│   │   └── SessionContext.jsx
│   │
│   ├── services/                  # API integration services
│   │   ├── api.js                # Axios instance and config
│   │   ├── chatService.js        # Chat API methods
│   │   └── healthService.js      # Health check API
│   │
│   ├── utils/                     # Utility functions
│   │   ├── dateFormatter.js
│   │   ├── sessionStorage.js
│   │   └── constants.js
│   │
│   ├── hooks/                     # Custom React hooks
│   │   ├── useChatStream.js
│   │   └── useSessionManager.js
│   │
│   ├── App.jsx                    # Root component with routing
│   ├── main.jsx                   # Application entry point
│   └── routes.jsx                 # Route definitions
│
├── server/                        # Express server for serving React
│   └── server.js
│
├── docs/                          # Additional documentation
│   ├── API_INTEGRATION.md
│   └── DEPLOYMENT.md
│
├── .dockerignore                  # Docker ignore patterns
├── .gitignore                     # Git ignore patterns
├── Dockerfile                     # Docker configuration
├── docker-compose.yml             # Docker Compose orchestration
├── package.json                   # Node dependencies
├── README.md                      # Project documentation
├── CONTRIBUTING.md                # Contribution guidelines
├── LICENSE                        # MIT License
└── vite.config.js                 # Build configuration (if using Vite)
```

### 4.2 File Organization Principles

- **Component-based:** Each UI element should be a reusable component
- **Feature separation:** Group related components together
- **Service layer:** Separate API logic from UI components
- **Context for state:** Use React Context for global state (chat, sessions)
- **Hooks for logic:** Extract complex logic into custom hooks

---

## 5. Architecture & Design Patterns

### 5.1 Application Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Browser (Port 9090)                      │
│  ┌────────────────────────────────────────────────────┐    │
│  │         React Application (SPA)                     │    │
│  │  ├── React Router (Navigation)                      │    │
│  │  ├── Context API (State Management)                 │    │
│  │  ├── Pages (Home, About, Contact, Support)         │    │
│  │  └── Components (Chat, Sessions, UI Elements)      │    │
│  └────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ HTTP/REST Requests
                            │ (Axios/Fetch)
                            ↓
┌─────────────────────────────────────────────────────────────┐
│              MSAv15Service API (Port 9080)                  │
│  ├── GET  /health                                           │
│  ├── POST /chat (streaming & non-streaming)                │
│  └── GET  / (service info)                                  │
└─────────────────────────────────────────────────────────────┘
```

### 5.2 Design Patterns

#### 5.2.1 Component Patterns
- **Container/Presentational:** Separate logic (containers) from UI (presentational)
- **Compound Components:** Complex components (e.g., ChatWindow) composed of smaller parts
- **Custom Hooks:** Reusable logic (e.g., `useChatStream`, `useSessionManager`)

#### 5.2.2 State Management Pattern
```
Context Providers (Global State)
    ↓
Custom Hooks (Access State)
    ↓
Components (Render UI)
```

#### 5.2.3 Service Layer Pattern
```
Component → Service → API → Backend
            (axios)  (REST)
```

### 5.3 Data Flow

#### Non-Streaming Chat Flow:
```
1. User types message in ChatInput
2. Component calls chatService.sendMessage()
3. Service makes POST /chat with message
4. Backend processes and returns complete response
5. ChatContext updates with new message
6. ChatWindow re-renders with response
```

#### Streaming Chat Flow:
```
1. User enables streaming toggle
2. User types message in ChatInput
3. Component calls chatService.sendStreamingMessage()
4. Service establishes SSE connection to POST /chat?stream=true
5. Backend sends response chunks via SSE events
6. Each chunk updates ChatContext in real-time
7. ChatWindow renders incrementally as chunks arrive
8. Connection closes on "done" event
```

---

## 6. REST API Integration

### 6.1 Backend Service Details

**Base URL:** `http://localhost:9080`  
**API Version:** 0.1.0  
**Content Type:** `application/json`  
**CORS:** Enabled (supports requests from http://localhost:9090)

### 6.2 API Endpoints

#### 6.2.1 Health Check

**Endpoint:** `GET /health`  
**Description:** Check if the backend service is running and healthy  
**Authentication:** None

**Response (200 OK):**
```json
{
  "status": "healthy",
  "service": "MSAv15Service",
  "version": "0.1.0",
  "timestamp": "2026-02-20T10:30:00.000Z",
  "dependencies": {
    "database": "connected",
    "mcp_server": "reachable"
  }
}
```

**Usage:**
- Call on application startup to verify backend availability
- Implement health check indicator in UI sidebar/footer
- Poll periodically (every 30 seconds) to monitor connection

---

#### 6.2.2 Chat Endpoint (Non-Streaming)

**Endpoint:** `POST /chat`  
**Description:** Send a message to the AI customer service agent  
**Authentication:** None

**Request Headers:**
```
Content-Type: application/json
Accept: application/json
```

**Request Body:**
```json
{
  "session_id": "optional-uuid-string",
  "message": "I want to place an order for a laptop",
  "stream": false
}
```

**Request Body Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `session_id` | string | No | UUID for multi-turn conversation. If omitted, backend creates new session |
| `message` | string | Yes | User's message to the agent (min 1 character) |
| `stream` | boolean | No | Set to `false` for complete response (default: false) |

**Response (200 OK):**
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "response": "I'd be happy to help you place an order for a laptop. To proceed, I'll need the following information:\n\n1. Product SKU (e.g., LAPTOP-HP-001)\n2. Quantity\n3. Billing address\n4. Your name\n\nPlease provide these details.",
  "timestamp": "2026-02-20T10:32:15.000Z",
  "metadata": {
    "turn_count": 1,
    "tools_used": [],
    "tokens_used": 0,
    "streaming": false
  }
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `session_id` | string | Session identifier (use for subsequent messages) |
| `response` | string | Agent's complete response text |
| `timestamp` | string (ISO 8601) | When response was generated |
| `metadata` | object | Additional information about the interaction |
| `metadata.turn_count` | integer | Number of turns in this session |
| `metadata.tools_used` | array | List of tools the agent invoked |
| `metadata.tokens_used` | integer | Token count (for monitoring) |
| `metadata.streaming` | boolean | Whether streaming was used |

**Error Response (500 Internal Server Error):**
```json
{
  "detail": "Agent execution failed: Connection timeout"
}
```

**Example cURL:**
```bash
curl -X POST http://localhost:9080/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Show me all my orders",
    "stream": false
  }'
```

---

#### 6.2.3 Chat Endpoint (Streaming)

**Endpoint:** `POST /chat` (with stream=true)  
**Description:** Send a message and receive response in real-time via Server-Sent Events  
**Authentication:** None

**Request Headers:**
```
Content-Type: application/json
Accept: text/event-stream
```

**Request Body:**
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "Update order 123 status to Shipped",
  "stream": true
}
```

**SSE Response Stream:**

The response is sent as Server-Sent Events with the following event types:

**Event: `message` (response chunk)**
```
event: message
data: {"chunk": "I'll update the ", "session_id": "550e8400-e29b-41d4-a716-446655440000"}

event: message
data: {"chunk": "order status for ", "session_id": "550e8400-e29b-41d4-a716-446655440000"}

event: message
data: {"chunk": "you right away.", "session_id": "550e8400-e29b-41d4-a716-446655440000"}
```

**Event: `done` (completion)**
```
event: done
data: {
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "metadata": {
    "turn_count": 3,
    "streaming": true
  }
}
```

**Event: `error` (error occurred)**
```
event: error
data: {
  "error": "Connection timeout",
  "session_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Implementation Guide:**

1. Use `EventSource` API or a library like `eventsource` for Node.js
2. Listen for `message` events and append chunks to UI
3. Listen for `done` event to finalize the response
4. Listen for `error` events to handle failures
5. Close the connection after receiving `done` or `error`

**Example JavaScript (Browser):**
```javascript
// Create EventSource for streaming
const eventSource = new EventSource('http://localhost:9080/chat?stream=true');

eventSource.addEventListener('message', (event) => {
  const data = JSON.parse(event.data);
  appendChunkToUI(data.chunk); // Update UI with chunk
});

eventSource.addEventListener('done', (event) => {
  const data = JSON.parse(event.data);
  console.log('Streaming complete', data.metadata);
  eventSource.close();
});

eventSource.addEventListener('error', (event) => {
  const data = JSON.parse(event.data);
  console.error('Streaming error:', data.error);
  eventSource.close();
});
```

**Note:** For POST requests with EventSource, you may need to use `fetch()` with streaming response handling or a library that supports POST with SSE.

---

#### 6.2.4 Service Info

**Endpoint:** `GET /`  
**Description:** Get basic service information  
**Authentication:** None

**Response (200 OK):**
```json
{
  "service": "MSAv15Service",
  "version": "0.1.0",
  "status": "running",
  "documentation": "http://localhost:9080/docs",
  "health": "http://localhost:9080/health"
}
```

---

### 6.3 API Integration Service Implementation Specs

Create a service layer that abstracts API calls:

**File: `src/services/api.js`**
- Configure Axios instance with base URL (`http://localhost:9080`)
- Set default headers (`Content-Type: application/json`)
- Implement request/response interceptors for error handling
- Export configured Axios instance

**File: `src/services/chatService.js`**
```javascript
// Expected methods:

/**
 * Send a non-streaming chat message
 * @param {string} message - User's message
 * @param {string} sessionId - Optional session ID
 * @returns {Promise<ChatResponse>}
 */
sendMessage(message, sessionId = null)

/**
 * Send a streaming chat message
 * @param {string} message - User's message
 * @param {string} sessionId - Optional session ID
 * @param {function} onChunk - Callback for each chunk
 * @param {function} onDone - Callback when complete
 * @param {function} onError - Callback on error
 * @returns {EventSource} - EventSource instance for cleanup
 */
sendStreamingMessage(message, sessionId, onChunk, onDone, onError)
```

**File: `src/services/healthService.js`**
```javascript
// Expected methods:

/**
 * Check backend service health
 * @returns {Promise<HealthResponse>}
 */
checkHealth()
```

---

### 6.4 Error Handling

#### Expected Error Scenarios:

1. **Network Error (Backend Offline)**
   - Detection: Request timeout or connection refused
   - UI Action: Show "Service Unavailable" message with retry option

2. **500 Internal Server Error**
   - Detection: HTTP 500 status code
   - UI Action: Show "Agent Error" message with error details

3. **Streaming Connection Lost**
   - Detection: EventSource error or timeout
   - UI Action: Show "Connection Lost" and retry streaming

4. **Invalid Request (400 Bad Request)**
   - Detection: HTTP 400 status code
   - UI Action: Show validation error message

#### Error Handling Strategy:
- Implement global error boundary in React
- Show user-friendly error messages (avoid technical jargon)
- Provide "Retry" action for transient failures
- Log errors to console for debugging (in development)

---

## 7. UI/UX Specifications

### 7.1 Tabler Admin Template Integration

**CDN Links (Add to `public/index.html`):**

```html
<!-- Tabler Core CSS -->
<link href="https://cdn.jsdelivr.net/npm/@tabler/core@latest/dist/css/tabler.min.css" rel="stylesheet"/>

<!-- Tabler Icons -->
<link href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/tabler-icons.min.css" rel="stylesheet"/>

<!-- Tabler JS (Optional, for interactive components) -->
<script src="https://cdn.jsdelivr.net/npm/@tabler/core@latest/dist/js/tabler.min.js"></script>
```

**Theme Configuration:**
- Use Tabler's default theme (light mode)
- Primary color: Tabler default blue (#206bc4)
- Sidebar navigation with menu items
- Top header with branding and user info placeholder

### 7.2 Layout Structure

**Global Layout:**
```
┌─────────────────────────────────────────────────────┐
│  Header (Branding, Navigation, Health Status)      │
├──────────┬──────────────────────────────────────────┤
│          │                                          │
│ Sidebar  │         Page Content Area                │
│ (Menu)   │                                          │
│          │                                          │
│          │                                          │
├──────────┴──────────────────────────────────────────┤
│  Footer (Copyright, Version)                        │
└─────────────────────────────────────────────────────┘
```

**Sidebar Menu Items:**
1. 🏠 Home
2. ℹ️ About Us
3. 📞 Contact Us
4. 💬 Support (Chat)

### 7.3 Responsive Design
- Desktop-first approach (primary use case)
- Collapsible sidebar on mobile (hamburger menu)
- Minimum supported width: 320px (mobile)
- Breakpoints: Follow Tabler's responsive breakpoints

### 7.4 Accessibility
- Semantic HTML5 elements
- ARIA labels for interactive elements
- Keyboard navigation support
- Sufficient color contrast (WCAG AA compliant)

---

## 8. Feature Specifications

### 8.1 Home Page

**Route:** `/`  
**Purpose:** Welcome page with service overview

**Content Sections:**

1. **Hero Section**
   - Heading: "MSAv15 Customer Service Portal"
   - Subheading: "AI-Powered Support Agent for Order & Complaint Management"
   - CTA Button: "Go to Support Chat" → Navigate to `/support`

2. **Features Overview (Cards/Grid)**
   - **AI Customer Service Agent**
     - Icon: 🤖
     - Description: "Intelligent agent that handles orders and complaints through natural conversation"
   - **Session Management**
     - Icon: 💬
     - Description: "Manage multiple customer conversations simultaneously"
   - **Real-time Responses**
     - Icon: ⚡
     - Description: "Choose between streaming or complete responses based on your preference"

3. **Quick Stats (Optional)**
   - Service Status: "Operational" (from health check)
   - API Version: Display from backend
   - Sessions Active: Show count from session context

**Design Notes:**
- Use Tabler's card components for feature showcase
- Include relevant Tabler icons
- Professional, clean design with clear CTAs

---

### 8.2 About Us Page

**Route:** `/about`  
**Purpose:** Information about the application and team

**Content Sections:**

1. **About the Application**
   - Heading: "About MSAv15 Service"
   - Content:
     - Overview of the customer service portal
     - Purpose: Internal tool for support agents
     - Technology: AI-powered by Microsoft Agent Framework
     - Capabilities: Order management, complaint handling

2. **Team Information**
   - Product Manager: Ramkumar
   - Development Team: CAP (Chandini, Ashok, Priya)
   - Version: 1.0.0

3. **Technology Stack**
   - Frontend: React 18+ with Tabler Admin
   - Backend: FastAPI with Microsoft Agent Framework
   - AI: Azure OpenAI (GPT-4o)

**Design Notes:**
- Use Tabler's typography classes for clean text presentation
- Include team member cards with roles
- Add version badge

---

### 8.3 Contact Us Page

**Route:** `/contact`  
**Purpose:** Contact information and support channels

**Content Sections:**

1. **Contact Information**
   - Product Manager: Ramkumar
   - Email: ram@example.com (placeholder)
   - Team: CAP Development Team

2. **Support Channels**
   - Primary: Use the Support Chat (link to `/support`)
   - Email Support: support@example.com (placeholder)
   - Documentation: Link to backend API docs (http://localhost:9080/docs)

3. **Feedback Form (Optional Future Enhancement)**
   - Note: "For immediate assistance, please use the Support Chat"

**Design Notes:**
- Use Tabler's contact card layouts
- Include icons for each contact method
- Emphasize the Support Chat as primary channel

---

### 8.4 Support Page (Chat Interface)

**Route:** `/support`  
**Purpose:** Main chat interface for interacting with AI agent

**Layout:**

```
┌─────────────────────────────────────────────────────────────┐
│  Support - Customer Service Agent                          │
├───────────────────┬─────────────────────────────────────────┤
│                   │                                         │
│  Session List     │         Chat Window                     │
│  ┌─────────────┐ │  ┌───────────────────────────────────┐ │
│  │ + New       │ │  │ Agent: How can I help you today? │ │
│  │   Session   │ │  │                                   │ │
│  └─────────────┘ │  │ User: Show me my orders           │ │
│                   │  │                                   │ │
│  ┌─────────────┐ │  │ Agent: I found 3 orders...       │ │
│  │ Session #1  │ │  │                                   │ │
│  │ 5 turns     │ │  └───────────────────────────────────┘ │
│  └─────────────┘ │                                         │
│                   │  ┌───────────────────────────────────┐ │
│  ┌─────────────┐ │  │ [Streaming: ON/OFF]               │ │
│  │ Session #2  │ │  │ Type message...          [Send]    │ │
│  │ 2 turns     │ │  └───────────────────────────────────┘ │
│  └─────────────┘ │                                         │
│                   │                                         │
└───────────────────┴─────────────────────────────────────────┘
```

#### 8.4.1 Session List (Left Sidebar)

**Purpose:** Manage multiple conversation sessions

**Components:**

1. **Create New Session Button**
   - Label: "+ New Session"
   - Action: Create new session (generates UUID)
   - Effect: Clears chat window and starts fresh conversation

2. **Session List Items**
   - Display: Session ID (shortened, e.g., "Session ...440000")
   - Metadata: Turn count (e.g., "5 turns")
   - Timestamp: Last message time (e.g., "5 mins ago")
   - Visual: Highlight active session
   - Action: Click to switch to that session

3. **Session Actions (on hover/context menu)**
   - Delete session (clear from local storage)
   - Copy session ID
   - Export chat history (future enhancement)

**Data Storage:**
- Use browser `localStorage` to persist sessions
- Store session ID and conversation history
- Limit: Store last 10 sessions (configurable)

**State Management:**
- Store in `SessionContext`
- Track: `activeSessionId`, `sessions[]`
- Methods: `createSession()`, `switchSession()`, `deleteSession()`

---

#### 8.4.2 Chat Window (Main Area)

**Purpose:** Display conversation between agent and user

**Components:**

1. **Message List (Scrollable)**
   - Auto-scroll to bottom on new message
   - Show user and agent messages with distinct styling
   - Timestamp for each message
   - Loading indicator while waiting for response

**Message Types:**

**User Message:**
```
┌─────────────────────────────────────┐
│  User (You)                10:30 AM │
│  Show me all my orders              │
└─────────────────────────────────────┘
```

**Agent Message:**
```
┌─────────────────────────────────────┐
│  AI Agent                  10:30 AM │
│  I found 3 orders for you:          │
│  1. Order #123 - Laptop - Delivered │
│  2. Order #124 - Mouse - Shipped    │
│  3. Order #125 - Keyboard - Pending │
└─────────────────────────────────────┘
```

**System Message (e.g., session created):**
```
┌─────────────────────────────────────┐
│        New session created          │
│    Session ID: 550e8400-e29b...     │
└─────────────────────────────────────┘
```

**Styling:**
- User messages: Right-aligned, blue background (Tabler primary)
- Agent messages: Left-aligned, gray background
- System messages: Center-aligned, subtle styling
- Use Tabler's message/card components

2. **Typing Indicator (During Response)**
   - Show when waiting for agent response
   - Animation: "Agent is typing..."
   - Hide when response received

3. **Error Message Display**
   - Show when API call fails
   - Styling: Red border/background (Tabler danger)
   - Include retry button

---

#### 8.4.3 Chat Input (Bottom)

**Purpose:** User input for sending messages to agent

**Components:**

1. **Streaming Toggle Switch**
   - Position: Above text input (top right)
   - Label: "Streaming"
   - Control: Toggle switch (Tabler switch component)
   - State: ON (streaming) / OFF (non-streaming)
   - Tooltip: "Enable for real-time word-by-word responses"

2. **Message Text Input**
   - Type: Textarea (multi-line)
   - Placeholder: "Type your message here..."
   - Max height: 150px (auto-expand up to limit)
   - Enter key: Send message
   - Shift+Enter: New line

3. **Send Button**
   - Label: Icon (paper plane) or "Send"
   - State: Disabled when input empty or sending
   - Loading state while waiting for response
   - Keyboard shortcut: Enter

**Behavior:**

**Non-Streaming Mode:**
1. User types message and clicks Send
2. Disable input and show loading indicator
3. Send POST /chat with `stream: false`
4. Wait for complete response
5. Display complete response in chat window
6. Re-enable input

**Streaming Mode:**
1. User types message and clicks Send
2. Disable input and show typing indicator
3. Send POST /chat with `stream: true`
4. Establish SSE connection
5. Display each chunk as it arrives in real-time
6. On completion, re-enable input

---

### 8.5 Common UI Components

#### 8.5.1 Header

**Content:**
- Left: Logo/Branding "MSAv15 Portal"
- Center: Navigation (optional, or use sidebar only)
- Right: Health status indicator + Service version

**Health Status Indicator:**
- Icon: Circle (●)
- Colors:
  - Green: Service healthy
  - Yellow: Service degraded
  - Red: Service unavailable
- Tooltip: Show health check details on hover

#### 8.5.2 Sidebar Navigation

**Menu Items:**
```
🏠 Home
ℹ️ About Us
📞 Contact Us
💬 Support
```

**Behavior:**
- Highlight active route
- Collapse on mobile
- Use Tabler's sidebar component

#### 8.5.3 Footer

**Content:**
- Left: "© 2026 MSAv15 Service. All rights reserved."
- Center: "Team CAP"
- Right: Version number from backend

---

## 9. State Management

### 9.1 React Context Architecture

Two primary contexts:

#### 9.1.1 ChatContext

**Purpose:** Manage chat messages and agent interactions

**State:**
```javascript
{
  messages: [
    {
      id: "uuid",
      type: "user" | "agent" | "system",
      content: "message text",
      timestamp: "2026-02-20T10:30:00Z",
      sessionId: "session-uuid"
    }
  ],
  isLoading: false,
  error: null,
  streamingEnabled: false
}
```

**Methods:**
- `sendMessage(message, sessionId)`
- `sendStreamingMessage(message, sessionId)`
- `addMessage(message)`
- `clearMessages(sessionId)`
- `toggleStreaming()`
- `setError(error)`
- `setLoading(isLoading)`

#### 9.1.2 SessionContext

**Purpose:** Manage conversation sessions

**State:**
```javascript
{
  sessions: [
    {
      id: "uuid",
      createdAt: "2026-02-20T10:00:00Z",
      lastMessageAt: "2026-02-20T10:30:00Z",
      turnCount: 5,
      messages: [] // Array of message objects
    }
  ],
  activeSessionId: "current-session-uuid"
}
```

**Methods:**
- `createSession()` - Generate new session UUID and add to list
- `switchSession(sessionId)` - Change active session
- `deleteSession(sessionId)` - Remove session from list
- `getActiveSession()` - Get current session object
- `updateSessionMetadata(sessionId, metadata)` - Update turn count, timestamp

### 9.2 Local Storage Persistence

**Session Storage Strategy:**
- Store sessions array in `localStorage` with key: `msav15_sessions`
- Store each session's messages separately: `msav15_messages_${sessionId}`
- Maximum stored sessions: 10 (remove oldest when limit reached)
- Sync with localStorage on every state update

**Implementation:**
```javascript
// Save to localStorage
localStorage.setItem('msav15_sessions', JSON.stringify(sessions));

// Load from localStorage on app startup
const savedSessions = JSON.parse(localStorage.getItem('msav15_sessions') || '[]');
```

### 9.3 Custom Hooks

#### useChatStream Hook

**Purpose:** Handle SSE streaming logic

**Usage:**
```javascript
const { startStream, stopStream, isStreaming } = useChatStream({
  onChunk: (chunk) => { /* append to UI */ },
  onDone: (metadata) => { /* finalize */ },
  onError: (error) => { /* handle error */ }
});
```

#### useSessionManager Hook

**Purpose:** Simplify session operations

**Usage:**
```javascript
const {
  sessions,
  activeSession,
  createSession,
  switchSession,
  deleteSession
} = useSessionManager();
```

---

## 10. Docker Configuration

### 10.1 Dockerfile Specifications

**File:** `Dockerfile`

**Configuration Details:**

```dockerfile
# Base image: Node.js 22 Alpine (lightweight)
FROM node:22-alpine

# Working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy application source
COPY . .

# Build React application
RUN npm run build

# Expose port
EXPOSE 9090

# Environment variables (can be overridden)
ENV NODE_ENV=production
ENV PORT=9090
ENV API_BASE_URL=http://localhost:9080

# Start Express server to serve React build
CMD ["node", "server/server.js"]
```

**Key Points:**
- Uses Node.js 22 Alpine (smallest footprint)
- Production dependencies only
- Builds React app during image creation
- Serves via Express server on port 9090
- Environment variables for configuration

---

### 10.2 Express Server Specifications

**File:** `server/server.js`

**Requirements:**
- Serve static React build files from `dist/` or `build/`
- Handle React Router (serve `index.html` for all routes)
- Proxy API requests to backend (optional, for CORS)
- Port: 9090
- Health check endpoint: `GET /api/health` (local check)

**Configuration:**
```javascript
// Expected structure
const express = require('express');
const path = require('path');
const app = express();

// Serve static files from React build
app.use(express.static(path.join(__dirname, '../dist')));

// Handle React Router - serve index.html for all routes
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, '../dist/index.html'));
});

// Start server
const PORT = process.env.PORT || 9090;
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
```

---

### 10.3 Docker Compose Specifications

**File:** `docker-compose.yml`

**Configuration Details:**

```yaml
# No version field (modern Docker Compose format)

services:
  frontend:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: msav15-frontend
    ports:
      - "9090:9090"
    environment:
      - NODE_ENV=production
      - PORT=9090
      - API_BASE_URL=http://api-service:9080
    depends_on:
      - api-service
    networks:
      - msav15-network
    restart: unless-stopped

  api-service:
    image: msav15-api-service:latest  # Or build from ../back-end/api-service
    container_name: msav15-api-service
    ports:
      - "9080:9080"
    networks:
      - msav15-network
    restart: unless-stopped

networks:
  msav15-network:
    driver: bridge
```

**Key Points:**
- No version field (follows modern Compose spec)
- Frontend service on port 9090
- Depends on api-service (ensures backend starts first)
- Shared network for inter-service communication
- Restart policy for reliability
- Environment variables for configuration

---

### 10.4 .dockerignore Specifications

**File:** `.dockerignore`

**Content:**
```
# Dependencies
node_modules
npm-debug.log
yarn-error.log

# Build outputs
dist
build
.next

# Environment files
.env
.env.local
.env.*.local

# IDE files
.vscode
.idea
*.swp
*.swo
*~

# Git
.git
.gitignore

# Documentation
README.md
docs/
*.md

# Testing
coverage
.nyc_output
*.test.js
*.spec.js

# Misc
.DS_Store
Thumbs.db
```

**Purpose:** Reduce Docker image size by excluding unnecessary files

---

## 11. Project Documentation

### 11.1 README.md Specifications

**File:** `README.md`

**Required Sections:**

```markdown
# MSAv15 Customer Service Portal

[Badges: License, Node Version, React Version]

## Overview
Brief description of the application and its purpose

## Features
- AI-powered chat interface
- Session management
- Streaming and non-streaming modes
- Professional Tabler Admin UI

## Prerequisites
- Node.js v22+
- npm or yarn
- Docker (for containerized deployment)
- Backend API running on port 9080

## Installation

### Local Development
1. Clone repository
2. Install dependencies: `npm install`
3. Configure environment: Copy `.env.example` to `.env`
4. Start dev server: `npm run dev`
5. Access at http://localhost:9090

### Docker Deployment
1. Build image: `docker build -t msav15-frontend .`
2. Run container: `docker run -p 9090:9090 msav15-frontend`
3. Or use Docker Compose: `docker-compose up -d`

## Configuration
Environment variables:
- `PORT` - Server port (default: 9090)
- `API_BASE_URL` - Backend API URL (default: http://localhost:9080)
- `NODE_ENV` - Environment (development/production)

## Project Structure
[Include directory tree]

## API Integration
Backend service: MSAv15Service REST API
- Base URL: http://localhost:9080
- Documentation: http://localhost:9080/docs

## Development

### Available Scripts
- `npm run dev` - Start development server
- `npm run build` - Build production bundle
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Contributing
See CONTRIBUTING.md

## License
MIT License - See LICENSE file

## Team
Product Manager: Ramkumar
Development Team: CAP (Chandini, Ashok, Priya)

## Version
1.0.0
```

---

### 11.2 CONTRIBUTING.md Specifications

**File:** `CONTRIBUTING.md`

**Required Sections:**

```markdown
# Contributing to MSAv15 Customer Service Portal

## Getting Started

### Development Setup
1. Fork the repository
2. Clone your fork: `git clone [your-fork-url]`
3. Install dependencies: `npm install`
4. Create feature branch: `git checkout -b feature/your-feature`

### Development Guidelines

#### Code Style
- Use ES6+ JavaScript features
- Follow React best practices (functional components, hooks)
- Use Prettier for formatting (config provided)
- ESLint for code quality

#### Component Guidelines
- Keep components small and focused
- Use PropTypes or TypeScript for type checking
- Extract reusable logic into custom hooks
- Follow naming conventions:
  - Components: PascalCase (e.g., ChatWindow.jsx)
  - Hooks: camelCase with 'use' prefix (e.g., useChatStream.js)
  - Utils: camelCase (e.g., dateFormatter.js)

#### State Management
- Use Context API for global state
- Keep component state local when possible
- Avoid prop drilling (use context instead)

#### API Integration
- All API calls should go through service layer
- Handle errors gracefully with user-friendly messages
- Implement loading states for async operations

### Git Workflow

#### Branching Strategy
- `main` - Production-ready code
- `develop` - Integration branch
- `feature/*` - New features
- `bugfix/*` - Bug fixes
- `hotfix/*` - Urgent production fixes

#### Commit Messages
Follow conventional commits:
- `feat: Add streaming toggle to chat input`
- `fix: Correct session switching behavior`
- `docs: Update API integration guide`
- `style: Format chat components`
- `refactor: Extract message rendering logic`

#### Pull Request Process
1. Update documentation if needed
2. Ensure all tests pass (when tests are added)
3. Update CHANGELOG.md
4. Request review from team member
5. Squash commits before merge

### Testing (Future)
[Placeholder for when testing is implemented]

### Code Review Checklist
- [ ] Code follows style guidelines
- [ ] Components are properly structured
- [ ] API calls use service layer
- [ ] Error handling implemented
- [ ] User-facing changes tested manually
- [ ] Documentation updated
- [ ] No console.log statements in production code

## Questions?
Contact Product Manager: Ramkumar (ram@example.com)
```

---

### 11.3 LICENSE Specifications

**File:** `LICENSE`

**Content: MIT License**

```
MIT License

Copyright (c) 2026 MSAv15 Service - Team CAP

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

### 11.4 .gitignore Specifications

**File:** `.gitignore`

**Content:**

```
# Dependencies
node_modules/
package-lock.json
yarn.lock

# Build outputs
dist/
build/
.next/
out/

# Environment variables
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# Logs
logs/
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Testing
coverage/
.nyc_output/

# Temporary files
*.tmp
.cache/
.parcel-cache/

# OS
Thumbs.db
.DS_Store
```

---

## 12. Development Guidelines

### 12.1 Component Development Best Practices

#### Functional Components with Hooks
```javascript
// Example component structure
import React, { useState, useEffect, useContext } from 'react';
import { ChatContext } from '../context/ChatContext';

const ChatMessage = ({ message }) => {
  const { formatTimestamp } = useContext(ChatContext);
  
  return (
    <div className={`message message-${message.type}`}>
      <div className="message-header">
        <span className="message-sender">{message.type}</span>
        <span className="message-time">{formatTimestamp(message.timestamp)}</span>
      </div>
      <div className="message-content">{message.content}</div>
    </div>
  );
};

export default ChatMessage;
```

#### Custom Hook Pattern
```javascript
// Example custom hook
import { useState, useEffect } from 'react';
import { chatService } from '../services/chatService';

export const useChatStream = ({ onChunk, onDone, onError }) => {
  const [isStreaming, setIsStreaming] = useState(false);
  const [eventSource, setEventSource] = useState(null);

  const startStream = (message, sessionId) => {
    setIsStreaming(true);
    const es = chatService.sendStreamingMessage(
      message,
      sessionId,
      onChunk,
      () => {
        setIsStreaming(false);
        onDone();
      },
      (error) => {
        setIsStreaming(false);
        onError(error);
      }
    );
    setEventSource(es);
  };

  const stopStream = () => {
    if (eventSource) {
      eventSource.close();
      setIsStreaming(false);
    }
  };

  return { startStream, stopStream, isStreaming };
};
```

### 12.2 API Service Pattern

```javascript
// Example service structure
import axios from 'axios';

const api = axios.create({
  baseURL: process.env.API_BASE_URL || 'http://localhost:9080',
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 seconds
});

// Request interceptor (for logging, auth tokens, etc.)
api.interceptors.request.use(
  (config) => {
    console.log('API Request:', config.method.toUpperCase(), config.url);
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor (for error handling)
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // Server responded with error
      console.error('API Error:', error.response.status, error.response.data);
    } else if (error.request) {
      // Request made but no response
      console.error('Network Error: No response from server');
    } else {
      // Request setup error
      console.error('Request Error:', error.message);
    }
    return Promise.reject(error);
  }
);

export default api;
```

### 12.3 Environment Variables

**File:** `.env.example` (template)

```bash
# Application
PORT=9090
NODE_ENV=development

# Backend API
API_BASE_URL=http://localhost:9080

# Feature Flags
ENABLE_STREAMING=true
MAX_SESSIONS=10
```

**File:** `.env` (actual, not committed)
```bash
# Copy from .env.example and configure
PORT=9090
NODE_ENV=development
API_BASE_URL=http://localhost:9080
```

### 12.4 Error Boundaries

Implement React Error Boundary for production-grade error handling:

```javascript
// Component structure (do not implement, just spec)
class ErrorBoundary extends React.Component {
  // Catches rendering errors
  // Displays fallback UI
  // Logs errors for debugging
}

// Wrap App component:
<ErrorBoundary>
  <App />
</ErrorBoundary>
```

---

## 13. Deployment Strategy

### 13.1 Development Environment

**Port:** 9090 (frontend), 9080 (backend)  
**Command:** `npm run dev`  
**Hot Reload:** Enabled via Vite

**Steps:**
1. Start backend API service: `cd back-end/api-service && python main.py`
2. Start frontend dev server: `npm run dev`
3. Access application: http://localhost:9090
4. Changes auto-reload in browser

### 13.2 Production Build

**Command:** `npm run build`  
**Output:** `dist/` folder with optimized static assets

**Build Configuration:**
- Minification: Enabled
- Source maps: Optional (for debugging)
- Asset optimization: Images, CSS, JS
- Environment: Set `NODE_ENV=production`

### 13.3 Docker Deployment

#### Local Docker Testing:

```bash
# Build image
docker build -t msav15-frontend:latest .

# Run container
docker run -d \
  --name msav15-frontend \
  -p 9090:9090 \
  -e API_BASE_URL=http://localhost:9080 \
  msav15-frontend:latest

# Check logs
docker logs msav15-frontend

# Stop container
docker stop msav15-frontend
```

#### Docker Compose Deployment:

```bash
# Start all services (frontend + backend)
docker-compose up -d

# View logs
docker-compose logs -f frontend

# Stop services
docker-compose down

# Rebuild and restart
docker-compose up -d --build
```

### 13.4 Container Orchestration (Future)

**Kubernetes Deployment (Placeholder):**
- Deployment manifest with replicas
- Service for load balancing
- Ingress for external access
- ConfigMap for environment variables
- Horizontal Pod Autoscaling (HPA)

**Azure Container Apps (Placeholder):**
- Container registry for image storage
- App deployment from registry
- Auto-scaling rules
- Custom domain and SSL

---

## Appendix A: Tabler Admin Components Reference

### Key Tabler Components to Use

1. **Layout Components**
   - `.page` - Main page container
   - `.page-wrapper` - Wrapper with sidebar
   - `.page-header` - Page header section
   - `.navbar` - Top navigation bar
   - `.navbar-vertical` - Sidebar navigation

2. **Card Components**
   - `.card` - Basic card container
   - `.card-header` - Card header
   - `.card-body` - Card content
   - `.card-footer` - Card footer
   - `.card-actions` - Card action buttons

3. **Form Components**
   - `.form-control` - Input fields
   - `.form-label` - Input labels
   - `.form-select` - Select dropdowns
   - `.form-switch` - Toggle switches

4. **Button Components**
   - `.btn` - Basic button
   - `.btn-primary` - Primary action button
   - `.btn-outline-primary` - Outlined button
   - `.btn-icon` - Icon-only button

5. **Message/Chat Components**
   - `.chat` - Chat container
   - `.chat-bubbles` - Chat message list
   - `.chat-bubble` - Individual message

### Tabler Icons

Use Tabler Icons for consistent iconography:
```html
<i class="ti ti-message"></i>  <!-- Message icon -->
<i class="ti ti-send"></i>     <!-- Send icon -->
<i class="ti ti-home"></i>     <!-- Home icon -->
<i class="ti ti-info-circle"></i> <!-- Info icon -->
```

**Icon Reference:** https://tabler-icons.io/

---

## Appendix B: API Request/Response Examples

### Example 1: First Chat Message (Creating Session)

**Request:**
```javascript
POST http://localhost:9080/chat
Content-Type: application/json

{
  "message": "Hello, I need help with my order",
  "stream": false
}
```

**Response:**
```json
{
  "session_id": "a3f5e8d2-1234-5678-90ab-cdef12345678",
  "response": "Hello! I'd be happy to help you with your order. Could you please provide me with your order number or tell me what you need assistance with?",
  "timestamp": "2026-02-20T14:23:15.000Z",
  "metadata": {
    "turn_count": 1,
    "tools_used": [],
    "tokens_used": 0,
    "streaming": false
  }
}
```

**Frontend Action:**
1. Store session_id in SessionContext
2. Display response in ChatWindow
3. Enable follow-up messages with same session_id

---

### Example 2: Continuing Conversation

**Request:**
```javascript
POST http://localhost:9080/chat
Content-Type: application/json

{
  "session_id": "a3f5e8d2-1234-5678-90ab-cdef12345678",
  "message": "Show me all my orders",
  "stream": false
}
```

**Response:**
```json
{
  "session_id": "a3f5e8d2-1234-5678-90ab-cdef12345678",
  "response": "I found 3 orders associated with your account:\n\n1. Order #123 - HP Laptop - Status: Delivered (Feb 15, 2026)\n2. Order #124 - Wireless Mouse - Status: Shipped (Feb 18, 2026)\n3. Order #125 - Mechanical Keyboard - Status: Processing (Feb 19, 2026)\n\nWould you like more details about any specific order?",
  "timestamp": "2026-02-20T14:24:30.000Z",
  "metadata": {
    "turn_count": 2,
    "tools_used": ["get_customer_orders"],
    "tokens_used": 0,
    "streaming": false
  }
}
```

---

### Example 3: Streaming Response

**Request:**
```javascript
POST http://localhost:9080/chat
Content-Type: application/json
Accept: text/event-stream

{
  "session_id": "a3f5e8d2-1234-5678-90ab-cdef12345678",
  "message": "Update order 124 status to Delivered",
  "stream": true
}
```

**SSE Response Stream:**
```
event: message
data: {"chunk": "I'll update ", "session_id": "a3f5e8d2-1234-5678-90ab-cdef12345678"}

event: message
data: {"chunk": "the order ", "session_id": "a3f5e8d2-1234-5678-90ab-cdef12345678"}

event: message
data: {"chunk": "status for ", "session_id": "a3f5e8d2-1234-5678-90ab-cdef12345678"}

event: message
data: {"chunk": "you. Order ", "session_id": "a3f5e8d2-1234-5678-90ab-cdef12345678"}

event: message
data: {"chunk": "#124 has been ", "session_id": "a3f5e8d2-1234-5678-90ab-cdef12345678"}

event: message
data: {"chunk": "updated to ", "session_id": "a3f5e8d2-1234-5678-90ab-cdef12345678"}

event: message
data: {"chunk": "Delivered status.", "session_id": "a3f5e8d2-1234-5678-90ab-cdef12345678"}

event: done
data: {"session_id": "a3f5e8d2-1234-5678-90ab-cdef12345678", "metadata": {"turn_count": 3, "streaming": true}}
```

**Frontend Implementation:**
```javascript
const eventSource = new EventSource('http://localhost:9080/chat?stream=true');
let fullResponse = '';

eventSource.addEventListener('message', (event) => {
  const data = JSON.parse(event.data);
  fullResponse += data.chunk;
  updateChatUI(fullResponse); // Update UI with accumulated text
});

eventSource.addEventListener('done', (event) => {
  const data = JSON.parse(event.data);
  console.log('Stream complete', data.metadata);
  eventSource.close();
});

eventSource.addEventListener('error', (event) => {
  console.error('Stream error');
  eventSource.close();
});
```

---

## Appendix C: Implementation Checklist

### Phase 1: Project Setup
- [ ] Initialize React project with Vite
- [ ] Install dependencies (React Router, Axios)
- [ ] Configure Tabler Admin CDN in index.html
- [ ] Set up project structure (folders: components, services, context, etc.)
- [ ] Create .env.example file
- [ ] Set up .gitignore
- [ ] Initialize Git repository

### Phase 2: Core Infrastructure
- [ ] Implement API service layer (api.js, chatService.js, healthService.js)
- [ ] Create ChatContext with state and methods
- [ ] Create SessionContext with state and methods
- [ ] Implement localStorage utilities for session persistence
- [ ] Set up React Router with routes
- [ ] Create global layout (Header, Sidebar, Footer)

### Phase 3: Pages
- [ ] Implement Home page with hero and features
- [ ] Implement About Us page
- [ ] Implement Contact Us page
- [ ] Implement Support page layout skeleton

### Phase 4: Chat Interface
- [ ] Implement Session List component
- [ ] Implement Chat Window component
- [ ] Implement Chat Message component
- [ ] Implement Chat Input component
- [ ] Implement Streaming Toggle component
- [ ] Implement Typing Indicator component

### Phase 5: API Integration
- [ ] Connect health check to Header status indicator
- [ ] Implement non-streaming chat (POST /chat)
- [ ] Implement streaming chat (SSE)
- [ ] Implement error handling for all API calls
- [ ] Test session creation and continuation
- [ ] Test streaming toggle behavior

### Phase 6: Session Management
- [ ] Implement create new session functionality
- [ ] Implement switch session functionality
- [ ] Implement delete session functionality
- [ ] Persist sessions to localStorage
- [ ] Load sessions from localStorage on startup
- [ ] Implement session limit (max 10 sessions)

### Phase 7: Polish & UX
- [ ] Add loading states for async operations
- [ ] Add error messages with retry buttons
- [ ] Implement auto-scroll in chat window
- [ ] Add keyboard shortcuts (Enter to send)
- [ ] Add tooltips for UI elements
- [ ] Responsive design testing (mobile, tablet, desktop)
- [ ] Accessibility improvements (ARIA labels, keyboard nav)

### Phase 8: Documentation
- [ ] Write README.md
- [ ] Write CONTRIBUTING.md
- [ ] Add API_INTEGRATION.md in docs/
- [ ] Add inline code comments
- [ ] Update CHANGELOG.md

### Phase 9: Deployment
- [ ] Create Express server for serving React
- [ ] Write Dockerfile
- [ ] Write docker-compose.yml
- [ ] Write .dockerignore
- [ ] Test Docker build locally
- [ ] Test Docker Compose with backend
- [ ] Create deployment documentation

### Phase 10: Final Review
- [ ] Manual testing of all features
- [ ] Cross-browser testing (Chrome, Firefox, Edge, Safari)
- [ ] Performance optimization (lazy loading, code splitting)
- [ ] Security review (no sensitive data in client)
- [ ] Documentation review
- [ ] Handoff to stakeholders

---

## Appendix D: Glossary

| Term | Definition |
|------|------------|
| **SSE** | Server-Sent Events - One-way communication from server to client for real-time updates |
| **MAF** | Microsoft Agent Framework - AI agent development framework |
| **Session** | Conversation context that maintains history across multiple turns |
| **Turn** | Single exchange (user message + agent response) in a conversation |
| **Streaming** | Real-time delivery of response chunks as they are generated |
| **Non-streaming** | Complete response delivered after full generation |
| **Context API** | React's built-in state management solution |
| **Tabler Admin** | Free, open-source admin template built with Bootstrap |
| **CDN** | Content Delivery Network - Remote hosting for libraries/assets |

---

## Document Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-02-20 | Ramkumar (PM) | Initial specification document |

---

## Contact & Support

**Product Manager:** Ramkumar  
**Email:** ram@example.com  
**Development Team:** CAP (Chandini, Ashok, Priya)  
**Project Repository:** [GitHub URL - TBD]  
**Backend API Docs:** http://localhost:9080/docs

---

**End of Specification Document**
