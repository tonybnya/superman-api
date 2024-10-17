"""
Router for customer-related endpoints.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from api.models.customer import Customer as CustomerModel
from api.dependencies import get_db

router = APIRouter(
    prefix="/customers",
    tags=["customers"]
)


# Pydantic models
class CustomerBase(BaseModel):
    """Create the Pydantic model of a customer."""
    firstname: str
    lastname: str
    email: EmailStr
    phone: str
    delivery_address: str
    billing_address: str


class Customer(CustomerBase):
    """Create the model of the customer based on the CustomerBase."""
    id: int

    class Config:
        """Provide configurations to Pydantic."""
        orm_mode = True


# Create a new customer
@router.post("/", response_model=Customer)
async def create_customer(customer: CustomerBase, db: Session = Depends(get_db)):
    """POST /customers endpoint to create a product."""
    db_customer = CustomerModel(**customer.model_dump())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer


# Retrieve a list of customers
@router.get("/", response_model=List[Customer])
async def get_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """GET /customers endpoint to get all the customers."""
    customers = db.query(CustomerModel).offset(skip).limit(limit).all()
    return customers


# Retrieve a single customer
@router.get("/{customer_id}", response_model=Customer)
async def get_customer(customer_id: int, db: Session = Depends(get_db)):
    """GET /customers/{customer_id} endpoint to retrieve a customer by its ID."""
    customer = db.query(CustomerModel).filter(CustomerModel.id == customer_id).first()
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


# Update a single customer
@router.put("/{customer_id}", response_model=Customer)
async def update_customer(
    customer_id: int,
    updated_customer: CustomerBase,
    db: Session = Depends(get_db)
):
    """PUT /customers/{customer_id} endpoint to update a product by its ID."""
    customer = db.query(CustomerModel).filter(CustomerModel.id == customer_id).first()
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    for key, value in updated_customer.model_dump().items():
        setattr(customer, key, value)
    db.commit()
    db.refresh(customer)
    return customer


# Delete a single customer
@router.delete("/{customer_id}", response_model=dict[str, str])
async def delete_product(customer_id: int, db: Session = Depends(get_db)):
    """DELETE /customers/{customer_id} endpoint to delete a customer by its ID."""
    customer = db.query(CustomerModel).filter(CustomerModel.id == customer_id).first()
    if customer is None:
        raise HTTPException(status_code = 404, detail="Customer not found")
    db.delete(customer)
    db.commit()
    return {"message": "Customer successfully deleted"}
