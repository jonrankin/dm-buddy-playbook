import os


from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

from Database_init.config import DatabaseConfig as dbconfig

db = create_engine(dbconfig.DATABASE_URI)
Base = declarative_base()



class User(Base):
    """ User Model for storing user related details """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    registered_on = Column(DateTime, nullable=False)
    admin = Column(Boolean, nullable=False, default=False)






def create_table():
  Base.metadata.create_all(db)
  
