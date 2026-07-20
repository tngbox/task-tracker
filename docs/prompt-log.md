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
