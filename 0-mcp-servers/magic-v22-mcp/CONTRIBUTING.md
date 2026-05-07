# Contributing

Thank you for considering contributing to **MAGIC-v22-MCP**!

## Branch Workflow

```
main          — stable, tagged releases
dev           — integration branch (open PRs here)
feature/<name>— feature branches off dev
fix/<name>    — bug-fix branches off dev
```

1. Fork the repo and create your branch from `dev`.
2. Make your changes with focused commits.
3. Ensure all checks pass (see below).
4. Open a Pull Request targeting `dev`.

## Local Development with uv

```bash
# Install all deps including dev extras
uv sync --all-extras

# Run the server locally
uv run magic-v22-mcp

# Run tests
uv run pytest tests/

# Type-check
uv run mypy src/

# Lint & format
uv run ruff check src/
uv run ruff format src/
```

## PR Checklist

- [ ] Code follows existing style (ruff / mypy pass)
- [ ] New tools/resources/prompts are covered by tests
- [ ] `CHANGELOG.md` entry added under `[Unreleased]`
- [ ] `.env.example` updated if new env vars added
- [ ] Docstrings added for public functions/classes
- [ ] No secrets or real data committed

## Commit Style

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add bulk order import tool
fix: handle ORD sequence reset on empty DB
docs: update TROUBLESHOOTING for port conflict
chore: bump fastmcp to 2.10.0
```

## Code of Conduct

Be respectful. Constructive feedback only.
