# Contributing to open-noc-ai

Thank you for your interest in contributing to **open-noc-ai**.

This project aims to build a modern, open-source AIOps platform for NOC/SOC operations. Contributions should follow structured engineering and architectural principles.

---

## How to contribute

1. Open an issue to report bugs or propose features
2. Fork the repository
3. Create a branch following naming conventions
4. Implement your changes
5. Submit a Pull Request with a clear description

---

## Branch naming conventions

* `feature/<name>` — new features
* `fix/<name>` — bug fixes
* `docs/<name>` — documentation changes
* `refactor/<name>` — code improvements without behavior change

---

## Commit message standard

Follow a structured format:

* `feat: add inventory API`
* `fix: correct SLA calculation bug`
* `docs: update architecture documentation`
* `refactor: improve service layer structure`

---

## Development principles

* Maintain modular architecture
* Prefer simplicity and readability
* Avoid unnecessary abstractions
* Document major design decisions
* Keep separation of concerns across layers

---

## Architecture guidelines

Contributions must respect the platform architecture:

* API layer → request handling only
* Services layer → business logic
* Persistence layer → data access
* AI layer → reasoning, models, agents
* Automation layer → workflows and execution
* Worker layer → async/background processing

Do not mix responsibilities across layers.

---

## AI and Agents contributions

When contributing to AI components:

* Follow definitions in `AGENTS.md`
* Keep agents focused and single-responsibility
* Avoid embedding business logic directly in prompts
* Prefer structured outputs (JSON/schema)
* Ensure traceability of decisions

---

## Code style

* Use clear and descriptive naming
* Keep functions small and focused
* Avoid large monolithic modules
* Separate business logic from API endpoints

---

## Observability and reliability

* Add logs for important operations
* Handle errors explicitly
* Avoid silent failures
* Ensure actions are traceable

---

## Scope

This project focuses on:

* NOC/SOC operations
* Inventory and incidents
* SLA / SLM
* AI assistants and agents
* Automation and workflows

---

## Pull request guidelines

* Provide a clear and objective description
* Reference related issues when applicable
* Keep changes focused and minimal
* Avoid unrelated modifications in the same PR

---

## Final note

open-noc-ai is designed to evolve into a production-grade AIOps platform.
Contributions should aim for quality, scalability, and long-term maintainability.
