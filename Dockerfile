# ───────────────────────────────────────────────
# Base: Python 3.11 + uv preinstalled
# ───────────────────────────────────────────────
FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim AS base

ENV PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Copy dependency manifests
COPY pyproject.toml uv.lock ./

# Install deps with uv (fast, cached, deterministic)
RUN uv pip install --system --no-cache --quiet --frozen -r uv.lock

# Copy project code
COPY . .

# Launch FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
