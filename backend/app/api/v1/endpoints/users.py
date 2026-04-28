from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import uuid4

from app.api.deps import get_db_session
from app.models.user import User
from app.models.tenant import Tenant

router = APIRouter()


@router.get("/")
def list_users(db: Session = Depends(get_db_session)):
    return db.query(User).all()


@router.post("/")
def create_user(db: Session = Depends(get_db_session)):
    tenant = db.query(Tenant).first()

    user = User(
        id=uuid4(),
        tenant_id=tenant.id,
        email="user@test.com",
        full_name="Test User",
        hashed_password="fakehashed",
        is_active=True,
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user
