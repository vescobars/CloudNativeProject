""" /users router """
from fastapi import APIRouter, Response

router = APIRouter()


@router.get("/ping")
async def ping():
    return Response(content="pong", media_type="application/text")
