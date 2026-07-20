# Task Tracker — Architecture (Strategy C)

## 1. What the app does

Task Tracker is a minimal FastAPI REST API for creating, listing, retrieving, partially updating, and deleting tasks. It also provides a `/health` endpoint; task data is held only in process memory.

## 2. Data model

The core entity is a **Task**: `id` (UUID string), `title`, `description`, `status`, `priority`, `assignee`, `created_at`, and `updated_at`.

`status` is one of `ToDo`, `InProgress`, or `Done`; `priority` is `Low`, `Medium`, or `High`. New tasks default to `ToDo` and `Medium`. Titles are trimmed, required, non-blank, and limited to 200 characters after trimming. `assignee` is nullable.

## 3. Request flow

When a client sends `POST /tasks`, FastAPI validates the request against `TaskCreate`. Valid requests reach `create_task`, which delegates to `storage.add_task`. Storage generates a UUID, sets both timestamps to the current UTC time, builds a `TaskResponse`, stores it in the module-level dictionary, and returns it as HTTP 201. Invalid payload shape or field values result in HTTP 422.

## 4. Key files

- `app/main.py` — FastAPI app setup, CORS, health route, and task CRUD routes.
- `app/models.py` — task enums and Pydantic create, update, and response schemas.
- `app/storage.py` — in-memory task dictionary, UUID generation, timestamps, and CRUD storage operations.
- `app/business_rules.py` — imported by `app/main.py` for status-transition validation; its contents are not visible from the files I read.
- `.env` — optionally loaded by `app/main.py`; its contents and operational use are not visible from the files I read.

## 5. Conventions

- **Validation:** Pydantic models forbid unknown fields. Updates apply only explicitly supplied fields; explicit `null` is rejected for title, description, status, and priority, while `assignee` may be null.
- **Storage:** Tasks are stored in a module-level `dict` keyed by ID, with no persistence beyond the running process.
- **Error handling:** Missing tasks produce HTTP 404. Invalid request values produce HTTP 422. Status updates are checked through an imported transition validator.
- **Frontend/backend interaction:** CORS permits all origins, methods, and headers. The actual frontend implementation is not visible from the files I read.

## 6. Not visible or assumptions

- Status-transition rules are not visible from the files I read.
- The frontend files, UI behavior, and exact API calls are not visible from the files I read.
- Test coverage, deployment configuration, dependency versions, and the server launch command are not visible from the files I read.
- Concurrent-request behavior and any production persistence strategy are not visible from the files I read.
