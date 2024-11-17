"""
Customer model for the Superman Store.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, CheckConstraint
from sqlalchemy.orm import relationship
from api.dependencies import Base


class Customer(Base):
    """
    Model for a customer in the Superman Store.
    
    Attributes:
        id (int): Unique identifier for the customer
        firstname (str): Customer's first name (max 50 chars)
        lastname (str): Customer's last name (max 50 chars)
        email (str): Customer's email address (unique, max 255 chars)
        phone (str): Customer's phone number (max 20 chars)
        delivery_address (str): Customer's delivery address (max 500 chars)
        billing_address (str): Customer's billing address (max 500 chars)
        created_at (datetime): Timestamp when customer account was created
        updated_at (datetime): Timestamp when customer details were last updated
    """
    __tablename__ = 'customers'

    # Basic information
    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    phone = Column(String(20), nullable=False)
    
    # Addresses
    delivery_address = Column(String(500), nullable=False)
    billing_address = Column(String(500), nullable=False)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    comments = relationship("Comment", back_populates="customer", cascade="all, delete-orphan")
    purchases = relationship("Purchase", back_populates="customer", cascade="all, delete-orphan")
    ratings = relationship("Rating", back_populates="customer", cascade="all, delete-orphan")

    # Constraints for data validation
    __table_args__ = (
        CheckConstraint(
            "length(firstname) >= 2",
            name="check_firstname_length"
        ),
        CheckConstraint(
            "length(lastname) >= 2",
            name="check_lastname_length"
        ),
        CheckConstraint(
            "email LIKE '%@%.%'",
            name="check_email_format"
        ),
        CheckConstraint(
            "length(phone) >= 10",
            name="check_phone_length"
        ),
    )

    def __repr__(self):
        """String representation of the Customer."""
        return f"<Customer(id={self.id}, name={self.firstname} {self.lastname}, email={self.email})>"

    @property
    def full_name(self):
        """Get customer's full name."""
        return f"{self.firstname} {self.lastname}"
