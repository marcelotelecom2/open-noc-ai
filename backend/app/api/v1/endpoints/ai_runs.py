from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud.ai_native_operations import create_ai_run, delete_ai_run, get_ai_run, get_ai_runs, update_ai_run
from app.schemas.ai_run import AIRunCreate, AIRunOut, AIRunUpdate

router = APIRouter()


@router.post("/", response_model=AIRunOut)
def create(run_in: AIRunCreate, db: Session = Depends(get_db)):
    try:
        return create_ai_run(db=db, run_in=run_in)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/", response_model=list[AIRunOut])
def read_all(tenant_id: UUID, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_ai_runs(db=db, tenant_id=tenant_id, skip=skip, limit=limit)


@router.get("/{run_id}", response_model=AIRunOut)
def read(run_id: UUID, tenant_id: UUID, db: Session = Depends(get_db)):
    run = get_ai_run(db=db, run_id=run_id, tenant_id=tenant_id)
    if not run:
        raise HTTPException(status_code=404, detail="AI run not found")
    return run


@router.put("/{run_id}", response_model=AIRunOut)
def update(run_id: UUID, tenant_id: UUID, run_in: AIRunUpdate, db: Session = Depends(get_db)):
    run = get_ai_run(db=db, run_id=run_id, tenant_id=tenant_id)
    if not run:
        raise HTTPException(status_code=404, detail="AI run not found")
    return update_ai_run(db=db, run=run, run_in=run_in)


@router.delete("/{run_id}", response_model=AIRunOut)
def deactivate(run_id: UUID, tenant_id: UUID, db: Session = Depends(get_db)):
    run = delete_ai_run(db=db, run_id=run_id, tenant_id=tenant_id)
    if not run:
        raise HTTPException(status_code=404, detail="AI run not found")
    return run
