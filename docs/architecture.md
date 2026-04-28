# Architecture

## Overview

open-noc-ai adopts a modular, API-first architecture designed for scalability, automation, and AI-driven operations.

The platform is built to evolve from an open-source system into a multi-tenant SaaS AIOps platform.

---

## Backend architecture

The backend is organized into the following layers:

* `api/` — HTTP entrypoints and request handling
* `services/` — business logic and orchestration
* `models/` — persistence entities
* `db/` — database setup and sessions
* `ai/` — assistants, agents, providers, prompts and context
* `automation/` — connectors, workflow engine, schedulers and tasks
* `workers/` — asynchronous execution and background processing
* `core/` — configuration, logging and security

---

## Conceptual flow

The platform follows a continuous operational loop:

```
Data ingestion → Correlation → Context enrichment → AI reasoning → Decision → Automation → Feedback loop
```

### Description

* **Data ingestion**
  Metrics, logs, events and external data sources

* **Correlation**
  Detection of patterns, incidents and anomalies

* **Context enrichment**
  Inventory, topology and historical data

* **AI reasoning**
  Assistants and agents analyze the situation

* **Decision**
  Recommendation or automated action

* **Automation**
  Execution via workflows, scripts or integrations

* **Feedback loop**
  Results are stored and reused for future decisions

---

## AI and automation interaction

The platform separates **decision** and **execution**:

* `ai/` → responsible for reasoning and recommendations
* `automation/` → responsible for execution and orchestration
* `workers/` → responsible for running tasks asynchronously

This separation ensures:

* safety
* traceability
* scalability

---

## Design principles

* modularity
* API-first architecture
* separation of concerns
* AI-provider agnostic
* automation-first design
* observability and traceability
* open-source friendly structure

---

## Observability model

Observability is treated as:

> validation of configuration, behavior and operational compliance

The platform tracks:

* configuration state
* execution results
* automation outcomes
* incident lifecycle

---

## Main domains

* inventory
* monitoring
* incidents
* SLA / SLM
* insights
* assistant center
* automation
* management

---

## Future evolution

* multi-agent architecture
* multi-tenant SaaS model
* advanced AI decision engines
* predictive analytics
* self-healing automation
