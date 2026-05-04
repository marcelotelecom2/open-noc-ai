# Database Rules — open-noc-ai

## ORM

Use SQLAlchemy patterns already present in the project.

## Model Requirements

Every persistent entity should include:

- id
- tenant_id
- created_at
- updated_at
- is_active

Use soft delete with is_active.

## Forbidden

Do not:

- hard delete records
- create tables without tenant_id
- create fields with unclear meaning
- create relationships without checking existing patterns
- introduce database behavior that is not explicit

## Migrations

If database structure changes, migration must be considered.

When applicable:

- create Alembic migration
- verify migration runs
- verify database schema matches model

## Data Integrity

Use foreign keys where relationships exist.

Examples:

- Site belongs to Customer
- Link belongs to Site
- Device belongs to Site
- Carrier belongs to Tenant