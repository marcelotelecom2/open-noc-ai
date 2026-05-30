from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud.network_telemetry import (
    create_flow_record,
    delete_flow_record,
    get_flow_record,
    get_flow_records,
)
from app.schemas.flow_record import FlowRecordCreate, FlowRecordOut

router = APIRouter()


@router.post("/", response_model=FlowRecordOut)
def create(record_in: FlowRecordCreate, db: Session = Depends(get_db)):
    try:
        return create_flow_record(db=db, record_in=record_in)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/", response_model=list[FlowRecordOut])
def read_all(
    tenant_id: UUID,
    device_id: UUID | None = None,
    interface_id: UUID | None = None,
    link_id: UUID | None = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return get_flow_records(
        db=db,
        tenant_id=tenant_id,
        device_id=device_id,
        interface_id=interface_id,
        link_id=link_id,
        skip=skip,
        limit=limit,
    )


@router.get("/{record_id}", response_model=FlowRecordOut)
def read(record_id: UUID, tenant_id: UUID, db: Session = Depends(get_db)):
    record = get_flow_record(db=db, record_id=record_id, tenant_id=tenant_id)
    if not record:
        raise HTTPException(status_code=404, detail="Flow record not found")
    return record


@router.delete("/{record_id}", response_model=FlowRecordOut)
def deactivate(record_id: UUID, tenant_id: UUID, db: Session = Depends(get_db)):
    record = delete_flow_record(db=db, record_id=record_id, tenant_id=tenant_id)
    if not record:
        raise HTTPException(status_code=404, detail="Flow record not found")
    return record
