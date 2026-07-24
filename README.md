# Task Tracker Final Project

A minimal FastAPI + Pydantic v2 REST backend for tracking tasks, built as a
learning project. It intentionally keeps the smallest possible
footprint: an in-memory store, no database, and no authentication. All task
state lives in memory and is lost when the server restarts.

Branch reviewed: final-project

### 1. What this submission demonstrates

- Existing Task Tracker app still runs inside the intended course scope.
- CI runs the pytest suite on push and pull request.
- Docker image builds and runs with `/health` returning 200.
- AI review, security, and ownership evidence is in `docs/`.

### 2. How to run locally

```bash
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn app.main:app --port 8000
```Optionally copy the example environment file:

```bash
cp .env.example .env
```

### 3. How to run tests

```bash
python -m pytest -v
```
```bash
pytest -v
```

Run a single file, a single test, or by name substring:

```bash
pytest tests/test_tasks.py
pytest tests/test_tasks.py::test_create_task_valid_returns_201_with_full_body
pytest -k transition
```

`tests/verify_a.py` is a standalone script (not a pytest module) that prints
PASS/FAIL for model validation rules:

```bash
python -m tests.verify_a
```
### 4. How to run with Docker

```bash
docker build -t task-tracker:final-check .
docker run --rm -p 8001:8000 task-tracker:final-check
```
Then, from another terminal:

```bash
curl http://localhost:8001/health
```

The image is a multi-stage build on `python:3.11-slim`, runs as a non-root
`app` user, and contains only the `app/` package plus its dependencies. The
runtime stage also includes a container `HEALTHCHECK` against `/health`.
The static frontend and tests are not included in the image.

### 5. Evidence files

- `docs/release-evidence.md`
- `docs/final-ai-review.md`
- `docs/ai-playbook.md`

### 6. AI assistance summary

AI helped draft or review: CI, Docker, docs, security, and debugging checks.
I verified the work by: tests, diff review, Docker build/run, `/health` checks, and manual scan of workflow safety shortcuts.
One AI suggestion I rejected or corrected: add a latest green GitHub Actions run URL without verifiable local evidence; I replaced it with a factual "not confirmed from local workspace" note.

## 7. CRUD endpoints
The API exposes CRUD endpoints for tasks, task comments, and a health check:

| Method | Path                                  | Purpose |
| ------ | ------------------------------------- | ------- |
| GET    | `/health`                             | Liveness check (`status` + UTC timestamp) |
| POST   | `/tasks`                              | Create a task |
| GET    | `/tasks`                              | List tasks (optional `status`/`priority`/`overdue` filters) |
| GET    | `/tasks/{task_id}`                    | Get one task by id |
| PATCH  | `/tasks/{task_id}`                    | Partially update a task |
| DELETE | `/tasks/{task_id}`                    | Delete a task |
| GET    | `/tasks/{task_id}/comments`           | List comments for a task |
| POST   | `/tasks/{task_id}/comments`           | Add a comment to a task |
| DELETE | `/tasks/{task_id}/comments/{comment_id}` | Delete a comment from a task |

Interactive API docs are auto-generated at `http://localhost:8000/docs` while
the server is running.

A separate static Kanban frontend lives in `frontend/index.html`. It is not
served by the API; open it directly in a browser (see below).

## 8. Verify the health endpoint:

The API is served at `http://localhost:8000`. Verify the health endpoint:

```bash
curl http://localhost:8000/health
```

Expected response (the `timestamp` is the current UTC time in ISO 8601 and
includes microseconds):

```json
{"status": "ok", "timestamp": "2026-07-17T17:53:48.489893+00:00"}
```

To use the Kanban frontend, keep the server running and open the static file in
a browser (it calls the API at `127.0.0.1:8000`):

```bash
# macOS: open frontend/index.html   |   Windows: start frontend/index.html
```

## 9. CI workflow summary

GitHub Actions runs `.github/workflows/ci.yml`:

- **Triggers:** every `push` (any branch) and every `pull_request` targeting `main`.
- **Jobs:**
  - `test`: checkout → set up Python 3.11 → cache pip (keyed on
    `requirements.txt`) → upgrade pip → `pip install -r requirements.txt` →
    `pytest -v --tb=short` (with `PYTHONPATH` set to the workspace root).
  - `docker-smoke` (after `test`): builds the Docker image, starts the
    container, waits for `/health`, then runs an API smoke test inside CI that
    verifies Feature A (due date), Feature B (overdue filter), and Feature C
    (task comments) against the containerized backend.

Any failing test or smoke check fails CI; there is no deployment step.

## 10. Project structure

```
task-tracker/
├── app/
│   ├── main.py            # FastAPI app, CORS, /health and /tasks routes
│   ├── models.py          # Pydantic schemas + TaskStatus/TaskPriority enums
│   ├── storage.py         # in-memory task store (dict), id/timestamp bookkeeping
│   └── business_rules.py  # status-transition rules
├── tests/
│   ├── conftest.py        # autouse fixture resets storage between tests
│   ├── test_tasks.py      # pytest suite (TestClient against the real app)
│   └── verify_a.py        # standalone validation script (run with python)
├── frontend/
│   └── index.html         # static Kanban UI (opened directly in a browser)
├── create_test_tasks.py   # seeds a running server with sample tasks over HTTP
├── requirements.txt
├── Dockerfile             # multi-stage, python:3.11-slim, non-root
├── .dockerignore
└── .github/workflows/ci.yml
```

> `create_test_tasks.py` imports `requests`, which is **not** in
> `requirements.txt`; install it separately (`pip install requests`) if you run
> that script.

## 11. Project conventions and current limitations

Conventions:

- Layered backend: routes (`main.py`) stay thin and delegate to `storage.py`
  (persistence) and `business_rules.py` (domain rules); `models.py` owns
  field-shape validation.
- Valid status transitions: `ToDo → InProgress`, `InProgress → Done`,
  `Done → InProgress`. Any other move — including same → same — returns HTTP 422.
- Task `title` is required, trimmed, non-empty, and at most 200 characters.
- Task `due_date` is optional (`YYYY-MM-DD`) and can be cleared via `null`.
- `GET /tasks` supports optional `overdue=true|false` filtering.
- Comments are task-scoped resources under `/tasks/{task_id}/comments`.
- Create/update payloads forbid unknown fields (HTTP 422).

Current limitations (by design for this module):

- **In-memory only** — all data is lost when the server restarts. No database.
- **No authentication or authorization.**
- **CORS is wide open** (`allow_origins=["*"]`) for local frontend development.
- **Not production-ready and not deployed** — this is a learning project.

## 12 Midcourse docs created during mid-course-project implementation

Midcourse feature artifacts are available in `docs/midcourse`:

- `docs/midcourse/mini-adr.md`
- `docs/midcourse/prompt-log.md`
- `docs/midcourse/reflection.md`
- `docs/midcourse/user-stories.md`
- `docs/midcourse/verification.md`

## 13. Design decisions

The code and `CLAUDE.md` refer to "ADR-001" as the rationale for the
no-database / no-auth / minimal design. That decision is documented in
[docs/decisions/adr-001.md](docs/decisions/adr-001.md), which covers the
in-memory task storage choice, the alternatives considered, and the trade-offs.


