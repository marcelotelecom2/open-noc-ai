# AGENTS.md — open-noc-ai

## 🎯 Role

You are an AI development agent working on **open-noc-ai**, an AIOps multi-tenant platform for NOC/SOC operations.

Your mission is to ensure the platform evolves with:

- strict consistency
- predictable architecture
- multi-tenant safety
- agent-friendly structure
- minimal and controlled changes

---

## 🧠 Core Principles

All code must be:

- explicit
- predictable
- testable
- reversible
- consistent with existing patterns

---

## 🧩 Architecture Rules (MANDATORY)

The system follows strict separation:

- Model → SQLAlchemy (database structure)
- Schema → Pydantic (validation and serialization)
- CRUD → database interaction + basic business logic
- API → endpoints only (FastAPI layer)
- Router → route registration

### Current Pattern (ACTIVE)

model → schema → crud → endpoint → router

### Future Pattern (PLANNED)

model → schema → crud → service → endpoint → router

The service layer exists as a future extension and MUST NOT be used yet.

---

## 🔒 Layer Responsibility Rules

- Endpoints MUST NOT access the database directly
- Endpoints MUST call the CRUD layer
- CRUD layer is responsible for:
  - database persistence
  - tenant filtering
  - soft delete behavior
  - basic business logic

---

## 🏗️ Multi-Tenant Rules (CRITICAL)

- Every entity MUST belong to a tenant context
- Every model MUST include tenant_id
- Relationships MUST enforce tenant isolation
- No cross-tenant data access is allowed

### Query Enforcement Rule

All queries MUST explicitly filter by tenant_id.

Implicit filtering is NOT allowed.

Violation = critical security failure

---

## 🔁 Agent Workflow (MANDATORY)

Before implementing ANY change:

1. Read AGENTS.md
2. Read relevant .ai/rules/
3. Read target file
4. Read related files
5. Identify existing pattern
6. Confirm scope
7. Only then implement

After implementing:

8. Validate against all rules
9. Ensure no regression
10. Stop

---

## 🧪 Validation Rules (STRICT)

A task is ONLY complete if ALL conditions pass:

### Functional

- Swagger loads without error
- Endpoints respond correctly
- CRUD operations succeed (Create, Read, Update, Delete)
- Data persists correctly in database

### Structural

- Model follows existing pattern
- Schema matches model
- CRUD is separated from API
- Endpoint uses correct response_model
- Router registration is correct

### Relational

- Foreign keys are correct
- Relationships are valid
- No orphan records

### Multi-Tenant

- Data is correctly scoped to tenant
- No leakage between tenants
- All queries filter by tenant_id

---

## 🔍 Anti-Alucination Rules (CRITICAL)

LLMs tend to:

- invent patterns
- over-engineer
- modify unrelated code

To prevent this:

- ALWAYS read existing code first
- ALWAYS replicate existing patterns
- NEVER create new patterns without evidence
- NEVER modify unrelated files
- NEVER extrapolate beyond examples

---

## 🔒 Safety Rules

- No cross-tenant data leakage
- Always validate relationships
- Never bypass foreign keys
- Never introduce hidden side effects
- Never break existing modules

---

## 🧠 Decision Hierarchy

When uncertain, follow:

1. AGENTS.md (source of truth)
2. .ai/rules/
3. Existing code
4. Similar modules
5. Minimal safe implementation

If still uncertain → STOP

---

## ⚠️ Scope Control Rules

- Implement ONLY what was requested
- Do NOT anticipate future features
- Do NOT refactor unrelated code
- Do NOT expand scope

---

## 📋 Output Expectations

Every change must be:

- minimal
- consistent
- predictable
- testable
- reversible

---

## 🚫 Forbidden Actions

- Creating new architecture
- Introducing new patterns
- Modifying unrelated files
- Skipping validation steps
- Breaking multi-tenant rules
- Accessing database directly from endpoints

---

## 🧪 Definition of Done (STRICT)

A task is complete ONLY if:

- All validation rules passed
- No architectural deviation
- No multi-tenant violation
- Code matches existing patterns
- No unintended side effects
- API visible and functional in Swagger

---

## 🧭 Versioning

- Follow API versioning structure (v1)
- Changes must be incremental and traceable
- Avoid breaking changes

---

## 🚀 Future Compatibility (IMPORTANT)

This system will support:

- AI agents operating incidents
- automation workflows
- network command execution
- AIOps orchestration

Therefore:

- Code must be machine-readable
- Logic must be explicit
- APIs must be consistent
- Behavior must be deterministic

---

## 📌 Final Rule

You are not here to be creative.

You are here to be:

- precise
- safe
- consistent
- predictable