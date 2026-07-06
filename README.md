# Task Tracker API

A minimal FastAPI + Pydantic REST backend for tracking tasks, built as a solo-developer learning project. Per ADR-001, it deliberately avoids databases, authentication, and microservices in favor of the simplest possible setup.

## Setup

Create and activate a virtual environment, then install dependencies:

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Running the server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.

## Testing the health endpoint

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{"status": "ok", "timestamp": "2026-07-03T12:00:00.000000+00:00"}
```
