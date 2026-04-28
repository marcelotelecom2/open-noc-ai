from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import uuid4

from app.api.deps import get_db_session
from app.models.user import User
from app.schemas.user import UserResponse, UserCreate
from app.core.security import get_password_hash, verify_password

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
        hashed_password=get_password_hash(payload.password),
        is_active=payload.is_active,
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/verify")
def verify_user_password(
    email: str,
    password: str,
    db: Session = Depends(get_db_session),
):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        return {"error": "User not found"}

    valid = verify_password(password, user.hashed_password)

    return {"valid": valid}
