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
- Collection: network-device telemetry only. The current scope receives data
  from routers, switches, firewalls, wireless controllers and other network
  appliances through syslog, SNMP traps, IP flow and active checks.
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

## Network Device Scope

The platform does not install agents on operating systems in the current scope.

Supported collection boundaries:

- Syslog from network equipment, normalized around RFC 5424 fields while keeping
  raw messages for vendor-specific parsing.
- SNMP traps from network equipment.
- IP flow records from exporters such as NetFlow, IPFIX and sFlow.
- Active monitoring checks executed by open-noc-ai against network resources.

Out of scope for now:

- Host agents installed on Linux, Windows or application servers.
- Endpoint telemetry that depends on software installed inside the operating
  system.
