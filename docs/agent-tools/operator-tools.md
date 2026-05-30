# Operator Agent Tool Contracts

This document defines the first tool contracts for future NOC agents.

Agents should use API-backed tools that map to existing domain resources.

## Context Tools

- `get_resource_context`
  - Input: `tenant_id`, `resource_type`, `resource_id`
  - Reads inventory, monitoring status, recent events and open incidents.

- `get_incident_context`
  - Input: `tenant_id`, `incident_id`
  - Reads incident, history, related resource, monitoring events and AI runs.

- `list_recent_events`
  - Input: `tenant_id`, optional `resource_type`, `resource_id`
  - Reads recent monitoring events.

## Reasoning Tools

- `create_ai_run`
  - Creates an auditable AI reasoning record.

- `create_agent_action`
  - Creates a proposed action instead of executing directly.

## Operation Tools

- `propose_incident_update`
  - Creates an agent action targeting an incident.

- `propose_change_request`
  - Creates an agent action and optional change request for risky work.

- `register_evidence`
  - Creates audit events and attaches structured evidence to the target context.

## Safety Rules

- Agents must prefer proposed actions over direct execution.
- Policy rules decide whether an action is allowed, denied or requires approval.
- Automation runs are the only valid record of real execution.
