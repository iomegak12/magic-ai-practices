# Contributing Guide

Thank you for considering contributing to the Orders & Complaints MCP Server!

## Development Setup

### Prerequisites
- Python 3.12+
- pip or uv

### Local Setup

```bash
# Clone the repo and navigate to the project
cd use-cases-day4/mcp

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Copy environment config
cp .env.example .env

# Run the server
python main.py
```

## Code Style

- Follow **PEP 8** conventions
- Use **type annotations** for all function signatures
- Use **modern SQLAlchemy** patterns (`Mapped[T]`, `mapped_column()`)
- Keep `main.py` minimal — all logic in modular packages
- Use structured response format for all tools:
  ```python
  {
      "operation": "tool_name",
      "success": True/False,
      "message": "...",    # on success
      "error": "...",      # on failure
      "result": ...,       # data payload
      "count": N           # for list results
  }
  ```

## Project Structure Rules

| Directory | Purpose |
|-----------|---------|
| `config/` | Environment loading and validation enums |
| `models/` | SQLAlchemy ORM models only |
| `database/` | Connection management and seed data |
| `tools/` | MCP tool implementations (business logic) |
| `resources/` | MCP resource implementations (read-only data) |
| `prompts/` | MCP prompt templates |
| `middleware/` | ASGI middleware (rate limiting, etc.) |

## Adding a New Tool

1. Implement the function in `tools/order_tools.py` or `tools/complaint_tools.py`
2. Register it with `@mcp.tool` in `tools/__init__.py`
3. Update `main.py` banner (`tools_list`) to include the new tool
4. Add tests and update `CHANGELOG.md`

## Adding a New Resource

1. Implement the query function in `resources/definitions.py`
2. Register it with `@mcp.resource` in `resources/__init__.py`
3. Update `main.py` banner (`resources_list`)
4. Update `CHANGELOG.md`

## Pull Request Guidelines

1. Create a feature branch: `git checkout -b feature/my-feature`
2. Keep commits focused and descriptive
3. Ensure the server starts without errors: `python main.py`
4. Update documentation if adding/changing features
5. Submit a PR with a clear description of changes
