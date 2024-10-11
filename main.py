from fastapi import FastAPI, HTTPException, Depends
from typing import Annotated, List
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import SessonLocal, engine
import model_products
from fastapi.middleware.cors import CORSMiddleware


# Create the FastAPI application
app = FastAPI()

# Define the app that can call our FastAPI application
origins: list[str] = [
    'http://localhost:5173',
    'http://localhost:8000',
    'https://superman-store.onrender.com'
]

# Allow the origins defined to pass the middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins
)


class ProductBase(BaseModel):
    """
    Create the Pydantic model of a product.
    """
    name: str
    price: float
    image_url: str
    category: str
    description: str
    quantity: int
    in_stock: bool


class ProductModel(ProductBase):
    """
    Create the model of the product based on the ProductBase.
    """
    id: int

    class Config:
        """
        Provide configurations to Pydantic.
        """
        orm_mode = True


def get_db():
    """
    Function to access the database.
    The database only opens when the request comes in
    and closes when the request is finished.
    """
    db = SessonLocal()
    try:
        yield db
    finally:
        db.close()


# Create the dependency injection
db_dependency = Annotated[Session, Depends(get_db)]

# Create the database (if not exist yet) and the tables
# when the FastAPI is launched
model_products.Base.metadata.create_all(bind=engine)


@app.post("/products/", response_model=ProductModel)
async def create_product(product: ProductBase, db: db_dependency):
    """
    POST /products/ endpoint
    """
    # Map all the data of the product
    # and store in the database
    db_product = model_products.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@app.get("/products", response_model=List[ProductModel])
async def get_products(db: db_dependency, skip: int = 0, limit: int = 100):
    """
    GET /products endpoint
    """
    products = db.query(model_products.Product).offset(skip).limit(limit).all()
    return products
