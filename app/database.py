import sqlalchemy
import aioredis
from starlette.requests import Request
import databases
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from app.config import settings
#from app.main import app

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
db = databases.Database(settings.DATABASE_URL)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

TEST_SQLALCHEMY_DATABASE_URL = settings.TEST_DATABASE_URL
test_db = databases.Database(settings.TEST_DATABASE_URL)
test_engine = create_engine(TEST_SQLALCHEMY_DATABASE_URL)

Base = declarative_base()

#app.dependency_overrides[db] = test_db

