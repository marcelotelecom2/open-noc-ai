from uuid import UUID

from sqlalchemy.orm import Session

from app.models.device import Device
from app.models.site import Site
from app.schemas.device import DeviceCreate, DeviceUpdate


def create_device(db: Session, device_in: DeviceCreate) -> Device:
    site = db.query(Site).filter(Site.id == device_in.site_id).first()
    if not site:
        raise ValueError("Site not found")

    if site.tenant_id != device_in.tenant_id:
        raise ValueError("Device tenant_id must match Site tenant_id")

    device = Device(
        tenant_id=device_in.tenant_id,
        site_id=device_in.site_id,
        name=device_in.name,
        ip_address=device_in.ip_address,
        vendor=device_in.vendor,
        model=device_in.model,
        role=device_in.role,
        is_active=device_in.is_active,
    )
    db.add(device)
    db.commit()
    db.refresh(device)
    return device


def get_device(db: Session, device_id: UUID) -> Device | None:
    return db.query(Device).filter(Device.id == device_id).first()


def get_devices(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Device).offset(skip).limit(limit).all()


def update_device(
    db: Session, device_id: UUID, device_in: DeviceUpdate
) -> Device | None:
    device = get_device(db=db, device_id=device_id)
    if not device:
        return None

    update_data = device_in.model_dump(exclude_unset=True)

    if "site_id" in update_data:
        site = db.query(Site).filter(Site.id == update_data["site_id"]).first()
        if not site:
            raise ValueError("Site not found")

        if site.tenant_id != device.tenant_id:
            raise ValueError("Device tenant_id must match Site tenant_id")

    for field, value in update_data.items():
        setattr(device, field, value)

    db.add(device)
    db.commit()
    db.refresh(device)
    return device


def delete_device(db: Session, device_id: UUID) -> Device | None:
    device = get_device(db=db, device_id=device_id)
    if not device:
        return None

    device.is_active = False

    db.add(device)
    db.commit()
    db.refresh(device)
    return device
