# Release Evidence

## Baseline
- Branch: final-project (tracks `origin/final-project`)
- Date: 2026-07-23
- Local app run command: `C:/Users/bigem/AppData/Local/Programs/Python/Python311/python.exe -m uvicorn app.main:app --port 8000`
- /health result: `{"status":"ok","timestamp":"2026-07-23T13:58:29.549768+00:00"}`
- Frontend check: opened `frontend/index.html` directly and confirmed Kanban columns, filter, and `+ New Task` control are visible.
- Test command: `C:/Users/bigem/AppData/Local/Programs/Python/Python311/python.exe -m pytest -v`
- Test result: 36 passed, 0 failed, 1 warning.

## CI evidence
- Workflow file: `.github/workflows/ci.yml`
- Latest run link or note: https://github.com/tngbox/task-tracker/actions/runs/30095873594 (workflow `CI`, branch `final-project`, conclusion `success`, commit `81be187fb5ac1ea7a2937b67c6ee9ed892285ad1`).
- Test command used by CI: `pytest -v --tb=short`
- Shortcut check: no `continue-on-error` / no `|| true` / pytest is not skipped.

## Docker evidence
- Build command: `docker build -t task-tracker:final-check .`
- Run command: `docker run --rm -d --name task-tracker-final-check -p 8001:8000 task-tracker:final-check`
- /health check: `curl.exe -s -o NUL -w "%{http_code}" http://127.0.0.1:8001/health` -> `200`
- Non-root check, if implemented: yes (`USER app` in `Dockerfile`).
- No-baked-secrets check: `.dockerignore` excludes `.env` and `.env.*` (keeps only `.env.example`).

## Documentation claim-vs-reality log
| Claim checked | Evidence used | Result | Change made, if any |
|---|---|---|---|
| README test command can validate baseline quality. | Ran `python -m pytest -v`; verified 36/36 passed. | Confirmed | Kept exact test command in README Final Project section. |
| README verify command for `verify_a` works from repository root. | Ran `.venv\Scripts\python.exe -m tests.verify_a`; all checks printed PASS. | Confirmed | Replaced `python tests/verify_a.py` with `python -m tests.verify_a` in README. |
| Docker verification endpoint must match mapped host port (`8001:8000`). | Checked README Docker section command mapping and expected endpoint. | Corrected | Updated README Docker health check URL from `localhost:8000` to `localhost:8001`. |
| CI runs pytest with dependency install and explicit Python version. | Inspected `.github/workflows/ci.yml` (`python-version: "3.11"`, `pip install -r requirements.txt`, `pytest -v --tb=short`). | Confirmed | Recorded CI evidence and shortcut check in this file. |
