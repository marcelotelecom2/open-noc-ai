from uuid import UUID

from sqlalchemy.orm import Session

from app.models.carrier import Carrier
from app.schemas.carrier import CarrierCreate, CarrierUpdate


def create_carrier(db: Session, carrier_in: CarrierCreate) -> Carrier:
    carrier = Carrier(
        tenant_id=carrier_in.tenant_id,
        name=carrier_in.name,
        type=carrier_in.type,
        is_active=True,
    )
    db.add(carrier)
    db.commit()
    db.refresh(carrier)
    return carrier


def get_carrier(
    db: Session,
    carrier_id: UUID,
    tenant_id: UUID | None = None,
) -> Carrier | None:
    query = (
        db.query(Carrier)
        .filter(Carrier.id == carrier_id)
        .filter(Carrier.is_active.is_(True))
    )
    if tenant_id is not None:
        query = query.filter(Carrier.tenant_id == tenant_id)
    return query.first()


def get_carriers(db: Session, tenant_id: UUID, skip: int = 0, limit: int = 100):
    return (
        db.query(Carrier)
        .filter(Carrier.tenant_id == tenant_id)
        .filter(Carrier.is_active.is_(True))
        .offset(skip)
        .limit(limit)
        .all()
    )


def update_carrier(
    db: Session, carrier: Carrier, carrier_in: CarrierUpdate
) -> Carrier:
    update_data = carrier_in.model_dump(exclude_unset=True)
    update_data.pop("tenant_id", None)

    for field, value in update_data.items():
        setattr(carrier, field, value)

    db.add(carrier)
    db.commit()
    db.refresh(carrier)
    return carrier


def delete_carrier(
    db: Session,
    carrier_id: UUID,
    tenant_id: UUID,
) -> Carrier | None:
    carrier = get_carrier(db=db, carrier_id=carrier_id, tenant_id=tenant_id)
    if not carrier:
        return None

    carrier.is_active = False

    db.add(carrier)
    db.commit()
    db.refresh(carrier)
    return carrier
