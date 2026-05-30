from uuid import UUID

from sqlalchemy.orm import Session

from app.models.device import Device
from app.models.link import Link
from app.models.monitoring_event import MonitoringEvent
from app.models.monitoring_status import MonitoringStatus
from app.schemas.monitoring_event import MonitoringEventCreate
from app.schemas.monitoring_status import MonitoringStatusCreate, MonitoringStatusUpdate

MONITORED_RESOURCE_TYPES = {"link", "device"}


def _validate_monitored_resource(
    db: Session,
    tenant_id: UUID,
    resource_type: str,
    resource_id: UUID,
) -> None:
    if resource_type not in MONITORED_RESOURCE_TYPES:
        raise ValueError("Unsupported monitored resource type")

    model = Link if resource_type == "link" else Device
    resource = (
        db.query(model)
        .filter(model.id == resource_id)
        .filter(model.tenant_id == tenant_id)
        .filter(model.is_active.is_(True))
        .first()
    )
    if not resource:
        raise ValueError("Monitored resource not found")


def create_monitoring_status(
    db: Session,
    status_in: MonitoringStatusCreate,
) -> MonitoringStatus:
    _validate_monitored_resource(
        db=db,
        tenant_id=status_in.tenant_id,
        resource_type=status_in.resource_type,
        resource_id=status_in.resource_id,
    )

    existing_status = get_monitoring_status_by_resource(
        db=db,
        tenant_id=status_in.tenant_id,
        resource_type=status_in.resource_type,
        resource_id=status_in.resource_id,
    )
    if existing_status:
        raise ValueError("Monitoring status already exists")

    monitoring_status = MonitoringStatus(
        tenant_id=status_in.tenant_id,
        resource_type=status_in.resource_type,
        resource_id=status_in.resource_id,
        status=status_in.status,
        severity=status_in.severity,
        metric_name=status_in.metric_name,
        metric_value=status_in.metric_value,
        message=status_in.message,
        last_check_at=status_in.last_check_at,
        last_event_at=status_in.last_event_at,
        is_active=True,
    )
    db.add(monitoring_status)
    db.commit()
    db.refresh(monitoring_status)
    return monitoring_status


def get_monitoring_status(
    db: Session,
    monitoring_status_id: UUID,
    tenant_id: UUID,
) -> MonitoringStatus | None:
    return (
        db.query(MonitoringStatus)
        .filter(MonitoringStatus.id == monitoring_status_id)
        .filter(MonitoringStatus.tenant_id == tenant_id)
        .filter(MonitoringStatus.is_active.is_(True))
        .first()
    )


def get_monitoring_status_by_resource(
    db: Session,
    tenant_id: UUID,
    resource_type: str,
    resource_id: UUID,
) -> MonitoringStatus | None:
    return (
        db.query(MonitoringStatus)
        .filter(MonitoringStatus.tenant_id == tenant_id)
        .filter(MonitoringStatus.resource_type == resource_type)
        .filter(MonitoringStatus.resource_id == resource_id)
        .filter(MonitoringStatus.is_active.is_(True))
        .first()
    )


def get_monitoring_statuses(
    db: Session,
    tenant_id: UUID,
    resource_type: str | None = None,
    resource_id: UUID | None = None,
    skip: int = 0,
    limit: int = 100,
):
    query = (
        db.query(MonitoringStatus)
        .filter(MonitoringStatus.tenant_id == tenant_id)
        .filter(MonitoringStatus.is_active.is_(True))
    )
    if resource_type is not None:
        query = query.filter(MonitoringStatus.resource_type == resource_type)
    if resource_id is not None:
        query = query.filter(MonitoringStatus.resource_id == resource_id)

    return query.offset(skip).limit(limit).all()


def update_monitoring_status(
    db: Session,
    monitoring_status: MonitoringStatus,
    status_in: MonitoringStatusUpdate,
) -> MonitoringStatus:
    update_data = status_in.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(monitoring_status, field, value)

    db.add(monitoring_status)
    db.commit()
    db.refresh(monitoring_status)
    return monitoring_status


def delete_monitoring_status(
    db: Session,
    monitoring_status_id: UUID,
    tenant_id: UUID,
) -> MonitoringStatus | None:
    monitoring_status = get_monitoring_status(
        db=db,
        monitoring_status_id=monitoring_status_id,
        tenant_id=tenant_id,
    )
    if not monitoring_status:
        return None

    monitoring_status.is_active = False
    db.add(monitoring_status)
    db.commit()
    db.refresh(monitoring_status)
    return monitoring_status


def create_monitoring_event(
    db: Session,
    event_in: MonitoringEventCreate,
) -> MonitoringEvent:
    _validate_monitored_resource(
        db=db,
        tenant_id=event_in.tenant_id,
        resource_type=event_in.resource_type,
        resource_id=event_in.resource_id,
    )

    monitoring_event = MonitoringEvent(
        tenant_id=event_in.tenant_id,
        resource_type=event_in.resource_type,
        resource_id=event_in.resource_id,
        event_type=event_in.event_type,
        status=event_in.status,
        severity=event_in.severity,
        metric_name=event_in.metric_name,
        metric_value=event_in.metric_value,
        message=event_in.message,
        occurred_at=event_in.occurred_at,
        is_active=True,
    )
    db.add(monitoring_event)
    db.commit()
    db.refresh(monitoring_event)
    return monitoring_event


def get_monitoring_event(
    db: Session,
    monitoring_event_id: UUID,
    tenant_id: UUID,
) -> MonitoringEvent | None:
    return (
        db.query(MonitoringEvent)
        .filter(MonitoringEvent.id == monitoring_event_id)
        .filter(MonitoringEvent.tenant_id == tenant_id)
        .filter(MonitoringEvent.is_active.is_(True))
        .first()
    )


def get_monitoring_events(
    db: Session,
    tenant_id: UUID,
    resource_type: str | None = None,
    resource_id: UUID | None = None,
    event_type: str | None = None,
    skip: int = 0,
    limit: int = 100,
):
    query = (
        db.query(MonitoringEvent)
        .filter(MonitoringEvent.tenant_id == tenant_id)
        .filter(MonitoringEvent.is_active.is_(True))
    )
    if resource_type is not None:
        query = query.filter(MonitoringEvent.resource_type == resource_type)
    if resource_id is not None:
        query = query.filter(MonitoringEvent.resource_id == resource_id)
    if event_type is not None:
        query = query.filter(MonitoringEvent.event_type == event_type)

    return query.order_by(MonitoringEvent.occurred_at.desc()).offset(skip).limit(limit).all()


def delete_monitoring_event(
    db: Session,
    monitoring_event_id: UUID,
    tenant_id: UUID,
) -> MonitoringEvent | None:
    monitoring_event = get_monitoring_event(
        db=db,
        monitoring_event_id=monitoring_event_id,
        tenant_id=tenant_id,
    )
    if not monitoring_event:
        return None

    monitoring_event.is_active = False
    db.add(monitoring_event)
    db.commit()
    db.refresh(monitoring_event)
    return monitoring_event
