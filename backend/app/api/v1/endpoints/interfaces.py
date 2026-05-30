from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud.interface import (
    create_interface,
    delete_interface,
    get_interface,
    get_interfaces,
    update_interface,
)
from app.schemas.interface import InterfaceCreate, InterfaceOut, InterfaceUpdate

router = APIRouter()


@router.post("/", response_model=InterfaceOut)
def create(interface_in: InterfaceCreate, db: Session = Depends(get_db)):
    try:
        return create_interface(db=db, interface_in=interface_in)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/", response_model=list[InterfaceOut])
def read_all(
    tenant_id: UUID,
    device_id: UUID | None = None,
    link_id: UUID | None = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return get_interfaces(
        db=db,
        tenant_id=tenant_id,
        device_id=device_id,
        link_id=link_id,
        skip=skip,
        limit=limit,
    )


@router.get("/{interface_id}", response_model=InterfaceOut)
def read(interface_id: UUID, tenant_id: UUID, db: Session = Depends(get_db)):
    interface = get_interface(db=db, interface_id=interface_id, tenant_id=tenant_id)
    if not interface:
        raise HTTPException(status_code=404, detail="Interface not found")
    return interface


@router.put("/{interface_id}", response_model=InterfaceOut)
def update(
    interface_id: UUID,
    tenant_id: UUID,
    interface_in: InterfaceUpdate,
    db: Session = Depends(get_db),
):
    interface = get_interface(db=db, interface_id=interface_id, tenant_id=tenant_id)
    if not interface:
        raise HTTPException(status_code=404, detail="Interface not found")

    try:
        return update_interface(
            db=db,
            interface=interface,
            interface_in=interface_in,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.delete("/{interface_id}", response_model=InterfaceOut)
def deactivate(interface_id: UUID, tenant_id: UUID, db: Session = Depends(get_db)):
    interface = delete_interface(
        db=db,
        interface_id=interface_id,
        tenant_id=tenant_id,
    )
    if not interface:
        raise HTTPException(status_code=404, detail="Interface not found")
    return interface
