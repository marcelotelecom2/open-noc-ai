# Command — Create Schema

## Task

Create or update Pydantic schemas for an entity.

## Required Context

Read:

1. AGENTS.md
2. .ai/rules/api.md
3. .ai/rules/naming.md
4. existing schemas from similar entities

## Required Schemas

Use project pattern, usually:

- EntityBase
- EntityCreate
- EntityUpdate
- EntityRead or EntityResponse

## Rules

Schemas must:

- validate API input
- define API output
- avoid exposing internal-only fields unnecessarily
- keep tenant handling consistent with project pattern

## Forbidden

Do not:

- bypass validation
- expose sensitive fields
- create inconsistent schema names
- invent new schema patterns

## Output

Return:

- files changed
- schemas created/updated
- validation checklist