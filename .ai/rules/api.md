# API Rules — open-noc-ai

## API Framework

The backend uses FastAPI.

## Endpoint Rules

Endpoints must:

- use APIRouter
- use Pydantic schemas
- call crud functions
- avoid direct database logic
- expose clear RESTful routes
- be visible in Swagger
- return predictable responses

## Naming

Use plural resource names:

- /customers
- /sites
- /carriers
- /links
- /devices

## HTTP Methods

Use:

- POST for create
- GET for read/list
- PUT or PATCH for update
- DELETE for soft delete

## Forbidden

Do not:

- create ambiguous routes
- return raw internal errors
- bypass schemas
- expose cross-tenant data
- create endpoints without tenant validation
- query the database directly from endpoints

## Required Validation

Before finishing:

- Swagger loads correctly
- endpoint imports work
- route is registered in router
- request schema validates input
- response schema is consistent
- endpoint calls the crud layer