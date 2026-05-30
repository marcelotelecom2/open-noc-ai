from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud.network_telemetry import (
    create_snmp_trap,
    delete_snmp_trap,
    get_snmp_trap,
    get_snmp_traps,
)
from app.schemas.snmp_trap import SNMPTrapCreate, SNMPTrapOut

router = APIRouter()


@router.post("/", response_model=SNMPTrapOut)
def create(trap_in: SNMPTrapCreate, db: Session = Depends(get_db)):
    try:
        return create_snmp_trap(db=db, trap_in=trap_in)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/", response_model=list[SNMPTrapOut])
def read_all(
    tenant_id: UUID,
    device_id: UUID | None = None,
    trap_oid: str | None = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return get_snmp_traps(
        db=db,
        tenant_id=tenant_id,
        device_id=device_id,
        trap_oid=trap_oid,
        skip=skip,
        limit=limit,
    )


@router.get("/{trap_id}", response_model=SNMPTrapOut)
def read(trap_id: UUID, tenant_id: UUID, db: Session = Depends(get_db)):
    trap = get_snmp_trap(db=db, trap_id=trap_id, tenant_id=tenant_id)
    if not trap:
        raise HTTPException(status_code=404, detail="SNMP trap not found")
    return trap


@router.delete("/{trap_id}", response_model=SNMPTrapOut)
def deactivate(trap_id: UUID, tenant_id: UUID, db: Session = Depends(get_db)):
    trap = delete_snmp_trap(db=db, trap_id=trap_id, tenant_id=tenant_id)
    if not trap:
        raise HTTPException(status_code=404, detail="SNMP trap not found")
    return trap
