"""
Connect the FastAPI application to the SQLite database.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# String for the SQLite database
URL_DATABASE: str = 'sqlite:///./superman.db'

engine = create_engine(URL_DATABASE, connect_args={"check_same_thread": False})
SessonLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
