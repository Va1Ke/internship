import psycopg2
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import asyncio
import aioredis

app = FastAPI()


async def connect_uri():
    conn = await aioredis.create_connection(
        'redis://localhost/0')
    val = await conn.execute('GET', 'my-key')

async def connect_tcp():
    conn = await aioredis.create_connection(
        ('localhost', 6379))
    val = await conn.execute('GET', 'my-key')

async def connect_unixsocket():
    conn = await aioredis.create_connection(
        '/path/to/redis/socket')
    # or uri 'unix:///path/to/redis/socket?db=1'
    val = await conn.execute('GET', 'my-key')

asyncio.get_event_loop().run_until_complete(connect_tcp())
asyncio.get_event_loop().run_until_complete(connect_unixsocket())



conn = psycopg2.connect(dbname="postgres", user="postgres", password="postgres")


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

@app.get("/")
async def root():
    return {"status": "Working"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=80, reload=True)