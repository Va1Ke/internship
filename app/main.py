import psycopg2
import databases
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import asyncio
import aioredis
from app.database import db
from app.config import settings
from app.schemas import *
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from app.crud import Cruds as crud
from app.routes import router
from fastapi.security import HTTPBearer
from app.utils import VerifyToken

token_auth_scheme = HTTPBearer()



app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    print(settings.DATABASE_URL)
    await db.connect()
    #app.state.redis = await aioredis.from_url(REDIS_URL)

@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()
    #await app.state.redis.close()

@app.get("/")
async def root():
    return {"status": "Working"}


@app.post("/users/")
async def create_user(user: SignUpUser):
    #print(f"({user.email})")
    db_user = await crud.get_user_by_email(email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await crud.create_user(user=user)

@app.put("/update-user/")
async def update_user(id: int, email: str, name: str, password: str):
    #result = VerifyToken(token.credentials).verify()
    db_user = await crud.get_user_by_id(user_id=id)
    if not db_user:
        raise HTTPException(status_code=400, detail="No such user")
    user_id = await crud.update_user(id_=id,email_=email,name_=name,password_=password)
    return user_id


@app.get("/users/", response_model=list[User])
async def read_users(skip: int = 0, limit: int = 100):
    return await crud.get_users(skip=skip, limit=limit)

@app.delete("/users/")
async def delete_user(user: UserDelete):
    db_user = crud.get_user_by_email(email=user.email)
    if db_user:
        crud.delete_user(user=user)
        return HTTPException(status_code=200, detail="User deleted successfully")
    else:
        return HTTPException(status_code=400, detail="No such user")

@app.get("/users/{user_id}")
async def read_user(user_id: int):
    db_user = await crud.get_user_by_id(id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=80, reload=True)