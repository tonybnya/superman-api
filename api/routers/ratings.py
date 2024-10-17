"""
Router for rating-related endpoints.
"""
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from api.models.rating import Rating as RatingModel
from api.dependencies import get_db


# Create a souter for rating-related routes
router = APIRouter(
    prefix="/ratings",
    tags=["ratings"]
)


# Pydantic models
class RatingBase(BaseModel):
    """Create the Pydantic model of a rating."""
    rating: int = Field(..., ge=1, le=5)
    customer_id: int
    product_id: int


class Rating(RatingBase):
    """Create the model of the rating based on the RatingBase."""
    id: int

    class Config:
        """Provide configurations to Pydantic."""
        orm_mode = True


# Create a new rating
@router.post("/", response_model=Rating)
async def create_rating(rating: RatingBase, db: Session = Depends(get_db)):
    """POST /ratings endpoint to create a rating."""
    db_rating = RatingModel(**rating.model_dump())
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    return db_rating


# Retrieve a list of all the ratings on a single product
@router.get("/products/{product_id}", response_model=List[Rating])
async def get_product_ratings(product_id: int, db: Session = Depends(get_db)):
    """GET /ratings/products/{product_id} endpoint to get ratings of a product."""
    return db.query(RatingModel).filter(RatingModel.product_id == product_id).all()
