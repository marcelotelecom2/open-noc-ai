from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud.ai_native_operations import create_runbook, delete_runbook, get_runbook, get_runbooks, update_runbook
from app.schemas.runbook import RunbookCreate, RunbookOut, RunbookUpdate

router = APIRouter()


@router.post("/", response_model=RunbookOut)
def create(runbook_in: RunbookCreate, db: Session = Depends(get_db)):
    try:
        return create_runbook(db=db, runbook_in=runbook_in)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/", response_model=list[RunbookOut])
def read_all(tenant_id: UUID, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_runbooks(db=db, tenant_id=tenant_id, skip=skip, limit=limit)


@router.get("/{runbook_id}", response_model=RunbookOut)
def read(runbook_id: UUID, tenant_id: UUID, db: Session = Depends(get_db)):
    runbook = get_runbook(db=db, runbook_id=runbook_id, tenant_id=tenant_id)
    if not runbook:
        raise HTTPException(status_code=404, detail="Runbook not found")
    return runbook


@router.put("/{runbook_id}", response_model=RunbookOut)
def update(runbook_id: UUID, tenant_id: UUID, runbook_in: RunbookUpdate, db: Session = Depends(get_db)):
    runbook = get_runbook(db=db, runbook_id=runbook_id, tenant_id=tenant_id)
    if not runbook:
        raise HTTPException(status_code=404, detail="Runbook not found")
    return update_runbook(db=db, runbook=runbook, runbook_in=runbook_in)


@router.delete("/{runbook_id}", response_model=RunbookOut)
def deactivate(runbook_id: UUID, tenant_id: UUID, db: Session = Depends(get_db)):
    runbook = delete_runbook(db=db, runbook_id=runbook_id, tenant_id=tenant_id)
    if not runbook:
        raise HTTPException(status_code=404, detail="Runbook not found")
    return runbook
