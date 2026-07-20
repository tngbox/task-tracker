# Personal AI Coding Playbook

## 1. When I reach for AI first

- **Cursor**: interactive implementation while I am actively driving in the IDE - small-to-medium features, focused refactors, and quick codebase questions.
- **Codex**: bounded repository tasks that need investigation, multi-file edits, commands, and verification; I review the resulting diff before accepting it.
- **GitHub Copilot**: GitHub-centered pull-request review and a second pass over a changed diff, after I have run the relevant local checks.

## 2. When I do not reach for AI

- When the task involves credentials, private customer data, production access, or material I am not authorized to share.
- When I cannot state the intended behavior and an observable way to verify it.
- When an irreversible production action needs a human decision, explicit approval, or a change record first.

## 3. My non-negotiables

- I keep secrets, tokens, `.env` values, customer data, and private keys out of AI prompts and tool output.
- I keep the task bounded, preserve existing user changes, and inspect the diff before I accept any edit.
- I run the relevant tests or checks myself; an AI claim that code works is not evidence.

## 4. My review rules

- I give the reviewer the goal, constraints, risk areas, and tests that should matter - not just "review this."
- I validate every finding against the code and requirements; I do not treat AI feedback as an approval or a blocker.
- I ask for a separate security, regression, and maintainability pass on changes with meaningful blast radius.

## 5. What I am still figuring out

- Which tasks are reliably faster with a tool than with a short manual implementation.
- Which repository instructions, prompts, and checklists improve the quality of reviews over time.
- Where tool permissions and autonomy should stop for infrastructure and production-adjacent work.

## Decision Card

- For a new feature I reach for: Cursor for interactive implementation; Codex for a bounded, verified repository task.
- For a code review I reach for: GitHub Copilot on the pull request, followed by human review.
- For debugging I reach for: Codex when investigation, reproduction, and test execution span the repository; Cursor for an IDE-local investigation.
- For infrastructure I reach for: Codex only for a scoped, reviewable plan or change; I retain human approval for execution.
- I will never paste secrets, credentials, private keys, or private customer data into an AI tool.
- My one rule is: I remain accountable for every change I accept.
