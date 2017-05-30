import os

class DatabaseConfig:
   """Base Database Configuration."""
   DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:@localhost/')
   DATABASE_NAME = os.getenv('DATABASE_NAME','dm-buddy')

class AppConfig:
   SECRET_KEY = os.getenv('SECRET_KEY','my_precious')


