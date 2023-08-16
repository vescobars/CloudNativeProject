""" Main class of FastAPI Users Microservice """

from fastapi import FastAPI

from src import models
from src.database import engine, SessionLocal
from src.users.router import router as users_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users_router, prefix="/users", tags=["Users"])


@app.get("/")
async def root():
    return {"message": "Hello World"}
