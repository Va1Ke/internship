import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path('..') / '.env'
load_dotenv(dotenv_path=env_path)

class Settings:
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB")
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    #DATABASE_URL = "postgresql://admin:admin@localhost:5432/postgresdb"
    POSTGRES_TEST_DB: str = os.getenv("POSTGRES_TEST_DB")
    TEST_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_TEST_DB}"
    REDIS_URL = f"redis://cache:6379/"
    DOMAIN: str = os.getenv("DOMAIN")
    API_AUDIENCE: str = os.getenv("API_AUDIENCE")
    SECRET: str = os.getenv("SECRET")
    ALGORITHMS: str = os.getenv("ALGORITHMS")
    MY_ALGORITHMS: str = os.getenv("MY_ALGORITHMS")
    ISSUER: str = os.getenv("ISSUER")
    CLIENT_ID: str = os.getenv("CLIENT_ID")
    CLIENT_SECRET: str = os.getenv("CLIENT_SECRET")
    CONNECTION: str = os.getenv("CONNECTION")
    ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
    APPHOST: str =os.getenv(("APPHOST"))
    APPPORT: str =os.getenv(("APPPORT"))

settings = Settings()