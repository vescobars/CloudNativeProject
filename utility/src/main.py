""" Main class of FastAPI Users Microservice """

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src import models
from src.database import engine
from src.utility.router import router as utility_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(utility_router, prefix="/utility", tags=["Utility"])


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_, exc):
    return JSONResponse(status_code=400, content={
        "msg": "Request body is not properly structured",
        "errors": exc.errors()
    })
