# Task Tracker Architecture

## What the app does

Task Tracker is a learning project providing a FastAPI REST API for task CRUD operations and a static vanilla-JavaScript Kanban board. Tasks can be created, listed, updated, moved through defined statuses, and deleted; they also support optional due dates and task-scoped comments, and list queries support overdue filtering. Data is held only in memory, so it is lost when the API process restarts.

## Data model

The central entity is a task: `id`, `title`, `description`, `status`, `priority`, `assignee`, `due_date`, `created_at`, and `updated_at`. Status is one of `ToDo`, `InProgress`, or `Done`; priority is `Low`, `Medium`, or `High`. New tasks default to `ToDo` and `Medium`. A task comment entity is also exposed via comment routes (`id`, `task_id`, `text`, `created_at`).

## Request flow: create a task

The frontend collects and trims form values, checks that the title is non-empty, then sends `POST /tasks` to the API. FastAPI/Pydantic validates the create payload; the storage layer generates a UUID and UTC timestamps, stores the response-shaped task in its in-memory dictionary, and returns it with HTTP 201. The frontend closes the modal and reloads the task list to redraw the board.

## Key files

- [app/main.py](D:/Cursor_Projects/task-tracker/app/main.py) — FastAPI app, CORS middleware, `/health`, `/tasks`, and comments route handlers.
- [app/models.py](D:/Cursor_Projects/task-tracker/app/models.py) — task/comment schemas, status/priority enums, defaults, and validation.
- [app/storage.py](D:/Cursor_Projects/task-tracker/app/storage.py) — in-memory task/comment stores, UUID creation, timestamps, CRUD, and overdue filtering.
- [app/business_rules.py](D:/Cursor_Projects/task-tracker/app/business_rules.py) — permitted status-transition rule enforcement.
- [frontend/index.html](D:/Cursor_Projects/task-tracker/frontend/index.html) — static Kanban UI, browser state, rendering, and API requests.
- [tests/test_tasks.py](D:/Cursor_Projects/task-tracker/tests/test_tasks.py) — API behavior tests.
- [tests/conftest.py](D:/Cursor_Projects/task-tracker/tests/conftest.py) — shared pytest fixtures.
- [AGENTS.md](D:/Cursor_Projects/task-tracker/AGENTS.md) — project constraints, architecture summary, and visible business rules.

## Conventions

Pydantic rejects unknown create/update fields; titles are trimmed, required, non-empty, and limited to 200 characters. Comments require trimmed non-blank text with max length 1000. `PATCH` is partial; explicit `null` is rejected for non-nullable task fields but permitted for `assignee` and `due_date`. Status changes must follow `ToDo → InProgress → Done`, with `Done → InProgress` also allowed; invalid or same-status changes return HTTP 422. Missing task/comment IDs return HTTP 404. Overdue is computed on backend (`due_date < today UTC` and `status != Done`) and filterable via `GET /tasks?overdue=true|false`. The frontend calls `http://127.0.0.1:8000`, uses backend status values exactly, and supports due dates, overdue filter, and comment list/add/delete in the task modal.

## Not visible or assumptions

No database, authentication, or durable persistence is present. API deployment, production configuration, user identity/authorization, and any behavior beyond the inspected routes, models, storage, business rules, frontend, and named test files are **not confirmed**.
