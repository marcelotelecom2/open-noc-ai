# Command — Create Model

## Task

Create or update a SQLAlchemy model for open-noc-ai.

## Required Context

Before coding:

1. Read AGENTS.md
2. Read .ai/rules/architecture.md
3. Read .ai/rules/database.md
4. Read .ai/rules/multi-tenant.md
5. Read similar models

## Rules

The model must:

- follow existing SQLAlchemy pattern
- use UUID primary key if that is the project pattern
- include tenant_id
- include created_at
- include updated_at
- include is_active for soft delete
- define relationships only if needed
- avoid unnecessary complexity

## Forbidden

Do not:

- create new architecture
- change unrelated models
- introduce hard delete
- remove tenant isolation
- add fields not requested

## Output

Return:

- files changed
- model created/updated
- assumptions made
- validation checklist