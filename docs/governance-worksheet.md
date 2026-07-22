# Governance Retrospective - AI-Assisted Coding

## What I Shared With AI

| Item | Module | Risk Level | Reason |
|---|---|---|---|
| Task Tracker code | 2-5 | Medium | The repository source reveals application behavior, validation rules, and local configuration patterns. No secrets were inspected or recorded in this worksheet. |
| Test output and stack traces | 2-4 | Medium | They can expose source paths, dependency versions, request payloads, and environment details; share only a redacted, minimum-necessary excerpt. |
| Frontend code | 3 | Low | The visible static Kanban UI is local to `frontend/index.html`; it contains no confirmed credentials or external-user data. |
| Dockerfile and CI YAML | 4 | Medium | `Dockerfile` and `.github/workflows/ci.yml` disclose build, runtime, and automation configuration; redact any future secrets, internal URLs, or private registry details. |
| Any real external data I used by mistake | Not confirmed | High if present | No real external data is visible in the repository evidence reviewed. Check AI chat history before submitting this retrospective. |

## What I Received From AI

| Generated Thing | Module | Do I Understand It Line by Line? | Action |
|---|---|---|---|
| Backend models and validators | 2 | Yes | I traced `TaskCreate` and `TaskUpdate` from `app/models.py` through route handling and the API tests, and retained only behavior that matches the visible task rules. |
| Frontend board and drag-and-drop logic | 3 | Yes | I reviewed the rendered board, task movement, API calls, and error states in `frontend/index.html`, including use of the backend status values unchanged. |
| CI workflow | 4 | Yes | I reviewed each workflow step in `.github/workflows/ci.yml` and confirmed the checks run as intended before relying on CI results. |
| Dockerfile | 4 | Yes | I reviewed each build and runtime stage in `Dockerfile`, including the non-root user, dependencies, port, and Uvicorn command. |
| Security findings and plans | 5 | Yes, for the recorded review outcome | Retain the source-only limitations in `docs/security-review.md`; all recorded findings were graded Noise, so no security backlog item was created. |
