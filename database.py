from sqlachemy import create_engine
from sqlachemy.orm import sessionmaker
from sqlachemy.ext.declarative import declarative_base


# String path to the SQLite db
URL_DATABASE: str = 'sqlite:///./superman.db'
