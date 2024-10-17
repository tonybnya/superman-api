"""
Router for purchase-related endpoints.
"""
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime, timezone
from api.models.purchase import Purchase as PurchaseModel
from api.dependencies import get_db


router = APIRouter(
    prefix="/purchases",
    tags=["purchases"]
)


# Pydantic models
class PurchaseBase(BaseModel):
    """Create the Pydantic model of a purchase."""
    customer_id: int
    product_id: int
    delivery_id: int
    quantity: int
    purchase_date: datetime = datetime.now(timezone.utc)


class Purchase(PurchaseBase):
    """Create the model of the purchase based on the PurchaseBase."""
    id: int

    class Config:
        """Provide configurations to Pydantic."""
        # orm_mode = True
        from_attributes = True


# Create a new purchase
@router.post("/", response_model=Purchase)
async def create_purchase(purchase: PurchaseBase, db: Session = Depends(get_db)):
    db_purchase = PurchaseModel(**purchase.model_dump())
    db.add(db_purchase)
    db.commit()
    db.refresh(db_purchase)
    return db_purchase


# Retrieve a list of all purchases
@router.get("/", response_model=List[Purchase])
async def get_purchases(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """GET /purchases endpoint to get all the purchases."""
    purchases = db.query(PurchaseModel).offset(skip).limit(limit).all()
    return purchases


# Retrieve the list of all purchases for a customer
@router.get("/customers/{customer_id}", response_model=List[Purchase])
async def get_customer_purchases(customer_id: int, db: Session = Depends(get_db)):
    """GET /purchases/customers/{customer_id} endpoint to get purchases of a customer."""
    return db.query(PurchaseModel).filter(PurchaseModel.customer_id == customer_id).all()
