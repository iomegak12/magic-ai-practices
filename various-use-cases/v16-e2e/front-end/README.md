# Customer Service Agent — Frontend UI

React 18 + Vite + Tabler web application for the Customer Service Agent API.

## Quick Start

```bash
# Install dependencies
npm install

# Start development server (port 3000)
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Development

- **Dev server:** http://localhost:3000
- **Backend API:** http://localhost:9080 (proxied via Vite)
- **Tabler docs:** https://tabler.io/docs

## Environment

Copy `.env.example` to `.env.local` and adjust values:

```bash
cp .env.example .env.local
```

Key variable: `VITE_API_BASE_URL` — defaults to `http://localhost:9080`.

## Project Structure

See [docs/PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md).

## Implementation Plan

See [docs/IMPLEMENTATION_PLAN.md](docs/IMPLEMENTATION_PLAN.md) for phased delivery.

## Docker

```bash
# Build and run with Docker Compose
docker compose up -d
```

See [docs/DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md) for full Docker instructions.
