# Multi-Tenant Rules — CRITICAL

Multi-tenant isolation is non-negotiable.

## Core Rule

Every tenant-scoped entity must include tenant_id.

## Model Rule

Every model must include:

- tenant_id
- foreign key to tenants.id when Tenant model exists
- non-null tenant reference

## Query Rule

Every query must filter by tenant_id.

Correct:

db.query(Model).filter(Model.tenant_id == tenant_id)

Incorrect:

db.query(Model).all()

## Endpoint Rule

Endpoints must never return data from another tenant.

## CRUD Rule

CRUD functions must enforce tenant filtering.

The crud layer is responsible for:

- create with tenant_id
- list filtered by tenant_id
- get filtered by tenant_id
- update filtered by tenant_id
- soft delete filtered by tenant_id

## Relationship Rule

Relationships must respect tenant isolation.

Example:

A Site must belong to a Customer from the same tenant.

## Security Classification

Any cross-tenant data access is a critical security issue.

## Before Finishing

Validate:

- tenant_id exists
- create uses tenant_id
- list filters by tenant_id
- get filters by tenant_id
- update filters by tenant_id
- soft delete filters by tenant_id