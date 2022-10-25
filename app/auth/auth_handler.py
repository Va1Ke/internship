import time, os
from typing import Dict
from pathlib import Path
import jwt
from dotenv import load_dotenv

env_path = Path('..') / '.config'
load_dotenv(dotenv_path=env_path)

JWT_SECRET = os.getenv("SECRET")
JWT_ALGORITHM = os.getenv("ALGORITHMS_MY")


def token_response(token: str):
    return {
        "access_token": token
    }

# function used for signing the JWT string
def signJWT(user_id: str) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "expires": time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}