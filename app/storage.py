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
    TaskCreate,
    TaskPriority,
    TaskResponse,
    TaskStatus,
    TaskUpdate,
)

_tasks: dict[str, TaskResponse] = {}


def _now() -> datetime:
    """Current UTC time, used for created_at/updated_at stamps."""
    return datetime.now(timezone.utc)


def add_task(payload: TaskCreate) -> TaskResponse:
    """Create and store a new task, returning the stored representation."""
    now = _now()
    task = TaskResponse(
        id=str(uuid.uuid4()),
        title=payload.title,
        description=payload.description or "",
        status=payload.status,
        priority=payload.priority,
        assignee=payload.assignee,
        created_at=now,
        updated_at=now,
    )
    _tasks[task.id] = task
    return task


def get_all_tasks(
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
) -> list[TaskResponse]:
    """Return all tasks, optionally filtered by status and/or priority."""
    tasks = list(_tasks.values())
    if status is not None:
        tasks = [t for t in tasks if t.status == status]
    if priority is not None:
        tasks = [t for t in tasks if t.priority == priority]
    return tasks


def get_task_by_id(task_id: str) -> Optional[TaskResponse]:
    """Return the task with the given id, or None if it does not exist."""
    return _tasks.get(task_id)


def update_task(task_id: str, payload: TaskUpdate) -> Optional[TaskResponse]:
    """
    Apply a partial update to an existing task.

    Only fields explicitly provided in the payload are changed. Returns the
    updated task, or None if no task with that id exists.
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
    """Delete a task by id. Returns True if a task was removed, else False."""
    return _tasks.pop(task_id, None) is not None


def _reset() -> None:
    """Clear all stored tasks. Intended for tests only."""
    _tasks.clear()
