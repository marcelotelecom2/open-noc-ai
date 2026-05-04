# Command — Create Endpoint

## Task

Create or update FastAPI endpoints for an entity.

## Required Context

Read:

1. AGENTS.md
2. .ai/rules/api.md
3. .ai/rules/multi-tenant.md
4. existing endpoint files
5. router registration pattern

## Rules

Endpoints must:

- use APIRouter
- use schemas
- call crud functions
- be registered in router
- be visible in Swagger
- preserve tenant isolation

## Required Endpoints

Only create requested endpoints.

Common endpoints:

- POST /
- GET /
- GET /{id}
- PUT or PATCH /{id}
- DELETE /{id}

## Forbidden

Do not:

- create direct database logic in endpoint
- skip schema validation
- expose data across tenants
- change unrelated routes
- introduce service layer unless explicitly requested

## Output

Return:

- files changed
- endpoints created/updated
- router registration status
- Swagger validation checklist