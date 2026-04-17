# Project Structure

**Version:** 1.0.0  
**Last Updated:** February 20, 2026

## Table of Contents

- [Overview](#overview)
- [Root Directory Structure](#root-directory-structure)
- [Source Directory (/src)](#source-directory-src)
- [Feature Organization](#feature-organization)
- [Component Structure](#component-structure)
- [File Naming Conventions](#file-naming-conventions)
- [Import/Export Patterns](#importexport-patterns)
- [Configuration Files](#configuration-files)
- [Testing Structure](#testing-structure)
- [Build Output](#build-output)

---

## Overview

This project follows a **feature-based architecture** where code is organized by business features rather than technical layers. This approach improves maintainability and scalability.

### Key Principles

1. **Feature-First**: Group code by feature, not by file type
2. **Colocation**: Keep related files close together
3. **Clear Boundaries**: Explicit module boundaries
4. **Reusability**: Shared code extracted to common modules
5. **Discoverability**: Intuitive file organization

---

## Root Directory Structure

```
v16-e2e/front-end/
├── .vscode/                    # VS Code workspace settings
│   ├── settings.json           # Editor configuration
│   ├── extensions.json         # Recommended extensions
│   └── launch.json             # Debug configurations
├── docs/                       # Documentation
│   ├── API_SPECIFICATION.md
│   ├── FRONTEND_ARCHITECTURE.md
│   ├── INTEGRATION_GUIDE.md
│   ├── PROJECT_STRUCTURE.md
│   ├── DEPLOYMENT_GUIDE.md
│   ├── UI_COMPONENT_GUIDE.md
│   ├── TENANT_MULTI_TENANCY.md
│   └── README.md
├── public/                     # Static assets
│   ├── favicon.ico
│   ├── logo.svg
│   ├── robots.txt
│   └── assets/                 # Images, fonts, etc.
├── src/                        # Source code (详见下方)
├── tests/                      # E2E tests
│   ├── e2e/                    # End-to-end tests
│   ├── integration/            # Integration tests
│   └── fixtures/               # Test fixtures
├── .env.example                # Environment variables template
├── .env.local                  # Local environment (gitignored)
├── .eslintrc.js                # ESLint configuration
├── .prettierrc                 # Prettier configuration
├── .gitignore                  # Git ignore rules
├── .dockerignore               # Docker ignore rules
├── docker-compose.yml          # Docker Compose config
├── Dockerfile                  # Docker image definition
├── index.html                  # HTML entry point
├── package.json                # Dependencies & scripts
├── tsconfig.json               # TypeScript configuration
├── vite.config.ts              # Vite build configuration
└── README.md                   # Project README
```

---

## Source Directory (/src)

```
src/
├── main.tsx                    # Application entry point
├── App.tsx                     # Root component
├── App.css                     # Global styles
├── vite-env.d.ts               # Vite type definitions
│
├── core/                       # Core application infrastructure
│   ├── api/                    # API client infrastructure
│   │   ├── client.ts           # Base API client
│   │   ├── interceptors.ts     # Request/response interceptors
│   │   ├── retry.ts            # Retry logic
│   │   ├── circuit-breaker.ts  # Circuit breaker
│   │   ├── rate-limiter.ts     # Rate limit tracking
│   │   └── errors.ts           # Error types & transforms
│   ├── config/                 # Application configuration
│   │   ├── env.ts              # Environment variables
│   │   ├── constants.ts        # App constants
│   │   └── endpoints.ts        # API endpoint definitions
│   ├── types/                  # Global TypeScript types
│   │   ├── api.types.ts        # API request/response types
│   │   ├── domain.types.ts     # Domain models
│   │   └── common.types.ts     # Common utility types
│   └── utils/                  # Core utilities
│       ├── logger.ts           # Logging utility
│       ├── storage.ts          # LocalStorage wrapper
│       ├── date.ts             # Date formatting
│       └── validation.ts       # Input validation
│
├── features/                   # Feature modules
│   ├── chat/                   # Chat feature
│   │   ├── index.ts            # Feature exports
│   │   ├── components/         # Feature-specific components
│   │   │   ├── ChatView.tsx
│   │   │   ├── MessageList.tsx
│   │   │   ├── MessageItem.tsx
│   │   │   ├── MessageInput.tsx
│   │   │   ├── TypingIndicator.tsx
│   │   │   └── ToolCallBadge.tsx
│   │   ├── hooks/              # Feature-specific hooks
│   │   │   ├── useChat.ts
│   │   │   ├── useSendMessage.ts
│   │   │   └── useStreamingMessage.ts
│   │   ├── services/           # Feature-specific services
│   │   │   └── chatService.ts
│   │   ├── context/            # Feature-specific context
│   │   │   ├── ChatContext.tsx
│   │   │   └── ChatProvider.tsx
│   │   ├── types/              # Feature-specific types
│   │   │   └── chat.types.ts
│   │   ├── utils/              # Feature-specific utilities
│   │   │   └── messageFormatter.ts
│   │   └── styles/             # Feature-specific styles
│   │       └── chat.module.css
│   │
│   ├── sessions/               # Session management feature
│   │   ├── index.ts
│   │   ├── components/
│   │   │   ├── SessionSelector.tsx
│   │   │   ├── SessionList.tsx
│   │   │   ├── SessionItem.tsx
│   │   │   ├── SessionFilter.tsx
│   │   │   └── SessionStats.tsx
│   │   ├── hooks/
│   │   │   ├── useSessions.ts
│   │   │   ├── useSessionHistory.ts
│   │   │   └── useSessionStats.ts
│   │   ├── services/
│   │   │   └── sessionService.ts
│   │   ├── context/
│   │   │   ├── SessionContext.tsx
│   │   │   └── SessionProvider.tsx
│   │   ├── types/
│   │   │   └── session.types.ts
│   │   └── styles/
│   │       └── sessions.module.css
│   │
│   ├── tenant/                 # Multi-tenancy feature
│   │   ├── index.ts
│   │   ├── components/
│   │   │   ├── TenantSelector.tsx
│   │   │   └── TenantIndicator.tsx
│   │   ├── hooks/
│   │   │   └── useTenant.ts
│   │   ├── services/
│   │   │   └── tenantManager.ts
│   │   ├── context/
│   │   │   ├── TenantContext.tsx
│   │   │   └── TenantProvider.tsx
│   │   └── types/
│   │       └── tenant.types.ts
│   │
│   ├── theme/                  # Theme management feature
│   │   ├── index.ts
│   │   ├── components/
│   │   │   └── ThemeToggle.tsx
│   │   ├── hooks/
│   │   │   └── useTheme.ts
│   │   ├── context/
│   │   │   ├── ThemeContext.tsx
│   │   │   └── ThemeProvider.tsx
│   │   └── types/
│   │       └── theme.types.ts
│   │
│   └── health/                 # Health monitoring feature
│       ├── index.ts
│       ├── components/
│       │   ├── HealthDashboard.tsx
│       │   └── HealthIndicator.tsx
│       ├── hooks/
│       │   └── useHealth.ts
│       └── services/
│           └── healthService.ts
│
├── shared/                     # Shared across features
│   ├── components/             # Reusable UI components
│   │   ├── ui/                 # Basic UI elements
│   │   │   ├── Button.tsx
│   │   │   ├── Input.tsx
│   │   │   ├── Textarea.tsx
│   │   │   ├── Modal.tsx
│   │   │   ├── Card.tsx
│   │   │   ├── Badge.tsx
│   │   │   ├── Spinner.tsx
│   │   │   ├── Progress.tsx
│   │   │   └── Toast.tsx
│   │   ├── layout/             # Layout components
│   │   │   ├── TopNavbar.tsx
│   │   │   ├── Footer.tsx
│   │   │   ├── MainLayout.tsx
│   │   │   └── PageContainer.tsx
│   │   ├── feedback/           # User feedback components
│   │   │   ├── EmptyState.tsx
│   │   │   ├── ErrorBoundary.tsx
│   │   │   ├── ErrorFallback.tsx
│   │   │   ├── LoadingState.tsx
│   │   │   └── SkeletonLoader.tsx
│   │   └── navigation/         # Navigation components
│   │       ├── Breadcrumbs.tsx
│   │       ├── Tabs.tsx
│   │       └── Pagination.tsx
│   ├── hooks/                  # Reusable hooks
│   │   ├── useAsync.ts         # Async operation hook
│   │   ├── useDebounce.ts      # Debounce hook
│   │   ├── useThrottle.ts      # Throttle hook
│   │   ├── useLocalStorage.ts  # LocalStorage hook
│   │   ├── useMediaQuery.ts    # Responsive hook
│   │   ├── useOnlineStatus.ts  # Connection status hook
│   │   ├── useInterval.ts      # Interval hook
│   │   └── usePrevious.ts      # Previous value hook
│   ├── utils/                  # Shared utilities
│   │   ├── cn.ts               # ClassName utility
│   │   ├── format.ts           # Formatting utilities
│   │   ├── debounce.ts         # Debounce function
│   │   ├── throttle.ts         # Throttle function
│   │   └── uid.ts              # UUID generation
│   └── constants/              # Shared constants
│       ├── routes.ts           # Route definitions
│       ├── messages.ts         # UI messages
│       └── config.ts           # Shared config values
│
├── routes/                     # Route configuration
│   ├── index.tsx               # Route definitions
│   ├── PrivateRoute.tsx        # Protected route wrapper (future)
│   └── RouteGuard.tsx          # Route guard logic
│
├── pages/                      # Page components
│   ├── HomePage.tsx            # Home/Landing page
│   ├── AboutPage.tsx           # About Us page
│   ├── ContactPage.tsx         # Contact Us page
│   ├── SupportPage.tsx         # Support page (chat interface)
│   └── SettingsPage.tsx        # Settings page
│
├── styles/                     # Global styles
│   ├── index.css               # Main stylesheet
│   ├── variables.css           # CSS variables
│   ├── reset.css               # CSS reset
│   └── utilities.css           # Utility classes
│
└── assets/                     # Source assets
    ├── images/                 # Images
    ├── icons/                  # Icon components
    └── fonts/                  # Custom fonts (if any)
```

---

## Feature Organization

### Feature Module Structure

Each feature follows a consistent structure:

```
features/{feature-name}/
├── index.ts                    # Public API (exports)
├── components/                 # React components
│   ├── {FeatureName}View.tsx   # Main view component
│   ├── {Component1}.tsx
│   ├── {Component2}.tsx
│   └── index.ts                # Barrel export
├── hooks/                      # Custom hooks
│   ├── use{Feature}.ts
│   ├── use{Operation}.ts
│   └── index.ts
├── services/                   # Business logic
│   ├── {feature}Service.ts
│   └── index.ts
├── context/                    # React Context
│   ├── {Feature}Context.tsx
│   ├── {Feature}Provider.tsx
│   └── index.ts
├── types/                      # TypeScript types
│   └── {feature}.types.ts
├── utils/                      # Feature utilities
│   └── {utility}.ts
├── constants/                  # Feature constants
│   └── {constants}.ts
└── styles/                     # Feature styles
    └── {feature}.module.css
```

### Feature Module Example: Chat

```typescript
// features/chat/index.ts
// Public API - only export what other features need

export { ChatView } from './components/ChatView';
export { ChatProvider } from './context/ChatProvider';
export { useChat } from './hooks/useChat';
export type { Message, ChatState } from './types/chat.types';
```

```typescript
// features/chat/components/index.ts
// Internal barrel export for components

export { ChatView } from './ChatView';
export { MessageList } from './MessageList';
export { MessageItem } from './MessageItem';
export { MessageInput } from './MessageInput';
export { TypingIndicator } from './TypingIndicator';
```

---

## Component Structure

### Component File Template

```typescript
// Component imports
import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';

// Local imports (features/shared)
import { useChat } from '../hooks/useChat';
import { Button } from '@/shared/components/ui/Button';

// Styles
import styles from './MessageInput.module.css';

// Types
interface MessageInputProps {
  sessionId: string;
  disabled?: boolean;
  onSend?: (message: string) => void;
}

/**
 * MessageInput component for composing and sending messages
 * 
 * @param sessionId - Current session ID
 * @param disabled - Whether input is disabled
 * @param onSend - Callback when message is sent
 */
export function MessageInput({ sessionId, disabled, onSend }: MessageInputProps) {
  // State
  const [input, setInput] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  
  // Hooks
  const { sendMessage } = useChat();
  
  // Handlers
  const handleSubmit = useCallback(async () => {
    if (!input.trim() || isSubmitting) return;
    
    setIsSubmitting(true);
    try {
      await sendMessage(sessionId, input);
      setInput('');
      onSend?.(input);
    } catch (error) {
      console.error('Failed to send message:', error);
    } finally {
      setIsSubmitting(false);
    }
  }, [input, sessionId, sendMessage, onSend, isSubmitting]);
  
  // Render
  return (
    <div className={styles.container}>
      <textarea
        value={input}
        onChange={(e) => setInput(e.target.value)}
        disabled={disabled || isSubmitting}
        placeholder="Type your message..."
        className={styles.textarea}
      />
      <Button
        onClick={handleSubmit}
        disabled={!input.trim() || disabled || isSubmitting}
        loading={isSubmitting}
      >
        Send
      </Button>
    </div>
  );
}
```

---

## File Naming Conventions

### TypeScript/TSX Files

| File Type | Convention | Example |
|-----------|------------|---------|
| React Component | PascalCase | `MessageItem.tsx` |
| Hook | camelCase with `use` prefix | `useChat.ts` |
| Service | camelCase with Service suffix | `chatService.ts` |
| Util | camelCase | `formatDate.ts` |
| Type definition | camelCase with `.types` suffix | `chat.types.ts` |
| Test | Same as file + `.test` or `.spec` | `MessageItem.test.tsx` |
| Story (Storybook) | Same as file + `.stories` | `Button.stories.tsx` |

### CSS Files

| File Type | Convention | Example |
|-----------|------------|---------|
| CSS Module | kebab-case + `.module.css` | `message-item.module.css` |
| Global CSS | kebab-case + `.css` | `variables.css` |

### Configuration Files

| File Type | Convention | Example |
|-----------|------------|---------|
| Config | dot-prefix or kebab-case | `.eslintrc.js`, `vite.config.ts` |
| Env | `.env` with suffix | `.env.local`, `.env.production` |

### Folders

| Folder Type | Convention | Example |
|-------------|------------|---------|
| Feature folder | kebab-case | `chat/`, `session-management/` |
| Component folder | kebab-case | `ui/`, `layout/` |
| Util folder | kebab-case | `api/`, `utils/` |

---

## Import/Export Patterns

### Path Aliases

Configure in `tsconfig.json`:

```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"],
      "@/core/*": ["src/core/*"],
      "@/features/*": ["src/features/*"],
      "@/shared/*": ["src/shared/*"]
    }
  }
}
```

### Import Order

```typescript
// 1. External libraries
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

// 2. Core
import { apiClient } from '@/core/api/client';
import { logger } from '@/core/utils/logger';

// 3. Features (other features)
import { useTenant } from '@/features/tenant';

// 4. Shared
import { Button } from '@/shared/components/ui/Button';
import { useDebounce } from '@/shared/hooks/useDebounce';

// 5. Local (same feature)
import { useChat } from '../hooks/useChat';
import { ChatContext } from '../context/ChatContext';

// 6. Types
import type { Message } from '../types/chat.types';

// 7. Styles
import styles from './ChatView.module.css';
```

### Barrel Exports

Use `index.ts` files for clean exports:

```typescript
// features/chat/components/index.ts
export { ChatView } from './ChatView';
export { MessageList } from './MessageList';
export { MessageItem } from './MessageItem';
export { MessageInput } from './MessageInput';
```

Then import:

```typescript
import { ChatView, MessageList } from '@/features/chat/components';
```

---

## Configuration Files

### package.json

```json
{
  "name": "v16-agent-ui",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
    "lint:fix": "eslint . --ext ts,tsx --fix",
    "format": "prettier --write \"src/**/*.{ts,tsx,css}\"",
    "type-check": "tsc --noEmit",
    "test": "vitest",
    "test:ui": "vitest --ui",
    "test:coverage": "vitest --coverage",
    "e2e": "playwright test"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.0",
    "axios": "^1.6.0",
    "zustand": "^4.4.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "@types/node": "^20.10.0",
    "@typescript-eslint/eslint-plugin": "^6.15.0",
    "@typescript-eslint/parser": "^6.15.0",
    "@vitejs/plugin-react": "^4.2.0",
    "eslint": "^8.56.0",
    "eslint-plugin-react-hooks": "^4.6.0",
    "eslint-plugin-react-refresh": "^0.4.5",
    "prettier": "^3.1.0",
    "typescript": "^5.3.0",
    "vite": "^5.0.0",
    "vitest": "^1.0.0",
    "@vitest/ui": "^1.0.0",
    "c8": "^9.0.0",
    "tsx": "^4.7.0",
    "@playwright/test": "^1.40.0"
  }
}
```

### tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    
    /* Bundler mode */
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    
    /* Linting */
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    
    /* Path mapping */
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"],
      "@/core/*": ["src/core/*"],
      "@/features/*": ["src/features/*"],
      "@/shared/*": ["src/shared/*"]
    }
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

### vite.config.ts

```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      '@/core': path.resolve(__dirname, './src/core'),
      '@/features': path.resolve(__dirname, './src/features'),
      '@/shared': path.resolve(__dirname, './src/shared')
    }
  },
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:9080',
        changeOrigin: true
      },
      '/health': {
        target: 'http://localhost:9080',
        changeOrigin: true
      }
    }
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
    rollupOptions: {
      output: {
        manualChunks: {
          'react-vendor': ['react', 'react-dom', 'react-router-dom'],
          'api-vendor': ['axios']
        }
      }
    }
  }
});
```

### .eslintrc.js

```javascript
module.exports = {
  root: true,
  env: { browser: true, es2020: true },
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:react-hooks/recommended',
  ],
  ignorePatterns: ['dist', '.eslintrc.js'],
  parser: '@typescript-eslint/parser',
  plugins: ['react-refresh'],
  rules: {
    'react-refresh/only-export-components': [
      'warn',
      { allowConstantExport: true },
    ],
    '@typescript-eslint/no-explicit-any': 'warn',
    '@typescript-eslint/no-unused-vars': ['error', { 
      argsIgnorePattern: '^_',
      varsIgnorePattern: '^_'
    }],
  },
};
```

### .prettierrc

```json
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 100,
  "tabWidth": 2,
  "useTabs": false,
  "arrowParens": "always",
  "endOfLine": "lf"
}
```

### .env.example

```bash
# API Configuration
VITE_API_BASE_URL=http://localhost:9080
VITE_API_TIMEOUT=30000

# Feature Flags
VITE_ENABLE_STREAMING=true
VITE_ENABLE_ANALYTICS=false

# Development
VITE_DEV_MODE=true
VITE_LOG_LEVEL=debug
```

---

## Testing Structure

### Test File Location

Tests should be colocated with the code they test:

```
features/chat/
├── components/
│   ├── MessageItem.tsx
│   ├── MessageItem.test.tsx       # Unit test
│   └── MessageItem.stories.tsx    # Storybook story
├── hooks/
│   ├── useChat.ts
│   └── useChat.test.ts
└── services/
    ├── chatService.ts
    └── chatService.test.ts
```

### Test Types

```
tests/
├── unit/                          # Unit tests (colocated)
├── integration/                   # Integration tests
│   ├── api/
│   │   └── chat.integration.test.ts
│   └── features/
│       └── chat-flow.integration.test.ts
├── e2e/                           # End-to-end tests
│   ├── chat.spec.ts
│   └── sessions.spec.ts
├── fixtures/                      # Test fixtures
│   ├── messages.json
│   └── sessions.json
└── setup.ts                       # Test setup
```

---

## Build Output

### Development

```
dist/ (not created in dev mode)
```

Development uses Vite's dev server with HMR.

### Production

```
dist/
├── assets/
│   ├── index-[hash].js          # Main bundle
│   ├── index-[hash].css         # Main styles
│   ├── react-vendor-[hash].js   # React chunk
│   ├── api-vendor-[hash].js     # API chunk
│   └── [component]-[hash].js    # Lazy-loaded chunks
├── index.html                    # HTML entry
└── favicon.ico                   # Static assets
```

---

## Best Practices

### 1. Feature Isolation

Keep features independent:

```typescript
// ❌ Bad: Direct import from another feature
import { SessionList } from '@/features/sessions/components/SessionList';

// ✅ Good: Import from feature's public API
import { SessionList } from '@/features/sessions';
```

### 2. Shared Code

Extract common code to `shared/`:

```typescript
// ❌ Bad: Duplicated code in multiple features
// features/chat/utils/formatDate.ts
// features/sessions/utils/formatDate.ts

// ✅ Good: Shared utility
// shared/utils/format.ts
export function formatDate(date: Date): string { /* ... */ }
```

### 3. Type Definitions

Keep types close to usage:

```typescript
// ✅ Good: Feature-specific types
// features/chat/types/chat.types.ts
export interface Message { /* ... */ }

// ✅ Good: Global types
// core/types/api.types.ts
export interface APIError { /* ... */ }
```

### 4. CSS Modules

Use CSS Modules for component styles:

```typescript
// MessageItem.tsx
import styles from './MessageItem.module.css';

export function MessageItem() {
  return <div className={styles.container}>...</div>;
}
```

### 5. Barrel Exports

Use index.ts for clean public APIs:

```typescript
// features/chat/index.ts
export { ChatView } from './components/ChatView';
export { ChatProvider } from './context/ChatProvider';
export { useChat } from './hooks/useChat';
// Don't export internal implementation details
```

---

## Migration Guide

### From Flat Structure

If migrating from a flat structure:

```
Before:
src/
├── components/  (all components mixed)
├── hooks/       (all hooks mixed)
└── utils/       (all utils mixed)

After:
src/
├── features/    (organized by feature)
├── shared/      (truly shared)
└── core/        (infrastructure)
```

### Migration Steps

1. **Identify Features**: Group components by feature
2. **Create Feature Folders**: Move related files
3. **Extract Shared**: Move truly shared code to `shared/`
4. **Update Imports**: Fix import paths
5. **Add Barrel Exports**: Create index.ts files
6. **Test**: Verify everything still works

---

## Summary

This structure provides:

✅ **Clear Organization**: Feature-based structure  
✅ **Scalability**: Easy to add new features  
✅ **Maintainability**: Code is easy to find  
✅ **Reusability**: Shared code is extracted  
✅ **Testability**: Tests are colocated  
✅ **Type Safety**: TypeScript throughout  
✅ **Consistency**: Standard naming conventions

---

## Next Steps

1. Review structure and approve
2. Initialize project with this structure
3. Create core infrastructure
4. Build first feature as template
5. Document feature-specific conventions

For implementation details, see:
- [Frontend Architecture](./FRONTEND_ARCHITECTURE.md)
- [Integration Guide](./INTEGRATION_GUIDE.md)
- [Deployment Guide](./DEPLOYMENT_GUIDE.md)
