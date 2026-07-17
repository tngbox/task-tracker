"""
Business rules for the Task Tracker API.

Currently defines the allowed task status-transition graph and a helper to
enforce it. Kept separate from models (which validate field shape) and
storage (which persists data) so domain rules live in one place.
"""

from fastapi import HTTPException, status

from app.models import TaskStatus

VALID_TRANSITIONS: frozenset[tuple[TaskStatus, TaskStatus]] = frozenset({
    (TaskStatus.TODO, TaskStatus.IN_PROGRESS),
    (TaskStatus.IN_PROGRESS, TaskStatus.DONE),
    (TaskStatus.DONE, TaskStatus.IN_PROGRESS),
})


def validate_status_transition(current: TaskStatus, new: TaskStatus) -> None:
    """Enforce the allowed status-transition graph.

    A transition is permitted only if the ``(current, new)`` pair is present in
    ``VALID_TRANSITIONS`` (ToDo->InProgress, InProgress->Done, Done->InProgress).
    Same-to-same and any other pair are rejected.

    Args:
        current: The task's current status.
        new: The requested new status.

    Returns:
        None: Returns nothing when the transition is allowed.

    Raises:
        HTTPException: 422 when the transition is not allowed; the detail lists
            the allowed transitions.
    """
    if (current, new) not in VALID_TRANSITIONS:
        allowed = sorted({f"{f.value}->{t.value}" for f, t in VALID_TRANSITIONS})
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid status transition from {current.value} to {new.value}. Allowed transitions: {allowed}",
        )
