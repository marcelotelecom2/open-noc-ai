from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud.customer import create_customer, get_customer, get_customers, update_customer
from app.schemas.customer import CustomerCreate, CustomerOut, CustomerUpdate

router = APIRouter()


@router.post("/", response_model=CustomerOut)
def create(customer_in: CustomerCreate, db: Session = Depends(get_db)):
    return create_customer(db=db, customer_in=customer_in)


@router.get("/", response_model=list[CustomerOut])
def read_all(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_customers(db=db, skip=skip, limit=limit)


@router.get("/{customer_id}", response_model=CustomerOut)
def read(customer_id: UUID, db: Session = Depends(get_db)):
    customer = get_customer(db=db, customer_id=customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@router.put("/{customer_id}", response_model=CustomerOut)
def update(
    customer_id: UUID,
    customer_in: CustomerUpdate,
    db: Session = Depends(get_db),
):
    customer = get_customer(db=db, customer_id=customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    return update_customer(db=db, customer=customer, customer_in=customer_in)
