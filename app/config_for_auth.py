import os
from dotenv import load_dotenv
from pathlib import Path


env_path = Path('..') / '.config'
load_dotenv(dotenv_path=env_path)

class Settings_for_auth:
    DOMAIN: str = os.getenv("DOMAIN")
    API_AUDIENCE: str = os.getenv("API_AUDIENCE")
    SECRET: str = os.getenv("SECRET")
    ALGORITHMS: str = os.getenv("ALGORITHMS")
    ENCODED_ALGORITHMS: str = os.getenv("ENCODED_ALGORITHMS")
    ISSUER: str = os.getenv("ISSUER")
    CLIENT_ID: str = os.getenv("CLIENT_ID")
    CLIENT_SECRET: str = os.getenv("CLIENT_SECRET")
    CONNECTION: str = os.getenv("CONNECTION")
    ACCESS_TOKEN_EXPIRE_MINUTES = 60*24


settings_for_auth = Settings_for_auth()