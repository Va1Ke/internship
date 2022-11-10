import aioredis
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.database import db
from app.config import settings
from fastapi import FastAPI
from app.routes import company_routes, routes, invitation_from_owner_routes, request_from_user_routes, quiz_routes, quiz_workflow_routes, analitics_routes, csv_routes


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
    await db.connect()

@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()


app.include_router(routes.router)
app.include_router(company_routes.router)
app.include_router(invitation_from_owner_routes.router)
app.include_router(request_from_user_routes.router)
app.include_router(quiz_routes.router)
app.include_router(quiz_workflow_routes.router)
app.include_router(analitics_routes.router)
app.include_router(csv_routes.router)


if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.APPHOST, port=settings.APPPORT, reload=True)