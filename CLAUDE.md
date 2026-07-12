# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

Setup (from repo root):

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Run the API server (reload on change):

```bash
uvicorn app.main:app --reload   # serves at http://localhost:8000
```

Interactive API docs are auto-generated at `http://localhost:8000/docs`.

Tests:

```bash
pytest                                  # full suite
pytest tests/test_tasks.py              # one file
pytest tests/test_tasks.py::test_create_task_valid_returns_201_with_full_body   # one test
pytest -k transition                    # by name substring
```

The frontend is a single static file — open `frontend/index.html` directly in a
browser (no build step). It calls the API at `http://127.0.0.1:8000`, so the
uvicorn server must be running first.

`create_test_tasks.py` seeds the running server with sample tasks over HTTP. It
depends on the `requests` package, which is **not** in `requirements.txt` (`pip
install requests` if you need it).

## Architecture

A minimal FastAPI + Pydantic v2 REST backend. Per ADR-001 (referenced
throughout the code) it deliberately has **no database, no authentication, and
no ORM** — all task state lives in memory and is lost on restart. This
constraint is intentional; don't introduce persistence or auth without
revisiting that decision.

The backend is layered so route handlers stay thin, and each layer owns one
concern:

- **`app/models.py`** — Pydantic schemas and the `TaskStatus`/`TaskPriority`
  enums. Owns *field-shape* validation only. `TaskCreate`/`TaskUpdate`/
  `TaskResponse` all set `extra="forbid"`, so unknown fields return HTTP 422.
  Title rules (strip, non-blank, ≤200 chars) live in the shared `_validate_title`
  helper used by both create and update.
- **`app/storage.py`** — the in-memory store: a module-level `_tasks` dict keyed
  by UUID string. Owns id generation and `created_at`/`updated_at` bookkeeping.
  `_reset()` clears the store and exists for tests only.
- **`app/business_rules.py`** — domain rules kept separate from shape validation.
  Currently the status-transition graph in `VALID_TRANSITIONS`: allowed moves are
  ToDo→InProgress, InProgress→Done, Done→InProgress. Anything else (including
  same→same) raises HTTP 422.
- **`app/main.py`** — the FastAPI app, CORS middleware (currently wide open,
  `allow_origins=["*"]` for frontend dev), the `/health` endpoint, and the
  `/tasks` CRUD routes. Handlers delegate to storage and business_rules; they
  raise 404 when an id is missing and rely on Pydantic for 422s.

Request flow for a task write: FastAPI parses/validates the body against a
Pydantic model (422 on bad shape) → `main.py` runs business-rule checks like
`validate_status_transition` (422 on bad transition) → `storage.py` mutates the
dict and stamps timestamps → the `TaskResponse` is serialized back.

## Testing notes

Tests use FastAPI's `TestClient` against the real app through the real in-memory
storage (no mocking). An autouse fixture in `tests/conftest.py` calls
`storage._reset()` before and after every test for isolation, so tests can freely
create tasks. `tests/verify_a.py` is a standalone script (run with `python
tests/verify_a.py`), not a pytest module — it prints PASS/FAIL for model
validation rules.
