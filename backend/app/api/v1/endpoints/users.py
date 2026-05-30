from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud.user import (
    create_user,
    get_users,
    verify_user_password as verify_user_password_crud,
)
from app.schemas.user import UserResponse, UserCreate

router = APIRouter()


@router.get("/", response_model=list[UserResponse])
def list_users(
    tenant_id: UUID,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return get_users(db=db, tenant_id=tenant_id, skip=skip, limit=limit)


@router.post("/", response_model=UserResponse)
def create(payload: UserCreate, db: Session = Depends(get_db)):
    try:
        return create_user(db=db, user_in=payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/verify")
def verify_user_password(
    tenant_id: UUID,
    email: str,
    password: str,
    db: Session = Depends(get_db),
):
    valid = verify_user_password_crud(
        db=db,
        tenant_id=tenant_id,
        email=email,
        password=password,
    )
    if valid is None:
        raise HTTPException(status_code=404, detail="User not found")

    return {"valid": valid}
