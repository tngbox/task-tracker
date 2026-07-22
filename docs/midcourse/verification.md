# Feature A & B(Overdue date and Filter) Verification

## Break-Test Evidence Summary (A/B/C)

| Feature | Target test (same in all 3 phases) | Baseline (correct code) | After deliberate defect | After restore |
|---|---|---|---|---|
| Feature A (overdue date persistence) | `tests/test_tasks.py::test_create_task_valid_due_date_returns_201` | `1 passed, 1 warning` | `1 failed, 1 warning` | `1 passed, 1 warning` |
| Feature B (overdue filter) | `tests/test_tasks.py::test_list_tasks_filter_by_overdue_returns_only_overdue_not_done` | `1 passed, 1 warning` | `1 failed, 1 warning` | `1 passed, 1 warning` |
| Feature C (task comments) | `tests/test_tasks.py::test_add_comment_returns_201_with_body` | `1 passed, 1 warning` | `1 failed, 1 warning` | `1 passed, 1 warning` |

Reviewer note: For each feature, the exact same test case was run in all three phases (correct code, deliberate defect, restored code) to satisfy break-test evidence requirements.

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
Feature A evidence - Due date persistence:

Target test used in all three phases:
- `tests/test_tasks.py::test_create_task_valid_due_date_returns_201`

Phase 1 - Correct code (pass):
```bash
PYTHONPATH=. .venv/Scripts/python.exe -m pytest -q tests/test_tasks.py::test_create_task_valid_due_date_returns_201
```
Observed result:
- `1 passed, 1 warning`

Phase 2 - Deliberate defect introduced (fail):
- Defect applied in `app/storage.py` within `add_task`: temporarily changed `due_date=payload.due_date` to `due_date=None`.

```bash
PYTHONPATH=. .venv/Scripts/python.exe -m pytest -q tests/test_tasks.py::test_create_task_valid_due_date_returns_201
```
Observed result:
- `1 failed, 1 warning`
- Failure excerpt: `assert response.json()["due_date"] == "2026-08-01"` failed because API returned `None`.

Phase 3 - Code restored (pass again):
- Restored `add_task` due-date mapping to `due_date=payload.due_date`.

```bash
PYTHONPATH=. .venv/Scripts/python.exe -m pytest -q tests/test_tasks.py::test_create_task_valid_due_date_returns_201
```
Observed result:
- `1 passed, 1 warning`

Feature B evidence - Overdue filter excludes Done tasks:

Target test used in all three phases:
- `tests/test_tasks.py::test_list_tasks_filter_by_overdue_returns_only_overdue_not_done`

Phase 1 - Correct code (pass):
```bash
PYTHONPATH=. .venv/Scripts/python.exe -m pytest -q tests/test_tasks.py::test_list_tasks_filter_by_overdue_returns_only_overdue_not_done
```
Observed result:
- `1 passed, 1 warning`

Phase 2 - Deliberate defect introduced (fail):
- Defect applied in `app/storage.py` within `_is_overdue`: temporarily removed `status == TaskStatus.DONE` exclusion so Done tasks could be treated as overdue.

```bash
PYTHONPATH=. .venv/Scripts/python.exe -m pytest -q tests/test_tasks.py::test_list_tasks_filter_by_overdue_returns_only_overdue_not_done
```
Observed result:
- `1 failed, 1 warning`
- Failure excerpt: `assert len(body) == 1` failed because response length became `2` (the overdue Done task was incorrectly included).

Phase 3 - Code restored (pass again):
- Restored `_is_overdue` to exclude Done tasks again.

```bash
PYTHONPATH=. .venv/Scripts/python.exe -m pytest -q tests/test_tasks.py::test_list_tasks_filter_by_overdue_returns_only_overdue_not_done
```
Observed result:
- `1 passed, 1 warning`

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
Feature selected for break test process: **Feature C (task comments)**

Target test used in all three phases:
- `tests/test_tasks.py::test_add_comment_returns_201_with_body`

Phase 1 - Correct code (pass):
```bash
PYTHONPATH=. .venv/Scripts/python.exe -m pytest -q tests/test_tasks.py::test_add_comment_returns_201_with_body
```
Observed result:
- `1 passed, 1 warning`

Phase 2 - Deliberate defect introduced (fail):
- Defect applied in `app/storage.py` within `add_comment`: temporarily inverted the existence check from `if task_id not in _tasks` to `if task_id in _tasks`, causing valid tasks to be treated as missing.

```bash
PYTHONPATH=. .venv/Scripts/python.exe -m pytest -q tests/test_tasks.py::test_add_comment_returns_201_with_body
```
Observed result:
- `1 failed, 1 warning`
- Failure excerpt: expected `201`, received `404` for comment creation on an existing task.

Phase 3 - Code restored (pass again):
- Restored `add_comment` task-existence check to `if task_id not in _tasks`.

```bash
PYTHONPATH=. .venv/Scripts/python.exe -m pytest -q tests/test_tasks.py::test_add_comment_returns_201_with_body
```
Observed result:
- `1 passed, 1 warning`
