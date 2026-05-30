# Runbook: Link Down

## Trigger

- `resource_type = link`
- `status = down`
- severity `major` or `critical`

## Agent Investigation Steps

1. Load link context.
2. Load site, carrier, related devices and interfaces.
3. Check recent monitoring events for the same link.
4. Check related interface operational status.
5. Check whether other links at the same site are impacted.
6. Create or update the incident.
7. Propose next action through `agent_actions`.

## Evidence To Collect

- last successful check
- failed check result
- related interface status
- impacted site/customer
- recent changes or automation runs

## Automation Boundary

Agents may run read-only diagnostics automatically when policy allows.
Corrective actions require policy evaluation and, when needed, approval.
