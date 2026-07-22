# Prompt Log

## Feature A: Due Dates

### Prompt A1
Prompt:
"Act as senior frontend and backend developer, read existing project files, go through all .md files and plan due dates + overdue filter features as below:
1. Expected backend work: Add optional due_date validation. Support create/update. Decide whether overdue is computed in the backend or UI. Optional query filter for overdue.
2. Expected frontend work: Add due date to the modal. Show due date or overdue pill on cards. Add an overdue filter or visual indicator.
3. Good tests to include: Valid due date, invalid date format, overdue detection, update due date, filter returns only overdue tasks.
First plan for backend implementation, then move to frontend.
Don’t execute at this point just provide the plan for implementation for my approval.

Current project:
- Backend: Python/FastAPI Task Tracker API.
- Main task fields: id, title, description, status, priority, assignee.
- Status values are exactly: ToDo, InProgress, Done.
- Priority values are exactly: Low, Medium, High.
- The frontend will live in frontend/index.html using vanilla HTML, CSS, and JavaScript.

Workflow rules:
- Work in small steps.
- Do not rewrite the whole file unless I explicitly ask.
- Do not add frameworks, build tools, auth, accounts, real-time sync, or new backend features.
- Treat your answer as a draft. I will inspect, run, test, and refine it."


AI returned:
- Backend-first plan with model/storage/route/test sequence.
- Suggested date-only field and optional overdue query.

Decision:
- Accepted sequencing and date-only recommendation.
- Edited scope to fit current branch docs/files only.

### Prompt A2
Prompt:
"start implementation the implementation of the following plan [I pasted here the plan provided in prompt A1]"

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
"Expected backend work: propose two plans for overdue is on backend or UI, optional query filter for overdue."

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
"Act as senior frontend and backend developer, read existing project files, go through all .md files and plan task comments features as below:

1. Add comment model or task comment list.
2. Expected backend work: Support list/add/delete comment behavior with non-blank text validation and not-found handling.
3. Expected frontend work: Add a comments section in the edit modal or a small task detail area. Show comment count on cards if useful.
4. Good tests to include: Add comment, reject blank comment, list comments for a task, delete comment, 404 for missing task/comment.
Propose a plan for backend implementation then move to frontend, don’t execute wait for my approval
Current project:
- Backend: Python/FastAPI Task Tracker API.
- Main task fields: id, title, description, status, priority, assignee.
- Status values are exactly: ToDo, InProgress, Done.
- Priority values are exactly: Low, Medium, High.
- The frontend will live in frontend/index.html using vanilla HTML, CSS, and JavaScript.

Workflow rules:
- Work in small steps.
- Do not rewrite the whole file unless I explicitly ask.
- Do not add frameworks, build tools, auth, accounts, real-time sync, or new backend features.
- Treat your answer as a draft. I will inspect, run, test, and refine it.


AI returned:
- Backend-first plan: models -> storage -> routes -> tests -> frontend.
- Proposed task-scoped comments endpoints and in-memory store keyed by task id.

Decision:
- Accepted backend-first sequencing and task-scoped endpoint design.
- Edited to keep initial frontend scope in edit modal only.

### Prompt C2
Prompt:
"start implementation of the porposed plan for task comments [I pasted here the proposed plan from Prompt C1]"

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

### Prompt C4 (added missing functionality)
Prompt:
Review the popup window of adding a task, the view doesn't fit the browser and user are unable to click on save comment button. Add a scroll bar for user to nagigate the popup window up and down"

AI returned:
- Popup scroll down functionality

Decision:
- Accepted this enhancement on the popup window