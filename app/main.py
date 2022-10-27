from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import asyncio
import aioredis
from app.database import db
from app.config import settings
from fastapi import FastAPI
from app.routes import router


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


app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=80, reload=True)