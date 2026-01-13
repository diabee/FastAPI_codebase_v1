# =============================================================================
# Stage 1: Builder - Install dependencies
# =============================================================================
FROM python:3.14-slim-bookworm AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install poetry
ENV POETRY_VERSION=1.7.1 \
    POETRY_HOME=/opt/poetry \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

RUN pip install --no-cache-dir poetry==${POETRY_VERSION}

WORKDIR /app

# Copy only dependency files first (better layer caching)
COPY pyproject.toml poetry.lock ./
RUN touch README.md

# Install production dependencies only
RUN --mount=type=cache,target=${POETRY_CACHE_DIR} \
    poetry install --only=main --no-root

# =============================================================================
# Stage 2: Runtime - Minimal production image
# =============================================================================
FROM python:3.14-slim-bookworm AS runtime

# Security: Set up non-root user with minimal permissions
RUN groupadd --gid 1000 appgroup && \
    useradd --uid 1000 --gid appgroup --shell /usr/sbin/nologin --create-home appuser

# Environment configuration
ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder --chown=appuser:appgroup ${VIRTUAL_ENV} ${VIRTUAL_ENV}

# Copy application code (copy app contents to /app)
COPY --chown=appuser:appgroup app/ ./app/
COPY --chown=appuser:appgroup config ./config

# Create log directory with proper permissions
RUN mkdir -p /tmp/log && chown -R appuser:appgroup /tmp/log

# Security: Switch to non-root user
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/docs')" || exit 1

# Expose port (documentation purpose)
EXPOSE 8080

# Run with uvicorn directly for better signal handling
ENTRYPOINT ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
