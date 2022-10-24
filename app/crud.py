from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
from app import schemas
from app.models import users
from app.database import db

class Cruds:
    async def get_user_by_id(self,id: int):
        user = await db.fetch_one(users.select().where(users.c.id == id))
        return user

    async def get_users(self,skip: int = 0, limit: int = 100):
        query = users.select().offset(skip).limit(limit)
        users_to_dict = await db.fetch_all(query=query)
        return users_to_dict

    async def get_user_by_email(self,email: str):
        user = await db.fetch_one(users.select().where(users.c.email == email))
        return user


    async def create_user(self,user: schemas.SignUpUser):
        db_user = users.insert().values(email=user.email, password=user.password,name=user.name, creation_date=user.creation_date)
        user_id= await db.execute(db_user)
        user_by_email = await db.fetch_one(users.select().where(users.c.email == user.email))
        return schemas.User(**user.dict(),id=user_by_email.id)

    async def delete_user(self,user: schemas.UserDelete):
        query = users.delete().where(users.c.email == user.email)
        await db.execute(query=query)
        return HTTPException(status_code=200, detail="Success")

    async def update_user(self,user : schemas.UserUpdate):
        query = (users.update().where(users.c.id == user.id).values(
        email=user.email,
        name=user.name,
        password=user.password
        ).returning(users.c.id))
        await db.execute(query=query)
        changed_user = await db.fetch_one(users.select().where(users.c.id == user.id))
        #return changed_user
        return schemas.User(id=changed_user.id,email=changed_user.email,name=changed_user.name,password=changed_user.password,creation_date=changed_user.creation_date)
