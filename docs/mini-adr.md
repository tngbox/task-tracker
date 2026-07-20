# Mini ADR: Due Dates and Overdue Filter

## Context
We added two features to a minimal FastAPI + static HTML app:
- Optional task due dates
- Overdue detection and filtering

Constraints:
- Keep ADR-001 style simplicity (in-memory, no DB, no auth)
- Keep route handlers thin
- Avoid introducing heavy time-zone logic

## Decision
1. Add `due_date` as optional date-only field on create/update/response models.
2. Define overdue in backend as:
   - due_date exists
   - due_date < today (UTC)
   - status != Done
3. Add optional query filter on `GET /tasks`:
   - `overdue=true` for only overdue tasks
   - `overdue=false` for non-overdue tasks
4. Keep frontend logic lightweight:
   - modal field for due date
   - overdue filter dropdown that calls backend
   - overdue pill rendering for visual cue

## Alternatives AI suggested
- Alternative 1: datetime with timezone (`due_at`) and local timezone conversion in UI.
- Alternative 2: frontend-only overdue filtering without backend query parameter.
- Alternative 3: introduce advanced filter combinations and saved filter state.

## Rejected as too complex/out of scope
- Rejected datetime+timezone handling (too complex for current scope).
- Rejected frontend-only source of truth for overdue (would duplicate business logic and create drift risk).
- Rejected persistence-level indexing/optimization (no DB in this project).

## Consequences
- Behavior is deterministic and easy to test.
- API remains backward compatible (field is optional).
- Frontend stays simple while relying on backend as source of truth for filtering.

---

# Mini ADR: Feature C Task Comments

## Context
We added task comments to the same minimal FastAPI + static HTML app.

Constraints:
- Keep ADR-001 simplicity (in-memory only, no DB, no auth).
- Preserve thin routes and layered responsibilities.
- Keep frontend in one static file without framework migration.

## Decision
1. Add task-scoped comments API:
   - `GET /tasks/{task_id}/comments`
   - `POST /tasks/{task_id}/comments`
   - `DELETE /tasks/{task_id}/comments/{comment_id}`
2. Validate comment text in model layer:
   - required, trimmed, non-blank
   - max length 1000 characters
3. Implement in-memory comment store keyed by task id; cascade-delete comments when task is deleted.
4. Add comments UI in Edit Task modal with list/add/delete behavior and task-not-saved hint in create mode.
5. Constrain modal height and add internal scrolling so comment actions remain reachable on smaller screens.

## Alternatives AI suggested
- Alternative 1: flatten comments into task payload (`comments: []`) and update through task PATCH.
- Alternative 2: add card-level comment counts immediately for all tasks.
- Alternative 3: use optimistic UI with rollback for comment add/delete.

## Rejected as too complex/out of scope
- Rejected nested task PATCH comments flow (larger update contract and conflict risk).
- Rejected immediate card counts (extra calls per card or extra API field design change not required for MVP).
- Rejected optimistic rollback flow (more client state complexity than needed for current scope).

## Consequences
- Comment behavior is explicit, testable, and separated from task CRUD concerns.
- 404 handling is consistent across task and comment endpoints.
- Modal remains usable for long content due to internal scroll behavior.
