# Task Tracker

## Project summary
Task Tracker is a learning project with a FastAPI REST API and a static vanilla-JavaScript Kanban frontend.

The API provides `/health`, CRUD endpoints under `/tasks`, and task comment endpoints under `/tasks/{task_id}/comments`. Tasks and comments are held in in-memory dictionaries, so data is lost when the server restarts. The project intentionally has no database or authentication.

## Tech stack
- Python 3.11
- FastAPI 0.111.0
- Pydantic 2.7.4
- Uvicorn 0.30.1
- pytest 8.2.2 and httpx 0.27.0
- Vanilla JavaScript frontend in `frontend/index.html`

## Supported commands
Run these from the repository root:

```bash
python -m venv venv
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
pytest -v
python tests/verify_a.py
```

The static frontend calls the API at `http://127.0.0.1:8000`; open `frontend/index.html` directly in a browser while the API is running.

## Architecture
- `app/main.py`: FastAPI application, CORS configuration, health endpoint, task routes, and comments routes.
- `app/models.py`: Pydantic task/comment request/response models, enums, and field validation.
- `app/storage.py`: in-memory task/comment storage, overdue filtering, UUID generation, and timestamps.
- `app/business_rules.py`: allowed task-status transitions.
- `tests/`: pytest API tests and shared fixtures.
- `frontend/index.html`: static Kanban UI.

## Visible business rules
- Status values: `ToDo`, `InProgress`, `Done`.
- Priority values: `Low`, `Medium`, `High`.
- Default task status is `ToDo`; default priority is `Medium`.
- A task title is required, trimmed, non-empty, and at most 200 characters after trimming.
- A task `due_date` is optional (`YYYY-MM-DD`) and can be cleared with `null`.
- Overdue is defined as `due_date < today UTC` and `status != Done`.
- `GET /tasks` accepts optional `overdue=true|false`.
- Create and update payloads reject unknown fields.
- `PATCH` accepts partial updates. Explicit `null` is rejected for `title`, `description`, `status`, and `priority`; `assignee` and `due_date` may be `null`.
- Comment `text` is required, trimmed, non-blank, and at most 1000 characters.
- Missing task/comment resources return HTTP 404 on comments endpoints.
- Allowed status transitions are:
  - `ToDo` -> `InProgress`
  - `InProgress` -> `Done`
  - `Done` -> `InProgress`
- Invalid or same-status transitions return HTTP 422.
- The frontend must retain loading, empty, error, and populated states, and must use the backend status values exactly.

## Module 5 guardrails
- This module is for grading and governing AI-assisted work, not building features.
- Prefer read-only analysis first.
- Use one bounded task per thread.
- Edit `docs/` only by default.
- Do not modify `app/` unless the user explicitly approves one specific minimal fix.
- Do not modify `frontend/` unless the user explicitly approves one specific minimal fix.
- Before claiming anything about the repository, inspect the relevant files and cite them.
- If a file, command, behavior, or rule is not visible, label it **not confirmed** rather than guessing.
- If unexpected unrequested changes appear in `app/` or `frontend/` while working, stop and ask the user how to proceed before continuing.

## Security and governance
- Do not paste, log, commit, or expose secrets, tokens, credentials, or `.env` contents.
- Do not run destructive commands or overwrite/remove files without explicit confirmation.
- Do not add authentication, a database, or change public API response shapes without explicit approval.
- Do not remove or weaken tests to make checks pass.
- Do not use broad "always allow" shell permissions.
- Preserve existing user changes; inspect the working tree before editing.
