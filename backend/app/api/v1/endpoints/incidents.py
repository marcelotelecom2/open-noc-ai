from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud.incident import (
    create_incident,
    delete_incident,
    get_incident,
    get_incident_history,
    get_incidents,
    update_incident,
)
from app.schemas.incident import (
    IncidentCreate,
    IncidentHistoryOut,
    IncidentOut,
    IncidentUpdate,
)

router = APIRouter()


@router.post("/", response_model=IncidentOut)
def create(incident_in: IncidentCreate, db: Session = Depends(get_db)):
    try:
        return create_incident(db=db, incident_in=incident_in)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/", response_model=list[IncidentOut])
def read_all(
    tenant_id: UUID,
    status: str | None = None,
    severity: str | None = None,
    priority: str | None = None,
    resource_type: str | None = None,
    resource_id: UUID | None = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return get_incidents(
        db=db,
        tenant_id=tenant_id,
        status=status,
        severity=severity,
        priority=priority,
        resource_type=resource_type,
        resource_id=resource_id,
        skip=skip,
        limit=limit,
    )


@router.get("/{incident_id}", response_model=IncidentOut)
def read(incident_id: UUID, tenant_id: UUID, db: Session = Depends(get_db)):
    incident = get_incident(db=db, incident_id=incident_id, tenant_id=tenant_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident


@router.put("/{incident_id}", response_model=IncidentOut)
def update(
    incident_id: UUID,
    tenant_id: UUID,
    incident_in: IncidentUpdate,
    db: Session = Depends(get_db),
):
    incident = get_incident(db=db, incident_id=incident_id, tenant_id=tenant_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")

    try:
        return update_incident(db=db, incident=incident, incident_in=incident_in)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.delete("/{incident_id}", response_model=IncidentOut)
def deactivate(incident_id: UUID, tenant_id: UUID, db: Session = Depends(get_db)):
    incident = delete_incident(db=db, incident_id=incident_id, tenant_id=tenant_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident


@router.get("/{incident_id}/history", response_model=list[IncidentHistoryOut])
def read_history(
    incident_id: UUID,
    tenant_id: UUID,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    incident = get_incident(db=db, incident_id=incident_id, tenant_id=tenant_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")

    return get_incident_history(
        db=db,
        incident_id=incident_id,
        tenant_id=tenant_id,
        skip=skip,
        limit=limit,
    )
