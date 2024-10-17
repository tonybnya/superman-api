"""
Router for product-related endpoints.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from api.models.product import Product as ProductModel
from api.dependencies import get_db


# Create a router for product-related routes
router = APIRouter(
    prefix="/products",
    tags=["products"]
)


# Pydantic models
class ProductBase(BaseModel):
    """Create the Pydantic model of a product."""
    name: str
    price: float
    image_url: str
    category: str
    description: str
    quantity: int
    in_stock: bool


class Product(ProductBase):
    """Create the model of the product based on the ProductBase."""
    id: int

    class Config:
        """Provide configurations to Pydantic."""
        orm_mode = True


# Create a new product
@router.post("/", response_model=Product)
async def create_product(product: ProductBase, db: Session = Depends(get_db)):
    """POST /products endpoint to create a product."""
    db_product = ProductModel(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


# Retrieve a list of products
@router.get("/", response_model=List[Product])
async def get_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """GET /products endpoint to get all the products."""
    products = db.query(ProductModel).offset(skip).limit(limit).all()
    return products


# Retrieve a single product
@router.get("/{product_id}", response_model=Product)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    """GET /products/{product_id} endpoint to retrieve a product by its ID."""
    product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


# Update a single product
@router.put("/{product_id}", response_model=Product)
async def update_product(
    product_id: int,
    updated_product: ProductBase,
    db: Session = Depends(get_db)
):
    """PUT /products/{product_id} endpoint to update a product by its ID."""
    product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    for key, value in updated_product.model_dump().items():
        setattr(product, key, value)
    db.commit()
    db.refresh(product)
    return product


# Delete a single product
@router.delete("/{product_id}", response_model=dict[str, str])
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    """DELETE /products/{product_id} endpoint to delete a product by its ID."""
    product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"message": "Product successfully deleted"}
