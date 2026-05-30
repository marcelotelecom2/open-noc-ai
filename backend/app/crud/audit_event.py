from uuid import UUID

from sqlalchemy.orm import Session

from app.crud.tenant import get_tenant
from app.models.audit_event import AuditEvent
from app.schemas.audit_event import AuditEventCreate


def create_audit_event(db: Session, audit_event_in: AuditEventCreate) -> AuditEvent:
    tenant = get_tenant(db=db, tenant_id=audit_event_in.tenant_id)
    if not tenant:
        raise ValueError("Tenant not found")

    audit_event = AuditEvent(
        tenant_id=audit_event_in.tenant_id,
        actor_type=audit_event_in.actor_type,
        actor_id=audit_event_in.actor_id,
        action=audit_event_in.action,
        target_type=audit_event_in.target_type,
        target_id=audit_event_in.target_id,
        status=audit_event_in.status,
        message=audit_event_in.message,
        event_metadata=audit_event_in.event_metadata,
        is_active=True,
    )
    db.add(audit_event)
    db.commit()
    db.refresh(audit_event)
    return audit_event


def get_audit_event(
    db: Session,
    audit_event_id: UUID,
    tenant_id: UUID,
) -> AuditEvent | None:
    return (
        db.query(AuditEvent)
        .filter(AuditEvent.id == audit_event_id)
        .filter(AuditEvent.tenant_id == tenant_id)
        .filter(AuditEvent.is_active.is_(True))
        .first()
    )


def get_audit_events(
    db: Session,
    tenant_id: UUID,
    actor_type: str | None = None,
    action: str | None = None,
    target_type: str | None = None,
    target_id: UUID | None = None,
    skip: int = 0,
    limit: int = 100,
):
    query = (
        db.query(AuditEvent)
        .filter(AuditEvent.tenant_id == tenant_id)
        .filter(AuditEvent.is_active.is_(True))
    )
    if actor_type is not None:
        query = query.filter(AuditEvent.actor_type == actor_type)
    if action is not None:
        query = query.filter(AuditEvent.action == action)
    if target_type is not None:
        query = query.filter(AuditEvent.target_type == target_type)
    if target_id is not None:
        query = query.filter(AuditEvent.target_id == target_id)

    return query.order_by(AuditEvent.created_at.desc()).offset(skip).limit(limit).all()
