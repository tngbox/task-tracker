"""
Shared pytest fixtures for the Task Tracker API tests.

Provides a TestClient bound to the real app, resets the in-memory storage
around every test for isolation, and a convenience fixture that creates a
single task.
"""

import pytest
from fastapi.testclient import TestClient

from app import storage
from app.main import app


@pytest.fixture(autouse=True)
def _reset_storage():
    """Clear in-memory storage before and after each test for isolation."""
    storage._reset()
    yield
    storage._reset()


@pytest.fixture
def client():
    """A TestClient wrapping the real FastAPI app."""
    return TestClient(app)


@pytest.fixture
def created_task(client):
    """Create one task via the API and return its response JSON."""
    response = client.post("/tasks", json={"title": "fixture task"})
    assert response.status_code == 201
    return response.json()
