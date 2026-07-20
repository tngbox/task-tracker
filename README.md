# Task Tracker API

A minimal FastAPI + Pydantic REST backend for tracking tasks, built as a solo-developer learning project. Per ADR-001, it deliberately avoids databases, authentication, and microservices in favor of the simplest possible setup.

## Setup

Create and activate a virtual environment, then install dependencies:

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Running the server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.

## Testing the health endpoint

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{"status": "ok", "timestamp": "2026-07-03T12:00:00.000000+00:00"}
```

## API usage examples

### Create a task with a due date

```bash
curl -X POST http://localhost:8000/tasks \
	-H "Content-Type: application/json" \
	-d '{
		"title": "Submit project milestone",
		"description": "Prepare final module handoff",
		"priority": "High",
		"due_date": "2026-08-01"
	}'
```

### Update a task due date

```bash
curl -X PATCH http://localhost:8000/tasks/<task_id> \
	-H "Content-Type: application/json" \
	-d '{
		"due_date": "2026-08-15"
	}'
```

To clear a due date:

```bash
curl -X PATCH http://localhost:8000/tasks/<task_id> \
	-H "Content-Type: application/json" \
	-d '{
		"due_date": null
	}'
```

### Filter tasks by overdue state

Get overdue tasks only:

```bash
curl "http://localhost:8000/tasks?overdue=true"
```

Get non-overdue tasks only:

```bash
curl "http://localhost:8000/tasks?overdue=false"
```

Overdue logic:
- `due_date` exists
- `due_date` is before today (UTC)
- `status` is not `Done`

### due_date format notes

- `due_date` is optional.
- Use ISO date format: `YYYY-MM-DD`.
- Invalid formats (for example `01-08-2026`) return HTTP 422.

## Frontend usage (short)

- Open `frontend/index.html` in your browser while the API is running at `http://127.0.0.1:8000`.
- In the task modal, use the new **Due Date** field to set or clear a task due date.
- Use the header **Filter** dropdown to switch between:
	- `All tasks`
	- `Overdue only`
	- `Not overdue`
- Task cards show `Due: YYYY-MM-DD`, and overdue tasks display an `Overdue` pill.
