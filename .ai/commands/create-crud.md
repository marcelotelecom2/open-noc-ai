# Command — Create CRUD

## Task

Create or update CRUD functions for an entity.

## Required Context

Read:

1. AGENTS.md
2. .ai/rules/architecture.md
3. .ai/rules/database.md
4. .ai/rules/multi-tenant.md
5. similar crud files

## Required Operations

Implement only requested operations.

Common operations:

- create
- get
- list
- update
- soft delete

## Rules

CRUD functions must:

- apply tenant_id filters
- avoid cross-tenant access
- use soft delete
- keep logic explicit
- return predictable results
- follow existing crud pattern

## Forbidden

Do not:

- hard delete
- query without tenant_id
- mix API response formatting into crud logic
- change unrelated crud files
- introduce service layer unless explicitly requested

## Output

Return:

- files changed
- functions created/updated
- tenant validation explanation
- validation checklist