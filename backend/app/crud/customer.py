from sqlalchemy.orm import Session
from uuid import UUID

from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerUpdate


def create_customer(db: Session, customer_in: CustomerCreate) -> Customer:
    customer = Customer(
        tenant_id=customer_in.tenant_id,
        name=customer_in.name,
        document=customer_in.document,
        is_active=customer_in.is_active,
    )
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


def get_customer(db: Session, customer_id: UUID) -> Customer | None:
    return db.query(Customer).filter(Customer.id == customer_id).first()


def get_customers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Customer).offset(skip).limit(limit).all()


def update_customer(
    db: Session, customer: Customer, customer_in: CustomerUpdate
) -> Customer:
    update_data = customer_in.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(customer, field, value)

    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer