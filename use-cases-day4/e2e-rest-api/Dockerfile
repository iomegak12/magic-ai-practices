# ── Stage 1: Builder ──────────────────────────────────────
FROM python:3.13-alpine AS builder

WORKDIR /build

# Install build dependencies for native extensions
RUN apk add --no-cache gcc g++ musl-dev libffi-dev

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ── Stage 2: Runtime ─────────────────────────────────────
FROM python:3.13-alpine AS runtime

LABEL maintainer="Enterprise E2E Team"
LABEL description="Enterprise E2E Use Case — MAF Agent REST API"

# Non-root user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy application source
COPY . .

# Create data directory for SQLite
RUN mkdir -p /app/data && chown -R appuser:appgroup /app

USER appuser

EXPOSE 8800

CMD ["python", "main.py"]
