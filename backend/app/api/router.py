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
)


api_router = APIRouter()

api_router.include_router(tenants.router, prefix="/tenants", tags=["tenants"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(customers.router, prefix="/customers", tags=["customers"])
api_router.include_router(sites.router, prefix="/sites", tags=["sites"])
api_router.include_router(carriers.router, prefix="/carriers", tags=["carriers"])
api_router.include_router(links.router, prefix="/links", tags=["links"])
api_router.include_router(devices.router, prefix="/devices", tags=["devices"])
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
