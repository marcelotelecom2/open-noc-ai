from uuid import UUID

from sqlalchemy.orm import Session

from app.models.site import Site
from app.schemas.site import SiteCreate


def create_site(db: Session, site_in: SiteCreate) -> Site:
    site = Site(
        tenant_id=site_in.tenant_id,
        customer_id=site_in.customer_id,
        name=site_in.name,
        city=site_in.city,
        state=site_in.state,
        is_active=site_in.is_active,
    )
    db.add(site)
    db.commit()
    db.refresh(site)
    return site


def get_site(db: Session, site_id: UUID) -> Site | None:
    return db.query(Site).filter(Site.id == site_id).first()


def get_sites(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Site).offset(skip).limit(limit).all()
