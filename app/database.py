import sqlalchemy
import databases
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
#SQLALCHEMY_DATABASE_URL = 'postgresql://admin:admin@db/postgresdb'
db = databases.Database(settings.DATABASE_URL)
engine = create_engine(SQLALCHEMY_DATABASE_URL)
Base = declarative_base()


