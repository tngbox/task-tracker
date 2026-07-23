# Feature A/B/C Delivery Plan (Updated)

## Status

This document supersedes the earlier draft comments plan. The backend behavior for:

- Feature A: optional `due_date`
- Feature B: backend overdue filtering
- Feature C: task comments

is now implemented, and this plan focuses on containerization and CI verification of that behavior.

## Implemented API contract to preserve

### Feature A - due date

- `POST /tasks` accepts optional `due_date` in `YYYY-MM-DD` format.
- `PATCH /tasks/{task_id}` supports setting `due_date` to a date or clearing it with `null`.
- `TaskResponse` includes `due_date`.

### Feature B - overdue filter

- `GET /tasks` supports `overdue=true|false`.
- Overdue is computed in backend storage as:
  - `due_date` exists
  - `due_date < today UTC`
  - `status != Done`

### Feature C - task comments

- `POST /tasks/{task_id}/comments` creates a comment with body shape `{ "text": "..." }`.
- `GET /tasks/{task_id}/comments` returns comment list for that task.
- `DELETE /tasks/{task_id}/comments/{comment_id}` deletes one comment.
- Missing task/comment resources return `404`.
- Blank comment text returns `422`.

## Dockerfile review and update

### Current encapsulation model

- Multi-stage build on `python:3.11-slim`.
- Runtime image copies only dependencies and `app/` source.
- Container runs as non-root user `app`.
- API is exposed on port `8000` with Uvicorn command:
  `uvicorn app.main:app --host 0.0.0.0 --port 8000`.

### Update applied

- Added a container `HEALTHCHECK` calling `GET /health` from inside the container.
- This gives runtime-level confirmation that the encapsulated backend process is alive.

## CI review and update

### Existing coverage

- Unit/integration API tests in `tests/test_tasks.py` already validate Feature A/B/C behavior.

### Update applied

Added a `docker-smoke` job in `.github/workflows/ci.yml` that:

1. Builds the Docker image.
2. Starts the backend container.
3. Waits for `/health` to be reachable.
4. Runs a smoke script against containerized API to verify:
   - Feature A: due date persists on create.
   - Feature B: overdue filter returns the overdue task.
   - Feature C: comment create and list work for the created task.
5. Prints container logs on failure and always stops/removes the container.

This ensures CI validates both:

- source-level backend behavior (pytest)
- packaged/runtime backend behavior (Docker)

## Acceptance checklist

- `pytest -v --tb=short` passes.
- Docker image builds successfully.
- Container health endpoint responds in CI.
- Smoke checks for A/B/C pass in container.

## Notes

- Data remains in-memory by design; container restarts reset tasks/comments.
- No auth/database changes are introduced by this update.
