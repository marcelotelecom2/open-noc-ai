# Testing Rules — open-noc-ai

## Minimum Validation

Every new entity must be validated for:

- create
- list
- get by id
- update
- soft delete
- tenant isolation

## Required Test Areas

Use this structure when possible:

tests/
├── api/
├── crud/
├── models/
└── multi_tenant/

## Critical Tests

Multi-tenant tests are mandatory for SaaS readiness.

Validate that:

- tenant A cannot read tenant B data
- tenant A cannot update tenant B data
- tenant A cannot delete tenant B data

## Before Finishing

Confirm:

- imports work
- app starts
- Swagger loads
- endpoint works
- data persists
- no broken tests