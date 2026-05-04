from uuid import UUID

from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.site import Site
from app.schemas.site import SiteCreate, SiteUpdate


def _validate_site_customer(
    db: Session,
    tenant_id: UUID,
    customer_id: UUID,
) -> None:
    customer = (
        db.query(Customer)
        .filter(Customer.id == customer_id)
        .filter(Customer.tenant_id == tenant_id)
        .filter(Customer.is_active.is_(True))
        .first()
    )
    if not customer:
        raise ValueError("Customer not found")


def create_site(db: Session, site_in: SiteCreate) -> Site:
    _validate_site_customer(
        db=db,
        tenant_id=site_in.tenant_id,
        customer_id=site_in.customer_id,
    )

    site = Site(
        tenant_id=site_in.tenant_id,
        customer_id=site_in.customer_id,
        name=site_in.name,
        city=site_in.city,
        state=site_in.state,
        is_active=True,
    )
    db.add(site)
    db.commit()
    db.refresh(site)
    return site


def get_site(
    db: Session,
    site_id: UUID,
    tenant_id: UUID | None = None,
) -> Site | None:
    query = (
        db.query(Site)
        .filter(Site.id == site_id)
        .filter(Site.is_active.is_(True))
    )
    if tenant_id is not None:
        query = query.filter(Site.tenant_id == tenant_id)
    return query.first()


def get_sites(db: Session, tenant_id: UUID, skip: int = 0, limit: int = 100):
    return (
        db.query(Site)
        .filter(Site.tenant_id == tenant_id)
        .filter(Site.is_active.is_(True))
        .offset(skip)
        .limit(limit)
        .all()
    )


def update_site(db: Session, site: Site, site_in: SiteUpdate) -> Site:
    update_data = site_in.model_dump(exclude_unset=True)
    update_data.pop("tenant_id", None)

    customer_id = update_data.get("customer_id", site.customer_id)
    _validate_site_customer(
        db=db,
        tenant_id=site.tenant_id,
        customer_id=customer_id,
    )

    for field, value in update_data.items():
        setattr(site, field, value)

    db.add(site)
    db.commit()
    db.refresh(site)
    return site


def delete_site(
    db: Session,
    site_id: UUID,
    tenant_id: UUID,
) -> Site | None:
    site = get_site(db=db, site_id=site_id, tenant_id=tenant_id)
    if not site:
        return None

    site.is_active = False

    db.add(site)
    db.commit()
    db.refresh(site)
    return site
