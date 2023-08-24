""" Main class of FastAPI Routes Microservice """

from fastapi import FastAPI

from src import models
from src.database import engine
from src.routes.router import router as routes_router

app = FastAPI()

app.include_router(routes_router, prefix="/routes", tags=["Routes"])

