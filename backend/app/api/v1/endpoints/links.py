from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud.link import create_link, delete_link, get_link, get_links, update_link
from app.schemas.link import LinkCreate, LinkOut, LinkUpdate

router = APIRouter()


@router.post("/", response_model=LinkOut)
def create(link_in: LinkCreate, db: Session = Depends(get_db)):
    try:
        return create_link(db=db, link_in=link_in)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/", response_model=list[LinkOut])
def read_all(
    tenant_id: UUID,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return get_links(db=db, tenant_id=tenant_id, skip=skip, limit=limit)


@router.get("/{link_id}", response_model=LinkOut)
def read(link_id: UUID, tenant_id: UUID, db: Session = Depends(get_db)):
    link = get_link(db=db, link_id=link_id, tenant_id=tenant_id)
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    return link


@router.put("/{link_id}", response_model=LinkOut)
def update(
    link_id: UUID,
    tenant_id: UUID,
    link_in: LinkUpdate,
    db: Session = Depends(get_db),
):
    link = get_link(db=db, link_id=link_id, tenant_id=tenant_id)
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")

    try:
        return update_link(db=db, link=link, link_in=link_in)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.delete("/{link_id}", response_model=LinkOut)
def deactivate(link_id: UUID, tenant_id: UUID, db: Session = Depends(get_db)):
    link = delete_link(db=db, link_id=link_id, tenant_id=tenant_id)
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")

    return link
