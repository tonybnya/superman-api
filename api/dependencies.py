"""
Connect the FastAPI application to the SQLite database.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from typing import Generator


# Database connection settings
DATABASE_URL: str = 'sqlite:///./superman.db'

# Create the database engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


# Dependency to access the database
def get_db() -> Generator[Session, None, None]:
    """
    Provides a generator that creates a new database session 
    for each request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
