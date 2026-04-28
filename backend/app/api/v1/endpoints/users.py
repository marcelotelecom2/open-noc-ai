from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import uuid4

from app.api.deps import get_db_session
from app.models.user import User
from app.schemas.user import UserResponse, UserCreate

router = APIRouter()


@router.get("/", response_model=list[UserResponse])
def list_users(db: Session = Depends(get_db_session)):
    return db.query(User).all()


@router.post("/", response_model=UserResponse)
def create_user(payload: UserCreate, db: Session = Depends(get_db_session)):
    user = User(
        id=uuid4(),
        tenant_id=payload.tenant_id,
        email=payload.email,
        full_name=payload.full_name,
        hashed_password="fakehashed",
        is_active=payload.is_active,
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user
