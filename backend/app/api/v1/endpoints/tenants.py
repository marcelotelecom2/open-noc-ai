from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud.tenant import create_tenant, get_tenants
from app.schemas.tenant import TenantResponse, TenantCreate

router = APIRouter()


@router.get("/", response_model=list[TenantResponse])
def list_tenants(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return get_tenants(db=db, skip=skip, limit=limit)


@router.post("/", response_model=TenantResponse)
def create(payload: TenantCreate, db: Session = Depends(get_db)):
    return create_tenant(db=db, tenant_in=payload)
