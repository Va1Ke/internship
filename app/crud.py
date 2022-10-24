from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
from app import schemas
from app.models import users
from app.database import db

class Cruds:
    async def get_user_by_id(self,id: int):
        return await db.fetch_one(users.select().where(users.c.id == id))

    async def get_users(self,skip: int = 0, limit: int = 100):
        query = users.select().offset(skip).limit(limit)
        return await db.fetch_all(query=query)

    async def get_user_by_email(self,email: str):
        return await db.fetch_one(users.select().where(users.c.email == email))

    async def create_user(self,user: schemas.SignUpUser):
        db_user = users.insert().values(email=user.email, password=user.password,name=user.name, creation_date=user.creation_date)
        user_id= await db.execute(db_user)
        user_by_email = await db.fetch_one(users.select().where(users.c.email == user.email))
        return schemas.User(**user.dict(),id=user_by_email.id)

    async def delete_user(self,user: schemas.UserDelete):
        query = users.delete().where(users.c.email == user.email)
        await db.execute(query=query)

        return 0

    async def update_user(self,user : schemas.UserUpdate):
        query = (users.update().where(users.c.id == user.id).values(
        email=user.email,
        name=user.name,
        password=user.password
        ))
        return await db.execute(query=query)
