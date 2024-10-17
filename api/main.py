"""
Main module to run the app.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import comments, customers, deliveries, products, purchases, ratings


# Create the FastAPI application
app = FastAPI(title='Superman Store API')

# Define allowed origins for CORS
origins: list[str] = [
    'http://localhost:5173',
    'https://superman-store.onrender.com'
]

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

# Include product-related routes
app.include_router(comments.router)
app.include_router(customers.router)
app.include_router(deliveries.router)
app.include_router(products.router)
app.include_router(purchases.router)
app.include_router(ratings.router)

# Root endpoint
@app.get("/", response_model=dict[str, str])
async def index():
    """
    GET / endpoint
    """
    return {"message": "Welcome to Superman Store API"}
