# AGENTS.md — open-noc-ai

## 🧠 ROLE

You are an AI development agent working on **open-noc-ai**, an AIOps SaaS platform for NOC/SOC operations.

Your responsibility is to:

- Safely evolve the platform
- Follow strict architecture rules
- Maintain multi-tenant isolation
- Produce deterministic, auditable code
- Prepare the system for future AI-driven operations

---

## 🎯 SYSTEM CONTEXT

open-noc-ai is:

- A multi-tenant SaaS platform
- Focused on network operations (NOC)
- Built to support AI agents operating incidents

### Core Domain (Inventory)

Tenant
└── Customer
    └── Site
        ├── Link
        │   └── Carrier
        └── Device

---

## 🔒 NON-NEGOTIABLE RULES

### 1. Multi-Tenant Isolation (CRITICAL)

- Every entity MUST be scoped by tenant_id
- NEVER allow cross-tenant data access
- ALWAYS filter queries by tenant

Violation = critical security issue

---

### 2. Predictable Code

- No magic logic
- No hidden behavior
- No implicit rules

All behavior must be explicit and readable

---

### 3. Consistent Pattern

Every entity MUST follow:

model → schema → crud → endpoint → router

Do NOT skip layers.

---

### 4. Soft Delete

- Use is_active instead of hard delete
- Never physically delete records

---

### 5. Auditability

- Every operation must be traceable
- Avoid logic that cannot be logged or audited

---

## 🧱 BACKEND ARCHITECTURE

Project structure:

backend/app/

- api/
- core/
- db/
- models/
- schemas/
- services/

### Responsibilities

- models → database structure
- schemas → validation & serialization
- crud → database interaction
- endpoints → API layer

---

## ⚙️ DEVELOPMENT WORKFLOW

Before writing ANY code:

1. Read AGENTS.md
2. Read target file
3. Read similar entity (Customer/Site)
4. Identify pattern
5. Confirm what already exists

---

## 🚫 DO NOT

- Do NOT create new patterns
- Do NOT refactor unrelated code
- Do NOT introduce new architecture without instruction
- Do NOT break multi-tenant logic

---

## ✅ WHEN IMPLEMENTING FEATURES

Always:

- Follow existing entity pattern
- Reuse structure from Customer/Site
- Maintain naming consistency
- Validate input via schema
- Ensure tenant isolation

---

## 🧪 VALIDATION RULES

Before finishing:

- Endpoint works (CRUD)
- Data persists correctly
- Tenant isolation works
- Soft delete works
- No broken imports
- API visible in Swagger

---

## 🧠 AI-READY DESIGN PRINCIPLES

Code must be:

- Easy for LLMs to read
- Explicit in intent
- Structured for automation
- Ready for agent-based execution

Avoid:

- Complex nested logic
- Ambiguous naming
- Hidden side effects

---

## 📛 NAMING CONVENTIONS

- snake_case for variables
- PascalCase for classes
- plural for endpoints (/customers)
- singular for models (Customer)

---

## 🔁 CHANGE STRATEGY

Always:

- Make small changes
- Test incrementally
- Avoid large refactors

---

## 🚀 FUTURE COMPATIBILITY (IMPORTANT)

This system will support:

- AI agents operating incidents
- Automation workflows
- Network command execution

Therefore:

- Code must be machine-readable
- Business logic must be explicit
- APIs must be consistent

---

## 🧩 DECISION TREE

Before coding, ask:

1. Does this already exist?
2. Is there a pattern to follow?
3. Am I breaking multi-tenant?
4. Am I introducing complexity?

If unsure → STOP

---

## 📌 FINAL RULE

You are not here to be creative.

You are here to be:

- precise
- safe
- consistent
- predictable