from uuid import UUID

from sqlalchemy.orm import Session

from app.models.device import Device
from app.models.site import Site
from app.schemas.device import DeviceCreate, DeviceUpdate


def create_device(db: Session, device_in: DeviceCreate) -> Device:
    site = (
        db.query(Site)
        .filter(Site.id == device_in.site_id)
        .filter(Site.tenant_id == device_in.tenant_id)
        .filter(Site.is_active.is_(True))
        .first()
    )
    if not site:
        raise ValueError("Site not found")

    device = Device(
        tenant_id=device_in.tenant_id,
        site_id=device_in.site_id,
        name=device_in.name,
        ip_address=device_in.ip_address,
        vendor=device_in.vendor,
        model=device_in.model,
        role=device_in.role,
        is_active=True,
    )
    db.add(device)
    db.commit()
    db.refresh(device)
    return device


def get_device(
    db: Session,
    device_id: UUID,
    tenant_id: UUID | None = None,
) -> Device | None:
    query = (
        db.query(Device)
        .filter(Device.id == device_id)
        .filter(Device.is_active.is_(True))
    )
    if tenant_id is not None:
        query = query.filter(Device.tenant_id == tenant_id)
    return query.first()


def get_devices(db: Session, tenant_id: UUID, skip: int = 0, limit: int = 100):
    return (
        db.query(Device)
        .filter(Device.tenant_id == tenant_id)
        .filter(Device.is_active.is_(True))
        .offset(skip)
        .limit(limit)
        .all()
    )


def update_device(
    db: Session,
    device_id: UUID,
    tenant_id: UUID,
    device_in: DeviceUpdate,
) -> Device | None:
    device = get_device(db=db, device_id=device_id, tenant_id=tenant_id)
    if not device:
        return None

    update_data = device_in.model_dump(exclude_unset=True)
    update_data.pop("tenant_id", None)

    site_id = update_data.get("site_id", device.site_id)
    site = (
        db.query(Site)
        .filter(Site.id == site_id)
        .filter(Site.tenant_id == device.tenant_id)
        .filter(Site.is_active.is_(True))
        .first()
    )
    if not site:
        raise ValueError("Site not found")

    for field, value in update_data.items():
        setattr(device, field, value)

    db.add(device)
    db.commit()
    db.refresh(device)
    return device


def delete_device(
    db: Session,
    device_id: UUID,
    tenant_id: UUID,
) -> Device | None:
    device = get_device(db=db, device_id=device_id, tenant_id=tenant_id)
    if not device:
        return None

    device.is_active = False

    db.add(device)
    db.commit()
    db.refresh(device)
    return device
