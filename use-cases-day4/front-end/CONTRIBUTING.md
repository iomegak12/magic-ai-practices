# Contributing

Thank you for your interest in contributing to the clonescript.ai frontend.

## Getting Started

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Install dependencies: `npm install`
4. Copy `.env.example` to `.env.local` and configure

## Code Style

- **JavaScript (ES2022+)** — no TypeScript in v1
- **React 18** — functional components only, hooks for all state/effects
- **Tailwind CSS v3** — utility-first, no inline styles except for dynamic values
- **Naming** — `PascalCase` for components, `camelCase` for hooks/utils, `UPPER_CASE` for constants
- **Imports** — group into React, third-party, local; sort alphabetically within groups

## Component Conventions

- One component per file
- Co-locate component-specific styles in the same file using Tailwind utilities
- Use the `glass-panel` and `glass-card` CSS classes for glassmorphism effects
- Never call `fetch` directly — use the `src/api/` layer
- Consume global state via `useChatContext()` or the `useChat()` convenience hook

## Making Changes

1. Keep changes focused — one feature or fix per PR
2. Update `CHANGELOG.md` with your changes under `[Unreleased]`
3. Test manually:
   - Start the REST API: `cd ../e2e-rest-api && python main.py`
   - Start the MCP server: `cd ../mcp && python main.py`
   - Start the frontend: `npm run dev`
   - Verify both streaming and non-streaming modes work

## Pull Request Process

1. Ensure `npm run build` succeeds without errors
2. Test on desktop (1024px+) and mobile (<768px) viewports
3. Verify no console errors in the browser
4. Write a clear PR description explaining the what and why

## Reporting Issues

Please include:
- Steps to reproduce
- Expected vs actual behaviour
- Browser and OS
- Console error output (if any)
