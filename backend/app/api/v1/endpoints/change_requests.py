from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud.ai_native_operations import create_change_request, delete_change_request, get_change_request, get_change_requests, update_change_request
from app.schemas.change_request import ChangeRequestCreate, ChangeRequestOut, ChangeRequestUpdate

router = APIRouter()


@router.post("/", response_model=ChangeRequestOut)
def create(change_in: ChangeRequestCreate, db: Session = Depends(get_db)):
    try:
        return create_change_request(db=db, change_in=change_in)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/", response_model=list[ChangeRequestOut])
def read_all(tenant_id: UUID, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_change_requests(db=db, tenant_id=tenant_id, skip=skip, limit=limit)


@router.get("/{change_id}", response_model=ChangeRequestOut)
def read(change_id: UUID, tenant_id: UUID, db: Session = Depends(get_db)):
    change = get_change_request(db=db, change_id=change_id, tenant_id=tenant_id)
    if not change:
        raise HTTPException(status_code=404, detail="Change request not found")
    return change


@router.put("/{change_id}", response_model=ChangeRequestOut)
def update(change_id: UUID, tenant_id: UUID, change_in: ChangeRequestUpdate, db: Session = Depends(get_db)):
    change = get_change_request(db=db, change_id=change_id, tenant_id=tenant_id)
    if not change:
        raise HTTPException(status_code=404, detail="Change request not found")
    return update_change_request(db=db, change=change, change_in=change_in)


@router.delete("/{change_id}", response_model=ChangeRequestOut)
def deactivate(change_id: UUID, tenant_id: UUID, db: Session = Depends(get_db)):
    change = delete_change_request(db=db, change_id=change_id, tenant_id=tenant_id)
    if not change:
        raise HTTPException(status_code=404, detail="Change request not found")
    return change
