"""
Product model.
"""
from sqlalchemy import Column, Integer, Boolean, String, Float
from api.dependencies import Base


class Product(Base):
    """
    Model for a product.
    """
    # Name of the table in the database
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    image_url = Column(String, nullable=False)
    category = Column(String, nullable=False)
    description = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    in_stock = Column(Boolean, default=True)
