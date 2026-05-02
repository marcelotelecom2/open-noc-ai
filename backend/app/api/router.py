from fastapi import APIRouter

from app.api.v1.endpoints import tenants, users, customers, sites, carriers, links


api_router = APIRouter()

api_router.include_router(tenants.router, prefix="/tenants", tags=["tenants"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(customers.router, prefix="/customers", tags=["customers"])
api_router.include_router(sites.router, prefix="/sites", tags=["sites"])
api_router.include_router(carriers.router, prefix="/carriers", tags=["carriers"])
api_router.include_router(links.router, prefix="/links", tags=["links"])
