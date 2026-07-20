# User Stories

## Feature A: Due Dates

### Story A1
As a user, I want to set an optional due date when creating a task so I can plan deadlines.

Acceptance criteria:
- Given I open create task modal, when I enter a valid date in `YYYY-MM-DD`, then task saves successfully.
- Given I do not enter a due date, when I save, then task still saves successfully.
- Given I enter invalid date format, when I save, then API returns 422 and task is not saved.

### Story A2
As a user, I want to edit a task due date so deadlines can change over time.

Acceptance criteria:
- Given an existing task, when I patch `due_date` with a valid date, then returned task includes new date.
- Given an existing task with due date, when I patch `due_date: null`, then due date is cleared.

### Story A3
As a user, I want to see due date on each task card so deadlines are visible during board review.

Acceptance criteria:
- Given a task has due date, when board renders, then card shows `Due: YYYY-MM-DD`.
- Given a task has no due date, when board renders, then no due date row is shown.

AI assumption corrected (Feature A):
- Initial AI tendency was to use full datetime (`due_at`) and timezone conversion. We corrected this to date-only (`due_date`) to match project simplicity and avoid timezone complexity.

## Feature B: Overdue Filter

### Story B1
As a user, I want overdue tasks highlighted so I can prioritize late work.

Acceptance criteria:
- Given a task due date is before today UTC and status is not `Done`, then card shows `Overdue` pill.
- Given a task due date is before today but status is `Done`, then `Overdue` pill is not shown.

### Story B2
As a user, I want to filter only overdue tasks so I can focus on urgent backlog.

Acceptance criteria:
- Given I set filter to `Overdue only`, when tasks reload, then only overdue tasks are shown.
- Given no overdue tasks exist, when filter is `Overdue only`, then board shows empty columns.

### Story B3
As a user, I want to view not-overdue tasks so I can plan upcoming work.

Acceptance criteria:
- Given I set filter to `Not overdue`, when tasks reload, then overdue tasks are excluded.
- Given tasks with future and null due dates exist, when filter is `Not overdue`, then those tasks remain visible.

AI assumption corrected (Feature B):
- AI initially split overdue logic between backend and frontend inconsistently. We corrected to canonical backend filtering (`overdue=true|false`) plus frontend display helper only for visual pill rendering.
