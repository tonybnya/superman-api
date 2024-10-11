"""
Create tables for the SQLite database.
"""
from database import Base
from sqlalchemy import Column, Integer, Boolean, String, Float


class Product(Base):
    """
    Model for a product.
    """
    # Name of the table in the database
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(Float)
    image_url = Column(String)
    category = Column(String)
    description = Column(String)
    quantity = Column(Integer)
    in_stock = Column(Boolean)
