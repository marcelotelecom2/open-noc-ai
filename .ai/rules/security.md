# Security Rules — open-noc-ai

## Security Priorities

The platform must protect:

- tenant isolation
- credentials
- API access
- operational data
- automation actions

## Forbidden

Never:

- expose secrets
- commit .env files
- log passwords or tokens
- return stack traces to API clients
- bypass tenant validation
- execute automation without explicit control

## Required

Always:

- validate inputs
- avoid hardcoded credentials
- use environment variables
- keep security logic explicit
- ensure tenant-scoped access

## Sensitive Operations

Automation and network execution features must be auditable.

Every future automation action should have:

- who requested
- tenant
- target
- action
- timestamp
- result