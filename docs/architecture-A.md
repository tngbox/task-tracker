# Task Tracker Architecture

## What the app does

Task Tracker is a learning-focused task-management app with a FastAPI REST API and a static vanilla-JavaScript Kanban board. Users can create, list, edit, move, and delete tasks, set optional due dates, filter by overdue state, and add comments to tasks; task data is held only in process memory, so it is lost when the API restarts.

## Data model

**Task** is the primary domain entity. Its fields are `id` (generated UUID), `title`, `description`, `status`, `priority`, `assignee`, `due_date`, `created_at`, and `updated_at`. Status values are `ToDo`, `InProgress`, and `Done`; priority values are `Low`, `Medium`, and `High`. New tasks default to `ToDo` and `Medium`.

**TaskComment** is a task-scoped entity with fields `id`, `task_id`, `text`, and `created_at`.

## Request flow: creating a task

1. The Kanban form collects task fields and sends `POST http://127.0.0.1:8000/tasks`.
2. FastAPI parses the body as `TaskCreate`; Pydantic validates its shape and fields.
3. The route calls the storage layer.
4. Storage creates a UUID and UTC timestamps, builds a response-model task, and saves it in the module-level dictionary.
5. The API returns the created task with HTTP 201; the frontend closes the modal and reloads the task list.

## Key files

- `app/main.py` — FastAPI app, CORS setup, health endpoint, task CRUD routes, and comments routes.
- `app/models.py` — Pydantic task/comment schemas, enums, defaults, and validation.
- `app/storage.py` — In-memory task/comment stores, UUID generation, filtering, and timestamps.
- `app/business_rules.py` — Permitted task-status transitions and 422 enforcement.
- `frontend/index.html` — Static Kanban UI, API calls, modal form, rendering, and drag/drop.
- `tests/test_tasks.py` — API CRUD, due-date/overdue, comments, validation, and transition tests.
- `tests/conftest.py` — Test client and automatic in-memory-store reset fixture.
- `requirements.txt` — Runtime and test dependencies.
- `Dockerfile` — Container build and Uvicorn runtime entry point.

## Conventions

- **Validation:** create and update payloads forbid unknown fields. Titles are trimmed, required, non-blank, and limited to 200 characters. Comment text is trimmed, required, non-blank, and limited to 1000 characters. `PATCH` supports partial updates; explicit `null` is rejected for title, description, status, and priority, while `assignee` and `due_date` may be null.
- **Storage:** routes stay thin and delegate persistence to `storage.py`. The module-level dictionary is not durable; IDs are UUIDs and timestamps are UTC.
- **Overdue logic:** a task is overdue when `due_date` is before current UTC date and `status` is not `Done`; `GET /tasks` supports `overdue=true|false`.
- **Business errors:** malformed payloads and invalid enum/query values receive FastAPI/Pydantic HTTP 422 responses. Missing tasks/comments return HTTP 404. Invalid and same-status transitions return HTTP 422.
- **Frontend/backend interaction:** the static frontend calls the API directly at `127.0.0.1:8000`, uses the backend status strings exactly, supports due date editing, overdue filtering, and comments list/add/delete in edit mode, and displays loading, error/retry, empty-column, and populated states.

## Not visible or assumptions

- No database persistence, authentication, or authorization is visible in the inspected application code.
- Deployment, production hosting, observability, rate limiting, and multi-process/concurrent-write behavior are **not confirmed**.
- The frontend is static and not served by the FastAPI routes visible in `app/main.py`.
