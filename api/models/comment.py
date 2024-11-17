"""
Comment model for the Superman Store.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, CheckConstraint
from sqlalchemy.orm import relationship
from api.dependencies import Base


class Comment(Base):
    """
    Model for product comments in the Superman Store.
    
    Attributes:
        id (int): Unique identifier for the comment
        content (str): The comment text (max 1000 chars)
        customer_id (int): ID of the customer who made the comment
        product_id (int): ID of the product being commented on
        created_at (datetime): When the comment was created
        updated_at (datetime): When the comment was last edited
        is_edited (bool): Whether the comment has been edited
    """
    __tablename__ = 'comments'

    # Basic information
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(1000), nullable=False)
    
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
        back_populates="comments",
        lazy='joined'  # Eager loading for better performance
    )
    product = relationship(
        "Product",
        back_populates="comments",
        lazy='joined'  # Eager loading for better performance
    )

    # Constraints
    __table_args__ = (
        CheckConstraint(
            'length(content) >= 3',
            name='check_comment_length'
        ),
    )

    @property
    def is_edited(self):
        """Check if the comment has been edited."""
        return self.updated_at > self.created_at

    def __repr__(self):
        """String representation of the Comment."""
        return f"<Comment(id={self.id}, customer={self.customer.full_name}, product_id={self.product_id})>"
