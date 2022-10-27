from datetime import datetime, timedelta
import jwt
from fastapi import Response, Depends, HTTPException
from fastapi.security import HTTPBearer
from starlette import status
from app.cruds.crud import crud
from app.config import settings

token_auth_scheme = HTTPBearer()

async def create_access_token(email: str, expires_delta: timedelta = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "email": email}
    config = set_up()
    encoded_jwt = jwt.encode(to_encode, config["SECRET"], algorithm=config["MY_ALGORITHMS"])
    return encoded_jwt

async def get_current_user(response: Response, token: str = Depends(token_auth_scheme)):
    pyload_from_auth = VerifyToken(token.credentials).verify()
    if pyload_from_auth.get("status"):
        pyload_from_me = VerifyToken(token.credentials).verify_my()
        if pyload_from_me.get("status"):
            response.status_code = status.HTTP_400_BAD_REQUEST
            return response

        user = await crud.get_user_by_email(pyload_from_me.get("email"))
        if not user:
            raise HTTPException(status_code=404,detail="User not found")
        return user

    user = await crud.get_user_by_email(email=pyload_from_auth.get("email"))
    if not user:
        user = await crud.create_user_by_email(email=pyload_from_auth.get("email"))
    return user

async def get_email_from_token(response: Response, token: str = Depends(token_auth_scheme)):
    pyload_from_auth = VerifyToken(token.credentials).verify()
    if pyload_from_auth.get("status"):
        pyload_from_me = VerifyToken(token.credentials).verify_my()
        if pyload_from_me.get("status"):
            response.status_code = status.HTTP_400_BAD_REQUEST
            return response
        return pyload_from_me.get("email")
    return pyload_from_auth.get("email")



def set_up():
    config = {
        "CLIENT_ID": settings.CLIENT_ID,
        "CLIENT_SECRET": settings.CLIENT_SECRET,
        "DOMAIN": settings.DOMAIN,
        "API_AUDIENCE": settings.API_AUDIENCE,
        "ISSUER": settings.ISSUER,
        "ALGORITHMS": settings.ALGORITHMS,
        "MY_ALGORITHMS": settings.MY_ALGORITHMS,
        "SECRET": settings.SECRET,
        "CONNECTION": settings.CONNECTION
        }
    return config

class VerifyToken():
    """Does all the token verification using PyJWT"""

    def __init__(self, token):
        self.token = token
        self.config = set_up()

        # This gets the JWKS from a given URL and does processing so you can
        # use any of the keys available
        jwks_url = f'https://{self.config["DOMAIN"]}/.well-known/jwks.json'
        self.jwks_client = jwt.PyJWKClient(jwks_url)

    def verify(self):
        # This gets the 'kid' from the passed token
        try:
            self.signing_key = self.jwks_client.get_signing_key_from_jwt(
                self.token
            ).key
        except jwt.exceptions.PyJWKClientError as error:
            return {"status": "error", "msg": error.__str__()}
        except jwt.exceptions.DecodeError as error:
            return {"status": "error", "msg": error.__str__()}

        try:
            payload = jwt.decode(
                self.token,
                self.signing_key,
                algorithms=self.config["ALGORITHMS"],
                audience=self.config["API_AUDIENCE"],
                issuer=self.config["ISSUER"],
            )
        except Exception as e:
            return {"status": "error", "message": str(e)}
        return payload

    def verify_my(self):
        try:
            payload = jwt.decode(
                self.token,
                self.config["SECRET"],
                algorithms=[self.config["MY_ALGORITHMS"]],
            )
        except Exception as e:
            return {"status": "error", "message": str(e)}

        return payload