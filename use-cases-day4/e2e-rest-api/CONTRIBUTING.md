# Contributing

Thank you for your interest in contributing to the Enterprise E2E Use Case project.

## Getting Started

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Install dependencies: `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and configure your environment

## Code Style

- **Python 3.13+** — use modern syntax (type hints, `match` statements where appropriate)
- **Formatting** — follow PEP 8; use `ruff` or `black` for auto-formatting
- **Imports** — group into standard library, third-party, and local; sort alphabetically
- **Naming** — `snake_case` for functions/variables, `PascalCase` for classes, `UPPER_CASE` for constants

## Project Structure

- `main.py` — Minimal entry point (do not add business logic here)
- `app/factory.py` — FastAPI app creation
- `app/agent/` — Agent construction and management
- `app/api/` — Routes, models, error handling
- `app/middleware/` — Both HTTP-level and agent-level middleware
- `app/history/` — Conversation history persistence
- `app/config/` — Settings and configuration
- `app/startup/` — Banner and startup utilities

## Making Changes

1. Keep changes focused — one feature or fix per PR
2. Update `CHANGELOG.md` with your changes under `[Unreleased]`
3. Add or update docstrings for public functions and classes
4. Test your changes manually:
   - Start the MCP server: `cd ../mcp && python main.py`
   - Start the API: `python main.py`
   - Verify endpoints via Swagger UI (`/docs`) or `curl`

## Pull Request Process

1. Ensure the server starts without errors
2. Test both `/chat` and `/chat/stream` endpoints
3. Verify health endpoints respond correctly
4. Update documentation if adding new features or environment variables
5. Write a clear PR description explaining the what and why

## Reporting Issues

Please include:
- Steps to reproduce the issue
- Expected vs actual behavior
- Environment details (OS, Python version, Docker version if applicable)
- Relevant log output
