# Architecture Rules — open-noc-ai

## Core Backend Pattern

Every backend entity must follow:

model → schema → crud → endpoint → router

Do not skip layers.

## Responsibilities

### models/

Represents database tables and relationships.

### schemas/

Validates API input and output using Pydantic.

### crud/

Contains database operations, tenant filtering, soft delete behavior and basic persistence logic.

### api/

Exposes FastAPI endpoints.

### core/

Contains configuration, security and logging.

### db/

Contains database session, base and initialization.

## Current Pattern

The active backend pattern is:

model → schema → crud → endpoint → router

## Future Extension

A service layer may be introduced later only when business logic becomes complex enough to justify orchestration.

Future pattern:

model → schema → crud → service → endpoint → router

Until then, endpoints must call crud functions directly.

## Forbidden

Do not:

- create new architectural patterns without instruction
- move files without instruction
- refactor unrelated code
- mix endpoint logic with database logic
- access database directly from endpoint
- introduce complex abstractions prematurely

## Required Behavior

Always:

- follow existing patterns
- keep logic explicit
- keep functions small
- maintain readable code
- preserve project structure