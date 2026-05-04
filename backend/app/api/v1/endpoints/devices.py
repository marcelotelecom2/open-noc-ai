from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud.device import (
    create_device,
    delete_device,
    get_device,
    get_devices,
    update_device,
)
from app.schemas.device import DeviceCreate, DeviceOut, DeviceUpdate

router = APIRouter()


@router.post("/", response_model=DeviceOut)
def create(device_in: DeviceCreate, db: Session = Depends(get_db)):
    try:
        return create_device(db=db, device_in=device_in)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/", response_model=list[DeviceOut])
def read_all(
    tenant_id: UUID,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return get_devices(db=db, tenant_id=tenant_id, skip=skip, limit=limit)


@router.get("/{device_id}", response_model=DeviceOut)
def read(device_id: UUID, tenant_id: UUID, db: Session = Depends(get_db)):
    device = get_device(db=db, device_id=device_id, tenant_id=tenant_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device


@router.put("/{device_id}", response_model=DeviceOut)
def update(
    device_id: UUID,
    tenant_id: UUID,
    device_in: DeviceUpdate,
    db: Session = Depends(get_db),
):
    try:
        device = update_device(
            db=db,
            device_id=device_id,
            tenant_id=tenant_id,
            device_in=device_in,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    return device


@router.delete("/{device_id}", response_model=DeviceOut)
def deactivate(device_id: UUID, tenant_id: UUID, db: Session = Depends(get_db)):
    device = delete_device(db=db, device_id=device_id, tenant_id=tenant_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    return device
