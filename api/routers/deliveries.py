"""
Router for delivery-related endpoints.
"""
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from api.models.delivery import Delivery as DeliveryModel
from api.dependencies import get_db


# Create a router for delivery-related routes
router = APIRouter(
    prefix="/deliveries",
    tags=["deliveries"]
)


# Pydantic models
class DeliveryBase(BaseModel):
    """Create the Pydantic model of a delivery."""
    type: str
    min_days: int
    max_days: int


class Delivery(DeliveryBase):
    """Create the model of the delivery based on the DeliveryBase."""
    id: int

    class Config:
        """Provide configurations to Pydantic."""
        # orm_mode = True
        from_attributes = True


# Create a new delivery
@router.post("/", response_model=Delivery)
async def create_delivery(delivery: DeliveryBase, db: Session = Depends(get_db)):
    """GET /deliveries endpoint to get all the deliveries."""
    db_delivery = DeliveryModel(**delivery.model_dump())
    db.add(db_delivery)
    db.commit()
    db.refresh(db_delivery)
    return db_delivery


# Get a list of deliveries
@router.get("/", response_model=List[Delivery])
async def get_deliveries(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    deliveries = db.query(DeliveryModel).offset(skip).limit(limit).all()
    return deliveries
