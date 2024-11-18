"""
Purchase model for the Superman Store.

This model represents a purchase transaction in the store, tracking what products
were bought, by whom, in what quantity, and their delivery status.
"""
from datetime import datetime, timezone
from decimal import Decimal
from sqlalchemy import Column, Integer, ForeignKey, DateTime, CheckConstraint, Numeric
from sqlalchemy.orm import relationship, column_property
from sqlalchemy.sql import select
from api.dependencies import Base


class Purchase(Base):
    """
    Model for tracking purchase transactions in the Superman Store.
    
    Attributes:
        id (int): Unique identifier for the purchase
        customer_id (int): ID of the customer who made the purchase
        product_id (int): ID of the product being purchased
        delivery_id (int): ID of the delivery record for this purchase
        quantity (int): Number of items purchased
        unit_price (Decimal): Price of the product at time of purchase
        total_amount (Decimal): Total amount for the purchase (quantity * unit_price)
        purchase_date (datetime): When the purchase was made (UTC)
        created_at (datetime): When the record was created
        updated_at (datetime): When the record was last modified
    
    Note:
        - Quantity must be positive
        - Unit price is stored to maintain historical pricing
        - All timestamps are in UTC
        - Deleting a customer or product will not delete the purchase record
        - Deleting a delivery will nullify the delivery_id
    """
    __tablename__ = 'purchases'

    # Basic information
    id = Column(Integer, primary_key=True, index=True)
    
    # Purchase details
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)  # Store historical price
    
    # Foreign keys
    customer_id = Column(
        Integer, 
        ForeignKey('customers.id', ondelete='RESTRICT'),  # Prevent deletion of referenced customer
        nullable=False,
        index=True
    )
    product_id = Column(
        Integer, 
        ForeignKey('products.id', ondelete='RESTRICT'),  # Prevent deletion of referenced product
        nullable=False,
        index=True
    )
    delivery_id = Column(
        Integer, 
        ForeignKey('deliveries.id', ondelete='SET NULL'),  # Allow deletion of delivery
        index=True
    )
    
    # Timestamps
    purchase_date = Column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    created_at = Column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Relationships
    customer = relationship(
        "Customer",
        back_populates="purchases",
        lazy='joined'  # Eager loading for better performance
    )
    product = relationship(
        "Product",
        back_populates="purchases",
        lazy='joined'  # Eager loading for better performance
    )
    delivery = relationship(
        "Delivery",
        back_populates="purchases",
        lazy='joined'  # Eager loading for better performance
    )

    # Constraints
    __table_args__ = (
        # Ensure quantity is positive
        CheckConstraint('quantity > 0', name='check_positive_quantity'),
        # Ensure unit price is positive
        CheckConstraint('unit_price > 0', name='check_positive_unit_price'),
    )

    # Computed properties
    total_amount = column_property(
        quantity * unit_price
    )

    @property
    def is_delivered(self):
        """Check if the purchase has been delivered."""
        return self.delivery is not None and self.delivery.delivery_date is not None

    @property
    def delivery_status(self):
        """Get the current delivery status."""
        if self.delivery is None:
            return "Not shipped"
        if self.delivery.delivery_date is not None:
            return "Delivered"
        if self.delivery.shipping_date is not None:
            return "In transit"
        return "Processing"

    def __repr__(self):
        """String representation of the Purchase."""
        return (
            f"<Purchase(id={self.id}, "
            f"customer={self.customer.full_name}, "
            f"product={self.product.name}, "
            f"quantity={self.quantity}, "
            f"total=${self.total_amount:.2f}, "
            f"status={self.delivery_status})>"
        )
