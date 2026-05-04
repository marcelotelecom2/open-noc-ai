from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud.carrier import (
    create_carrier,
    delete_carrier,
    get_carrier,
    get_carriers,
    update_carrier,
)
from app.schemas.carrier import CarrierCreate, CarrierOut, CarrierUpdate

router = APIRouter()


@router.post("/", response_model=CarrierOut)
def create(carrier_in: CarrierCreate, db: Session = Depends(get_db)):
    try:
        return create_carrier(db=db, carrier_in=carrier_in)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/", response_model=list[CarrierOut])
def read_all(
    tenant_id: UUID,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return get_carriers(db=db, tenant_id=tenant_id, skip=skip, limit=limit)


@router.get("/{carrier_id}", response_model=CarrierOut)
def read(carrier_id: UUID, tenant_id: UUID, db: Session = Depends(get_db)):
    carrier = get_carrier(db=db, carrier_id=carrier_id, tenant_id=tenant_id)
    if not carrier:
        raise HTTPException(status_code=404, detail="Carrier not found")
    return carrier


@router.put("/{carrier_id}", response_model=CarrierOut)
def update(
    carrier_id: UUID,
    tenant_id: UUID,
    carrier_in: CarrierUpdate,
    db: Session = Depends(get_db),
):
    carrier = get_carrier(db=db, carrier_id=carrier_id, tenant_id=tenant_id)
    if not carrier:
        raise HTTPException(status_code=404, detail="Carrier not found")

    try:
        return update_carrier(db=db, carrier=carrier, carrier_in=carrier_in)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.delete("/{carrier_id}", response_model=CarrierOut)
def deactivate(carrier_id: UUID, tenant_id: UUID, db: Session = Depends(get_db)):
    carrier = delete_carrier(
        db=db,
        carrier_id=carrier_id,
        tenant_id=tenant_id,
    )
    if not carrier:
        raise HTTPException(status_code=404, detail="Carrier not found")

    return carrier
