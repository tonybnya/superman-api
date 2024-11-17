"""
Rating model for the Superman Store.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, DateTime, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import relationship
from api.dependencies import Base


class Rating(Base):
    """
    Model for product ratings in the Superman Store.
    
    Attributes:
        id (int): Unique identifier for the rating
        rating (int): Rating value (1-5 stars)
        customer_id (int): ID of the customer who made the rating
        product_id (int): ID of the product being rated
        created_at (datetime): When the rating was created
        updated_at (datetime): When the rating was last modified
    
    Note:
        - Each customer can only rate a product once
        - Rating value must be between 1 and 5
        - Rating can be updated by the customer
    """
    __tablename__ = 'ratings'

    # Basic information
    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Integer, nullable=False)
    
    # Foreign keys
    customer_id = Column(
        Integer, 
        ForeignKey('customers.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    product_id = Column(
        Integer, 
        ForeignKey('products.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    customer = relationship(
        "Customer",
        back_populates="ratings",
        lazy='joined'  # Eager loading for better performance
    )
    product = relationship(
        "Product",
        back_populates="ratings",
        lazy='joined'  # Eager loading for better performance
    )

    # Constraints
    __table_args__ = (
        # Ensure rating is between 1 and 5
        CheckConstraint(
            'rating >= 1 AND rating <= 5',
            name='check_rating_range'
        ),
        # Ensure each customer can only rate a product once
        UniqueConstraint('customer_id', 'product_id', name='unique_customer_product_rating'),
    )

    @property
    def is_edited(self):
        """Check if the rating has been modified."""
        return self.updated_at > self.created_at

    def __repr__(self):
        """String representation of the Rating."""
        return f"<Rating(product_id={self.product_id}, customer={self.customer.full_name}, stars={self.rating})>"
