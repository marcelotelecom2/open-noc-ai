from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud.audit_event import create_audit_event, get_audit_event, get_audit_events
from app.schemas.audit_event import AuditEventCreate, AuditEventOut

router = APIRouter()


@router.post("/", response_model=AuditEventOut)
def create(audit_event_in: AuditEventCreate, db: Session = Depends(get_db)):
    try:
        return create_audit_event(db=db, audit_event_in=audit_event_in)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/", response_model=list[AuditEventOut])
def read_all(
    tenant_id: UUID,
    actor_type: str | None = None,
    action: str | None = None,
    target_type: str | None = None,
    target_id: UUID | None = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return get_audit_events(
        db=db,
        tenant_id=tenant_id,
        actor_type=actor_type,
        action=action,
        target_type=target_type,
        target_id=target_id,
        skip=skip,
        limit=limit,
    )


@router.get("/{audit_event_id}", response_model=AuditEventOut)
def read(audit_event_id: UUID, tenant_id: UUID, db: Session = Depends(get_db)):
    audit_event = get_audit_event(
        db=db,
        audit_event_id=audit_event_id,
        tenant_id=tenant_id,
    )
    if not audit_event:
        raise HTTPException(status_code=404, detail="Audit event not found")
    return audit_event
