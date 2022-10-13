import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname('../'))
load_dotenv(dotenv_path=f"{basedir}/.env")


POSTGRES_URL = os.getenv("POSTGRES_URL")
REDIS_URL = os.getenv("REDIS_URL")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
