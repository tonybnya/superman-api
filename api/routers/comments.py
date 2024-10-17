"""
Router for comment-related endpoints.
"""
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from api.models.comment import Comment as CommentModel
from api.dependencies import get_db


# Create a router for comment-related routes
router = APIRouter(
    prefix="/comments",
    tags=["comments"]
)


# Pydantic models
class CommentBase(BaseModel):
    """Create the Pydantic model of a comment."""
    comment: str
    customer_id: int
    product_id: int


class Comment(CommentBase):
    """Create the model of the comment based on the CommentBase."""
    id: int

    class Config:
        """Provide configurations to Pydantic."""
        orm_mode = True


# Create a new comment
@router.post("/", response_model=Comment)
async def create_comment(review: CommentBase, db: Session = Depends(get_db)):
    """POST /comments endpoint to create a comment."""
    db_comment = CommentModel(**review.model_dump())
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


# Retrieve a list of all comments for a single product
@router.get("/products/{product_id}", response_model=List[Comment])
async def get_product_reviews(product_id: int, db: Session = Depends(get_db)):
    """GET /comments/products/{product_id} endpoint to get comments of a product."""
    return db.query(CommentModel).filter(CommentModel.product_id == product_id).all()
