# ── Stage 1: build (installs deps) ──────────────────────────────────────────
FROM python:3.11-slim AS builder

WORKDIR /build
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --prefix=/install -r requirements.txt

# ── Stage 2: lean runtime image (no build tools) ────────────────────────────
FROM python:3.11-slim AS runtime

WORKDIR /app

# Copy installed packages from builder stage
COPY --from=builder /install /usr/local

# Copy application source
COPY app/ .

EXPOSE 8000

# Start the API server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
