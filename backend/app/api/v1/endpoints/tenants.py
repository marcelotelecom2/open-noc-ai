from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import uuid4

from app.api.deps import get_db_session
from app.models.tenant import Tenant
from app.schemas.tenant import TenantResponse

router = APIRouter()


@router.get("/", response_model=list[TenantResponse])
def list_tenants(db: Session = Depends(get_db_session)):
    return db.query(Tenant).all()


@router.post("/", response_model=TenantResponse)
def create_tenant(db: Session = Depends(get_db_session)):
    tenant = Tenant(
        id=uuid4(),
        name="Test Tenant",
        slug="test-tenant-2",
        status="active",
        plan="basic",
        is_active=True,
    )
    db.add(tenant)
    db.commit()
    db.refresh(tenant)
    return tenant
