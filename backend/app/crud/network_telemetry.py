from uuid import UUID

from sqlalchemy.orm import Session

from app.models.device import Device
from app.models.flow_record import FlowRecord
from app.models.interface import Interface
from app.models.link import Link
from app.models.snmp_trap import SNMPTrap
from app.models.syslog_message import SyslogMessage
from app.schemas.flow_record import FlowRecordCreate
from app.schemas.snmp_trap import SNMPTrapCreate
from app.schemas.syslog_message import SyslogMessageCreate


def _validate_optional_resource(db: Session, model, resource_id: UUID | None, tenant_id: UUID, label: str) -> None:
    if resource_id is None:
        return
    resource = (
        db.query(model)
        .filter(model.id == resource_id)
        .filter(model.tenant_id == tenant_id)
        .filter(model.is_active.is_(True))
        .first()
    )
    if not resource:
        raise ValueError(f"{label} not found")


def create_syslog_message(db: Session, message_in: SyslogMessageCreate) -> SyslogMessage:
    _validate_optional_resource(db, Device, message_in.device_id, message_in.tenant_id, "Device")
    message = SyslogMessage(**message_in.model_dump(), is_active=True)
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


def get_syslog_message(db: Session, message_id: UUID, tenant_id: UUID) -> SyslogMessage | None:
    return (
        db.query(SyslogMessage)
        .filter(SyslogMessage.id == message_id)
        .filter(SyslogMessage.tenant_id == tenant_id)
        .filter(SyslogMessage.is_active.is_(True))
        .first()
    )


def get_syslog_messages(
    db: Session,
    tenant_id: UUID,
    device_id: UUID | None = None,
    severity: int | None = None,
    skip: int = 0,
    limit: int = 100,
):
    query = db.query(SyslogMessage).filter(SyslogMessage.tenant_id == tenant_id).filter(SyslogMessage.is_active.is_(True))
    if device_id is not None:
        query = query.filter(SyslogMessage.device_id == device_id)
    if severity is not None:
        query = query.filter(SyslogMessage.severity == severity)
    return query.order_by(SyslogMessage.received_at.desc()).offset(skip).limit(limit).all()


def delete_syslog_message(db: Session, message_id: UUID, tenant_id: UUID) -> SyslogMessage | None:
    message = get_syslog_message(db=db, message_id=message_id, tenant_id=tenant_id)
    if not message:
        return None
    message.is_active = False
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


def create_snmp_trap(db: Session, trap_in: SNMPTrapCreate) -> SNMPTrap:
    _validate_optional_resource(db, Device, trap_in.device_id, trap_in.tenant_id, "Device")
    trap = SNMPTrap(**trap_in.model_dump(), is_active=True)
    db.add(trap)
    db.commit()
    db.refresh(trap)
    return trap


def get_snmp_trap(db: Session, trap_id: UUID, tenant_id: UUID) -> SNMPTrap | None:
    return (
        db.query(SNMPTrap)
        .filter(SNMPTrap.id == trap_id)
        .filter(SNMPTrap.tenant_id == tenant_id)
        .filter(SNMPTrap.is_active.is_(True))
        .first()
    )


def get_snmp_traps(
    db: Session,
    tenant_id: UUID,
    device_id: UUID | None = None,
    trap_oid: str | None = None,
    skip: int = 0,
    limit: int = 100,
):
    query = db.query(SNMPTrap).filter(SNMPTrap.tenant_id == tenant_id).filter(SNMPTrap.is_active.is_(True))
    if device_id is not None:
        query = query.filter(SNMPTrap.device_id == device_id)
    if trap_oid is not None:
        query = query.filter(SNMPTrap.trap_oid == trap_oid)
    return query.order_by(SNMPTrap.received_at.desc()).offset(skip).limit(limit).all()


def delete_snmp_trap(db: Session, trap_id: UUID, tenant_id: UUID) -> SNMPTrap | None:
    trap = get_snmp_trap(db=db, trap_id=trap_id, tenant_id=tenant_id)
    if not trap:
        return None
    trap.is_active = False
    db.add(trap)
    db.commit()
    db.refresh(trap)
    return trap


def create_flow_record(db: Session, record_in: FlowRecordCreate) -> FlowRecord:
    _validate_optional_resource(db, Device, record_in.device_id, record_in.tenant_id, "Device")
    _validate_optional_resource(db, Interface, record_in.interface_id, record_in.tenant_id, "Interface")
    _validate_optional_resource(db, Link, record_in.link_id, record_in.tenant_id, "Link")
    record = FlowRecord(**record_in.model_dump(), is_active=True)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_flow_record(db: Session, record_id: UUID, tenant_id: UUID) -> FlowRecord | None:
    return (
        db.query(FlowRecord)
        .filter(FlowRecord.id == record_id)
        .filter(FlowRecord.tenant_id == tenant_id)
        .filter(FlowRecord.is_active.is_(True))
        .first()
    )


def get_flow_records(
    db: Session,
    tenant_id: UUID,
    device_id: UUID | None = None,
    interface_id: UUID | None = None,
    link_id: UUID | None = None,
    skip: int = 0,
    limit: int = 100,
):
    query = db.query(FlowRecord).filter(FlowRecord.tenant_id == tenant_id).filter(FlowRecord.is_active.is_(True))
    if device_id is not None:
        query = query.filter(FlowRecord.device_id == device_id)
    if interface_id is not None:
        query = query.filter(FlowRecord.interface_id == interface_id)
    if link_id is not None:
        query = query.filter(FlowRecord.link_id == link_id)
    return query.order_by(FlowRecord.received_at.desc()).offset(skip).limit(limit).all()


def delete_flow_record(db: Session, record_id: UUID, tenant_id: UUID) -> FlowRecord | None:
    record = get_flow_record(db=db, record_id=record_id, tenant_id=tenant_id)
    if not record:
        return None
    record.is_active = False
    db.add(record)
    db.commit()
    db.refresh(record)
    return record
