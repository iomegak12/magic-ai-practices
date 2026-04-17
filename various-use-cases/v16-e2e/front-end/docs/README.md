# Customer Service Agent Web UI

> Modern React-based web interface for AI-powered customer service operations

**Version**: 1.0.0  
**Status**: Production Ready  
**License**: MIT

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Documentation](#documentation)
- [Quick Start](#quick-start)
- [Development](#development)
- [Deployment](#deployment)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

The Customer Service Agent Web UI is a sophisticated frontend application that provides an intuitive interface for interacting with an AI-powered customer service agent. It enables users to have natural conversations, manage sessions, track analytics, and perform customer service operations through an intelligent agent.

### What It Does

- **Conversational Interface**: Natural language chat with AI agent
- **Session Management**: Create, list, delete, and restore conversation sessions
- **Multi-Tenancy**: Support for multiple tenants with isolated data
- **Real-Time Streaming**: Live message streaming for responsive interactions
- **Tool Integration**: Automatic tool execution (order management, email, complaints)
- **Analytics Dashboard**: Usage statistics and insights
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile

---

## ✨ Features

### Core Capabilities

✅ **Multi-Turn Conversations**
- Context-aware AI agent
- Conversation history
- Session persistence (24h TTL)

✅ **Session Management**
- Create new sessions with custom IDs
- List all sessions with pagination
- View session history
- Delete sessions
- Session cleanup (expired)
- Session statistics

✅ **Agent Tools** (Automatic Execution)
- Order search and management
- Email sending capabilities
- Complaint registration and tracking
- Database queries
- Extended context retrieval

✅ **Multi-Tenancy**
- Tenant-based data isolation
- Tenant selector UI
- Tenant-scoped sessions
- Per-tenant statistics

✅ **Streaming Support** (Future)
- Server-Sent Events (SSE)
- Real-time message chunks
- Tool execution indicators
- Cancel streaming

✅ **Error Handling**
- Automatic retry with exponential backoff
- Circuit breaker for failing services
- Rate limit management
- User-friendly error messages

✅ **Performance**
- Code splitting
- Lazy loading
- Virtual scrolling
- Optimistic updates
- Request caching

---

## 🛠 Technology Stack

### Frontend

| Technology | Version | Purpose |
|------------|---------|---------|
| **React** | 18.x | UI framework |
| **TypeScript** | 5.x | Type safety |
| **Vite** | 5.x | Build tool & dev server |
| **React Router** | 6.x | Client-side routing |
| **Axios** | 1.x | HTTP client |
| **Tabler** | Latest | UI framework (CDN) |

### Deployment

| Technology | Version | Purpose |
|------------|---------|---------|
| **nginx** | alpine | Static file server |
| **Docker** | 24+ | Containerization |
| **Docker Compose** | 2+ | Orchestration |

**Note**: React SPA communicates directly with FastAPI backend (port 9080) - no BFF middleware.

### Development Tools

| Tool | Purpose |
|------|---------|
| **ESLint** | Code linting |
| **Prettier** | Code formatting |
| **Vitest** | Unit testing |
| **Playwright** | E2E testing |

---

## 📚 Documentation

Comprehensive documentation is available in the `/docs` folder:

### Getting Started

1. **[API Specification](./API_SPECIFICATION.md)** (16,000+ lines)
   - Complete REST API reference
   - TypeScript interfaces
   - Request/response examples
   - Error handling
   - Rate limiting
   - Multi-tenancy

### Architecture & Design

2. **[Frontend Architecture](./FRONTEND_ARCHITECTURE.md)**
   - System architecture
   - Component patterns
   - State management
   - Performance optimization
   - Security considerations

3. **[Project Structure](./PROJECT_STRUCTURE.md)**
   - Folder organization
   - File naming conventions
   - Module boundaries
   - Import/export patterns

### Implementation Guides

4. **[Integration Guide](./INTEGRATION_GUIDE.md)**
   - API client setup
   - Retry strategies
   - Rate limit handling
   - Circuit breaker pattern
   - Timeout configuration
   - Connection resilience
   - Streaming integration

5. **[UI Component Guide](./UI_COMPONENT_GUIDE.md)**
   - Chat interface patterns
   - Session management UI
   - Error displays
   - Loading states
   - Tool call indicators
   - Form components
   - Navigation
   - Data tables

6. **[Multi-Tenancy Guide](./TENANT_MULTI_TENANCY.md)**
   - Tenant concept
   - Tenant selection UI
   - Context management
   - API integration
   - Storage patterns
   - Tenant switching

### Deployment

7. **[Deployment Guide](./DEPLOYMENT_GUIDE.md)**
   - Docker setup
   - Dockerfile configuration
   - Docker Compose
   - Environment variables
   - Build process
   - Container management
   - Troubleshooting

---

## 🚀 Quick Start

### Prerequisites

**For Development**:
- **Node.js**: v22 or later
- **npm**: v9 or later
- **Git**: For cloning repository

**For Production Deployment**:
- **Docker**: v24 or later
- **Docker Compose**: v2 or later

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd v16-e2e/front-end

# Install dependencies
npm install

# Create environment file
cp .env.example .env.local

# Edit .env.local with your API endpoint
# VITE_API_BASE_URL=http://localhost:9080
```

### Running Locally

```bash
# Start development server
npm run dev

# Open browser to http://localhost:3000
```

### Running with Docker

```bash
# Build image
docker build -t v16-agent-service:latest .

# Run with docker-compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

---

## 💻 Development

### Available Scripts

```bash
# Development server with HMR
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run tests
npm test

# Run tests with UI
npm test:ui

# Run tests with coverage
npm test:coverage

# Run E2E tests
npm run e2e

# Lint code
npm run lint

# Lint and fix
npm run lint:fix

# Format code
npm run format

# Type check
npm run type-check
```

### Environment Variables

Create `.env.local` file:

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

# Multi-Tenancy
VITE_DEFAULT_TENANT=default
```

### Development Workflow

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/my-feature
   ```

2. **Make Changes**
   - Follow TypeScript best practices
   - Write unit tests
   - Update documentation

3. **Test Changes**
   ```bash
   npm run lint
   npm run type-check
   npm test
   ```

4. **Commit Changes**
   ```bash
   git add .
   git commit -m "feat: add new feature"
   ```

5. **Push and Create PR**
   ```bash
   git push origin feature/my-feature
   ```

### Code Style

This project uses:
- **ESLint**: For code linting
- **Prettier**: For code formatting
- **TypeScript**: Strict mode enabled

Configuration files:
- `.eslintrc.js`
- `.prettierrc`
- `tsconfig.json`

### Commit Convention

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: Add new feature
fix: Fix bug
docs: Update documentation
style: Format code
refactor: Refactor code
test: Add tests
chore: Update dependencies
```

---

## 🐳 Deployment

### Docker Deployment

#### Production Build

```bash
# Build image
docker build -t v16-agent-service:latest .

# Tag for registry
docker tag v16-agent-service:latest registry.example.com/v16-agent-service:1.0.0

# Push to registry
docker push registry.example.com/v16-agent-service:1.0.0
```

#### Docker Compose

```bash
# Start all services
docker-compose up -d

# Scale frontend
docker-compose up -d --scale frontend-ui=3

# View logs
docker-compose logs -f frontend-ui

# Stop services
docker-compose down
```

#### Health Checks

```bash
# Check container health
docker ps --filter "name=v16-agent-ui"

# Inspect health status
docker inspect --format='{{.State.Health.Status}}' v16-agent-ui

# Test health endpoint
curl http://localhost:3000/health
```

### Environment Configuration

**Production** (`.env.production`):
```bash
VITE_API_BASE_URL=https://api.production.com
VITE_API_TIMEOUT=30000
VITE_ENABLE_STREAMING=true
VITE_ENABLE_ANALYTICS=true
VITE_LOG_LEVEL=error
```

**Staging** (`.env.staging`):
```bash
VITE_API_BASE_URL=https://api.staging.com
VITE_API_TIMEOUT=30000
VITE_ENABLE_STREAMING=true
VITE_ENABLE_ANALYTICS=false
VITE_LOG_LEVEL=info
```

---

## 📁 Project Structure

```
v16-e2e/front-end/
├── docs/                       # Documentation
│   ├── API_SPECIFICATION.md
│   ├── FRONTEND_ARCHITECTURE.md
│   ├── INTEGRATION_GUIDE.md
│   ├── PROJECT_STRUCTURE.md
│   ├── DEPLOYMENT_GUIDE.md
│   ├── UI_COMPONENT_GUIDE.md
│   ├── TENANT_MULTI_TENANCY.md
│   └── README.md
├── src/                        # Source code
│   ├── core/                   # Core infrastructure
│   │   ├── api/                # API client
│   │   ├── config/             # Configuration
│   │   ├── types/              # Global types
│   │   └── utils/              # Utilities
│   ├── features/               # Feature modules
│   │   ├── chat/               # Chat feature
│   │   ├── sessions/           # Session management
│   │   ├── tenant/             # Multi-tenancy
│   │   └── health/             # Health monitoring
│   ├── shared/                 # Shared components
│   │   ├── components/         # Reusable UI
│   │   ├── hooks/              # Reusable hooks
│   │   └── utils/              # Shared utilities
│   ├── routes/                 # Route configuration
│   ├── pages/                  # Page components
│   ├── styles/                 # Global styles
│   └── main.tsx                # Entry point
├── tests/                      # E2E tests
├── public/                     # Static assets
├── nginx.conf                  # nginx configuration (production)
├── Dockerfile                  # Docker configuration
├── docker-compose.yml          # Docker Compose
├── vite.config.ts              # Vite configuration
├── package.json                # Dependencies
└── README.md                   # This file
```

For detailed structure, see [Project Structure](./PROJECT_STRUCTURE.md).

---

## 🧪 Testing

### Unit Tests

```bash
# Run all unit tests
npm test

# Run with watch mode
npm test -- --watch

# Run with coverage
npm test:coverage

# Run specific test file
npm test -- MessageItem.test.tsx
```

### Integration Tests

```bash
# Run integration tests
npm test -- tests/integration/

# Run with specific pattern
npm test -- --testPathPattern=integration
```

### E2E Tests

```bash
# Run Playwright tests
npm run e2e

# Run in headed mode
npm run e2e -- --headed

# Run specific test
npm run e2e -- --grep "chat flow"
```

---

## 🔒 Security

### Best Practices Implemented

✅ **XSS Prevention**: Input sanitization  
✅ **CORS**: Vite proxy (dev) & FastAPI CORS (production)  
✅ **Content Security Policy**: HTTP headers  
✅ **Non-Root Container**: nginx runs as nginx user  
✅ **Secrets Management**: Environment variables  
✅ **Rate Limiting**: Client-side handling  
✅ **Error Handling**: No sensitive data in errors

### Future Security Enhancements

- Authentication (OAuth2/OpenID Connect)
- Authorization (RBAC)
- CSRF protection
- Session encryption
- API key rotation

---

## 📊 Monitoring (Future)

### Planned Integrations

- **Application Insights**: Performance monitoring
- **Sentry**: Error tracking
- **Prometheus**: Metrics collection
- **Grafana**: Dashboards

### Metrics to Track

- Page load time
- API response time
- Error rate
- Session duration
- User interactions

---

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

### Getting Started

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write/update tests
5. Update documentation
6. Submit a pull request

### Code Review Checklist

- [ ] Code follows project conventions
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No console.log statements
- [ ] Error handling implemented
- [ ] Accessibility considered
- [ ] Performance optimized
- [ ] Security reviewed

### Reporting Issues

Use GitHub Issues with the following template:

```markdown
## Description
Brief description of the issue

## Steps to Reproduce
1. Go to ...
2. Click on ...
3. See error

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: Windows 11
- Browser: Chrome 119
- Node: 22.0.0
- Version: 1.0.0

## Screenshots
If applicable
```

---

## 📝 Changelog

### Version 1.0.0 (2026-02-20)

**Added**:
- Initial release
- Chat interface with message history
- Session management (create, list, delete)
- Multi-tenancy support
- Agent tool integration
- Error handling with retry logic
- Rate limit management
- Docker deployment
- Comprehensive documentation

**Known Issues**:
- Streaming support not yet implemented (documented for future)
- No authentication (planned for future)

---

## 📄 License

MIT License

Copyright (c) 2026 [Your Organization]

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

---

## 🙏 Acknowledgments

- **Tabler**: Beautiful UI framework
- **React Team**: Amazing frontend library
- **Vite Team**: Lightning-fast build tool
- **TypeScript Team**: Type safety for JavaScript
- **FastAPI Team**: Backend API framework

---

## 📞 Support

For support and questions:

- **Documentation**: See `/docs` folder
- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions
- **Email**: support@example.com

---

## 🗺 Roadmap

### Version 1.1 (Q2 2026)

- [ ] Streaming message support (SSE)
- [ ] File upload/download
- [ ] Export conversations (PDF, CSV)
- [ ] Dark mode toggle
- [ ] Keyboard shortcuts

### Version 1.2 (Q3 2026)

- [ ] Authentication (OAuth2)
- [ ] User profiles
- [ ] Session sharing
- [ ] Conversation search
- [ ] Advanced analytics

### Version 2.0 (Q4 2026)

- [ ] Voice input/output
- [ ] Multi-language support
- [ ] Mobile app (React Native)
- [ ] Offline support
- [ ] Real-time collaboration

---

## 📈 Stats

- **Documentation**: 8 comprehensive guides
- **API Endpoints**: 16 fully documented
- **TypeScript Interfaces**: 20+ defined
- **Lines of Code**: ~10,000+ (estimated)
- **Test Coverage**: TBD
- **Build Size**: ~500KB (gzipped)

---

**Built with ❤️ by the V16 Team**

For detailed documentation, see the `/docs` folder.
