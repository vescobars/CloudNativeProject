""" Main class of FastAPI Users Microservice """

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.config import lifespan
from src.creditcards.router import router as creditcards_router
from src.exceptions import ResponseException

app = FastAPI(lifespan=lifespan)

app.include_router(creditcards_router, prefix="/credit-cards", tags=["Credit Cards"])


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
