

import psycopg2
import databases
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import asyncio
import aioredis
from app.database import db
from app.config import settings
from app.schemas import *
from fastapi import Depends, FastAPI, HTTPException, Response,status
from sqlalchemy.orm import Session
from app.crud import Cruds
from app.routes import router
from fastapi.security import HTTPBearer
from app.utils import VerifyToken

token_auth_scheme = HTTPBearer()
crud = Cruds()


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



@app.post("/users/",response_model=User)
async def create_user(user: SignUpUser):
    db_user = await crud.get_user_by_email(email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await crud.create_user(user=user)

@app.put("/update-user/",response_model=User)
async def update_user(user: UserUpdate):
    #result = VerifyToken(token.credentials).verify()
    db_user = await crud.get_user_by_id(id=user.id)
    if not db_user:
        raise HTTPException(status_code=400, detail="No such user")
    return await crud.update_user(user=user)


@app.get("/users/", response_model=list[User])
async def read_users(skip: int = 0, limit: int = 100):
    return await crud.get_users(skip=skip, limit=limit)

@app.delete("/users/")
async def delete_user(user: UserDelete):
    db_user = crud.get_user_by_email(email=user.email)
    if db_user:
        return await crud.delete_user(user=user)
    else:
        raise HTTPException(status_code=400, detail="No such user")

@app.get("/users/{user_id}")
async def read_user(response: Response, user_id: int,token: str = Depends(token_auth_scheme)):

    result = VerifyToken(token.credentials).verify()
    if result.get("status"):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return result

    db_user = await crud.get_user_by_id(id=user_id)
    if db_user is None:
        raise HTTPException(status_code=400, detail="No such user")
    return db_user


app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=80, reload=True)