# Development Workflow

This document defines the recommended local and assisted-development setup for
open-noc-ai.

The goal is to keep every change predictable, testable, tenant-safe, and easy to
review across local tools and GitHub.

## Tool Roles

### WSL

WSL is the runtime source of truth.

Use WSL to run:

- database services
- backend dependencies
- Alembic migrations
- FastAPI
- automated tests
- Swagger validation

All runtime validation must happen in WSL before a pull request is considered
ready.

### VS Code with Codex

VS Code with Codex is the primary implementation surface.

Use it for:

- editing focused code changes
- following existing model, schema, crud, endpoint, and router patterns
- fixing local test failures
- inspecting related files while implementing a feature
- making small, reversible changes

Do not use it to perform broad refactors unless the task explicitly requires
that scope.

### Codex App

Codex App is the local agent cockpit.

Use it for:

- planning local tasks against the checked-out repository
- reviewing the current diff before commit
- coordinating longer local work sessions
- checking architecture, tenant isolation, migrations, and tests before push
- preparing concise pull request summaries

Codex App does not replace runtime validation. WSL remains the source of truth
for running the application, migrations, tests, and Swagger.

### Codex Web and GitHub

Codex Web and GitHub are the remote review layer.

Use them for:

- pull request review
- architecture review against AGENTS.md and .ai/rules
- detecting tenant-isolation regressions
- reviewing migration safety
- checking that the change stayed within scope

Codex Web should act as an independent reviewer, not as the primary local
executor.

### GitHub Actions

GitHub Actions should be the automated quality gate.

CI should validate at minimum:

- backend imports compile
- automated tests pass
- Alembic migrations run against a clean database

## Recommended Flow

1. Plan the change in Codex App or Codex Web.
2. Implement the change in VS Code with Codex.
3. Validate runtime behavior in WSL.
4. Review the local diff in Codex App.
5. Commit and push the branch.
6. Open a pull request in GitHub.
7. Request Codex Web or GitHub review.
8. Fix review comments locally.
9. Re-run WSL validation.
10. Merge only after tests, migrations, Swagger, and review are clean.

## Local Validation Checklist

Run these checks before pushing a feature branch:

```bash
cd backend
python -m compileall app tests
python -m unittest discover -s tests -v
alembic upgrade head
uvicorn app.main:app --reload
```

Then open Swagger:

```text
http://localhost:8000/docs
```

Validate that the affected v1 endpoints are visible and respond correctly.

## Multi-Tenant Review Checklist

For every persistent entity, confirm:

- the model has tenant_id
- all queries filter explicitly by tenant_id
- endpoints call crud functions instead of accessing the database directly
- tenant A cannot read tenant B data
- tenant A cannot update tenant B data
- tenant A cannot delete tenant B data
- soft delete is used instead of hard delete
- schemas match the model fields exposed by the API
- migrations match the SQLAlchemy models

## Prompt Template

Use this prompt when asking any Codex surface to modify the project:

```text
You are working on open-noc-ai.

Before changing code:
1. Read AGENTS.md.
2. Read relevant .ai/rules files.
3. Read the target file.
4. Read similar existing files.
5. Follow the active pattern: model -> schema -> crud -> endpoint -> router.
6. Do not create a service layer.
7. Keep the change minimal and reversible.

Requirements:
- every persistent entity must be tenant-scoped
- every query must explicitly filter by tenant_id
- endpoints must call crud functions
- use soft delete where deletion is needed
- do not modify unrelated files

After changing code:
- run tests
- validate migrations
- confirm Swagger loads
- summarize files changed and validation performed
```

## Branch Discipline

Use one branch per focused change.

Recommended examples:

```bash
git checkout main
git pull
git checkout -b feat/monitoring-checks
```

Keep pull requests small enough for Codex App, Codex Web, and human review to
reason about safely.

