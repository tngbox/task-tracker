# Final AI Review and Ownership Evidence

## AGENTS.md guardrails
- Repo-specific stack and commands included: yes
- Docs-first/read-first guardrail included: yes
- Unexpected app/frontend edits rule included: yes

## AI code review mini-log
| AI comment | Grade: Useful / Noise / Wrong | Reason | Verification or decision |
|---|---|---|---|
| Add an exact Final Project command block in README for local run, tests, and Docker. | Useful | Improved grading clarity and reproducibility. | Accepted; README Final Project section now uses exact runnable commands. |
| Keep Docker health verification on `localhost:8000` while run mapping is `8001:8000`. | Wrong | The endpoint must match the mapped host port. | Rejected as-is; corrected README and release evidence to use `localhost:8001/health`. |
| Keep only `docker run -p 8000:8000` in evidence. | Noise | Local environment had host port 8000 already allocated during verification. | Corrected to `-p 8001:8000` for proof run and documented why. |

## AI security mini-review
| Finding | File evidence | Grade: Valid / False Positive / Noise | Reason | Next action |
|---|---|---|---|---|
| Container runs as non-root user. | `Dockerfile` (`USER app`) | Valid | Clear least-privilege control is present. | Keep as-is; no change required. |
| `.env` and secret-like env files are excluded from Docker build context. | `.dockerignore` (`.env`, `.env.*`, `!.env.example`) | Valid | Reduces accidental secret bake-in risk. | Keep as-is; continue review before image publish. |
| No auth + permissive CORS means immediate defect for this submission. | `AGENTS.md`, `app/main.py` | Noise | This repository is intentionally local-scope learning project; no production deployment claimed. | Keep documented scope and avoid production claims. |

## Manual security check
I manually checked CI shortcut risks and container health behavior instead of copying AI text. I ran `findstr` checks on `.github/workflows/ci.yml` to confirm pytest and dependency install steps are present and no `continue-on-error` pattern is used. I also ran the container and verified `/health` returned HTTP 200. This matters because it validates both process safety and runtime readiness with direct evidence.

## One AI output I rejected or corrected
AI suggested keeping Docker health verification on `localhost:8000` even when the run command mapped host `8001:8000`. I did not accept that as-is because it mismatches the mapped host port and can produce a false-negative check. I corrected the command and evidence to use `http://localhost:8001/health`.

## Three AI usage rules
1. Never paste: secrets, tokens, `.env` values, credentials, private keys, or real customer data.
2. Always verify: commands, test results, and runtime behavior before accepting AI claims.
3. Record AI contributions by: logging what AI suggested, what files/commands were checked, and why each suggestion was accepted, corrected, or rejected.

## Ownership statement
I am comfortable submitting this repository as my work because I validated accepted AI suggestions against real files, commands, and outputs. I kept the project scope constrained to final-project requirements and avoided feature expansion. I explicitly rejected suggestions that were not verifiable from available evidence. I can explain each changed line in the final docs and each command outcome used to support them. I remain responsible for the final state I submit.
