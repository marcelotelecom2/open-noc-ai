from uuid import UUID

from sqlalchemy.orm import Session

from app.models.tenant import Tenant
from app.schemas.tenant import TenantCreate


def create_tenant(db: Session, tenant_in: TenantCreate) -> Tenant:
    tenant = Tenant(
        name=tenant_in.name,
        slug=tenant_in.slug,
        status=tenant_in.status,
        plan=tenant_in.plan,
        is_active=tenant_in.is_active,
    )
    db.add(tenant)
    db.commit()
    db.refresh(tenant)
    return tenant


def get_tenant(db: Session, tenant_id: UUID) -> Tenant | None:
    return (
        db.query(Tenant)
        .filter(Tenant.id == tenant_id)
        .filter(Tenant.is_active.is_(True))
        .first()
    )


def get_tenants(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(Tenant)
        .filter(Tenant.is_active.is_(True))
        .offset(skip)
        .limit(limit)
        .all()
    )
