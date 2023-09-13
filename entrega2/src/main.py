""" Main class of FastAPI Users Microservice """

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src import models
from src.config import lifespan
from src.database import engine
from src.exceptions import ResponseException
from src.rf004.router import router as rf004_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI(lifespan=lifespan)

app.include_router(rf004_router, prefix="/rf004", tags=["RF004"])


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_, exc):
    return JSONResponse(status_code=400, content={
        "msg": "Request body is not properly structured",
        "errors": exc.errors()
    })


@app.exception_handler(ResponseException)
async def response_exception_handler(_, exc: ResponseException):
    return JSONResponse(status_code=exc.status_code, content={
        "msg": exc.msg,
        "detail": exc.detail
    })
