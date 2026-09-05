# AI Dev Tools 2026 — Homework

DataTalks.Club "AI Dev Tools" course. Building apps with an AI coding agent (Claude Code in VSCode).

## Lesson 1 — Shared Household Chores

Turn a vague idea ("a tool for managing shared household chores") into a spec, a backlog, and a working Django app.

- [`Lesson_1/README.MD`](Lesson_1/README.MD) — homework instructions
- [`Lesson_1/_docs/plan.md`](Lesson_1/_docs/plan.md) — project scope / spec
- [`Lesson_1/_docs/backlog.md`](Lesson_1/_docs/backlog.md) — task backlog

### Run

```bash
cd Lesson_1
uv sync
uv run python manage.py migrate
uv run python manage.py runserver
```

### Stack

Django 5.2 (backend + templates), SQLite, managed with `uv`.
