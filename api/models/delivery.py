"""
Delivery model.
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from api.dependencies import Base

class Delivery(Base):
    """Model for a delivery."""
    # Name of the table in the database
    __tablename__ = 'deliveries'

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, nullable=False)
    min_days = Column(Integer, nullable=False)
    max_days = Column(Integer, nullable=False)

    # Relationships
    purchases = relationship("Purchase", back_populates="delivery")
