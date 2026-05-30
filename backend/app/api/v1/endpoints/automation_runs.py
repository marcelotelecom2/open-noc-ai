from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud.ai_native_operations import create_automation_run, delete_automation_run, get_automation_run, get_automation_runs, update_automation_run
from app.schemas.automation_run import AutomationRunCreate, AutomationRunOut, AutomationRunUpdate

router = APIRouter()


@router.post("/", response_model=AutomationRunOut)
def create(run_in: AutomationRunCreate, db: Session = Depends(get_db)):
    try:
        return create_automation_run(db=db, run_in=run_in)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/", response_model=list[AutomationRunOut])
def read_all(tenant_id: UUID, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_automation_runs(db=db, tenant_id=tenant_id, skip=skip, limit=limit)


@router.get("/{run_id}", response_model=AutomationRunOut)
def read(run_id: UUID, tenant_id: UUID, db: Session = Depends(get_db)):
    run = get_automation_run(db=db, run_id=run_id, tenant_id=tenant_id)
    if not run:
        raise HTTPException(status_code=404, detail="Automation run not found")
    return run


@router.put("/{run_id}", response_model=AutomationRunOut)
def update(run_id: UUID, tenant_id: UUID, run_in: AutomationRunUpdate, db: Session = Depends(get_db)):
    run = get_automation_run(db=db, run_id=run_id, tenant_id=tenant_id)
    if not run:
        raise HTTPException(status_code=404, detail="Automation run not found")
    return update_automation_run(db=db, run=run, run_in=run_in)


@router.delete("/{run_id}", response_model=AutomationRunOut)
def deactivate(run_id: UUID, tenant_id: UUID, db: Session = Depends(get_db)):
    run = delete_automation_run(db=db, run_id=run_id, tenant_id=tenant_id)
    if not run:
        raise HTTPException(status_code=404, detail="Automation run not found")
    return run
