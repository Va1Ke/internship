import psycopg2
import databases
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import asyncio
import aioredis
from app.config import settings
from app.schemas import User
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.database import SessionLocal
from app.routes import router

db = databases.Database(settings.DATABASE_URL)

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


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.SignUpUser, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.post("/update-user/")
def create_user(user: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        return crud.update_user(db=db,user=user)
    else:
        return HTTPException(status_code=400, detail="No such user")


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.delete("/users/")
def delete_user(user: schemas.UserDelete, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        crud.delete_user(db=db, user=user)
        return HTTPException(status_code=200, detail="User deleted successfully")
    else:
        return HTTPException(status_code=400, detail="No such user")

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=80, reload=True)