# Task Tracker Architecture

## What the app does

Task Tracker is a learning project providing a FastAPI REST API for task CRUD operations and a static vanilla-JavaScript Kanban board. Tasks can be created, listed, updated, moved through defined statuses, and deleted; data is held only in memory, so it is lost when the API process restarts.

## Data model

The central entity is a task: `id`, `title`, `description`, `status`, `priority`, `assignee`, `created_at`, and `updated_at`. Status is one of `ToDo`, `InProgress`, or `Done`; priority is `Low`, `Medium`, or `High`. New tasks default to `ToDo` and `Medium`.

## Request flow: create a task

The frontend collects and trims form values, checks that the title is non-empty, then sends `POST /tasks` to the API. FastAPI/Pydantic validates the create payload; the storage layer generates a UUID and UTC timestamps, stores the response-shaped task in its in-memory dictionary, and returns it with HTTP 201. The frontend closes the modal and reloads the task list to redraw the board.

## Key files

- [app/main.py](D:/Cursor_Projects/task-tracker/app/main.py) — FastAPI app, CORS middleware, `/health`, and `/tasks` route handlers.
- [app/models.py](D:/Cursor_Projects/task-tracker/app/models.py) — task schemas, status/priority enums, defaults, and field validation.
- [app/storage.py](D:/Cursor_Projects/task-tracker/app/storage.py) — in-memory dictionary, UUID creation, timestamps, and CRUD storage operations.
- [app/business_rules.py](D:/Cursor_Projects/task-tracker/app/business_rules.py) — permitted status-transition rule enforcement.
- [frontend/index.html](D:/Cursor_Projects/task-tracker/frontend/index.html) — static Kanban UI, browser state, rendering, and API requests.
- [tests/test_tasks.py](D:/Cursor_Projects/task-tracker/tests/test_tasks.py) — API behavior tests.
- [tests/conftest.py](D:/Cursor_Projects/task-tracker/tests/conftest.py) — shared pytest fixtures.
- [AGENTS.md](D:/Cursor_Projects/task-tracker/AGENTS.md) — project constraints, architecture summary, and visible business rules.

## Conventions

Pydantic rejects unknown create/update fields; titles are trimmed, required, non-empty, and limited to 200 characters. `PATCH` is partial; explicit `null` is rejected for non-nullable task fields but permitted for `assignee`. Status changes must follow `ToDo → InProgress → Done`, with `Done → InProgress` also allowed; invalid or same-status changes return HTTP 422. Missing task IDs return HTTP 404. The frontend calls `http://127.0.0.1:8000`, uses the backend status values exactly, and maintains loading, empty, error, and populated UI states.

## Not visible or assumptions

No database, authentication, or durable persistence is present. API deployment, production configuration, user identity/authorization, and any behavior beyond the inspected routes, models, storage, business rules, frontend, and named test files are **not confirmed**.
