# Verification

## 1) Baseline Check
- Branch: `MidCourseProject`
- Backend run mode: `uvicorn app.main:app --reload --port 8000`
- Baseline after implementation: tests passing, frontend loading, API reachable.

## 2) Backend Test Results
Command:
```bash
PYTHONPATH=. pytest -q
```
Observed result:
- `22 passed, 1 warning`

Warning noted:
- `PendingDeprecationWarning` from `starlette.formparsers` (`python_multipart` import path), unrelated to feature logic.

## 3) Manual Browser Checks
Checks performed on `frontend/index.html` while API running:
- Confirmed header `Filter` dropdown exists with `All tasks`, `Overdue only`, `Not overdue`.
- Confirmed modal has `Due Date` input and accepts date values.
- Confirmed task cards show `Due: YYYY-MM-DD`.
- Confirmed overdue task shows `Overdue` pill.
- Confirmed selecting `Overdue only` reduces visible cards to overdue set.

## 4) Behavior Contract Before/After Refactor
Before:
- No due date in task schema.
- No overdue definition.
- No overdue query filter.
- No due-date UI field or overdue visual indicator.

After:
- Optional `due_date` in create/update/response.
- Overdue defined as `due_date < today UTC` and `status != Done`.
- `GET /tasks` supports `?overdue=true|false`.
- Frontend modal supports due date edit.
- Board displays due date row and overdue pill.
- Frontend filter dropdown calls backend overdue filter.

## 5) Break Test Evidence
Break Test 1:
- Test: `test_create_task_invalid_due_date_format_returns_422`
- Intentional bad input: `due_date: "01-08-2026"`
- Expected/Observed: HTTP 422, test passes.

Break Test 2:
- Test: `test_patch_invalid_transition_todo_to_done_returns_422`
- Intentional invalid status jump: `ToDo -> Done`
- Expected/Observed: HTTP 422, test passes.

Targeted run used for evidence:
```bash
PYTHONPATH=. pytest -q tests/test_tasks.py::test_create_task_invalid_due_date_format_returns_422 tests/test_tasks.py::test_patch_invalid_transition_todo_to_done_returns_422
```
Observed result:
- `2 passed, 1 warning`
