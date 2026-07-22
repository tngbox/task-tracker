"""
In-memory storage layer for the Task Tracker API.

Holds tasks in a module-level dictionary keyed by id. There is no
database or ORM (per ADR-001) - all state lives in memory and is lost
when the process restarts. This module owns id generation and timestamp
bookkeeping so route handlers can stay thin.
"""

import uuid
from datetime import datetime, timezone
from typing import Optional

from app.models import (
    TaskCommentCreate,
    TaskCommentResponse,
    TaskCreate,
    TaskPriority,
    TaskResponse,
    TaskStatus,
    TaskUpdate,
)

_tasks: dict[str, TaskResponse] = {}
_task_comments: dict[str, list[TaskCommentResponse]] = {}


def _now() -> datetime:
    """Current UTC time, used for created_at/updated_at stamps."""
    return datetime.now(timezone.utc)


def _is_overdue(task: TaskResponse) -> bool:
    """A task is overdue when due_date is in the past and status is not Done."""
    if task.due_date is None or task.status == TaskStatus.DONE:
        return False
    today_utc = _now().date()
    return task.due_date < today_utc


def add_task(payload: TaskCreate) -> TaskResponse:
    """Create and store a new task.

    Generates a UUID id and sets ``created_at``/``updated_at`` to the current
    UTC time. ``description`` becomes an empty string when the payload's value
    is ``None``.

    Args:
        payload: The validated task-creation data.

    Returns:
        TaskResponse: The stored task, including its generated id and timestamps.
    """
    now = _now()
    task = TaskResponse(
        id=str(uuid.uuid4()),
        title=payload.title,
        description=payload.description or "",
        status=payload.status,
        priority=payload.priority,
        assignee=payload.assignee,
        due_date=payload.due_date,
        created_at=now,
        updated_at=now,
    )
    _tasks[task.id] = task
    return task


def get_all_tasks(
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
    overdue: Optional[bool] = None,
) -> list[TaskResponse]:
    """Return all stored tasks, optionally filtered.

    Args:
        status: Optional status to filter by; ``None`` applies no status filter.
        priority: Optional priority to filter by; ``None`` applies no priority
            filter.
        overdue: Optional overdue filter.

    Returns:
        list[TaskResponse]: Tasks matching every supplied filter (all tasks when
            no filter is given); empty list if none match.
    """
    tasks = list(_tasks.values())
    if status is not None:
        tasks = [t for t in tasks if t.status == status]
    if priority is not None:
        tasks = [t for t in tasks if t.priority == priority]
    if overdue is not None:
        tasks = [t for t in tasks if _is_overdue(t) is overdue]
    return tasks


def get_task_by_id(task_id: str) -> Optional[TaskResponse]:
    """Look up a task by id.

    Args:
        task_id: The id to look up.

    Returns:
        Optional[TaskResponse]: The matching task, or ``None`` if no task with
            that id exists.
    """
    return _tasks.get(task_id)


def update_task(task_id: str, payload: TaskUpdate) -> Optional[TaskResponse]:
    """Apply a partial update to an existing task.

    Only fields explicitly set in the payload (``exclude_unset``) are changed.
    When there are changes, ``updated_at`` is refreshed to the current UTC time;
    a payload with no set fields leaves the task (and its ``updated_at``)
    unchanged. This function does not check status transitions; that rule is
    enforced by the route handler.

    Args:
        task_id: The id of the task to update.
        payload: The fields to change; unset fields are ignored.

    Returns:
        Optional[TaskResponse]: The updated task, or ``None`` if no task with
            that id exists.
    """
    existing = _tasks.get(task_id)
    if existing is None:
        return None

    changes = payload.model_dump(exclude_unset=True)
    if not changes:
        return existing

    updated = existing.model_copy(update=changes)
    updated.updated_at = _now()
    _tasks[task_id] = updated
    return updated


def delete_task(task_id: str) -> bool:
    """Delete a task by id.

    Args:
        task_id: The id of the task to delete.

    Returns:
        bool: ``True`` if a task was removed, ``False`` if no task with that id
            existed.
    """
    removed = _tasks.pop(task_id, None) is not None
    if removed:
        _task_comments.pop(task_id, None)
    return removed


def list_comments(task_id: str) -> Optional[list[TaskCommentResponse]]:
    """Return comments for a task, or None if the task does not exist."""
    if task_id not in _tasks:
        return None
    return list(_task_comments.get(task_id, []))


def add_comment(task_id: str, payload: TaskCommentCreate) -> Optional[TaskCommentResponse]:
    """Create a task comment, or return None if the task does not exist."""
    if task_id not in _tasks:
        return None

    comment = TaskCommentResponse(
        id=str(uuid.uuid4()),
        task_id=task_id,
        text=payload.text,
        created_at=_now(),
    )
    _task_comments.setdefault(task_id, []).append(comment)
    return comment


def delete_comment(task_id: str, comment_id: str) -> tuple[bool, bool]:
    """
    Delete a comment by id for a task.

    Returns (task_exists, comment_deleted).
    """
    if task_id not in _tasks:
        return (False, False)

    comments = _task_comments.get(task_id, [])
    for idx, comment in enumerate(comments):
        if comment.id == comment_id:
            del comments[idx]
            if not comments:
                _task_comments.pop(task_id, None)
            return (True, True)
    return (True, False)


def _reset() -> None:
    """Clear all stored tasks. Intended for tests only."""
    _tasks.clear()
    _task_comments.clear()
