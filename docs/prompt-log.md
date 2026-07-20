# Prompt Log

## Feature A: Due Dates

### Prompt A1
Prompt:
"Act as senior frontend and backend developer, read project files and plan due dates + overdue filter."

AI returned:
- Backend-first plan with model/storage/route/test sequence.
- Suggested date-only field and optional overdue query.

Decision:
- Accepted sequencing and date-only recommendation.
- Edited scope to fit current branch docs/files only.

### Prompt A2
Prompt:
"start implementation"

AI returned:
- Implemented `due_date` in models, storage, routes.
- Added tests for valid/invalid date and due date update.

Decision:
- Accepted core implementation and tests.
- Edited README after implementation to include API examples.

### Prompt A3 (weak -> stronger)
Weak prompt:
"add due date"

Why weak:
- No format, validation, API behavior, or UI requirements.

Stronger prompt:
"Add optional `due_date` in `YYYY-MM-DD` to create/update/response; reject invalid formats with 422; update tests for create valid/invalid and update flow; keep backward compatibility."

AI returned:
- Clean implementation aligned with contract.

Decision:
- Accepted with minor adjustments to docs language.

## Feature B: Overdue Filter

### Prompt B1
Prompt:
"Expected backend work: decide if overdue is backend or UI, optional query filter for overdue."

AI returned:
- Recommended backend canonical logic + optional frontend visual helper.

Decision:
- Accepted because it centralizes rules and supports API filtering.

### Prompt B2
Prompt:
"Expected frontend work: overdue filter or visual indicator on cards."

AI returned:
- Added filter dropdown (`All`, `Overdue only`, `Not overdue`) and overdue pill.

Decision:
- Accepted UI behavior.
- Edited to use backend query params for filtering rather than local-only filtering.

### Prompt B3
Prompt:
"update README API usage examples"

AI returned:
- Added due_date create/update examples and overdue filter examples.

Decision:
- Accepted and then extended with short frontend usage section.

## Feature C: Task Comments

### Prompt C1
Prompt:
"Act as senior frontend and backend developer, read the project files and plan feature C comments: backend list/add/delete with non-blank validation and 404 handling, then frontend comments section."

AI returned:
- Backend-first plan: models -> storage -> routes -> tests -> frontend.
- Proposed task-scoped comments endpoints and in-memory store keyed by task id.

Decision:
- Accepted backend-first sequencing and task-scoped endpoint design.
- Edited to keep initial frontend scope in edit modal only.

### Prompt C2
Prompt:
"start implementation"

AI returned:
- Implemented comment models, storage ops, and API endpoints.
- Added tests for add/list/delete, blank 422, and missing task/comment 404.
- Added edit modal comments UI for list/add/delete.

Decision:
- Accepted implementation and tests.
- Edited CSS after review to make modal body scrollable so comment controls remain visible.

### Prompt C3 (weak -> stronger)
Weak prompt:
"add comments"

Why weak:
- Missing endpoint contract, validation rules, error handling, and UI location.

Stronger prompt:
"Add task comments as a separate resource with GET/POST/DELETE under /tasks/{task_id}/comments; enforce trimmed non-blank text and 404 for missing task/comment; add integration tests for add/list/delete and errors; add comments section in edit modal with add and delete actions."

AI returned:
- Complete implementation aligned with backend contract and UI scope.

Decision:
- Accepted with one scope correction: deferred card comment count to avoid extra API churn in this iteration.
