"""
Entry point for the Task Tracker API.

Creates the FastAPI application instance and defines the health check
endpoint. Per ADR-001, this project intentionally has no database and
no authentication - it is a minimal, learning-focused REST backend.
"""

from datetime import datetime, timezone

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app import storage
from app.business_rules import validate_status_transition
from app.models import TaskCreate, TaskPriority, TaskResponse, TaskStatus, TaskUpdate

# Load variables from .env (e.g., PORT, APP_ENV) into the process environment.
# Safe to call even if no .env file exists yet - it just does nothing in that case.
load_dotenv()

# The FastAPI application instance. Uvicorn imports this object directly
# (see README for the exact run command: `uvicorn app.main:app --reload`).
app = FastAPI(
    title="Task Tracker API",
    description="A minimal FastAPI backend for tracking tasks (learning project, ADR-001).",
    version="0.1.0",
)

# Enable CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class HealthResponse(BaseModel):
    """Pydantic response schema for the /health endpoint."""

    status: str
    timestamp: str


@app.get("/health", response_model=HealthResponse, status_code=200)
def health_check() -> HealthResponse:
    """Report service liveness.

    Returns a fixed ``"ok"`` status plus the current UTC timestamp in ISO 8601
    format, so callers can confirm both that the server is up and roughly when
    the response was generated.

    Returns:
        HealthResponse: An object with ``status="ok"`` and an ISO 8601
            ``timestamp`` in UTC.

    Example:
        ``GET /health`` returns HTTP 200 with::

            {"status": "ok", "timestamp": "2026-07-17T12:00:00+00:00"}
    """
    return HealthResponse(
        status="ok",
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


@app.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["tasks"],
)
def create_task(payload: TaskCreate) -> TaskResponse:
    """Create a new task.

    Field-shape validation (title rules, enum values, unknown fields) is
    enforced by Pydantic on ``TaskCreate`` before this handler runs, so invalid
    input returns HTTP 422 automatically. The id and ``created_at``/
    ``updated_at`` timestamps are assigned by the storage layer.

    Args:
        payload: The task to create. ``title`` is required; ``status`` defaults
            to ``ToDo`` and ``priority`` to ``Medium`` when omitted.

    Returns:
        TaskResponse: The stored task, including its generated id and timestamps.

    Raises:
        HTTPException: 422 (raised by FastAPI/Pydantic) if the payload has a
            blank or too-long title, an invalid enum value, or unknown fields.

    Example:
        ``POST /tasks`` with ``{"title": "Write docs"}`` returns HTTP 201 and
        the created task with ``status="ToDo"`` and ``priority="Medium"``.
    """
    return storage.add_task(payload)


@app.get("/tasks", response_model=list[TaskResponse], tags=["tasks"])
def list_tasks(
    status: TaskStatus | None = None,
    priority: TaskPriority | None = None,
) -> list[TaskResponse]:
    """List tasks, optionally filtered by status and/or priority.

    When both filters are supplied, a task must match both to be included.
    Invalid query values are rejected by FastAPI with HTTP 422.

    Args:
        status: Optional status to filter by. ``None`` applies no status filter.
        priority: Optional priority to filter by. ``None`` applies no priority
            filter.

    Returns:
        list[TaskResponse]: Matching tasks. An empty list (HTTP 200 with ``[]``)
            is returned when nothing matches or no tasks exist.

    Example:
        ``GET /tasks?status=InProgress&priority=High`` returns HTTP 200 with a
        JSON array of the matching tasks.
    """
    return storage.get_all_tasks(status=status, priority=priority)


@app.get("/tasks/{task_id}", response_model=TaskResponse, tags=["tasks"])
def get_task(task_id: str) -> TaskResponse:
    """Retrieve a single task by its id.

    Args:
        task_id: The id of the task to fetch.

    Returns:
        TaskResponse: The task with the given id.

    Raises:
        HTTPException: 404 if no task with ``task_id`` exists.

    Example:
        ``GET /tasks/3f...`` returns HTTP 200 with the task, or HTTP 404 with
        ``{"detail": "Task with id 3f... not found"}``.
    """
    task = storage.get_task_by_id(task_id)
    if task is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task with id {task_id} not found",
        )
    return task


@app.patch("/tasks/{task_id}", response_model=TaskResponse, tags=["tasks"])
def update_task(task_id: str, payload: TaskUpdate) -> TaskResponse:
    """Partially update a task by its id.

    Only fields present in the body are changed; body values are validated by
    Pydantic (HTTP 422 on bad shape). When a new ``status`` is supplied, the
    task must exist and the move must be an allowed transition from its current
    status (see ``validate_status_transition``); same-to-same is not allowed.

    Args:
        task_id: The id of the task to update.
        payload: The fields to change. Omitted fields are left untouched.

    Returns:
        TaskResponse: The updated task.

    Raises:
        HTTPException: 404 if no task with ``task_id`` exists; 422 if the body
            shape is invalid or the requested status transition is not allowed.

    Example:
        ``PATCH /tasks/3f...`` with ``{"status": "InProgress"}`` returns HTTP
        200 and the updated task when the transition ToDo->InProgress is valid.
    """
    if payload.status is not None:
        existing = storage.get_task_by_id(task_id)
        if existing is None:
            raise HTTPException(
                status_code=404,
                detail=f"Task with id {task_id} not found",
            )
        validate_status_transition(existing.status, payload.status)

    task = storage.update_task(task_id, payload)
    if task is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task with id {task_id} not found",
        )
    return task


@app.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["tasks"],
)
def delete_task(task_id: str) -> None:
    """Delete a task by its id.

    Args:
        task_id: The id of the task to delete.

    Returns:
        None: On success the endpoint responds with HTTP 204 (no body).

    Raises:
        HTTPException: 404 if no task with ``task_id`` exists.

    Example:
        ``DELETE /tasks/3f...`` returns HTTP 204 on success, or HTTP 404 if the
        id is unknown.
    """
    if not storage.delete_task(task_id):
        raise HTTPException(
            status_code=404,
            detail=f"Task with id {task_id} not found",
        )


