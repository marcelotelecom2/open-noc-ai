# Runbook: High Bandwidth Usage

## Trigger

- `resource_type = interface` or `link`
- metric `bandwidth_usage`
- threshold above tenant policy

## Agent Investigation Steps

1. Load resource context.
2. Review metric samples for the affected interval.
3. Compare against recent baseline.
4. Check if related incidents already exist.
5. Identify affected customer, site, link and interface.
6. Create an AI run for summary and probable cause.
7. Propose incident update or change request if action is needed.

## Evidence To Collect

- metric samples
- alert rule that triggered
- interface speed
- utilization percentage
- related incidents

## Automation Boundary

Traffic-shaping, reroute or configuration changes must become change requests
before execution.
