# Lesson 1: AI-Native Developer Workflow

In this Lesson, we'll build an application with AI — but instead of us handing you a finished spec, you'll turn a vague idea into one yourself, then implement it in Django.

## Lesson From Data Talk Club Idea

For this Lesson, we start with a very vague idea:

> A tool for managing shared household chores

We don't specify anything else, and most of you will finish with different homework solutions.

In this homework, we want to turn this vague description into a clear specification.


## 1: Select your coding agent

You can use any coding agent you want. Which one did you choose? 

In This Section We use Claude Code in VSCode


## Question 2: Turn the idea into a spec

Open a chat assistant and brainstorm with a prompt like:

```text
I want to build a tool for managing shared household chores.

Help me set the scope for this homework precisely. I want to brainstorm with you
and understand how the tool should work. Give me options.

Ask me one question at a time and keep your output short.
```

Answer its questions, then ask it to save everything to a markdown file. 

What are the 2-4 features your spec settled on?
Examples
1. C. A generic tool other households could sign up and use
2. A. Full multi-tenant: user accounts, each user joins/creates a household, data isolated per household
3. C. + Rotation (auto-assign to next person each cycle) and points/fairness tracking
4. A. Points per chore; dashboard shows each person's total for the period
5. C. Both: rotation by default, manual override anytime
6. A. Nothing automatic — just show it as overdue (red) in the list
7. A. Trust-based: mark done, points awarded immediately
8. A. Web app (responsive, works on phone browser)
9. A. Python backend (FastAPI/Flask) + simple frontend
10. A. SQLite (single file, zero setup)


## GitHub Repository

Create an empty GitHub repository, clone it locally. Create two files there:

- `.gitignore`
- `README.md`
- `_docs/plan.md` with the plan

Commit and push.

## Question 3: Django project

For this homework we'll use Django. 

Ask your agent to install Django and create a project and an app for it. At some point, you will need to include the app you created in the project.

What's the file you need to edit for that?

- `settings.py` <------ Setting register Apps
- `manage.py`
- `urls.py`
- `wsgi.py`

For this and next questions you can ask your coding assistant to select the correct option.


## Question 4: Backlog

Then give your agent the `plan.md` and ask it to propose a small backlog of tasks for building this in Django. Write the result to `backlog.md`.

What's task 1 in the backlog your agent came up with?

## Task 1 — Project scaffolding *(DONE)*
- `uv add django`, `django-admin startproject config .`, `manage.py startapp chores`
- Register `chores` in `INSTALLED_APPS` (`config/settings.py`)
- Run initial `migrate`; `manage.py check` passes
- **Status:** complete


## Question 5: First version

Implement the first few tasks. Just open your agent and say:

```
Implement task #1 from backlog.md
```

Run the server. Which command do you use to start the Django development server?

- `uv run python manage.py runserver` <---start server apps
- `uv run django-admin startserver`
- `python manage.py start`
- `uv run python app.py runserver`



## Question 6: Tests

After implementing a few items from the backlog, let's make sure the code is covered with tests. 

- Tell the agent we want to cover the code with tests
- Ask it which scenarios we should cover
- Make sure they make sense
- Let it implement them and run them

What's the command you use for running tests in the terminal?

- `pytest`
- `python manage.py test` <---- Answers
- `python -m django run_tests`
- `django-admin test`
