from uuid import UUID

from sqlalchemy.orm import Session

from app.models.carrier import Carrier
from app.schemas.carrier import CarrierCreate, CarrierUpdate


def create_carrier(db: Session, carrier_in: CarrierCreate) -> Carrier:
    carrier = Carrier(
        name=carrier_in.name,
        type=carrier_in.type,
    )
    db.add(carrier)
    db.commit()
    db.refresh(carrier)
    return carrier


def get_carrier(db: Session, carrier_id: UUID) -> Carrier | None:
    return db.query(Carrier).filter(Carrier.id == carrier_id).first()


def get_carriers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Carrier).offset(skip).limit(limit).all()


def update_carrier(
    db: Session, carrier: Carrier, carrier_in: CarrierUpdate
) -> Carrier:
    update_data = carrier_in.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(carrier, field, value)

    db.add(carrier)
    db.commit()
    db.refresh(carrier)
    return carrier


def delete_carrier(db: Session, carrier: Carrier) -> Carrier:
    db.delete(carrier)
    db.commit()
    return carrier
