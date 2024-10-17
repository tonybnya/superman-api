"""
Rating model.
"""
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from api.dependencies import Base

class Rating(Base):
    """Model for a rating."""
    __tablename__ = 'ratings'

    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Integer, nullable=False)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    product_id = Column(Integer, ForeignKey('products.id'))

    # Relationships
    customer = relationship("Customer", back_populates="ratings")
    product = relationship("Product", back_populates="ratings")
