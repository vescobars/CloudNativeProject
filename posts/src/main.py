from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from src.database import engine
from src import models

from .posts.router import router as posts_router

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(posts_router, prefix="/posts", tags=["Posts"])

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_, exc):
    return JSONResponse(status_code=400, content={
        "msg": "Request body is not properly structured",
        "errors": exc.errors()
    })