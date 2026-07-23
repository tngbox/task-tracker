# Personal AI Coding Playbook

## 1. When I reach for AI first

- I reach for AI first when the task is bounded and verifiable: summarize a file I just changed, draft a test matrix, or produce a checklist for release evidence.
- During this course, AI helped most when I needed fast repository navigation and command sequencing: run baseline checks, verify `/health`, confirm CI steps, and write short evidence docs.
- I use AI as an accelerator, not an approver. I still decide what gets merged.

## 2. When I do not reach for AI

- I do not start with AI when secrets, private data, or production-only context is involved.
- I do not start with AI when I cannot define success criteria or a concrete verification command.
- I do not start with AI when the goal is my own learning of a core concept that I should practice directly first.

## 3. My non-negotiables

- Never paste secrets, tokens, `.env` values, customer data, or keys into prompts.
- Keep scope tight: no feature creep when the task is review, grading, or release readiness.
- Inspect every diff before accepting it, especially docs that claim commands or results.
- Run commands myself (`pytest`, health checks, Docker checks) before I trust any AI summary.
- Ownership is mine; if I cannot explain a line, I do not submit it.

## 4. My review rules

- I review in this order: scope, behavior, safety, then style.
- I grade AI comments explicitly: Useful, Noise, or Wrong, and I record why.
- I reject any suggestion that is unverifiable from files, commands, or tests.
- I prefer exact evidence over broad claims: command used, output observed, file updated.
- For risky areas, I ask for separate passes (security, regression, maintainability) instead of one blended review.

## 5. What I am still figuring out

- Where the handoff line should be between AI-generated docs and my own manual notes.
- How strict to be about requiring two independent checks for higher-risk suggestions.
- What team norm works best for storing prompt logs without creating noise.

## Decision Card

- New feature: use AI for scaffolding and edge-case brainstorming; implement and verify behavior myself.
- Code review: let AI produce candidate findings, then I grade each finding before acting.
- Debugging: use AI to narrow hypotheses, then reproduce and confirm with tests or runtime checks.
- Infrastructure: use AI for draft plans and checklists; execute only with explicit human approval.
- Never paste: secrets, credentials, private keys, `.env` values, or real customer data.
- One rule: if I cannot explain it, I do not keep it.
