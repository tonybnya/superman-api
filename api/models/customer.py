"""
Customer model.
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from api.dependencies import Base

class Customer(Base):
    """Model for a customer."""
    # Name of the table in the database
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=False)
    delivery_address = Column(String, nullable=False)
    billing_address = Column(String, nullable=False)

    # Relationships
    comments = relationship("Comment", back_populates="customer")
    purchases = relationship("Purchase", back_populates="customer")
    ratings = relationship("Rating", back_populates="customer")
