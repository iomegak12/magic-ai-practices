# Deployment Guide

**Version:** 1.0.0  
**Last Updated:** February 20, 2026

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Docker Setup](#docker-setup)
- [Dockerfile Configuration](#dockerfile-configuration)
- [Docker Compose Configuration](#docker-compose-configuration)
- [Environment Variables](#environment-variables)
- [Build Process](#build-process)
- [Running Containers](#running-containers)
- [Container Management](#container-management)
- [Troubleshooting](#troubleshooting)

---

## Overview

This guide covers Docker-based deployment for the Customer Service Agent Web UI. The application is containerized as a static build served by nginx.

### Deployment Architecture

```
┌─────────────────────────────────────┐
│     Docker Host                     │
│                                     │
│  ┌─────────────────────────────┐   │
│  │  v16-agent-ui Container     │   │
│  │  (nginx:alpine)             │   │
│  │                             │   │
│  │  - Static React Build       │   │
│  │  - nginx Web Server         │   │
│  │  - Port: 80                 │   │
│  └─────────┬───────────────────┘   │
│            │                        │
│            │ HTTP (API calls)       │
│            ↓                        │
│  ┌─────────────────────────────┐   │
│  │  Backend API Container      │   │
│  │  (Python FastAPI)           │   │
│  │  - Port: 9080               │   │
│  └─────────────────────────────┘   │
│                                     │
└─────────────────────────────────────┘
```

**Note**: The React SPA makes direct API calls to FastAPI (port 9080) with CORS enabled on the backend.

---

## Prerequisites

### Required Software

- **Docker**: 24.0 or later
- **Docker Compose**: 2.0 or later (no version field required)
- **Git**: For cloning repository

### Installation

#### Windows

```powershell
# Install Docker Desktop for Windows
# Download from: https://www.docker.com/products/docker-desktop

# Verify installation
docker --version
docker-compose --version
```

#### Linux

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo apt-get install docker-compose-plugin

# Verify installation
docker --version
docker compose version
```

#### macOS

```bash
# Install Docker Desktop for Mac
# Download from: https://www.docker.com/products/docker-desktop

# Verify installation
docker --version
docker compose version
```

---

## Docker Setup

### Directory Structure

```
v16-e2e/front-end/
├── Dockerfile                    # Multi-stage build definition
├── docker-compose.yml            # Service orchestration
├── .dockerignore                 # Files to exclude from image
├── .env.example                  # Environment variable template
├── .env.local                    # Local environment (gitignored)
├── package.json                  # Dependencies
├── vite.config.ts                # Vite configuration
├── nginx.conf                    # nginx configuration for production
├── src/                          # React application
└── public/                       # Static assets
```

---

## Dockerfile Configuration

### Multi-Stage Build

Create `Dockerfile` in project root:

```dockerfile
# ============================================
# Stage 1: Builder
# ============================================
FROM node:22-alpine AS builder

# Set working directory
WORKDIR /app

# Copy package files
COPY package.json package-lock.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY . .

# Build application
RUN npm run build

#  ============================================
# Stage 2: Production 
# ============================================
FROM nginx:alpine AS production

# Copy nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Copy built assets from builder
COPY --from=builder /app/dist /usr/share/nginx/html

# Expose port
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost/health || exit 1

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
```

### nginx Configuration

Create `nginx.conf` in project root:

```nginx
events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # Logging
    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log;

    # Performance
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 10240;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types text/plain text/css text/xml text/javascript 
               application/json application/javascript application/xml+rss 
               application/rss+xml font/truetype font/opentype 
               application/vnd.ms-fontobject image/svg+xml;

    server {
        listen 80;
        server_name _;
        root /usr/share/nginx/html;
        index index.html;

        # Security headers
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header X-XSS-Protection "1; mode=block" always;

        # SPA routing - serve index.html for all routes
        location / {
            try_files $uri $uri/ /index.html;
        }

        # Health check endpoint
        location /health {
            access_log off;
            return 200 "healthy\n";
            add_header Content-Type text/plain;
        }

        # Cache static assets
        location ~* \\.(?:css|js|jpg|jpeg|gif|png|ico|svg|woff|woff2|ttf|eot)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }

        # No cache for HTML
        location ~* \\.html$ {
            add_header Cache-Control "no-cache, no-store, must-revalidate";
        }
    }
}
```

### Dockerfile Optimization

#### Layer Caching

```dockerfile
# ✅ Good: Copy package files first (cached if unchanged)
COPY package.json package-lock.json ./
RUN npm ci

# Then copy source code (changes frequently)
COPY . .
```

#### Multi-Stage Benefits

1. **Smaller Image Size**: Production image doesn't include build tools
2. **Faster Builds**: Builder stage can be cached
3. **Security**: Fewer packages in production image

---

## Docker Compose Configuration

### docker-compose.yml

Create `docker-compose.yml` in project root:

```yaml
# No version field required (Docker Compose v2+)

services:
  # Frontend UI Service
  frontend-ui:
    image: v16-agent-service:latest
    container_name: v16-agent-ui
    build:
      context: .
      dockerfile: Dockerfile
      target: production
    ports:
      - "80:80"
    environment:
      - VITE_API_BASE_URL=http://localhost:9080
    networks:
      - app-network
    depends_on:
      backend-api:
        condition: service_healthy
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "wget", "--no-verbose", "--tries=1", "--spider", "http://localhost/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 5s

  # Backend API Service (reference)
  backend-api:
    image: v16-backend-api:latest
    container_name: v16-backend-api
    ports:
      - "9080:9080"
    environment:
      - PYTHONUNBUFFERED=1
      - API_HOST=0.0.0.0
      - API_PORT=9080
    networks:
      - app-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s

networks:
  app-network:
    driver: bridge
```

### Development Override

Create `docker-compose.dev.yml` for development:

```yaml
services:
  frontend-ui:
    build:
      target: builder  # Use builder stage for dev
    volumes:
      # Mount source code for hot reload
      - ./src:/app/src:ro
      - ./server:/app/server:ro
      - ./public:/app/public:ro
      # Exclude node_modules
      - /app/node_modules
    environment:
      - NODE_ENV=development
      - VITE_DEV_MODE=true
      - VITE_LOG_LEVEL=debug
    command: npm run dev
    ports:
      - "3000:3000"
      - "24678:24678"  # Vite HMR port
```

---

## Environment Variables

### .env.example Template

```bash
# ============================================
# API Configuration
# ============================================
VITE_API_BASE_URL=http://localhost:9080
VITE_API_TIMEOUT=30000

# ============================================
# Feature Flags
# ============================================
VITE_ENABLE_STREAMING=true
VITE_ENABLE_ANALYTICS=false
VITE_ENABLE_DEBUG=false

# ============================================
# Logging
# ============================================
VITE_LOG_LEVEL=info

# ============================================
# Multi-Tenancy
# ============================================
VITE_DEFAULT_TENANT=default

# ============================================
# Performance
# ============================================
VITE_API_RETRY_ATTEMPTS=3
VITE_API_RETRY_DELAY=1000
VITE_API_MAX_RETRIES=5
```

### Environment Variable Loading

```typescript
// src/core/config/env.ts

interface EnvConfig {
  apiBaseURL: string;
  apiTimeout: number;
  enableStreaming: boolean;
  enableAnalytics: boolean;
  logLevel: string;
  defaultTenant: string;
  retryAttempts: number;
  retryDelay: number;
}

function loadEnv(): EnvConfig {
  return {
    apiBaseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:9080',
    apiTimeout: parseInt(import.meta.env.VITE_API_TIMEOUT || '30000'),
    enableStreaming: import.meta.env.VITE_ENABLE_STREAMING === 'true',
    enableAnalytics: import.meta.env.VITE_ENABLE_ANALYTICS === 'true',
    logLevel: import.meta.env.VITE_LOG_LEVEL || 'info',
    defaultTenant: import.meta.env.VITE_DEFAULT_TENANT || 'default',
    retryAttempts: parseInt(import.meta.env.VITE_API_RETRY_ATTEMPTS || '3'),
    retryDelay: parseInt(import.meta.env.VITE_API_RETRY_DELAY || '1000')
  };
}

export const env = loadEnv();
```

---

## .dockerignore Configuration

Create `.dockerignore` to exclude unnecessary files:

```
# Dependencies
node_modules
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*

# Build output
dist
build
.vite
.cache

# Testing
coverage
.nyc_output
*.test.ts
*.test.tsx
*.spec.ts
*.spec.tsx
__tests__
__mocks__

# Environment
.env
.env.local
.env.*.local

# IDEs
.vscode
.idea
*.swp
*.swo
*~

# Git
.git
.gitignore
.gitattributes

# CI/CD
.github
.gitlab-ci.yml

# Documentation
README.md
CHANGELOG.md
docs/
*.md

# Docker
Dockerfile*
docker-compose*.yml
.dockerignore

# OS
.DS_Store
Thumbs.db

# Logs
logs
*.log

# Temporary
tmp
temp
*.tmp
```

---

## Build Process

### Build Docker Image

```powershell
# Navigate to project directory
cd v16-e2e/front-end

# Build image with tag
docker build -t v16-agent-service:latest .

# Build with specific tag
docker build -t v16-agent-service:1.0.0 .

# Build with build args
docker build \
  --build-arg NODE_ENV=production \
  -t v16-agent-service:latest \
  .
```

### Verify Build

```powershell
# List images
docker images | grep v16-agent-service

# Inspect image
docker inspect v16-agent-service:latest

# Check image size
docker images v16-agent-service:latest --format "{{.Size}}"
```

### Multi-Platform Build (Optional)

```powershell
# Create builder
docker buildx create --name multiplatform --use

# Build for multiple platforms
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t v16-agent-service:latest \
  --push \
  .
```

---

## Running Containers

### Using Docker Compose (Recommended)

#### Production

```powershell
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f frontend-ui

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

#### Development

```powershell
# Start with development overrides
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

# Rebuild and start
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build

# Stop development services
docker-compose -f docker-compose.yml -f docker-compose.dev.yml down
```

### Using Docker Run

```powershell
# Run standalone container
docker run -d \
  --name v16-agent-ui \
  -p 3000:3000 \
  -e NODE_ENV=production \
  -e API_BASE_URL=http://backend-api:9080 \
  --network app-network \
  v16-agent-service:latest

# View logs
docker logs -f v16-agent-ui

# Stop container
docker stop v16-agent-ui

# Remove container
docker rm v16-agent-ui
```

---

## Container Management

### Health Checks

```powershell
# Check container health
docker ps --filter "name=v16-agent-ui"

# Inspect health status
docker inspect --format='{{.State.Health.Status}}' v16-agent-ui

# View health check logs
docker inspect --format='{{json .State.Health}}' v16-agent-ui | jq
```

### Resource Limits

Add to `docker-compose.yml`:

```yaml
services:
  frontend-ui:
    # ... other config
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
```

### Logs Management

```powershell
# Follow logs
docker-compose logs -f frontend-ui

# Last 100 lines
docker-compose logs --tail=100 frontend-ui

# Since timestamp
docker-compose logs --since 2024-01-01T00:00:00 frontend-ui

# With timestamps
docker-compose logs -t frontend-ui
```

### Container Shell Access

```powershell
# Execute shell in running container
docker exec -it v16-agent-ui sh

# Run one-off command
docker exec v16-agent-ui node --version

# Check environment variables
docker exec v16-agent-ui env
```

---

## Troubleshooting

### Common Issues

#### Issue 1: Container Fails to Start

```powershell
# Check logs
docker logs v16-agent-ui

# Inspect container
docker inspect v16-agent-ui

# Check exit code
docker inspect --format='{{.State.ExitCode}}' v16-agent-ui
```

**Solution**:
- Verify environment variables
- Check port conflicts
- Ensure backend API is running

#### Issue 2: Cannot Connect to Backend API

```powershell
# Check network
docker network inspect app-network

# Test connectivity from frontend container
docker exec v16-agent-ui ping backend-api

# Check backend health
curl http://localhost:9080/health
```

**Solution**:
- Ensure both containers are on same network
- Verify API_BASE_URL environment variable
- Check backend container is healthy

#### Issue 3: Build Fails

```powershell
# Build with verbose output
docker build --progress=plain --no-cache -t v16-agent-service:latest .

# Check Docker logs
docker logs <container-id>
```

**Solution**:
- Clear Docker cache: `docker system prune -a`
- Check Dockerfile syntax
- Verify package.json dependencies

#### Issue 4: Port Already in Use

```powershell
# Find process using port 3000
netstat -ano | findstr :3000

# Kill process (Windows)
taskkill /PID <PID> /F

# Or change port in docker-compose.yml
ports:
  - "3001:3000"
```

### Debugging

#### Enable Debug Mode

```yaml
# docker-compose.dev.yml
services:
  frontend-ui:
    environment:
      - DEBUG=*
      - VITE_LOG_LEVEL=debug
    command: npm run dev
```

#### Inspect Build Stages

```powershell
# Build and tag intermediate stages
docker build --target builder -t v16-agent-service:builder .
docker build --target production -t v16-agent-service:production .

# Run builder stage
docker run -it v16-agent-service:builder sh
```

---

## Performance Optimization

### Image Size Optimization

```dockerfile
# Use Alpine for smaller base
FROM node:22-alpine

# Multi-stage build
FROM node:22-alpine AS builder
# ... build stage

FROM node:22-alpine AS production
# ... production stage (smaller)

# Clean npm cache
RUN npm cache clean --force

# Remove dev dependencies
RUN npm prune --production
```

### Build Cache Optimization

```dockerfile
# Copy package files first (cached)
COPY package.json package-lock.json ./
RUN npm ci

# Copy source code last (changes frequently)
COPY . .
```

### Layer Optimization

```dockerfile
# ❌ Bad: Creates unnecessary layers
RUN apk add --no-cache curl
RUN apk add --no-cache wget
RUN apk add --no-cache git

# ✅ Good: Single layer
RUN apk add --no-cache \
    curl \
    wget \
    git
```

---

## Security Best Practices

### Non-Root User

```dockerfile
# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

# Change ownership
COPY --chown=nodejs:nodejs . .

# Switch user
USER nodejs
```

### Secret Management

```powershell
# Use Docker secrets (Swarm mode)
docker secret create api_key api_key.txt

# Reference in compose
secrets:
  api_key:
    external: true

services:
  frontend-ui:
    secrets:
      - api_key
```

### Image Scanning

```powershell
# Scan for vulnerabilities
docker scan v16-agent-service:latest

# Use Trivy
trivy image v16-agent-service:latest
```

---

## Monitoring

### Container Stats

```powershell
# Real-time stats
docker stats v16-agent-ui

# All containers
docker stats

# Format output
docker stats --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"
```

### Prometheus Metrics (Future)

```yaml
# docker-compose.yml
services:
  frontend-ui:
    labels:
      - "prometheus.io/scrape=true"
      - "prometheus.io/port=3000"
      - "prometheus.io/path=/metrics"
```

---

## Backup and Restore

### Export Image

```powershell
# Save image to tar
docker save v16-agent-service:latest -o v16-agent-service.tar

# Compress
gzip v16-agent-service.tar
```

### Import Image

```powershell
# Load from tar
docker load -i v16-agent-service.tar

# Or from compressed
gunzip -c v16-agent-service.tar.gz | docker load
```

---

## Summary

This deployment guide provides:

✅ **Docker Configuration**: Multi-stage Dockerfile  
✅ **Docker Compose**: Service orchestration  
✅ **Environment Management**: .env configuration  
✅ **Build Process**: Optimized builds  
✅ **Container Management**: Health checks, logs, shell access  
✅ **Troubleshooting**: Common issues and solutions  
✅ **Performance**: Image optimization  
✅ **Security**: Non-root user, secrets management

---

## Quick Reference

### Common Commands

```powershell
# Build
docker-compose build

# Start
docker-compose up -d

# Stop
docker-compose down

# Logs
docker-compose logs -f

# Restart
docker-compose restart

# Rebuild and start
docker-compose up --build -d

# Clean up
docker-compose down -v
docker system prune -a
```

---

## Next Steps

1. Review Docker configuration
2. Build and test locally
3. Deploy to environment
4. Set up monitoring
5. Configure CI/CD pipeline

For project structure, see [Project Structure](./PROJECT_STRUCTURE.md).
For API integration, see [Integration Guide](./INTEGRATION_GUIDE.md).
