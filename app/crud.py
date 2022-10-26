from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
from app import schemas
from app.models import users
from app.database import db

class Cruds:
    async def get_user_by_id(self,id: int):
        user = await db.fetch_one(users.select().where(users.c.id == id))
        if user == None:
            return None
        return schemas.User(id=user.id, email=user.email,password=user.password, name=user.name, creation_date=user.creation_date)

    async def get_users(self,skip: int = 0, limit: int = 100):
        query = users.select().offset(skip).limit(limit)
        users_to_dict = await db.fetch_all(query=query)
        return [schemas.User(**user) for user in users_to_dict]


    async def get_user_by_email(self,email: str):
        user = await db.fetch_one(users.select().where(users.c.email == email))
        if user == None:
            return None
        return schemas.User(id=user.id,email=user.email,password=user.password,name=user.name,creation_date=user.creation_date)


    async def create_user(self,user: schemas.SignUpUser):
        db_user = users.insert().values(email=user.email, password=user.password,name=user.name, creation_date=user.creation_date)
        user_id= await db.execute(db_user)
        user_by_email = await db.fetch_one(users.select().where(users.c.email == user.email))
        return schemas.User(**user.dict(),id=user_by_email.id)

    async def create_user_by_email(self,email: str):
        db_user = users.insert().values(email=email, password="123",name="default", creation_date=datetime.now())
        user_id= await db.execute(db_user)
        user_by_email = await db.fetch_one(users.select().where(users.c.email == email))
        return schemas.User(**user_by_email)

    async def delete_user(self,user: schemas.UserBase):
        query = users.delete().where(users.c.email == user.email)
        await db.execute(query=query)
        return HTTPException(status_code=200, detail="Success")

    async def update_user(self,user : schemas.UserUpdate):
        query = (users.update().where(users.c.email == user.email).values(
        name=user.name,
        password=user.password
        ).returning(users.c.id))
        await db.execute(query=query)
        changed_user = await db.fetch_one(users.select().where(users.c.email == user.email))
        #return changed_user
        return schemas.User(id=changed_user.id,email=changed_user.email,password=changed_user.password,name=changed_user.name,creation_date=changed_user.creation_date)

crud = Cruds()