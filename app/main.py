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
    """
    Simple liveness check.

    Returns a fixed "ok" status plus the current UTC timestamp in ISO 8601
    format, so callers can confirm both that the server is up and roughly
    when the response was generated.
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
    """
    Create a new task.

    Validation (title rules, enum values, unknown fields) is enforced by
    Pydantic on TaskCreate, so invalid input returns HTTP 422 automatically.
    Id and timestamps are assigned by the storage layer.
    """
    return storage.add_task(payload)


@app.get("/tasks", response_model=list[TaskResponse], tags=["tasks"])
def list_tasks(
    status: TaskStatus | None = None,
    priority: TaskPriority | None = None,
    overdue: bool | None = None,
) -> list[TaskResponse]:
    """
    List tasks, optionally filtered by status, priority, and overdue.

    Invalid query values are rejected by FastAPI with HTTP 422. An empty
    result (including a filter that matches nothing) returns 200 with [].
    """
    return storage.get_all_tasks(status=status, priority=priority, overdue=overdue)


@app.get("/tasks/{task_id}", response_model=TaskResponse, tags=["tasks"])
def get_task(task_id: str) -> TaskResponse:
    """
    Retrieve a single task by its id.

    Returns the task if it exists, otherwise raises HTTP 404.
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
    """
    Partially update a task by its id.

    Only fields provided in the body are changed; invalid body values are
    rejected by Pydantic with HTTP 422. When a new status is supplied it must
    be a valid transition from the task's current status (HTTP 422 otherwise).
    Returns the updated task, or raises HTTP 404 if no task with the given id
    exists.
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
    """
    Delete a task by its id.

    Returns an empty 204 response on success, or raises HTTP 404 if no task
    with the given id exists.
    """
    if not storage.delete_task(task_id):
        raise HTTPException(
            status_code=404,
            detail=f"Task with id {task_id} not found",
        )


