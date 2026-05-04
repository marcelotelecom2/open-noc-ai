from sqlalchemy.orm import Session
from uuid import UUID

from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerUpdate


def create_customer(db: Session, customer_in: CustomerCreate) -> Customer:
    customer = Customer(
        tenant_id=customer_in.tenant_id,
        name=customer_in.name,
        document=customer_in.document,
        is_active=True,
    )
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


def get_customer(
    db: Session,
    customer_id: UUID,
    tenant_id: UUID | None = None,
) -> Customer | None:
    query = (
        db.query(Customer)
        .filter(Customer.id == customer_id)
        .filter(Customer.is_active.is_(True))
    )
    if tenant_id is not None:
        query = query.filter(Customer.tenant_id == tenant_id)
    return query.first()


def get_customers(db: Session, tenant_id: UUID, skip: int = 0, limit: int = 100):
    return (
        db.query(Customer)
        .filter(Customer.tenant_id == tenant_id)
        .filter(Customer.is_active.is_(True))
        .offset(skip)
        .limit(limit)
        .all()
    )


def update_customer(
    db: Session, customer: Customer, customer_in: CustomerUpdate
) -> Customer:
    update_data = customer_in.model_dump(exclude_unset=True)
    update_data.pop("tenant_id", None)

    for field, value in update_data.items():
        setattr(customer, field, value)

    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


def delete_customer(
    db: Session,
    customer_id: UUID,
    tenant_id: UUID,
) -> Customer | None:
    customer = get_customer(db=db, customer_id=customer_id, tenant_id=tenant_id)
    if not customer:
        return None

    customer.is_active = False

    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer
