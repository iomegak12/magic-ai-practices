# ============================================================
# Stage 1: Builder — install dependencies into a virtual env
# ============================================================
FROM python:3.12-slim AS builder

WORKDIR /build

COPY requirements.txt .

RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir --upgrade pip && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt


# ============================================================
# Stage 2: Runtime — lightweight production image
# ============================================================
FROM python:3.12-slim AS runtime

# Create non-root user
RUN groupadd --gid 1000 appuser && \
    useradd --uid 1000 --gid appuser --create-home appuser

WORKDIR /app

# Copy virtual env from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy application code
COPY . .

# Ensure DB directory exists and is writable
RUN mkdir -p /app/db && chown -R appuser:appuser /app

USER appuser

EXPOSE 8700

CMD ["python", "main.py"]
