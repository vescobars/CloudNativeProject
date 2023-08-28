""" Main class of FastAPI Routes Microservice """

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src import models
from src.database import engine
from src.exception import ErrorResponseException
from src.routes.router import router as routes_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.exception_handler(ErrorResponseException)
async def error_response_exception_handler(request: Request, exc: ErrorResponseException):
    """
    Send custom error response
    :param request:
    :param exc: an object with a status code and a detail
    :return:
    """
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail,
    )


app.include_router(routes_router, prefix="/routes", tags=["Routes"])
