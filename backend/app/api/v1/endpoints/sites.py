from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud.site import create_site, delete_site, get_site, get_sites, update_site
from app.schemas.site import SiteCreate, SiteOut, SiteUpdate

router = APIRouter()


@router.post("/", response_model=SiteOut)
def create(site_in: SiteCreate, db: Session = Depends(get_db)):
    return create_site(db=db, site_in=site_in)


@router.get("/", response_model=list[SiteOut])
def read_all(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_sites(db=db, skip=skip, limit=limit)


@router.get("/{site_id}", response_model=SiteOut)
def read(site_id: UUID, db: Session = Depends(get_db)):
    site = get_site(db=db, site_id=site_id)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    return site


@router.put("/{site_id}", response_model=SiteOut)
def update(
    site_id: UUID,
    site_in: SiteUpdate,
    db: Session = Depends(get_db),
):
    site = get_site(db=db, site_id=site_id)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")

    return update_site(db=db, site=site, site_in=site_in)


@router.delete("/{site_id}", response_model=SiteOut)
def deactivate(site_id: UUID, db: Session = Depends(get_db)):
    site = get_site(db=db, site_id=site_id)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")

    return delete_site(db=db, site=site)