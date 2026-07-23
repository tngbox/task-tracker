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
- Latest run link or note: run link not confirmed from local workspace; file check plus local baseline tests completed successfully.
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
| Container health endpoint returns HTTP 200 after run. | Built image, ran container on host port 8001, checked `curl -w "%{http_code}" /health`. | Confirmed | README Docker section uses exact command sequence with HTTP status check. |
| CI runs pytest with dependency install and explicit Python version. | Inspected `.github/workflows/ci.yml` (`python-version: "3.11"`, `pip install -r requirements.txt`, `pytest -v --tb=short`). | Confirmed | Recorded CI evidence and shortcut check in this file. |
