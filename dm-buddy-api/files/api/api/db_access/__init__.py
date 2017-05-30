# /api/db_access/__init__.py

import os

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

from api import Databaseconfig as dbconfig

import bcrypt

Base = declarative_base()

from db_access.models import *

db = create_engine(dbconfig.DATABASE_URI + dbconfig.DATABASE_NAME)
