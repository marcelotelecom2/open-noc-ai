from uuid import UUID

from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.crud.tenant import get_tenant
from app.models.user import User
from app.schemas.user import UserCreate


def create_user(db: Session, user_in: UserCreate) -> User:
    tenant = get_tenant(db=db, tenant_id=user_in.tenant_id)
    if not tenant:
        raise ValueError("Tenant not found")

    user = User(
        tenant_id=user_in.tenant_id,
        email=user_in.email,
        full_name=user_in.full_name,
        hashed_password=get_password_hash(user_in.password),
        is_active=user_in.is_active,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_users(db: Session, tenant_id: UUID, skip: int = 0, limit: int = 100):
    return (
        db.query(User)
        .filter(User.tenant_id == tenant_id)
        .filter(User.is_active.is_(True))
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_user_by_email(
    db: Session,
    tenant_id: UUID,
    email: str,
) -> User | None:
    return (
        db.query(User)
        .filter(User.tenant_id == tenant_id)
        .filter(User.email == email)
        .filter(User.is_active.is_(True))
        .first()
    )


def verify_user_password(
    db: Session,
    tenant_id: UUID,
    email: str,
    password: str,
) -> bool | None:
    user = get_user_by_email(db=db, tenant_id=tenant_id, email=email)
    if not user:
        return None

    return verify_password(password, user.hashed_password)
