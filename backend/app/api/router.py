from fastapi import APIRouter

from app.api.v1.endpoints import (
    tenants,
    users,
    customers,
    sites,
    carriers,
    links,
    devices,
    monitoring_statuses,
    monitoring_events,
    incidents,
    ai_provider_configs,
    interfaces,
    audit_events,
    agent_actions,
    monitoring_checks,
    check_results,
    metric_samples,
    alert_rules,
    ai_runs,
    policy_rules,
    change_requests,
    automation_runs,
    runbooks,
)


api_router = APIRouter()

api_router.include_router(tenants.router, prefix="/tenants", tags=["tenants"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(customers.router, prefix="/customers", tags=["customers"])
api_router.include_router(sites.router, prefix="/sites", tags=["sites"])
api_router.include_router(carriers.router, prefix="/carriers", tags=["carriers"])
api_router.include_router(links.router, prefix="/links", tags=["links"])
api_router.include_router(devices.router, prefix="/devices", tags=["devices"])
api_router.include_router(interfaces.router, prefix="/interfaces", tags=["interfaces"])
api_router.include_router(
    monitoring_statuses.router,
    prefix="/monitoring-statuses",
    tags=["monitoring-statuses"],
)
api_router.include_router(
    monitoring_events.router,
    prefix="/monitoring-events",
    tags=["monitoring-events"],
)
api_router.include_router(incidents.router, prefix="/incidents", tags=["incidents"])
api_router.include_router(
    ai_provider_configs.router,
    prefix="/ai-provider-configs",
    tags=["ai-provider-configs"],
)
api_router.include_router(audit_events.router, prefix="/audit-events", tags=["audit-events"])
api_router.include_router(agent_actions.router, prefix="/agent-actions", tags=["agent-actions"])
api_router.include_router(monitoring_checks.router, prefix="/monitoring-checks", tags=["monitoring-checks"])
api_router.include_router(check_results.router, prefix="/check-results", tags=["check-results"])
api_router.include_router(metric_samples.router, prefix="/metric-samples", tags=["metric-samples"])
api_router.include_router(alert_rules.router, prefix="/alert-rules", tags=["alert-rules"])
api_router.include_router(ai_runs.router, prefix="/ai-runs", tags=["ai-runs"])
api_router.include_router(policy_rules.router, prefix="/policy-rules", tags=["policy-rules"])
api_router.include_router(change_requests.router, prefix="/change-requests", tags=["change-requests"])
api_router.include_router(automation_runs.router, prefix="/automation-runs", tags=["automation-runs"])
api_router.include_router(runbooks.router, prefix="/runbooks", tags=["runbooks"])
