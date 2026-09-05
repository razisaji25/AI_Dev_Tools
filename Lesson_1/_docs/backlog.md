# Backlog — Shared Household Chores (Django)

Derived from [`plan.md`](plan.md). Small, dependency-ordered tasks. Each is one focused commit.

---

## Task 1 — Project scaffolding *(DONE)*
- `uv add django`, `django-admin startproject config .`, `manage.py startapp chores`
- Register `chores` in `INSTALLED_APPS` (`config/settings.py`)
- Run initial `migrate`; `manage.py check` passes
- **Status:** complete

## Task 2 — Core data models
- In `chores/models.py`: `Household`, `Membership` (User↔Household, role, rotation position),
  `Chore` (household, title, description, points, recurrence, due date, current assignee),
  `ChoreCompletion` (chore, completed_by, completed_at, points_awarded, period)
- `makemigrations` + `migrate`
- Register all models in `chores/admin.py`

## Task 3 — Authentication
- Signup, login, logout using `django.contrib.auth`
- Login-required redirect; base template with nav showing auth state

## Task 4 — Household create / join
- Create a household (creator becomes owner + first member)
- Join via invite code; leave household
- Scope all later views to the user's current household (data isolation)

## Task 5 — Chore CRUD
- List / create / edit / delete chores within the current household
- Fields: title, description, points, due date, recurrence, rotation order

## Task 6 — Assignment & rotation
- Set rotation order (list of members) per chore
- On completion of a recurring chore, advance assignee to next member
- Manual override: reassign a chore to any member anytime

## Task 7 — Complete a chore
- "Mark done" action → create `ChoreCompletion`, award points immediately (trust-based)
- Generate the next occurrence for recurring chores

## Task 8 — Fairness dashboard
- Per-member point totals for the current period
- Simple bar/table view; define period (e.g. rolling 7 days)

## Task 9 — Overdue display
- Chores past due date render in red in the list
- No notifications, no auto-reassign (per plan)

## Task 10 — Responsive templates & styling
- Mobile-first CSS; usable in a phone browser
- Consistent base layout, forms, list views

## Task 11 — Tests
- Models: point awarding, rotation advance, overdue detection
- Views: auth required, household data isolation, chore CRUD, completion flow
- Run with `python manage.py test`
