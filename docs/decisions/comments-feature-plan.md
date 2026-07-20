# Comments on Tasks — Design Plan

## 1. Data Model

Add comment schemas to `app/models.py`, alongside the existing `TaskCreate`,
`TaskUpdate`, and `TaskResponse` Pydantic models.

Proposed model responsibilities:

- `CommentCreate`
  - Accepts only `author` and `body`.
  - Uses `extra="forbid"`, matching the task payload convention.
  - Validates `author` after trimming: required, 1–100 characters.
  - Validates `body` after trimming: required, 1–2000 characters.
  - Does not accept `id`, `task_id`, or `created_at`; those are server-owned.
- `CommentResponse`
  - Contains `id`, `task_id`, `author`, `body`, and `created_at`.
  - Uses the same `datetime` response-field pattern as `TaskResponse`.

`task_id` should come from the URL path rather than the create request body.
This prevents a client from submitting a body whose task reference disagrees
with the URL.

Do not reuse the existing title validator unchanged: it encodes task-title-
specific limits (200 characters), while comments need different limits. A
small reusable trimmed-string validator with a supplied field name and maximum
length would fit the model-layer validation pattern.

## 2. API Routes

Add routes to `app/main.py`, which currently owns all HTTP route handlers and
delegates persistence to `app/storage.py`.

| Method | Path | Request body | Success response | Error cases |
| --- | --- | --- | --- | --- |
| POST | `/tasks/{task_id}/comments` | `CommentCreate` (`author`, `body`) | 201 with `CommentResponse` | 404 if task is absent; 422 for invalid/blank/overlong fields or unknown fields |
| GET | `/tasks/{task_id}/comments` | None | 200 with `list[CommentResponse]`, including `[]` for an existing task with no comments | 404 if task is absent |

Route behavior should match existing task conventions:

- Verify that the parent task exists before creating or listing comments, as
  the task routes already turn missing resources into explicit HTTP 404
  responses.
- Let Pydantic perform field-shape validation and emit HTTP 422, as existing
  create/update routes do.
- Keep route handlers thin: route code should coordinate task existence and
  call storage helpers; ID and timestamp creation belong in storage.
- Do not change existing task response shapes. Comments should initially be
  retrieved through their own endpoint.

## 3. Tests

Extend `tests/test_tasks.py`, which uses the real FastAPI app through
`TestClient`, and rely on the existing autouse storage reset fixture in
`tests/conftest.py`.

### Happy path

- `test_create_comment_valid_returns_201_with_full_body`
- `test_create_comment_sets_uuid_and_utc_created_at`
- `test_list_comments_for_existing_task_returns_200_and_comments`
- `test_list_comments_for_existing_task_with_none_returns_200_and_empty_list`
- `test_list_comments_returns_only_comments_for_requested_task`

### Validation

- `test_create_comment_missing_author_returns_422`
- `test_create_comment_blank_author_returns_422`
- `test_create_comment_author_over_100_characters_returns_422`
- `test_create_comment_missing_body_returns_422`
- `test_create_comment_blank_body_returns_422`
- `test_create_comment_body_over_2000_characters_returns_422`
- `test_create_comment_unknown_field_returns_422`
- `test_create_comment_client_supplied_id_or_created_at_returns_422`
- `test_create_comment_client_supplied_task_id_returns_422` if `task_id` is
  intentionally path-owned only

### Edge cases

- `test_create_comment_for_missing_task_returns_404`
- `test_list_comments_for_missing_task_returns_404`
- `test_comments_are_cleared_by_test_storage_reset`
- `test_multiple_comments_preserve_their_task_id`
- `test_comment_order_matches_the_decided_contract`

The final ordering test depends on a product decision; no comment ordering
convention is visible in the existing repository.

## 4. Frontend Changes

The only frontend file currently visible is `frontend/index.html`. It contains
the markup, styles, and JavaScript in one file; task cards are built by
`createTaskCard`, and task create/edit behavior uses the existing modal.

Planned changes to that file:

- Add a comments area associated with a selected task—most naturally in the
  existing task modal, or in a separate task-detail view if the team prefers
  not to expand the modal.
- Fetch comments from `GET /tasks/{task_id}/comments` when the comment area
  opens.
- Add inputs for author and body plus a submit action that calls
  `POST /tasks/{task_id}/comments`.
- Render author, body, and created time from each returned `CommentResponse`.
- Maintain loading, empty, error, and populated states for comments,
  consistent with the project guardrail in `AGENTS.md`.
- Escape comment text before insertion into generated HTML, following the
  existing `escapeHtml` pattern used for task content.

The UI should not allow a user to choose `task_id`; it is determined by the
task whose comments are being displayed.

## 5. Migration Notes

No database migration is needed because `app/storage.py` uses in-memory
dictionaries and the project intentionally has no database.

Storage design changes needed:

- Add in-memory comment storage keyed by comment ID, plus a lookup approach
  for comments belonging to one task.
- Generate comment UUIDs and UTC `created_at` values in storage, matching task
  ID/timestamp ownership.
- Update `_reset()` so test isolation clears comments as well as tasks.
- Decide task-deletion behavior before implementation. The existing task delete
  helper only removes the task; without a defined comment policy, comments
  could become orphaned in storage.

Existing task data needs no shape migration if comments stay in separate
storage and are returned through separate routes. All state, including
comments, will be lost on restart under the existing in-memory design.

## 6. Open Questions

1. When a task is deleted, should its comments be deleted automatically,
   retained as orphaned data, or should deletion be blocked?
2. Should comments be immutable, or should the app later support editing and
   deleting them?
3. In what order should comments be returned: oldest-first or newest-first?
4. Should the frontend show comments inside the existing edit modal or
   introduce a separate task-detail interface?
5. The repository intentionally has no authentication. Is free-text `author`
   sufficient for this learning feature, or should the API later derive
   authorship from an authenticated user?
6. Should comment listing add pagination before any future persistent or
   multi-user version?

## Files read

- `AGENTS.md`
- `README.md`
- `app/main.py`
- `app/models.py`
- `app/storage.py`
- `app/business_rules.py`
- `tests/conftest.py`
- `tests/test_tasks.py`
- `frontend/index.html`

## Assumptions to verify

- No comment model, route, or storage implementation is currently visible.
- No comment-specific frontend test setup is visible.
- The intended feature includes creation and listing only; edit/delete comment
  behavior is not specified.
- The comment ordering contract is not specified.
- The supplied `task_id` requirement is interpreted as a field of the
  stored/returned comment, with the path parameter as its source.

## Module 5 Plan Critique

| Section | Label | Evidence | Minimal correction |
| --- | --- | --- | --- |
| Data Model | Right | The plan places schemas in `app/models.py` alongside the existing request/response models, preserves server-owned fields, and recognizes that the title validator's 200-character rule cannot be reused unchanged. | None. |
| API Routes | Right | It follows the repository's existing route/storage split: routes in `app/main.py`, persistence in `app/storage.py`, with explicit 404 and Pydantic-driven 422 behavior. | None. |
| Tests | Needs-Resequencing | The proposed tests match the existing `TestClient` and storage-reset conventions, but ordering and task-deletion policy are still unresolved in the Open Questions section. Tests for those behaviors should follow an agreed contract. | Move deletion and ordering decisions before finalizing the edge-case test list. |
| Frontend Changes | Right | It identifies the actual single-file frontend, `frontend/index.html`, its current modal/card pattern, and the required loading, empty, error, and populated states from `AGENTS.md`. | None. |
| Migration Notes | Right | It accurately notes the visible in-memory dictionary storage and no-database design, including the need to update the test reset path and decide whether task deletion cascades to comments. | None. |
| Open Questions | Right | It identifies real undecided product and design choices not visible in the repo: deletion behavior, edit/delete scope, ordering, UI location, authorship, and pagination. | None. |

## Generic vs. Repo-Grounded Plan Comparison

- **Biggest difference:** The generic plan describes a sensible comments
  feature, while the repo-grounded plan maps it to this repository's actual
  models, route/storage layering, test fixture pattern, and one-file frontend.
- **Plan I would hand to a teammate and why:** The repo-grounded plan, because
  it cites the implementation locations and explicitly preserves existing
  constraints rather than assuming a generic architecture.
- **A task shape where generic chat is enough:** Early requirements exploration
  for a new feature before repository access, when the goal is to identify
  decisions and acceptance criteria rather than assign files or tests.
