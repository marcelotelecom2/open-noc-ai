# AI-Native NOC Domain

open-noc-ai is the operational system of record for an AI-native NOC.

It is not an integration layer over Zabbix, Grafana or ServiceNow. It is designed
to replace tool silos with one tenant-safe operational context where humans and
agents can monitor, reason, act and audit.

## Core Loop

```text
Inventory -> Collection -> Metrics -> Monitoring -> Alerting -> Incidents
-> AI Reasoning -> Agent Actions -> Policy -> Change -> Automation -> Audit
```

## Domains

- Inventory: customers, sites, links, devices and interfaces.
- Collection: monitoring checks and check results.
- Metrics: metric samples owned by open-noc-ai.
- Monitoring: current status and event history.
- Alerting: tenant-scoped rules that turn metrics and events into signals.
- Incidents: operational work items and history.
- AI Runtime: AI runs against explicit operational context.
- Agent Operations: proposed and controlled agent actions.
- Policy: rules that decide what is allowed, denied or approval-gated.
- Change: approved operational changes with rollback intent.
- Automation: execution records for approved actions.
- Audit: immutable operational narrative across users, agents and system jobs.

## Agent Principles

- Agents never bypass tenant boundaries.
- Agents never access the database directly.
- Agents create actions, evidence, AI runs and audit events.
- Sensitive execution is represented as a change or automation run.
- Every autonomous or assisted action must be explainable after the fact.
