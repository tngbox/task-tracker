# syntax=docker/dockerfile:1

# ---------- Builder stage ----------
FROM python:3.11-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Isolated virtualenv we can hand off to the runtime stage
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# ---------- Runtime stage ----------
FROM python:3.11-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

# Non-root user
RUN useradd --create-home --uid 1000 app

WORKDIR /app

# Prebuilt dependencies from the builder stage
COPY --from=builder /opt/venv /opt/venv

# Only the runtime application code
COPY app/ ./app/

EXPOSE 8000

USER app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
