# Frontend Architecture

**Version:** 1.0.0  
**Last Updated:** February 20, 2026

## Table of Contents

- [Overview](#overview)
- [Technology Stack](#technology-stack)
- [Architecture Patterns](#architecture-patterns)
- [Component Architecture](#component-architecture)
- [State Management](#state-management)
- [API Integration Layer](#api-integration-layer)
- [Error Handling Strategy](#error-handling-strategy)
- [Performance Optimization](#performance-optimization)
- [Security Considerations](#security-considerations)

---

## Overview

The frontend application is a React-based web UI for interacting with the Customer Service Agent API. It provides a conversational interface for customer service operations with real-time streaming support.

### Key Requirements

- **Framework:** React 18 with TypeScript
- **Build Tool:** Vite
- **API Communication:** Direct to FastAPI backend (no BFF layer)
- **UI Framework:** Tabler Admin Template (CDN, Free Edition)
- **Runtime:** Node.js v22
- **Deployment:** Docker with Alpine Linux
- **Theme:** Indigo blue & white color scheme with dark/light mode

---

## Technology Stack

### Core Technologies

```yaml
Frontend:
  - React: 18.x
  - TypeScript: 5.x
  - Vite: 5.x
  - React Router: 6.x

UI/Styling:
  - Tabler: Latest (CDN)
  - CSS Modules
  - Responsive Design
  - Indigo Blue & White Theme
  - Dark/Light Mode Support

State Management:
  - React Context API
  - Custom Hooks
  - Optional: Zustand/Jotai (lightweight)

HTTP Client:
  - Axios or Fetch API
  - EventSource (for SSE streaming)

Development:
  - ESLint
  - Prettier
  - Vitest (testing)

Containerization:
  - Docker (Alpine Node 22)
  - Docker Compose
```

---

## Architecture Patterns

### 1. Direct API Communication

```
┌─────────────────┐
│   React SPA     │
│  (Port 3000)    │
│                 │
│  - Vite Dev     │
│  - Axios Client │
│  - CORS Proxy   │
└────────┬────────┘
         │ HTTP/HTTPS
         │ Direct API Calls
         ↓
┌─────────────────┐
│  FastAPI Backend│
│  (Port 9080)    │
│                 │
│  - CORS Enabled │
│  - RESTful API  │
└─────────────────┘
```

**Direct Communication Benefits:**
- Simplified architecture (no middleware layer)
- Faster development iteration
- Lower deployment complexity
- Direct error feedback from API
- Vite proxy handles CORS in development
- Production: Backend CORS configuration

**Rationale:**
- Reduced complexity for single-page application
- FastAPI handles CORS natively
- No need for intermediate transformation layer
- Client-side error handling sufficient

### 2. Layered Architecture

```
┌──────────────────────────────────────┐
│         Presentation Layer           │
│   (React Components, UI Logic)       │
└──────────────┬───────────────────────┘
               │
┌──────────────▼───────────────────────┐
│         Application Layer            │
│  (Business Logic, State Management)  │
└──────────────┬───────────────────────┘
               │
┌──────────────▼───────────────────────┐
│         Integration Layer            │
│    (API Client, Error Handling)      │
└──────────────┬───────────────────────┘
               │
┌──────────────▼───────────────────────┐
│         Infrastructure Layer         │
│  (HTTP, WebSocket, Storage, Utils)   │
└──────────────────────────────────────┘
```

### 3. Feature-Based Structure

Organize code by features rather than technical layers:

```
src/
├── features/
│   ├── chat/                    # Chat feature
│   │   ├── components/          # Feature-specific components
│   │   ├── hooks/               # Feature-specific hooks
│   │   ├── services/            # Feature-specific services
│   │   ├── types/               # Feature-specific types
│   │   └── utils/               # Feature-specific utilities
│   ├── sessions/                # Session management
│   └── orders/                  # Order management
├── shared/                      # Shared across features
│   ├── components/              # Reusable UI components
│   ├── hooks/                   # Reusable hooks
│   ├── services/                # Shared services
│   └── utils/                   # Shared utilities
└── core/                        # Core application
    ├── api/                     # API client
    ├── config/                  # Configuration
    └── types/                   # Global types
```

---

## Component Architecture

### Component Hierarchy

```
App
├── Layout
│   ├── TopNavbar
│   │   ├── Logo
│   │   ├── Navigation (Home, About, Contact, Support, Settings)
│   │   ├── ThemeToggle (Dark/Light)
│   │   ├── TenantSelector
│   │   └── UserMenu
│   └── Footer
├── Routes
│   ├── HomePage (Landing/Dashboard)
│   ├── AboutPage (Company information)
│   ├── ContactPage (Contact form)
│   ├── SupportPage (Main chat interface)
│   │   ├── SessionSelector
│   │   ├── ChatView
│   │   │   ├── MessageList
│   │   │   │   ├── MessageItem (user)
│   │   │   │   ├── MessageItem (assistant)
│   │   │   │   └── ToolCallIndicator
│   │   │   ├── MessageInput
│   │   │   │   ├── TextArea
│   │   │   │   ├── SendButton
│   │   │   │   └── StreamToggle
│   │   │   └── TypingIndicator
│   │   └── SessionManagement
│   │       ├── SessionsFilter
│   │       ├── SessionsTable
│   │       └── Pagination
│   └── SettingsPage
│       ├── ThemeSettings
│       ├── TenantSettings
│       └── PreferencesForm
└── ErrorBoundary
```

### Component Types

#### 1. Container Components (Smart)

**Responsibility:** Business logic, state management, API calls

```typescript
// Example: ChatContainer
interface ChatContainerProps {
  sessionId: string;
}

// - Manages chat state
// - Handles message sending
// - Manages streaming toggle
// - Error handling
```

#### 2. Presentation Components (Dumb)

**Responsibility:** UI rendering only, no business logic

```typescript
// Example: MessageItem
interface MessageItemProps {
  message: Message;
  onRetry?: () => void;
}

// - Pure rendering
// - Receives data via props
// - Emits events via callbacks
```

#### 3. Layout Components

**Responsibility:** Page structure and positioning

```typescript
// Example: MainLayout
interface MainLayoutProps {
  children: React.ReactNode;
}

// - Defines page structure
// - Top navigation bar
// - Responsive layout
// - Theme-aware styling
// - No business logic
```

#### 4. HOC (Higher Order Components)

**Responsibility:** Cross-cutting concerns

```typescript
// Example: withErrorBoundary
// Example: withAuth (future)
// Example: withTenant

// - Wraps components
// - Adds common behavior
// - Reusable patterns
```

---

## State Management

### Strategy: Context API + Custom Hooks

Use React Context API for global state management with custom hooks for business logic.

### Global State Structure

```typescript
// Application State
interface AppState {
  // User context (if auth is added)
  user: UserState | null;
  
  // Current tenant
  tenant: TenantState;
  
  // UI preferences
  preferences: PreferencesState;
  
  // Theme state
  theme: 'light' | 'dark';
  
  // API configuration
  apiConfig: APIConfigState;
}

// Chat State
interface ChatState {
  currentSession: Session | null;
  messages: Message[];
  isLoading: boolean;
  isStreaming: boolean;
  error: Error | null;
}

// Sessions State
interface SessionsState {
  sessions: Session[];
  selectedSession: string | null;
  isLoading: boolean;
  error: Error | null;
  pagination: PaginationState;
}

// UI State
interface UIState {
  modalStack: Modal[];
  toasts: Toast[];
  theme: 'light' | 'dark';
}
```

### Context Providers

```
<AppProvider>
  <ThemeProvider>
    <TenantProvider>
      <APIProvider>
        <ChatProvider>
          <SessionsProvider>
            <UIProvider>
              <App />
            </UIProvider>
          </SessionsProvider>
        </ChatProvider>
      </APIProvider>
    </TenantProvider>
  </ThemeProvider>
</AppProvider>
```

### Custom Hooks Pattern

```typescript
// Feature hooks
export const useChat = () => {
  const context = useChatContext();
  
  return {
    messages: context.messages,
    sendMessage: context.sendMessage,
    isLoading: context.isLoading,
    error: context.error,
    ...
  };
};

// API hooks
export const useAPI = <T>(
  fetcher: () => Promise<T>,
  options?: UseAPIOptions
) => {
  // Generic API hook with:
  // - Loading state
  // - Error handling
  // - Retry logic
  // - Caching
};

// Streaming hooks
export const useStreamingMessage = (
  sessionId: string,
  onChunk: (chunk: string) => void
) => {
  // EventSource management
  // Chunk handling
  // Connection state
};
```

---

## API Integration Layer

### API Client Architecture

```typescript
// Core API Client
class APIClient {
  private baseURL: string;
  private axiosInstance: AxiosInstance;
  
  constructor(config: APIConfig) {
    this.baseURL = config.baseURL;
    this.axiosInstance = this.createAxiosInstance();
  }
  
  // Request/response interceptors
  // Error handling
  // Retry logic
  // Timeout handling
}

// Feature-specific clients
class AgentAPIClient extends APIClient {
  async createSession(data: CreateSessionRequest): Promise<CreateSessionResponse>
  async sendMessage(data: SendMessageRequest): Promise<SendMessageResponse>
  async listSessions(): Promise<ListSessionsResponse>
  async deleteSession(sessionId: string): Promise<DeleteSessionResponse>
}

class SessionAPIClient extends APIClient {
  async getHistory(sessionId: string, tenantId?: string): Promise<SessionHistoryResponse>
  async listSessions(tenantId?: string, pagination?: PaginationParams): Promise<SessionListResponse>
  async deleteSession(sessionId: string, tenantId?: string): Promise<void>
  async getStats(): Promise<SessionStats>
}

class HealthAPIClient extends APIClient {
  async checkHealth(): Promise<HealthResponse>
  async checkReadiness(): Promise<ReadinessResponse>
}
```

### Request Interceptors

```typescript
// Add request ID for tracing
axiosInstance.interceptors.request.use(config => {
  config.headers['X-Request-ID'] = generateUUID();
  config.headers['X-Tenant-ID'] = getCurrentTenantId();
  return config;
});

// Log requests in development
axiosInstance.interceptors.request.use(config => {
  if (isDevelopment) {
    console.log(`[API] ${config.method?.toUpperCase()} ${config.url}`);
  }
  return config;
});
```

### Response Interceptors

```typescript
// Handle rate limiting
axiosInstance.interceptors.response.use(
  response => response,
  async error => {
    if (error.response?.status === 429) {
      const retryAfter = error.response.headers['retry-after'];
      await delay(retryAfter * 1000);
      return axiosInstance.request(error.config);
    }
    throw error;
  }
);

// Normalize errors
axiosInstance.interceptors.response.use(
  response => response,
  error => {
    throw normalizeAPIError(error);
  }
);
```

---

## Error Handling Strategy

### Error Types

```typescript
// Base error class
class AppError extends Error {
  code: string;
  context?: any;
  
  constructor(message: string, code: string, context?: any) {
    super(message);
    this.code = code;
    this.context = context;
  }
}

// Specific error types
class NetworkError extends AppError {}
class ValidationError extends AppError {}
class APIError extends AppError {
  statusCode: number;
  retryable: boolean;
}
class SessionError extends AppError {}
class RateLimitError extends AppError {
  retryAfter: number;
}
```

### Error Handling Layers

#### 1. API Layer

```typescript
// Catch and transform API errors
try {
  const response = await apiClient.sendMessage(data);
  return response;
} catch (error) {
  if (isAxiosError(error)) {
    throw transformAPIError(error);
  }
  throw new NetworkError('Request failed', 'NETWORK_ERROR');
}
```

#### 2. Service Layer

```typescript
// Business logic error handling
try {
  const result = await chatService.sendMessage(message);
  return result;
} catch (error) {
  if (error instanceof RateLimitError) {
    // Queue message for retry
    messageQueue.enqueue(message);
    return { queued: true, retryAfter: error.retryAfter };
  }
  throw error;
}
```

#### 3. Component Layer

```typescript
// UI error handling
try {
  await sendMessage(inputValue);
} catch (error) {
  if (error instanceof ValidationError) {
    setFieldError(error.message);
  } else if (error instanceof RateLimitError) {
    showToast(`Rate limit exceeded. Retry in ${error.retryAfter}s`);
  } else {
    showToast('Failed to send message. Please try again.');
  }
}
```

#### 4. Global Error Boundary

```typescript
// Catch unhandled errors
class GlobalErrorBoundary extends React.Component {
  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    // Log to error tracking service
    logError(error, errorInfo);
    
    // Show error UI
    this.setState({ hasError: true, error });
  }
  
  render() {
    if (this.state.hasError) {
      return <ErrorFallback error={this.state.error} />;
    }
    return this.props.children;
  }
}
```

---

## Performance Optimization

### 1. Code Splitting

```typescript
// Route-based splitting
const ChatView = lazy(() => import('./features/chat/ChatView'));
const SessionsView = lazy(() => import('./features/sessions/SessionsView'));
const StatsView = lazy(() => import('./features/stats/StatsView'));

// Component-based splitting
const HeavyChart = lazy(() => import('./components/HeavyChart'));
```

### 2. Memoization

```typescript
// Memoize expensive computations
const sortedMessages = useMemo(
  () => messages.sort((a, b) => a.timestamp - b.timestamp),
  [messages]
);

// Memoize callbacks
const handleSendMessage = useCallback(
  async (message: string) => {
    await sendMessage(sessionId, message);
  },
  [sessionId, sendMessage]
);

// Memoize components
const MessageItem = memo(({ message }: MessageItemProps) => {
  // Rendering logic
});
```

### 3. Virtual Scrolling

For long message lists, implement virtual scrolling:

```typescript
// Use react-window or react-virtual
import { FixedSizeList } from 'react-window';

<FixedSizeList
  height={600}
  itemCount={messages.length}
  itemSize={80}
  width="100%"
>
  {({ index, style }) => (
    <MessageItem message={messages[index]} style={style} />
  )}
</FixedSizeList>
```

### 4. Debouncing & Throttling

```typescript
// Debounce search input
const debouncedSearch = useMemo(
  () => debounce((query: string) => searchSessions(query), 300),
  [searchSessions]
);

// Throttle scroll events
const throttledScroll = useMemo(
  () => throttle(() => loadMoreMessages(), 100),
  [loadMoreMessages]
);
```

### 5. Optimistic Updates

```typescript
// Update UI immediately, rollback on error
const sendMessage = async (message: string) => {
  const optimisticMessage = {
    id: generateTempId(),
    role: 'user',
    content: message,
    timestamp: new Date().toISOString(),
    pending: true
  };
  
  // Add to UI immediately
  addMessage(optimisticMessage);
  
  try {
    const response = await api.sendMessage({ sessionId, message });
    // Replace optimistic message with real one
    updateMessage(optimisticMessage.id, {
      ...response,
      pending: false
    });
  } catch (error) {
    // Remove optimistic message or mark as failed
    removeMessage(optimisticMessage.id);
    throw error;
  }
};
```

### 6. Caching Strategy

```typescript
// Session history cache
const sessionCache = new Map<string, SessionHistory>();
const CACHE_TTL = 5 * 60 * 1000; // 5 minutes

const getSessionHistory = async (sessionId: string) => {
  const cached = sessionCache.get(sessionId);
  if (cached && Date.now() - cached.timestamp < CACHE_TTL) {
    return cached.data;
  }
  
  const data = await api.getSessionHistory(sessionId);
  sessionCache.set(sessionId, {
    data,
    timestamp: Date.now()
  });
  return data;
};
```

---

## Security Considerations

### 1. XSS Prevention

```typescript
// Sanitize user input before rendering
import DOMPurify from 'dompurify';

const sanitizedContent = DOMPurify.sanitize(userInput);
```

### 2. CSRF Protection (when auth is added)

```typescript
// Include CSRF token in requests
axiosInstance.interceptors.request.use(config => {
  config.headers['X-CSRF-Token'] = getCSRFToken();
  return config;
});
```

### 3. Content Security Policy

```html
<!-- In index.html -->
<meta http-equiv="Content-Security-Policy" 
      content="default-src 'self'; 
               script-src 'self' cdn.tabler.io; 
               style-src 'self' cdn.tabler.io 'unsafe-inline';">
```

### 4. Secrets Management

```typescript
// Never hardcode API keys or secrets
// Use environment variables
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;
const API_KEY = import.meta.env.VITE_API_KEY; // If needed
```

### 5. Input Validation

```typescript
// Validate on client side (but also server side)
const validateMessage = (message: string): ValidationResult => {
  if (!message.trim()) {
    return { valid: false, error: 'Message cannot be empty' };
  }
  if (message.length > 5000) {
    return { valid: false, error: 'Message too long (max 5000 characters)' };
  }
  return { valid: true };
};
```

---

## Mobile Responsiveness

### Breakpoints

```typescript
// Following Tabler's breakpoint system
const breakpoints = {
  xs: '0px',      // Extra small devices (phones)
  sm: '576px',    // Small devices (landscape phones)
  md: '768px',    // Medium devices (tablets)
  lg: '992px',    // Large devices (desktops)
  xl: '1200px',   // Extra large devices (large desktops)
  xxl: '1400px'   // Extra extra large devices
};
```

### Responsive Design Patterns

1. **Mobile-First Approach**: Design for mobile, enhance for desktop
2. **Collapsible Navigation**: Hamburger menu on mobile, full horizontal nav on desktop
3. **Touch-Friendly**: Minimum 44x44px touch targets
4. **Responsive Tables**: Convert to cards on mobile
5. **Adaptive Layout**: Full-width chat on mobile, centered layout on desktop

---

## Testing Strategy

### Unit Tests

```typescript
// Component tests with Vitest + React Testing Library
describe('MessageItem', () => {
  it('renders user message correctly', () => {
    const message = { role: 'user', content: 'Hello' };
    render(<MessageItem message={message} />);
    expect(screen.getByText('Hello')).toBeInTheDocument();
  });
});

// Hook tests
describe('useChat', () => {
  it('sends message successfully', async () => {
    const { result } = renderHook(() => useChat());
    await act(() => result.current.sendMessage('Test'));
    expect(result.current.messages).toHaveLength(1);
  });
});
```

### Integration Tests

```typescript
// Test feature workflows
describe('Chat Feature', () => {
  it('completes full conversation flow', async () => {
    render(<ChatView />);
    // ... test full user flow
  });
});
```

### E2E Tests (Optional)

```typescript
// Playwright or Cypress
test('send message and receive response', async ({ page }) => {
  await page.goto('/chat');
  await page.fill('[data-testid="message-input"]', 'Hello');
  await page.click('[data-testid="send-button"]');
  await expect(page.locator('[data-testid="assistant-message"]')).toBeVisible();
});
```

---

## Accessibility (a11y)

### Guidelines

1. **Semantic HTML**: Use proper HTML5 elements
2. **ARIA Labels**: Add aria-* attributes where needed
3. **Keyboard Navigation**: All interactive elements keyboard accessible
4. **Focus Management**: Visible focus indicators
5. **Color Contrast**: WCAG AA compliance (4.5:1 ratio)
6. **Screen Reader**: Test with NVDA/JAWS
7. **Alt Text**: All images have meaningful alt text

### Examples

```typescript
// Accessible button
<button
  aria-label="Send message"
  aria-disabled={isLoading}
  disabled={isLoading}
>
  Send
</button>

// Accessible form
<label htmlFor="message-input">Your message</label>
<textarea
  id="message-input"
  aria-describedby="message-help"
  aria-required="true"
/>
<span id="message-help">Enter your message (max 5000 characters)</span>

// Skip to main content
<a href="#main-content" className="sr-only sr-only-focusable">
  Skip to main content
</a>
```

---

## Development Workflow

### Branch Strategy

- `main` - Production-ready code
- `develop` - Integration branch
- `feature/*` - Feature branches
- `bugfix/*` - Bug fix branches
- `hotfix/*` - Production hotfixes

### Commit Convention

Follow Conventional Commits:

```
feat: Add streaming message support
fix: Fix session list pagination
docs: Update API integration guide
style: Format code with Prettier
refactor: Simplify error handling logic
test: Add tests for chat hooks
chore: Update dependencies
```

### Code Review Checklist

- [ ] Code follows project conventions
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No console.log statements
- [ ] Error handling implemented
- [ ] Accessibility considered
- [ ] Performance optimized
- [ ] Security reviewed

---

## Monitoring & Observability

### Client-Side Logging

```typescript
// Structured logging
class Logger {
  info(message: string, context?: any) {
    console.log(`[INFO] ${message}`, context);
    // Send to logging service (future)
  }
  
  error(message: string, error: Error, context?: any) {
    console.error(`[ERROR] ${message}`, error, context);
    // Send to error tracking (future)
  }
  
  performance(metric: string, duration: number) {
    console.log(`[PERF] ${metric}: ${duration}ms`);
    // Send to analytics (future)
  }
}
```

### Performance Metrics

```typescript
// Measure API call duration
const start = performance.now();
await apiClient.sendMessage(data);
const duration = performance.now() - start;
logger.performance('sendMessage', duration);

// React Profiler
<Profiler id="ChatView" onRender={onRenderCallback}>
  <ChatView />
</Profiler>
```

### Error Tracking

```typescript
// Log errors with context
window.addEventListener('error', (event) => {
  logger.error('Unhandled error', event.error, {
    url: window.location.href,
    userAgent: navigator.userAgent
  });
});

window.addEventListener('unhandledrejection', (event) => {
  logger.error('Unhandled promise rejection', event.reason);
});
```

---

## Summary

This architecture provides:

✅ **Scalability**: Modular, feature-based structure  
✅ **Maintainability**: Clear separation of concerns  
✅ **Performance**: Optimized rendering and data fetching  
✅ **Reliability**: Comprehensive error handling  
✅ **Security**: Best practices for web security  
✅ **Accessibility**: WCAG compliance  
✅ **Testability**: Unit, integration, and E2E tests  
✅ **Developer Experience**: Clear patterns and conventions

---

## Next Steps

1. Review and approve architecture
2. Set up project structure
3. Implement core infrastructure
4. Build feature modules
5. Add tests
6. Deploy and monitor

For implementation details, see:
- [Integration Guide](./INTEGRATION_GUIDE.md)
- [Project Structure](./PROJECT_STRUCTURE.md)
- [UI Component Guide](./UI_COMPONENT_GUIDE.md)
