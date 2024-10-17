"""
Purchase model.
"""
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from api.dependencies import Base

class Purchase(Base):
    """Model for a purchase."""
    # Name of the table in the database
    __tablename__ = 'purchases'

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    delivery_id = Column(Integer, ForeignKey('deliveries.id'))
    quantity = Column(Integer, nullable=False)
    purchase_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    customer = relationship("Customer", back_populates="purchases")
    product = relationship("Product", back_populates="purchases")
    delivery = relationship("Delivery", back_populates="purchases")
