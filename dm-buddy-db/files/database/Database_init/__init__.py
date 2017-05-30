import os


from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

from Database_init.config import DatabaseConfig as dbconfig

import bcrypt

Base = declarative_base()

from Database_init.models import *

db = create_engine(dbconfig.DATABASE_URI + dbconfig.DATABASE_NAME)
