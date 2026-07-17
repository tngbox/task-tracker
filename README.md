# Task Tracker

A minimal FastAPI + Pydantic v2 REST backend for tracking tasks, built as a
learning project (Module 4). It intentionally keeps the smallest possible
footprint: an in-memory store, no database, and no authentication. All task
state lives in memory and is lost when the server restarts.

## 1. Project overview

The API exposes CRUD endpoints for tasks plus a health check:

| Method | Path               | Purpose                                  |
| ------ | ------------------ | ---------------------------------------- |
| GET    | `/health`          | Liveness check (`status` + UTC timestamp)|
| POST   | `/tasks`           | Create a task                            |
| GET    | `/tasks`           | List tasks (optional `status`/`priority` filters) |
| GET    | `/tasks/{task_id}` | Get one task by id                       |
| PATCH  | `/tasks/{task_id}` | Partially update a task                  |
| DELETE | `/tasks/{task_id}` | Delete a task                            |

Interactive API docs are auto-generated at `http://localhost:8000/docs` while
the server is running.

A separate static Kanban frontend lives in `frontend/index.html`. It is not
served by the API; open it directly in a browser (see below).

## 2. Prerequisites

- **Python 3.11**
- **pip** and the ability to create a virtual environment (`venv`)
- **Docker** (only if you want to run the containerized version in section 6)

## 3. Local setup

Run from the repo root:

```bash
python -m venv venv
source venv/bin/activate        # Windows (PowerShell): venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Optionally copy the example environment file:

```bash
cp .env.example .env
```

> Note: `.env` (`PORT`, `APP_ENV`) is loaded via `load_dotenv()` but is not
> currently read by the application code, so it does not change the server
> port or behavior yet. [VERIFY]

## 4. Run the app locally

```bash
uvicorn app.main:app --reload --port 8000
```

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

## 5. Run tests

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
python tests/verify_a.py
```

## 6. Run with Docker

Build the image and run the container (serves the API on port 8000):

```bash
docker build -t task-tracker:dev .
docker run --rm -p 8000:8000 task-tracker:dev
```

Then, from another terminal:

```bash
curl http://localhost:8000/health
```

The image is a multi-stage build on `python:3.11-slim`, runs as a non-root
`app` user, and contains only the `app/` package plus its dependencies. The
static frontend and tests are not included in the image.

## 7. CI workflow summary

GitHub Actions runs `.github/workflows/ci.yml`:

- **Triggers:** every `push` (any branch) and every `pull_request` targeting `main`.
- **Job:** a single `test` job on `ubuntu-latest`.
- **Steps:** checkout → set up Python 3.11 → cache pip (keyed on
  `requirements.txt`) → upgrade pip → `pip install -r requirements.txt` →
  `pytest -v --tb=short` (with `PYTHONPATH` set to the workspace root).

A failing test fails the job; there is no deployment step.

## 8. Project structure

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
> that script. [VERIFY]

## 9. Project conventions and current limitations

Conventions:

- Layered backend: routes (`main.py`) stay thin and delegate to `storage.py`
  (persistence) and `business_rules.py` (domain rules); `models.py` owns
  field-shape validation.
- Valid status transitions: `ToDo → InProgress`, `InProgress → Done`,
  `Done → InProgress`. Any other move — including same → same — returns HTTP 422.
- Task `title` is required, trimmed, non-empty, and at most 200 characters.
- Create/update payloads forbid unknown fields (HTTP 422).

Current limitations (by design for this module):

- **In-memory only** — all data is lost when the server restarts. No database.
- **No authentication or authorization.**
- **CORS is wide open** (`allow_origins=["*"]`) for local frontend development.
- **Not production-ready and not deployed** — this is a learning project.

## 10. Design decisions

The code and `CLAUDE.md` refer to "ADR-001" as the rationale for the
no-database / no-auth / minimal design, but no ADR document currently exists in
this repository. [VERIFY] — add `docs/decisions/adr-001.md` (or similar) if a
written technical note is expected, then link it here.
