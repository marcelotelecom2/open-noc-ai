from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud.monitoring import (
    create_monitoring_event,
    delete_monitoring_event,
    get_monitoring_event,
    get_monitoring_events,
)
from app.schemas.monitoring_event import MonitoringEventCreate, MonitoringEventOut

router = APIRouter()


@router.post("/", response_model=MonitoringEventOut)
def create(event_in: MonitoringEventCreate, db: Session = Depends(get_db)):
    try:
        return create_monitoring_event(db=db, event_in=event_in)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/", response_model=list[MonitoringEventOut])
def read_all(
    tenant_id: UUID,
    resource_type: str | None = None,
    resource_id: UUID | None = None,
    event_type: str | None = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return get_monitoring_events(
        db=db,
        tenant_id=tenant_id,
        resource_type=resource_type,
        resource_id=resource_id,
        event_type=event_type,
        skip=skip,
        limit=limit,
    )


@router.get("/{monitoring_event_id}", response_model=MonitoringEventOut)
def read(
    monitoring_event_id: UUID,
    tenant_id: UUID,
    db: Session = Depends(get_db),
):
    monitoring_event = get_monitoring_event(
        db=db,
        monitoring_event_id=monitoring_event_id,
        tenant_id=tenant_id,
    )
    if not monitoring_event:
        raise HTTPException(status_code=404, detail="Monitoring event not found")
    return monitoring_event


@router.delete("/{monitoring_event_id}", response_model=MonitoringEventOut)
def deactivate(
    monitoring_event_id: UUID,
    tenant_id: UUID,
    db: Session = Depends(get_db),
):
    monitoring_event = delete_monitoring_event(
        db=db,
        monitoring_event_id=monitoring_event_id,
        tenant_id=tenant_id,
    )
    if not monitoring_event:
        raise HTTPException(status_code=404, detail="Monitoring event not found")

    return monitoring_event
