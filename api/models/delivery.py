"""
Delivery model for the Superman Store.

This model represents delivery options and tracks shipping status for purchases.
"""
from datetime import datetime, timezone, timedelta
from enum import Enum, auto
from sqlalchemy import Column, Integer, String, DateTime, CheckConstraint, Enum as SQLEnum
from sqlalchemy.orm import relationship
from api.dependencies import Base


class DeliveryType(str, Enum):
    """Enumeration of available delivery types."""
    STANDARD = "Standard"
    EXPRESS = "Express"
    SAME_DAY = "Same Day"
    INTERNATIONAL = "International"


class DeliveryStatus(str, Enum):
    """Enumeration of delivery status states."""
    PROCESSING = "Processing"
    SHIPPED = "Shipped"
    IN_TRANSIT = "In Transit"
    OUT_FOR_DELIVERY = "Out for Delivery"
    DELIVERED = "Delivered"
    FAILED = "Failed"
    RETURNED = "Returned"


class Delivery(Base):
    """
    Model for tracking deliveries in the Superman Store.
    
    Attributes:
        id (int): Unique identifier for the delivery
        type (DeliveryType): Type of delivery service
        status (DeliveryStatus): Current delivery status
        min_days (int): Minimum expected delivery days
        max_days (int): Maximum expected delivery days
        tracking_number (str): Shipping carrier tracking number
        carrier (str): Shipping carrier name
        shipping_date (datetime): When the item was shipped
        delivery_date (datetime): When the item was delivered
        estimated_delivery (datetime): Expected delivery date
        notes (str): Additional delivery information
        created_at (datetime): When the record was created
        updated_at (datetime): When the record was last modified
    
    Note:
        - Delivery times are estimates based on type
        - All timestamps are in UTC
        - Status transitions are tracked with timestamps
        - Tracking number format depends on carrier
    """
    __tablename__ = 'deliveries'

    # Basic information
    id = Column(Integer, primary_key=True, index=True)
    
    # Delivery details
    type = Column(SQLEnum(DeliveryType), nullable=False)
    status = Column(
        SQLEnum(DeliveryStatus),
        nullable=False,
        default=DeliveryStatus.PROCESSING
    )
    min_days = Column(Integer, nullable=False)
    max_days = Column(Integer, nullable=False)
    tracking_number = Column(String(100))
    carrier = Column(String(100))
    notes = Column(String(500))
    
    # Timestamps
    shipping_date = Column(DateTime(timezone=True))
    delivery_date = Column(DateTime(timezone=True))
    estimated_delivery = Column(DateTime(timezone=True))
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    purchases = relationship(
        "Purchase",
        back_populates="delivery",
        lazy='joined'  # Eager loading for better performance
    )

    # Constraints
    __table_args__ = (
        # Ensure min_days is positive and less than max_days
        CheckConstraint('min_days >= 0', name='check_min_days_positive'),
        CheckConstraint('max_days > min_days', name='check_max_days_greater'),
        # Ensure shipping_date is before delivery_date
        CheckConstraint(
            '(shipping_date IS NULL) OR (delivery_date IS NULL) OR (shipping_date <= delivery_date)',
            name='check_shipping_before_delivery'
        ),
    )

    @property
    def is_delivered(self):
        """Check if the delivery is complete."""
        return self.status == DeliveryStatus.DELIVERED and self.delivery_date is not None

    @property
    def is_in_transit(self):
        """Check if the delivery is currently in transit."""
        return (
            self.status in {DeliveryStatus.SHIPPED, DeliveryStatus.IN_TRANSIT, DeliveryStatus.OUT_FOR_DELIVERY}
            and self.shipping_date is not None
            and self.delivery_date is None
        )

    @property
    def is_delayed(self):
        """Check if the delivery is delayed beyond estimated date."""
        if not self.estimated_delivery or self.is_delivered:
            return False
        return datetime.now(timezone.utc) > self.estimated_delivery

    def calculate_estimated_delivery(self):
        """Calculate the estimated delivery date based on type and shipping date."""
        if not self.shipping_date:
            return None
        
        # Use average of min and max days as estimate
        avg_days = (self.min_days + self.max_days) / 2
        return self.shipping_date + timedelta(days=avg_days)

    def update_status(self, new_status: DeliveryStatus, notes: str = None):
        """
        Update delivery status and related timestamps.
        
        Args:
            new_status: New delivery status
            notes: Optional notes about the status change
        """
        self.status = new_status
        
        if new_status == DeliveryStatus.SHIPPED and not self.shipping_date:
            self.shipping_date = datetime.now(timezone.utc)
            self.estimated_delivery = self.calculate_estimated_delivery()
        
        elif new_status == DeliveryStatus.DELIVERED and not self.delivery_date:
            self.delivery_date = datetime.now(timezone.utc)
        
        if notes:
            self.notes = (self.notes or "") + f"\n[{datetime.now(timezone.utc)}] {notes}"

    def __repr__(self):
        """String representation of the Delivery."""
        status_info = f"status={self.status.value}"
        if self.tracking_number:
            status_info += f", tracking={self.tracking_number}"
        if self.is_delivered:
            status_info += f", delivered={self.delivery_date}"
        elif self.is_in_transit:
            status_info += f", est_delivery={self.estimated_delivery}"
        
        return f"<Delivery(id={self.id}, type={self.type.value}, {status_info})>"
