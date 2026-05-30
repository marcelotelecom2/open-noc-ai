from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud.network_telemetry import (
    create_syslog_message,
    delete_syslog_message,
    get_syslog_message,
    get_syslog_messages,
)
from app.schemas.syslog_message import SyslogMessageCreate, SyslogMessageOut

router = APIRouter()


@router.post("/", response_model=SyslogMessageOut)
def create(message_in: SyslogMessageCreate, db: Session = Depends(get_db)):
    try:
        return create_syslog_message(db=db, message_in=message_in)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/", response_model=list[SyslogMessageOut])
def read_all(
    tenant_id: UUID,
    device_id: UUID | None = None,
    severity: int | None = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return get_syslog_messages(
        db=db,
        tenant_id=tenant_id,
        device_id=device_id,
        severity=severity,
        skip=skip,
        limit=limit,
    )


@router.get("/{message_id}", response_model=SyslogMessageOut)
def read(message_id: UUID, tenant_id: UUID, db: Session = Depends(get_db)):
    message = get_syslog_message(db=db, message_id=message_id, tenant_id=tenant_id)
    if not message:
        raise HTTPException(status_code=404, detail="Syslog message not found")
    return message


@router.delete("/{message_id}", response_model=SyslogMessageOut)
def deactivate(message_id: UUID, tenant_id: UUID, db: Session = Depends(get_db)):
    message = delete_syslog_message(db=db, message_id=message_id, tenant_id=tenant_id)
    if not message:
        raise HTTPException(status_code=404, detail="Syslog message not found")
    return message
