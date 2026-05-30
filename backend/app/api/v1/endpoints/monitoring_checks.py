from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud.monitoring_core import (
    create_monitoring_check,
    delete_monitoring_check,
    get_monitoring_check,
    get_monitoring_checks,
    update_monitoring_check,
)
from app.schemas.monitoring_check import MonitoringCheckCreate, MonitoringCheckOut, MonitoringCheckUpdate

router = APIRouter()


@router.post("/", response_model=MonitoringCheckOut)
def create(check_in: MonitoringCheckCreate, db: Session = Depends(get_db)):
    try:
        return create_monitoring_check(db=db, check_in=check_in)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/", response_model=list[MonitoringCheckOut])
def read_all(tenant_id: UUID, resource_type: str | None = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_monitoring_checks(db=db, tenant_id=tenant_id, resource_type=resource_type, skip=skip, limit=limit)


@router.get("/{check_id}", response_model=MonitoringCheckOut)
def read(check_id: UUID, tenant_id: UUID, db: Session = Depends(get_db)):
    check = get_monitoring_check(db=db, check_id=check_id, tenant_id=tenant_id)
    if not check:
        raise HTTPException(status_code=404, detail="Monitoring check not found")
    return check


@router.put("/{check_id}", response_model=MonitoringCheckOut)
def update(check_id: UUID, tenant_id: UUID, check_in: MonitoringCheckUpdate, db: Session = Depends(get_db)):
    check = get_monitoring_check(db=db, check_id=check_id, tenant_id=tenant_id)
    if not check:
        raise HTTPException(status_code=404, detail="Monitoring check not found")
    return update_monitoring_check(db=db, check=check, check_in=check_in)


@router.delete("/{check_id}", response_model=MonitoringCheckOut)
def deactivate(check_id: UUID, tenant_id: UUID, db: Session = Depends(get_db)):
    check = delete_monitoring_check(db=db, check_id=check_id, tenant_id=tenant_id)
    if not check:
        raise HTTPException(status_code=404, detail="Monitoring check not found")
    return check
