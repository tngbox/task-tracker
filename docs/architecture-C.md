# Task Tracker — Architecture (Strategy C)

## 1. What the app does

Task Tracker is a minimal FastAPI REST API for creating, listing, retrieving, partially updating, and deleting tasks. It also provides task-comment endpoints and a `/health` endpoint; task data is held only in process memory.

## 2. Data model

The core entity is a **Task**: `id` (UUID string), `title`, `description`, `status`, `priority`, `assignee`, `due_date`, `created_at`, and `updated_at`.

`status` is one of `ToDo`, `InProgress`, or `Done`; `priority` is `Low`, `Medium`, or `High`. New tasks default to `ToDo` and `Medium`. Titles are trimmed, required, non-blank, and limited to 200 characters after trimming. `assignee` and `due_date` are nullable.

The app also exposes a **TaskComment** resource (`id`, `task_id`, `text`, `created_at`) under `/tasks/{task_id}/comments`.

## 3. Request flow

When a client sends `POST /tasks`, FastAPI validates the request against `TaskCreate`. Valid requests reach `create_task`, which delegates to `storage.add_task`. Storage generates a UUID, sets both timestamps to the current UTC time, builds a `TaskResponse`, stores it in the module-level dictionary, and returns it as HTTP 201. Invalid payload shape or field values result in HTTP 422.

`GET /tasks` can filter by `status`, `priority`, and `overdue`; overdue is computed in backend storage as `due_date < today UTC` and `status != Done`.

## 4. Key files

- `app/main.py` — FastAPI app setup, CORS, health route, task CRUD routes, and comment routes.
- `app/models.py` — task/comment enums and Pydantic create, update, and response schemas.
- `app/storage.py` — in-memory task/comment dictionaries, UUID generation, timestamps, CRUD operations, and overdue filtering.
- `app/business_rules.py` — status-transition validation.
- `.env` — optionally loaded by `app/main.py`; its contents and operational use are not visible from the files I read.

## 5. Conventions

- **Validation:** Pydantic models forbid unknown fields. Updates apply only explicitly supplied fields; explicit `null` is rejected for title, description, status, and priority, while `assignee` and `due_date` may be null. Comments require non-blank text.
- **Storage:** Tasks and comments are stored in module-level `dict` structures, with no persistence beyond the running process.
- **Error handling:** Missing tasks/comments produce HTTP 404. Invalid request values produce HTTP 422. Status updates are checked through transition validation.
- **Frontend/backend interaction:** CORS permits all origins, methods, and headers. The frontend calls backend routes for task CRUD, overdue filters, and comment list/add/delete.

## 6. Not visible or assumptions

- Deployment, production hosting, observability, rate limiting, and concurrent-write behavior are **not confirmed**.
- Any persistence strategy beyond in-memory storage is **not confirmed**.
