from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
from app import schemas
from app.models import users
from app.database import db

class Cruds:
    async def get_user_by_id(id: int):
        return await db.fetch_one(users.select().where(users.c.id == id))

    async def get_users(skip: int = 0, limit: int = 100):
        query = users.select().offset(skip).limit(limit)
        return await db.fetch_all(query=query)

    async def get_user_by_email(email: str):
        return await db.fetch_one(users.select().where(users.c.email == email))

    async def create_user(user: schemas.SignUpUser):
        #fake_hashed_password = user.password + "notreallyhashed"
        #print(f"({user.email})")
        creation_time = datetime.now()
        db_user = users.insert().values(email=user.email, password=user.password,name=user.name, creation_date=creation_time)
        user_id= await db.execute(db_user)
        print(user_id)
        print(type(user_id))
        return schemas.User(**user.dict(),id=user_id,creation_date=creation_time)

    async def delete_user( user: schemas.UserDelete):
        query = users.delete().where(email == user.c.email)
        return await db.execute(query=query)

    async def update_user(id_: int, email_: str, name_: str, password_: str):
        query = (users.update().where(id == id_).values(
        email=email_,
        name=name_,
        password=password_
        ).returning(users.c.id))
        return await db.execute(query=query)

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


