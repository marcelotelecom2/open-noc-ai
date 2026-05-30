from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud.monitoring_core import create_check_result, get_check_results
from app.schemas.check_result import CheckResultCreate, CheckResultOut

router = APIRouter()


@router.post("/", response_model=CheckResultOut)
def create(result_in: CheckResultCreate, db: Session = Depends(get_db)):
    try:
        return create_check_result(db=db, result_in=result_in)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/", response_model=list[CheckResultOut])
def read_all(tenant_id: UUID, monitoring_check_id: UUID | None = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_check_results(db=db, tenant_id=tenant_id, monitoring_check_id=monitoring_check_id, skip=skip, limit=limit)
