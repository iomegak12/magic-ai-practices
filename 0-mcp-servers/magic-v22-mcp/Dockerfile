# syntax=docker/dockerfile:1

# ── Stage 1: builder ──────────────────────────────────────────────────────────
FROM python:3.12-slim AS builder

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy project definition first for layer caching
COPY pyproject.toml ./
COPY src/ ./src/

# Sync production deps only into the project venv
RUN uv sync --no-dev --frozen 2>/dev/null || uv sync --no-dev


# ── Stage 2: runtime ─────────────────────────────────────────────────────────
FROM python:3.12-slim AS runtime

WORKDIR /app

# Non-root user for security
RUN addgroup --system mcp && adduser --system --ingroup mcp mcp

# Copy venv and source from builder
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/src /app/src

# Ensure the data directory exists and is owned by the non-root user
RUN mkdir -p /app/data && chown mcp:mcp /app/data

USER mcp

# Put the venv on PATH
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH="/app/src" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

EXPOSE 9898

CMD ["python", "-m", "magic_v22_mcp"]
