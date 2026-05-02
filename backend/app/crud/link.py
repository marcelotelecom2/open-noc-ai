from uuid import UUID

from sqlalchemy.orm import Session

from app.models.carrier import Carrier
from app.models.link import Link
from app.models.site import Site
from app.schemas.link import LinkCreate, LinkUpdate


def _validate_link_tenant(
    db: Session,
    tenant_id: UUID,
    site_id: UUID,
    carrier_id: UUID,
) -> None:
    site = db.query(Site).filter(Site.id == site_id).first()
    if not site:
        raise ValueError("Site not found")

    carrier = db.query(Carrier).filter(Carrier.id == carrier_id).first()
    if not carrier:
        raise ValueError("Carrier not found")

    if site.tenant_id != tenant_id:
        raise ValueError("Link tenant_id must match Site tenant_id")

    if carrier.tenant_id != tenant_id:
        raise ValueError("Link tenant_id must match Carrier tenant_id")


def create_link(db: Session, link_in: LinkCreate) -> Link:
    _validate_link_tenant(
        db=db,
        tenant_id=link_in.tenant_id,
        site_id=link_in.site_id,
        carrier_id=link_in.carrier_id,
    )

    link = Link(
        tenant_id=link_in.tenant_id,
        site_id=link_in.site_id,
        carrier_id=link_in.carrier_id,
        type=link_in.type,
        bandwidth=link_in.bandwidth,
        status=link_in.status,
        is_active=link_in.is_active,
    )
    db.add(link)
    db.commit()
    db.refresh(link)
    return link


def get_link(db: Session, link_id: UUID) -> Link | None:
    return db.query(Link).filter(Link.id == link_id).first()


def get_links(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Link).offset(skip).limit(limit).all()


def update_link(db: Session, link: Link, link_in: LinkUpdate) -> Link:
    update_data = link_in.model_dump(exclude_unset=True)

    tenant_id = update_data.get("tenant_id", link.tenant_id)
    site_id = update_data.get("site_id", link.site_id)
    carrier_id = update_data.get("carrier_id", link.carrier_id)
    _validate_link_tenant(
        db=db,
        tenant_id=tenant_id,
        site_id=site_id,
        carrier_id=carrier_id,
    )

    for field, value in update_data.items():
        setattr(link, field, value)

    db.add(link)
    db.commit()
    db.refresh(link)
    return link


def delete_link(db: Session, link: Link) -> Link:
    link.is_active = False

    db.add(link)
    db.commit()
    db.refresh(link)
    return link
