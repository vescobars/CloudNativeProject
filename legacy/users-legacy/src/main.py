""" Main class of FastAPI Users Microservice """

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


from src import models
from src.database import engine
from src.users.router import router as users_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users_router, prefix="/users", tags=["Users"])


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_, exc):
    return JSONResponse(status_code=400, content={
        "msg": "Request body is not properly structured",
        "errors": exc.errors()
    })
