"""
Product model for the Superman Store.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, Boolean, String, Float, DateTime, CheckConstraint
from sqlalchemy.orm import relationship
from api.dependencies import Base


class Product(Base):
    """
    Model for a product in the Superman Store.
    
    Attributes:
        id (int): Unique identifier for the product
        name (str): Name of the product (max 100 chars)
        price (float): Price in USD (must be positive)
        image_url (str): URL to product image
        category (str): Product category (e.g., 'Comics', 'Clothing', 'Collectibles')
        description (str): Detailed product description
        quantity (int): Current stock quantity (non-negative)
        in_stock (bool): Whether the product is in stock
        created_at (datetime): Timestamp when product was created
        updated_at (datetime): Timestamp when product was last updated
    """
    __tablename__ = 'products'

    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Basic information
    name = Column(String(100), nullable=False, index=True)
    price = Column(Float, nullable=False)
    image_url = Column(String(500), nullable=False)
    category = Column(String(50), nullable=False, index=True)
    description = Column(String(1000), nullable=False)
    
    # Inventory management
    quantity = Column(Integer, nullable=False)
    in_stock = Column(Boolean, default=True)
    
    # Additional metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    purchases = relationship("Purchase", back_populates="product")
    comments = relationship("Comment", back_populates="product")
    ratings = relationship("Rating", back_populates="product")

    # Constraints
    __table_args__ = (
        CheckConstraint('price > 0', name='check_positive_price'),
        CheckConstraint('quantity >= 0', name='check_non_negative_quantity'),
    )

    def __repr__(self):
        """String representation of the Product."""
        return f"<Product(name={self.name}, price=${self.price:.2f})>"
