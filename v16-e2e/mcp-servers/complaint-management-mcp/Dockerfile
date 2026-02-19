# ============================================================
# Complaint Management MCP Server — Optimised Dockerfile
#
# Optimisation techniques applied:
#   1. Multi-stage build — compiler toolchain stays in the
#      builder stage, never ships to the runtime image.
#   2. Wheel cache — all dependencies are built to .whl files
#      in the builder and installed from local cache in the
#      runtime stage (no network access required at runtime).
#   3. Layer-cache ordering — requirements.txt is copied and
#      installed before application source so that a code-only
#      change never invalidates the expensive pip layer.
#   4. Non-root user — the process runs as an unprivileged
#      'appuser' (UID 1001) to reduce the container attack
#      surface.
#   5. .dockerignore — tests, docs, .env, caches, and the venv
#      are excluded from the build context, keeping builds fast.
#   6. --no-cache-dir / --no-index — pip never writes to its own
#      HTTP cache inside the image layers.
# ============================================================


# ============================================================
# Stage 1 — builder
# Purpose : compile C extensions and build Python wheels.
#           gcc lives here and never reaches the runtime image.
# ============================================================
FROM python:3.12-slim AS builder

# Install build dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build

# Upgrade pip once (cached as its own layer)
RUN pip install --no-cache-dir --upgrade pip

# Build all dependency wheels into /wheels
COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt


# ============================================================
# Stage 2 — runtime
# Purpose : lean production image.
#           Only the pre-built wheels and the app source land here.
# ============================================================
FROM python:3.12-slim AS runtime

# Python runtime knobs — set before any pip / python invocation
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONFAULTHANDLER=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# ---- Non-root user ----
RUN groupadd --gid 1001 appgroup \
    && useradd --uid 1001 --gid appgroup --no-create-home --shell /bin/false appuser

WORKDIR /app

# Install from local wheels — zero network traffic, no gcc needed
COPY --from=builder /wheels /wheels
COPY requirements.txt .
RUN pip install --no-index --find-links=/wheels -r requirements.txt \
    # Remove the wheel cache from this layer — saves ~30 MB
    && rm -rf /wheels

# ---- Application source ----
# requirements first (already installed above), source last so
# code edits only invalidate this single cheap layer.
COPY server.py .
COPY src/ src/

# ---- Persistent volume mount points ----
# These directories are owned by appuser so the process can write
# to them even without root privileges.
RUN mkdir -p db logs \
    && chown -R appuser:appgroup /app

USER appuser

EXPOSE 8000

CMD ["python", "server.py"]
