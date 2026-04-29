# open-noc-ai

Open-source AIOps platform designed for modern NOC/SOC operations, combining monitoring, incidents, SLA management, automation, and AI-driven agents into a unified operational system.

---

## Vision

To redefine network operations by transforming reactive monitoring into intelligent, autonomous, and data-driven operations using AI and automation.

---

## Positioning

open-noc-ai is an open-source AIOps platform focused on NOC environments, combining:

- real-time observability
- AI-assisted troubleshooting
- autonomous agents
- workflow automation
- offline-first AI capabilities

---

## Core Pillars

- **Inventory**  
  Configuration items, topology, and asset lifecycle

- **Monitoring**  
  Metrics, logs, events, and observability pipelines

- **Incidents**  
  Centralized incident workspace and lifecycle management

- **SLA / SLM**  
  Service-level tracking, compliance, and reporting

- **Assistant Center**  
  AI copilots for NOC engineers

- **Automation & Agents**  
  Runbooks, workflows, and autonomous execution

- **AI Layer**  
  Multi-agent architecture with LLM integration, local and cloud

---

## Architecture

The platform follows a modular, API-first architecture composed of:

- API layer using FastAPI
- Services layer
- Persistence layer
- AI layer with LLMs and agents
- Automation layer for workflows and orchestration
- Worker layer for execution engine tasks

---

## Current Status

The platform is currently under active development.

### Implemented

- Backend foundation using FastAPI, PostgreSQL and Alembic
- Multi-tenant base structure
- Inventory module, partial:
  - Customer management complete
  - Site management API implemented

### In Progress

- Carrier management
- Link management
- Device management

### Planned

- Monitoring engine
- Incident management
- SLA tracking
- AI agents and automation workflows

---

## Getting Started

### Requirements

- Python 3.11+
- PostgreSQL
- Virtual environment with venv

### Installation

Clone the repository:

`git clone https://github.com/your-user/open-noc-ai.git`

Enter the backend folder:

`cd open-noc-ai/backend`

Create and activate the virtual environment:

`python3 -m venv .venv`

`source .venv/bin/activate`

Install dependencies:

`pip install -r requirements.txt`

### Run the API

`uvicorn app.main:app --reload`

### Access API Documentation

`http://127.0.0.1:8000/docs`

---

## Current Modules

### Inventory

| Entity | Status |
|---|---|
| Tenant | Implemented |
| User | Implemented |
| Customer | Complete |
| Site | API implemented |
| Carrier | In progress |
| Link | Planned |
| Device | Planned |

---

## Roadmap

### Phase 1 — Inventory API

- Complete all inventory entities
- Validate full data flow

### Phase 2 — Monitoring

- Metrics ingestion
- Event processing pipeline

### Phase 3 — Incidents

- Incident lifecycle management
- Correlation engine

### Phase 4 — AI & Automation

- LLM integration
- Autonomous agents
- Intelligent runbooks

---

## License

This project is licensed under the MIT License.
