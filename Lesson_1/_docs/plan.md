# Shared Household Chores — Project Scope

## One-line idea
A tool for managing shared household chores.

## Target users
A generic, multi-tenant web tool that any household can sign up and use.

## Core decisions

| # | Topic | Decision |
|---|-------|----------|
| 1 | Audience | Generic tool — multiple households sign up and use one deployment |
| 2 | Tenancy | Full multi-tenant: user accounts; each user creates or joins a household; all data isolated per household |
| 3 | Chore model | Rich: title, assignee, done/not-done, due date, recurrence (daily/weekly/custom), rotation, and points |
| 4 | Fairness | Points per chore. Dashboard shows each member's point total for the current period |
| 5 | Assignment | Rotation by default (set an order once, system cycles it each recurrence); manual override allowed anytime |
| 6 | Overdue handling | No automation — overdue chores just render as overdue (red) in the list |
| 7 | Completion | Trust-based — marking done awards points immediately; no verification/approval step |
| 8 | Form factor | Responsive web app that works well in a phone browser |
| 9 | Stack | **Django** (Python). Handles backend logic *and* the frontend via Django templates (server-side rendered HTML). Managed with `uv` |
| 10 | Storage | SQLite (single file, zero setup) |

## Out of scope
- No native mobile app; no real-time push / websockets
- No payments or points-redemption / rewards store
- No external calendar integrations (Google Calendar, iCal, etc.)
- No admin analytics beyond the fairness dashboard

## Feature summary (2–4 headline features)
1. **Multi-tenant households** — sign up, create/join a household, per-household data isolation
2. **Recurring chores with rotation** — recurrence + auto-assign to the next person each cycle, with manual override
3. **Points-based fairness dashboard** — every completed chore earns points; dashboard shows per-member totals for the period
4. **Trust-based completion** — one tap marks done and awards points; overdue chores shown in red, no automation

## Architecture
- **Django is the backend** — a Python web framework: URL routing, views, ORM, auth, admin.
- It **also serves the frontend** using its built-in template engine (server-side rendered HTML pages + a little CSS). No separate JS framework.
- So the single Django project is "full-stack", but Django's core role is backend.

## Data model sketch
- **User** — auth, name
- **Household** — name; has many members (Users) via Membership
- **Membership** — User ↔ Household, role (owner/member), rotation position
- **Chore** — household, title, description, points, recurrence rule, due date, rotation order (list of memberships), current assignee
- **ChoreCompletion** — chore, completed_by, completed_at, points_awarded, period

## Open questions for later
- Recurrence rule format (simple enum vs. cron-like vs. RRULE)
- Period definition for the fairness dashboard (rolling 7 days? calendar week? month?)
- What happens to a rotation when a member leaves the household
