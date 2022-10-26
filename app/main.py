import http.client
from datetime import timedelta
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import asyncio
import aioredis
from app.database import db
from app.config import settings
from app.schemas import *
from fastapi import Depends, FastAPI, HTTPException, Response, status
from app.crud import crud
from app.routes import router
from app.utils import create_access_token, get_current_user, set_up


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
async def read_user(user_id: int):
    db_user = await crud.get_user_by_id(id=user_id)
    if db_user is None:
        raise HTTPException(status_code=400, detail="No such user")
    return db_user

@app.get("/users/email/{user_email}")
async def read_user_by_email(user_email: str):
    db_user = await crud.get_user_by_email(email=user_email)
    if db_user is None:
        raise HTTPException(status_code=400, detail="No such user")
    return db_user



@app.get("/user/login/me", tags=["auth"])
def get_me(user: User = Depends(get_current_user)):
    return user

@app.post("/user/login/", tags=["auth"])
async def sign_in_my(user: SignInUser):
    user_check = await crud.get_user_by_email(user.email)
    if user_check and user_check.password == user.password:
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        token = await create_access_token(user.email,expires_delta=access_token_expires)
        return token
    else:
        raise HTTPException(status_code=400,detail="No such user or incorrect email, password")

@app.post("/user/register/", tags=["auth"])
async def sign_up_my(user: SignUpUser):
    does_exist = await crud.get_user_by_email(email=user.email)
    if does_exist:
        raise HTTPException(status_code=400,detail="Email already registered")
    config = set_up()
    conn = http.client.HTTPSConnection(config['DOMAIN'])
    pyload="{" \
            f"\"client_id\":\"{config['CLIENT_ID']}\"," \
            f"\"client_secret\":\"{config['CLIENT_SECRET']}\"," \
            f"\"audience\":\"{config['API_AUDIENCE']}\"," \
            f"\"email\":\"{user.email}\"," \
            f"\"password\":\"{user.password}\"," \
            f"\"connection\":\"{config['CONNECTION']}\"," \
            f"\"grant_type\":\"client_credentials\"" \
           "}"
    headers = {"content-type":"application/json"}
    conn.request("POST","/dbconnections/signup",pyload,headers)
    conn.getresponse()

    user = await crud.create_user(user)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = await create_access_token(user.email,expires_delta=access_token_expires)
    return token

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=80, reload=True)