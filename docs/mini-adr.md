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
