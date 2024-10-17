"""
Comment model.
"""
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from api.dependencies import Base

class Comment(Base):
    """Model for a comment."""
    # Name of the table in the database
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, index=True)
    comment = Column(String, nullable=False)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    product_id = Column(Integer, ForeignKey('products.id'))

    # Relationships
    customer = relationship("Customer", back_populates="comments")
    product = relationship("Product", back_populates="comments")
