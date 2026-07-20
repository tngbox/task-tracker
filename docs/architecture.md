# Architecture-Document Context Strategy Comparison

| Strategy | What it got right | What it got wrong, missed, or invented | Best suited task shape |
|---|---|---|---|
| A — minimal context | Produced a broad, usable architecture outline: API, static Kanban UI, data model, create flow, validation, storage, and UI states. It also clearly separates confirmed behavior from “not visible or assumptions.” | It makes several highly specific claims not corroborated by the other drafts, including the `Dockerfile`, test-fixture reset behavior, frontend modal behavior, filtering, and optimistic drag/drop rollback. Those details may be correct, but are unsupported within this three-draft comparison. | Fast, broad documentation drafts where a high-level overview matters more than traceability of every detail. |
| B — structured context | Gives the most balanced description of the app and covers both backend and frontend behavior. It identifies `AGENTS.md` as a source of architecture and business-rule context, while retaining concrete validation and transition details. | Its file links are machine-local paths, so they are less portable in a repository document. Compared with A, it omits details such as the full request-flow sequence and frontend recovery behavior; compared with C, it does not state which claims came from which anchor files. | Architecture documentation that must combine repository conventions, file summaries, and behavior rules into a coherent project-level overview. |
| C — targeted anchor files | Is the most disciplined about scope: it explicitly limits claims to files it says it read, gives a precise `POST /tasks` flow, and labels unavailable frontend, test, deployment, and transition-rule details as not confirmed. | It is incomplete for a full architecture document because it excludes the frontend and treats status-transition rules as unavailable. Its `.env` claim appears only in this draft and is not supported by A or B, so it should not be carried forward without separate verification. | Focused documentation or review tasks centered on a small, known set of implementation files, especially when avoiding unsupported claims is the priority. |

## Verdict

I chose Strategy B for the final architecture document because it provides the strongest project-level account: it includes the API, frontend, data rules, and explicitly available project guidance without narrowing the document to only a few implementation anchors. I would retain B’s structure, avoid its non-portable local file links, and include only additional A or C details after independently verifying them.

## Context-engineering rule

For task shape: a repository-wide architecture summary that needs code behavior, project conventions, and user-facing flow, I use Strategy B because structured context supplies both breadth and the governing rules needed to connect the pieces accurately.

For task shape: a narrowly scoped implementation explanation based on a defined set of files, I use Strategy C because targeted anchors make unsupported assumptions easier to identify and exclude.
