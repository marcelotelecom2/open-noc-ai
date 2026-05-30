from uuid import UUID

from sqlalchemy.orm import Session

from app.models.device import Device
from app.models.interface import Interface
from app.models.link import Link
from app.schemas.interface import InterfaceCreate, InterfaceUpdate


def _validate_interface_parent(
    db: Session,
    tenant_id: UUID,
    device_id: UUID,
    link_id: UUID | None = None,
) -> None:
    device = (
        db.query(Device)
        .filter(Device.id == device_id)
        .filter(Device.tenant_id == tenant_id)
        .filter(Device.is_active.is_(True))
        .first()
    )
    if not device:
        raise ValueError("Device not found")

    if link_id is None:
        return

    link = (
        db.query(Link)
        .filter(Link.id == link_id)
        .filter(Link.tenant_id == tenant_id)
        .filter(Link.is_active.is_(True))
        .first()
    )
    if not link:
        raise ValueError("Link not found")


def create_interface(db: Session, interface_in: InterfaceCreate) -> Interface:
    _validate_interface_parent(
        db=db,
        tenant_id=interface_in.tenant_id,
        device_id=interface_in.device_id,
        link_id=interface_in.link_id,
    )

    interface = Interface(
        tenant_id=interface_in.tenant_id,
        device_id=interface_in.device_id,
        link_id=interface_in.link_id,
        name=interface_in.name,
        description=interface_in.description,
        type=interface_in.type,
        mac_address=interface_in.mac_address,
        ip_address=interface_in.ip_address,
        speed_mbps=interface_in.speed_mbps,
        admin_status=interface_in.admin_status,
        operational_status=interface_in.operational_status,
        is_active=True,
    )
    db.add(interface)
    db.commit()
    db.refresh(interface)
    return interface


def get_interface(
    db: Session,
    interface_id: UUID,
    tenant_id: UUID,
) -> Interface | None:
    return (
        db.query(Interface)
        .filter(Interface.id == interface_id)
        .filter(Interface.tenant_id == tenant_id)
        .filter(Interface.is_active.is_(True))
        .first()
    )


def get_interfaces(
    db: Session,
    tenant_id: UUID,
    device_id: UUID | None = None,
    link_id: UUID | None = None,
    skip: int = 0,
    limit: int = 100,
):
    query = (
        db.query(Interface)
        .filter(Interface.tenant_id == tenant_id)
        .filter(Interface.is_active.is_(True))
    )
    if device_id is not None:
        query = query.filter(Interface.device_id == device_id)
    if link_id is not None:
        query = query.filter(Interface.link_id == link_id)

    return query.offset(skip).limit(limit).all()


def update_interface(
    db: Session,
    interface: Interface,
    interface_in: InterfaceUpdate,
) -> Interface:
    update_data = interface_in.model_dump(exclude_unset=True)

    link_id = update_data.get("link_id", interface.link_id)
    _validate_interface_parent(
        db=db,
        tenant_id=interface.tenant_id,
        device_id=interface.device_id,
        link_id=link_id,
    )

    for field, value in update_data.items():
        setattr(interface, field, value)

    db.add(interface)
    db.commit()
    db.refresh(interface)
    return interface


def delete_interface(
    db: Session,
    interface_id: UUID,
    tenant_id: UUID,
) -> Interface | None:
    interface = get_interface(db=db, interface_id=interface_id, tenant_id=tenant_id)
    if not interface:
        return None

    interface.is_active = False
    db.add(interface)
    db.commit()
    db.refresh(interface)
    return interface
