# Feature A & B(Overdue date and Filter) Verification

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

---

## Feature C Verification (Task Comments)

## 1) Baseline Check
- Branch: `MidCourseProject`
- Backend run mode: `uvicorn app.main:app --reload --port 8000`
- Baseline before feature C: no comments API, no comments UI in edit modal.

## 2) Backend Test Results
Command:
```bash
PYTHONPATH=. pytest -q
```
Observed result after feature C:
- `30 passed, 1 warning`

Warning noted:
- `PendingDeprecationWarning` from `starlette.formparsers` (`python_multipart` import path), unrelated to comments logic.

## 3) Manual Browser Checks
Checks performed on `frontend/index.html` while API running:
- Opened Edit Task and confirmed Comments section renders with count badge and list area.
- Added a non-blank comment and confirmed it appears immediately after refresh.
- Deleted a comment and confirmed it disappears and count updates.
- Opened Create Task and confirmed save-first hint is shown and comments actions are not available yet.
- Confirmed modal now scrolls internally for long content, keeping comment controls reachable.

## 4) Behavior Contract Before/After Refactor
Before:
- No task comments resource.
- No API support for listing/adding/deleting comments.
- No comments UI in task modal.

After:
- Added `GET /tasks/{task_id}/comments`.
- Added `POST /tasks/{task_id}/comments`.
- Added `DELETE /tasks/{task_id}/comments/{comment_id}`.
- Non-blank comment text enforced by model validation (422 on blank).
- Missing task returns 404 for list/add/delete comments.
- Missing comment returns 404 on delete comment.
- Edit modal includes comments list/add/delete and internal scroll support.

## 5) Break Test Evidence
Break Test 1:
- Test: `test_add_comment_blank_text_returns_422`
- Intentional bad input: `{"text": "   "}`
- Expected/Observed: HTTP 422, test passes.

Break Test 2:
- Test: `test_delete_comment_missing_comment_returns_404`
- Intentional bad input: delete unknown comment id for existing task
- Expected/Observed: HTTP 404, test passes.

Targeted run used for evidence:
```bash
PYTHONPATH=. pytest -q tests/test_tasks.py::test_add_comment_blank_text_returns_422 tests/test_tasks.py::test_delete_comment_missing_comment_returns_404
```
Observed result:
- `2 passed, 1 warning`
