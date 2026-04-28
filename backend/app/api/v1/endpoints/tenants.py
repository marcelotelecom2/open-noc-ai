from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db_session
from app.models.tenant import Tenant

router = APIRouter()


@router.get("/")
def list_tenants(db: Session = Depends(get_db_session)):
    return db.query(Tenant).all()
