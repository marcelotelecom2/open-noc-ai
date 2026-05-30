from uuid import UUID

from sqlalchemy.orm import Session

from app.crud.monitoring import _validate_monitored_resource
from app.models.incident import Incident
from app.models.incident_history import IncidentHistory
from app.models.monitoring_event import MonitoringEvent
from app.models.user import User
from app.schemas.incident import IncidentCreate, IncidentUpdate


def _validate_monitoring_event(
    db: Session,
    tenant_id: UUID,
    monitoring_event_id: UUID | None,
) -> None:
    if monitoring_event_id is None:
        return

    monitoring_event = (
        db.query(MonitoringEvent)
        .filter(MonitoringEvent.id == monitoring_event_id)
        .filter(MonitoringEvent.tenant_id == tenant_id)
        .filter(MonitoringEvent.is_active.is_(True))
        .first()
    )
    if not monitoring_event:
        raise ValueError("Monitoring event not found")


def _validate_assigned_user(
    db: Session,
    tenant_id: UUID,
    assigned_user_id: UUID | None,
) -> None:
    if assigned_user_id is None:
        return

    user = (
        db.query(User)
        .filter(User.id == assigned_user_id)
        .filter(User.tenant_id == tenant_id)
        .filter(User.is_active.is_(True))
        .first()
    )
    if not user:
        raise ValueError("Assigned user not found")


def _create_incident_history(
    db: Session,
    tenant_id: UUID,
    incident_id: UUID,
    action: str,
    from_status: str | None = None,
    to_status: str | None = None,
    message: str | None = None,
) -> IncidentHistory:
    history = IncidentHistory(
        tenant_id=tenant_id,
        incident_id=incident_id,
        action=action,
        from_status=from_status,
        to_status=to_status,
        message=message,
        is_active=True,
    )
    db.add(history)
    return history


def create_incident(db: Session, incident_in: IncidentCreate) -> Incident:
    _validate_monitored_resource(
        db=db,
        tenant_id=incident_in.tenant_id,
        resource_type=incident_in.resource_type,
        resource_id=incident_in.resource_id,
    )
    _validate_monitoring_event(
        db=db,
        tenant_id=incident_in.tenant_id,
        monitoring_event_id=incident_in.monitoring_event_id,
    )
    _validate_assigned_user(
        db=db,
        tenant_id=incident_in.tenant_id,
        assigned_user_id=incident_in.assigned_user_id,
    )

    incident = Incident(
        tenant_id=incident_in.tenant_id,
        monitoring_event_id=incident_in.monitoring_event_id,
        resource_type=incident_in.resource_type,
        resource_id=incident_in.resource_id,
        title=incident_in.title,
        description=incident_in.description,
        status=incident_in.status,
        severity=incident_in.severity,
        priority=incident_in.priority,
        assigned_user_id=incident_in.assigned_user_id,
        acknowledged_at=incident_in.acknowledged_at,
        resolved_at=incident_in.resolved_at,
        closed_at=incident_in.closed_at,
        is_active=True,
    )
    db.add(incident)
    db.flush()
    _create_incident_history(
        db=db,
        tenant_id=incident.tenant_id,
        incident_id=incident.id,
        action="created",
        to_status=incident.status,
        message="Incident created",
    )
    db.commit()
    db.refresh(incident)
    return incident


def get_incident(
    db: Session,
    incident_id: UUID,
    tenant_id: UUID,
) -> Incident | None:
    return (
        db.query(Incident)
        .filter(Incident.id == incident_id)
        .filter(Incident.tenant_id == tenant_id)
        .filter(Incident.is_active.is_(True))
        .first()
    )


def get_incidents(
    db: Session,
    tenant_id: UUID,
    status: str | None = None,
    severity: str | None = None,
    priority: str | None = None,
    resource_type: str | None = None,
    resource_id: UUID | None = None,
    skip: int = 0,
    limit: int = 100,
):
    query = (
        db.query(Incident)
        .filter(Incident.tenant_id == tenant_id)
        .filter(Incident.is_active.is_(True))
    )
    if status is not None:
        query = query.filter(Incident.status == status)
    if severity is not None:
        query = query.filter(Incident.severity == severity)
    if priority is not None:
        query = query.filter(Incident.priority == priority)
    if resource_type is not None:
        query = query.filter(Incident.resource_type == resource_type)
    if resource_id is not None:
        query = query.filter(Incident.resource_id == resource_id)

    return query.order_by(Incident.opened_at.desc()).offset(skip).limit(limit).all()


def update_incident(
    db: Session,
    incident: Incident,
    incident_in: IncidentUpdate,
) -> Incident:
    update_data = incident_in.model_dump(exclude_unset=True)
    history_message = update_data.pop("history_message", None)

    assigned_user_id = update_data.get("assigned_user_id", incident.assigned_user_id)
    _validate_assigned_user(
        db=db,
        tenant_id=incident.tenant_id,
        assigned_user_id=assigned_user_id,
    )

    old_status = incident.status
    new_status = update_data.get("status", old_status)

    for field, value in update_data.items():
        setattr(incident, field, value)

    db.add(incident)
    if new_status != old_status:
        _create_incident_history(
            db=db,
            tenant_id=incident.tenant_id,
            incident_id=incident.id,
            action="status_changed",
            from_status=old_status,
            to_status=new_status,
            message=history_message,
        )
    else:
        _create_incident_history(
            db=db,
            tenant_id=incident.tenant_id,
            incident_id=incident.id,
            action="updated",
            from_status=old_status,
            to_status=new_status,
            message=history_message,
        )

    db.commit()
    db.refresh(incident)
    return incident


def delete_incident(
    db: Session,
    incident_id: UUID,
    tenant_id: UUID,
) -> Incident | None:
    incident = get_incident(db=db, incident_id=incident_id, tenant_id=tenant_id)
    if not incident:
        return None

    incident.is_active = False
    _create_incident_history(
        db=db,
        tenant_id=tenant_id,
        incident_id=incident.id,
        action="deactivated",
        from_status=incident.status,
        to_status=incident.status,
        message="Incident deactivated",
    )
    db.add(incident)
    db.commit()
    db.refresh(incident)
    return incident


def get_incident_history(
    db: Session,
    incident_id: UUID,
    tenant_id: UUID,
    skip: int = 0,
    limit: int = 100,
):
    return (
        db.query(IncidentHistory)
        .filter(IncidentHistory.incident_id == incident_id)
        .filter(IncidentHistory.tenant_id == tenant_id)
        .filter(IncidentHistory.is_active.is_(True))
        .order_by(IncidentHistory.created_at.asc())
        .offset(skip)
        .limit(limit)
        .all()
    )
