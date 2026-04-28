from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import uuid4

from app.api.deps import get_db_session
from app.models.tenant import Tenant

router = APIRouter()


@router.get("/")
def list_tenants(db: Session = Depends(get_db_session)):
    return db.query(Tenant).all()


@router.post("/")
def create_tenant(db: Session = Depends(get_db_session)):
    tenant = Tenant(
        id=uuid4(),
        name="Test Tenant",
        slug="test-tenant",
        status="active",
        plan="basic",
        is_active=True,
    )
    db.add(tenant)
    db.commit()
    db.refresh(tenant)
    return tenant
