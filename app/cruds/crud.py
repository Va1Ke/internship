from fastapi import HTTPException
from datetime import datetime
import databases
from app.schemas import schemas
from app.models.models import users
import secrets


class Cruds:
    def __init__(self, db: databases.Database):
        self.db = db

    async def get_user_by_id(self,id: int) -> schemas.User:
        user = await self.db.fetch_one(users.select().where(users.c.id == id))
        if user == None:
            return None
        return schemas.User(id=user.id, email=user.email,password=user.password, name=user.name, creation_date=user.creation_date)

    async def get_users(self,skip: int = 0, limit: int = 100) -> list:
        query = users.select().offset(skip).limit(limit)
        users_to_dict = await self.db.fetch_all(query=query)
        return [schemas.User(**user) for user in users_to_dict]


    async def get_user_by_email(self,email: str) -> schemas.User:
        user = await self.db.fetch_one(users.select().where(users.c.email == email))
        if user == None:
            return None
        return schemas.User(id=user.id,email=user.email,password=user.password,name=user.name,creation_date=user.creation_date)


    async def create_user(self,user: schemas.SignUpUser) -> schemas.User:
        db_user = users.insert().values(email=user.email, password=user.password,name=user.name, creation_date=user.creation_date)
        user_id= await self.db.execute(db_user)
        user_by_email = await self.db.fetch_one(users.select().where(users.c.email == user.email))
        return schemas.User(**user.dict(),id=user_by_email.id)

    async def create_user_by_email(self,email: str) -> schemas.User:
        db_user = users.insert().values(email=email, password=str(secrets.token_hex(8)),name="default", creation_date=datetime.now())
        user_id= await self.db.execute(db_user)
        user_by_email = await self.db.fetch_one(users.select().where(users.c.email == email))
        return schemas.User(**user_by_email)

    async def delete_user(self,user: schemas.UserBase) -> HTTPException:
        query = users.delete().where(users.c.email == user.email)
        await self.db.execute(query=query)
        return HTTPException(status_code=200, detail="Success")

    async def update_user(self,user : schemas.UserUpdate) -> schemas.User:
        query = (users.update().where(users.c.email == user.email).values(
        name=user.name,
        password=user.password
        ).returning(users.c.id))
        await self.db.execute(query=query)
        changed_user = await self.db.fetch_one(users.select().where(users.c.email == user.email))
        #return changed_user
        return schemas.User(id=changed_user.id,email=changed_user.email,password=changed_user.password,name=changed_user.name,creation_date=changed_user.creation_date)

#crud = Cruds()