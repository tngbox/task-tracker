# Module 5 Security Review

## Scope

This was a read-only security review of the Task Tracker learning project. It
covered the FastAPI backend, validation and in-memory storage, tests, static
frontend, dependency manifest, Docker configuration, CI workflow, and project
guardrails. No source files or runtime configuration were changed as part of
the review.

## Evidence reviewed

- `AGENTS.md`
- `app/main.py`, `app/models.py`, `app/storage.py`, and `app/business_rules.py`
- `tests/conftest.py`, `tests/test_tasks.py`, and `tests/verify_a.py`
- `frontend/index.html`
- `requirements.txt`, `Dockerfile`, `.dockerignore`, and `.github/workflows/ci.yml`

## AI findings and final grading

| ID | AI finding summary | Evidence reviewed | Final grade | Reason for Grading | Fix |
| --- | --- | --- | --- | --- | --- |
| SEC-01 | No authentication, broad CORS, and a Docker listener on all interfaces could expose task operations if deployed. | `app/main.py`, `Dockerfile`, `AGENTS.md` | Noise | No authentication is an intentional local learning-project constraint. The risk is conditional on a production deployment that is not in scope. | |
| SEC-02 | Unbounded `description`/`assignee` fields and unpaginated in-memory listing could permit resource growth. | `app/models.py`, `app/storage.py` | Noise | The absence of bounds is visible, but no demonstrated abuse path, scale requirement, or in-scope action item was established for this learning project. | |
| SEC-03 | Mutable GitHub Action tags, an unpinned pip upgrade, and no hash-locked transitive dependencies weaken supply-chain controls. | `requirements.txt`, `Dockerfile`, `.github/workflows/ci.yml` | Noise | This is generic production hardening. No vulnerable dependency, compromised action, or repository-specific exposure was identified. | |
| SEC-04 | A hard-coded loopback frontend API URL, displayed API details, and broad CORS could be unsafe in deployment. | `frontend/index.html`, `app/main.py` | Noise | The loopback URL is intentional for local use; no HTTPS deployment is visible; and the CORS concern duplicates SEC-01. No sensitive error disclosure was demonstrated. | |

## Outcome

All reviewed AI security findings were graded **Noise**. The review identified
no confirmed, actionable security backlog items for Module 5.

## Review limits

- The review was source-only: the app, tests, container, and CI workflow were
  not executed.
- Dependency vulnerability status was not externally scanned.
- `.env` content was not inspected. Its handling was assessed only through
  `.gitignore` and `.dockerignore`.
- Production hosting, reverse-proxy, and runtime configuration were not
  visible and are therefore not confirmed.
