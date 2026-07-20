"""
End-to-end tests for the Task Tracker REST API (Module 2).

Exercises the full CRUD surface plus status-transition rules through the
real in-memory storage, using FastAPI's TestClient.
"""

from datetime import datetime, timedelta, timezone


# --------------------------------------------------------------------------
# POST /tasks
# --------------------------------------------------------------------------

def test_create_task_valid_returns_201_with_full_body(client):
    response = client.post(
        "/tasks",
        json={
            "title": "Write tests",
            "description": "cover the API",
            "priority": "High",
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "Write tests"
    assert body["description"] == "cover the API"
    assert body["status"] == "ToDo"
    assert body["priority"] == "High"
    assert body["assignee"] is None
    assert body["due_date"] is None
    assert isinstance(body["id"], str) and body["id"]
    assert "created_at" in body
    assert "updated_at" in body


def test_create_task_valid_due_date_returns_201(client):
    response = client.post(
        "/tasks",
        json={
            "title": "Task with due date",
            "due_date": "2026-08-01",
        },
    )
    assert response.status_code == 201
    assert response.json()["due_date"] == "2026-08-01"


def test_create_task_invalid_due_date_format_returns_422(client):
    response = client.post(
        "/tasks",
        json={
            "title": "Invalid due date",
            "due_date": "01-08-2026",
        },
    )
    assert response.status_code == 422


def test_create_task_missing_title_returns_422(client):
    response = client.post("/tasks", json={"priority": "High"})
    assert response.status_code == 422


def test_create_task_blank_title_returns_422(client):
    response = client.post("/tasks", json={"title": "   "})
    assert response.status_code == 422


def test_create_task_invalid_priority_returns_422(client):
    response = client.post("/tasks", json={"title": "x", "priority": "Urgent"})
    assert response.status_code == 422


def test_create_task_unknown_field_returns_422(client):
    response = client.post("/tasks", json={"title": "x", "made_up": "value"})
    assert response.status_code == 422


# --------------------------------------------------------------------------
# GET /tasks
# --------------------------------------------------------------------------

def test_list_tasks_empty_returns_200_and_empty_list(client):
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_filter_by_status_no_match_returns_200_and_empty_list(client):
    client.post("/tasks", json={"title": "a task"})
    response = client.get("/tasks", params={"status": "Done"})
    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_filter_by_priority_returns_only_matches(client):
    client.post("/tasks", json={"title": "high one", "priority": "High"})
    client.post("/tasks", json={"title": "low one", "priority": "Low"})
    client.post("/tasks", json={"title": "another high", "priority": "High"})

    response = client.get("/tasks", params={"priority": "High"})
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 2
    assert {t["title"] for t in body} == {"high one", "another high"}
    assert all(t["priority"] == "High" for t in body)


def test_list_tasks_filter_by_overdue_returns_only_overdue_not_done(client):
    today = datetime.now(timezone.utc).date()
    past_due = (today - timedelta(days=1)).isoformat()
    future_due = (today + timedelta(days=2)).isoformat()

    client.post("/tasks", json={"title": "overdue todo", "due_date": past_due})
    client.post("/tasks", json={"title": "future todo", "due_date": future_due})
    client.post("/tasks", json={"title": "no due"})

    done_response = client.post(
        "/tasks",
        json={"title": "overdue done", "due_date": past_due},
    )
    done_id = done_response.json()["id"]
    client.patch(f"/tasks/{done_id}", json={"status": "InProgress"})
    client.patch(f"/tasks/{done_id}", json={"status": "Done"})

    response = client.get("/tasks", params={"overdue": "true"})
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["title"] == "overdue todo"


def test_list_tasks_filter_by_overdue_false_excludes_overdue(client):
    today = datetime.now(timezone.utc).date()
    past_due = (today - timedelta(days=1)).isoformat()
    future_due = (today + timedelta(days=1)).isoformat()

    client.post("/tasks", json={"title": "overdue todo", "due_date": past_due})
    client.post("/tasks", json={"title": "future todo", "due_date": future_due})
    client.post("/tasks", json={"title": "no due"})

    response = client.get("/tasks", params={"overdue": "false"})
    assert response.status_code == 200
    titles = {t["title"] for t in response.json()}
    assert "overdue todo" not in titles
    assert titles == {"future todo", "no due"}


# --------------------------------------------------------------------------
# GET /tasks/{id}
# --------------------------------------------------------------------------

def test_get_task_by_id_returns_task(client, created_task):
    task_id = created_task["id"]
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json() == created_task


def test_get_task_by_id_not_found_returns_404_with_detail(client):
    response = client.get("/tasks/missing-id")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task with id missing-id not found"


# --------------------------------------------------------------------------
# PATCH /tasks/{id}
# --------------------------------------------------------------------------

def test_patch_partial_update_keeps_other_fields(client, created_task):
    task_id = created_task["id"]
    response = client.patch(f"/tasks/{task_id}", json={"description": "updated"})
    assert response.status_code == 200
    body = response.json()
    assert body["description"] == "updated"
    assert body["title"] == created_task["title"]
    assert body["status"] == created_task["status"]
    assert body["priority"] == created_task["priority"]
    assert body["due_date"] == created_task["due_date"]
    assert body["id"] == task_id


def test_patch_update_due_date_returns_updated_due_date(client, created_task):
    task_id = created_task["id"]

    response = client.patch(f"/tasks/{task_id}", json={"due_date": "2026-08-15"})
    assert response.status_code == 200
    assert response.json()["due_date"] == "2026-08-15"


def test_patch_not_found_returns_404(client):
    response = client.patch("/tasks/missing-id", json={"description": "x"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Task with id missing-id not found"


def test_patch_valid_transition_todo_to_inprogress_returns_200(client, created_task):
    task_id = created_task["id"]
    response = client.patch(f"/tasks/{task_id}", json={"status": "InProgress"})
    assert response.status_code == 200
    assert response.json()["status"] == "InProgress"


def test_patch_invalid_transition_todo_to_done_returns_422(client, created_task):
    task_id = created_task["id"]
    response = client.patch(f"/tasks/{task_id}", json={"status": "Done"})
    assert response.status_code == 422


def test_patch_same_status_returns_422(client, created_task):
    task_id = created_task["id"]
    response = client.patch(f"/tasks/{task_id}", json={"status": "ToDo"})
    assert response.status_code == 422


# --------------------------------------------------------------------------
# DELETE /tasks/{id}
# --------------------------------------------------------------------------

def test_delete_existing_returns_204_no_body(client, created_task):
    task_id = created_task["id"]
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 204
    assert response.content == b""


def test_delete_missing_returns_404(client):
    response = client.delete("/tasks/missing-id")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task with id missing-id not found"
