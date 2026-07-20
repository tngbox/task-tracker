"""
Pydantic v2 models and enums for the Task Tracker API.

Defines the task status/priority enums plus the create, update, and
response schemas. This module has no storage or routing logic - it only
describes the shape and validation rules of task data (per ADR-001, this
is a minimal, in-memory learning project with no database).
"""

from datetime import date, datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator


class TaskStatus(str, Enum):
    """Allowed lifecycle states for a task."""

    TODO = "ToDo"
    IN_PROGRESS = "InProgress"
    DONE = "Done"


class TaskPriority(str, Enum):
    """Allowed priority levels for a task."""

    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


def _validate_title(value: str) -> str:
    """
    Shared title rule: strip whitespace, reject blank titles, and reject
    titles longer than 200 characters (measured after stripping).
    """
    stripped = value.strip()
    if not stripped:
        raise ValueError("title must not be blank")
    if len(stripped) > 200:
        raise ValueError("title must be at most 200 characters")
    return stripped


def _validate_comment_text(value: str) -> str:
    """
    Shared comment text rule: strip whitespace, reject blank values, and
    enforce a reasonable max length to prevent unbounded payloads.
    """
    stripped = value.strip()
    if not stripped:
        raise ValueError("comment text must not be blank")
    if len(stripped) > 1000:
        raise ValueError("comment text must be at most 1000 characters")
    return stripped


class TaskCreate(BaseModel):
    """Payload for creating a new task."""

    model_config = ConfigDict(extra="forbid")

    title: str
    description: Optional[str] = ""
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    assignee: Optional[str] = None
    due_date: Optional[date] = None

    @field_validator("title")
    @classmethod
    def _check_title(cls, value: str) -> str:
        return _validate_title(value)


class TaskUpdate(BaseModel):
    """Payload for partially updating an existing task."""

    model_config = ConfigDict(extra="forbid")

    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    assignee: Optional[str] = None
    due_date: Optional[date] = None

    @field_validator("title")
    @classmethod
    def _check_title(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        return _validate_title(value)


class TaskResponse(BaseModel):
    """Full task representation returned by the API."""

    model_config = ConfigDict(extra="forbid")

    id: str
    title: str
    description: str
    status: TaskStatus
    priority: TaskPriority
    assignee: Optional[str]
    due_date: Optional[date]
    created_at: datetime
    updated_at: datetime


class TaskCommentCreate(BaseModel):
    """Payload for creating a task comment."""

    model_config = ConfigDict(extra="forbid")

    text: str

    @field_validator("text")
    @classmethod
    def _check_text(cls, value: str) -> str:
        return _validate_comment_text(value)


class TaskCommentResponse(BaseModel):
    """Task comment representation returned by the API."""

    model_config = ConfigDict(extra="forbid")

    id: str
    task_id: str
    text: str
    created_at: datetime
