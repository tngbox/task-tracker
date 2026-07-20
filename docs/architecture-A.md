# Task Tracker Architecture

## What the app does

Task Tracker is a learning-focused task-management app with a FastAPI REST API and a static vanilla-JavaScript Kanban board. Users can create, list, edit, move, and delete tasks; task data is held only in process memory, so it is lost when the API restarts.

## Data model

**Task** is the only domain entity. Its fields are `id` (generated UUID), `title`, `description`, `status`, `priority`, `assignee`, `created_at`, and `updated_at`. Status values are `ToDo`, `InProgress`, and `Done`; priority values are `Low`, `Medium`, and `High`. New tasks default to `ToDo` and `Medium`.

## Request flow: creating a task

1. The Kanban form collects task fields and sends `POST http://127.0.0.1:8000/tasks`.
2. FastAPI parses the body as `TaskCreate`; Pydantic validates its shape and fields.
3. The route calls the storage layer.
4. Storage creates a UUID and UTC timestamps, builds a response-model task, and saves it in the module-level dictionary.
5. The API returns the created task with HTTP 201; the frontend closes the modal and reloads the task list.

## Key files

- `app/main.py` — FastAPI app, CORS setup, health endpoint, and task CRUD routes.
- `app/models.py` — Pydantic task schemas, enums, defaults, and field validation.
- `app/storage.py` — In-memory dictionary store, UUID generation, filtering, and timestamp updates.
- `app/business_rules.py` — Permitted task-status transitions and 422 enforcement.
- `frontend/index.html` — Static Kanban UI, API calls, modal form, rendering, and drag/drop.
- `tests/test_tasks.py` — API CRUD, validation, and transition behavior tests.
- `tests/conftest.py` — Test client and automatic in-memory-store reset fixture.
- `requirements.txt` — Runtime and test dependencies.
- `Dockerfile` — Container build and Uvicorn runtime entry point.

## Conventions

- **Validation:** create and update payloads forbid unknown fields. Titles are trimmed, required, non-blank, and limited to 200 characters. `PATCH` supports partial updates; explicit `null` is rejected for title, description, status, and priority, while `assignee` may be null.
- **Storage:** routes stay thin and delegate persistence to `storage.py`. The module-level dictionary is not durable; IDs are UUIDs and timestamps are UTC.
- **Business errors:** malformed payloads and invalid enum/query values receive FastAPI/Pydantic HTTP 422 responses. Missing tasks return HTTP 404. Invalid and same-status transitions return HTTP 422.
- **Frontend/backend interaction:** the static frontend calls the API directly at `127.0.0.1:8000`, uses the backend status strings exactly, and displays loading, error/retry, empty-column, and populated states. Drag/drop performs an optimistic status update and restores the prior UI state if the request fails.

## Not visible or assumptions

- No database persistence, authentication, or authorization is visible in the inspected application code.
- Deployment, production hosting, observability, rate limiting, and multi-process/concurrent-write behavior are **not confirmed**.
- The frontend is static and not served by the FastAPI routes visible in `app/main.py`.
