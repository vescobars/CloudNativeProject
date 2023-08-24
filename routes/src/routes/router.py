from fastapi import APIRouter, Response

router = APIRouter()


@router.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@router.get("/ping")
async def ping():
    return Response(content="pong", media_type="application/text")
