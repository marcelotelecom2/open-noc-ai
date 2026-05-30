from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud.monitoring import (
    create_monitoring_status,
    delete_monitoring_status,
    get_monitoring_status,
    get_monitoring_statuses,
    update_monitoring_status,
)
from app.schemas.monitoring_status import (
    MonitoringStatusCreate,
    MonitoringStatusOut,
    MonitoringStatusUpdate,
)

router = APIRouter()


@router.post("/", response_model=MonitoringStatusOut)
def create(status_in: MonitoringStatusCreate, db: Session = Depends(get_db)):
    try:
        return create_monitoring_status(db=db, status_in=status_in)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/", response_model=list[MonitoringStatusOut])
def read_all(
    tenant_id: UUID,
    resource_type: str | None = None,
    resource_id: UUID | None = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return get_monitoring_statuses(
        db=db,
        tenant_id=tenant_id,
        resource_type=resource_type,
        resource_id=resource_id,
        skip=skip,
        limit=limit,
    )


@router.get("/{monitoring_status_id}", response_model=MonitoringStatusOut)
def read(
    monitoring_status_id: UUID,
    tenant_id: UUID,
    db: Session = Depends(get_db),
):
    monitoring_status = get_monitoring_status(
        db=db,
        monitoring_status_id=monitoring_status_id,
        tenant_id=tenant_id,
    )
    if not monitoring_status:
        raise HTTPException(status_code=404, detail="Monitoring status not found")
    return monitoring_status


@router.put("/{monitoring_status_id}", response_model=MonitoringStatusOut)
def update(
    monitoring_status_id: UUID,
    tenant_id: UUID,
    status_in: MonitoringStatusUpdate,
    db: Session = Depends(get_db),
):
    monitoring_status = get_monitoring_status(
        db=db,
        monitoring_status_id=monitoring_status_id,
        tenant_id=tenant_id,
    )
    if not monitoring_status:
        raise HTTPException(status_code=404, detail="Monitoring status not found")

    return update_monitoring_status(
        db=db,
        monitoring_status=monitoring_status,
        status_in=status_in,
    )


@router.delete("/{monitoring_status_id}", response_model=MonitoringStatusOut)
def deactivate(
    monitoring_status_id: UUID,
    tenant_id: UUID,
    db: Session = Depends(get_db),
):
    monitoring_status = delete_monitoring_status(
        db=db,
        monitoring_status_id=monitoring_status_id,
        tenant_id=tenant_id,
    )
    if not monitoring_status:
        raise HTTPException(status_code=404, detail="Monitoring status not found")

    return monitoring_status
