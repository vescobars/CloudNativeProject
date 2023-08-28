import logging
from src.posts.schemas import GetPostRequestSchema, GetPostsResponseSchema, GetSchema
from src.posts.schemas import CreatePostRequestSchema, CreatePostResponseSchema
from fastapi import APIRouter, HTTPException, Response, Request, Depends, Header
from sqlalchemy.orm import Session
from sqlalchemy import delete
from typing import Annotated
from src.database import get_session
from src.posts.utils import Posts
from src.constants import datetime_to_str
from src.exceptions import UniqueConstraintViolatedException
import uuid
from datetime import datetime, timezone
from starlette.responses import JSONResponse
from src.models import Post
import json

router = APIRouter()

@router.post("/reset")
async def reset(
        session: Session = Depends(get_session),
):
    try:
        statement = delete(Post)
        print(statement)
        with session:
            session.execute(statement)
            session.commit()
    except Exception as e:
        logging.error(e)
        return JSONResponse(status_code=500, content={
            "msg": "Un error desconocido ha ocurrido", "error": json.dumps(e)})
    return {"msg": "Todos los datos fueron eliminados"}

@router.post("/")
def create_post(
        post_data: CreatePostRequestSchema, 
        response: Response,
        request:Request,
        sess: Annotated[Session, Depends(get_session)]
) -> CreatePostResponseSchema:
    try:
        if not request.headers.get('Authorization') or 'Bearer ' not in request.headers.get('Authorization'):
            raise HTTPException(status_code=403, detail="")
        
        if not post_data.routeId or not isinstance(post_data.routeId, str) or not uuid.UUID(post_data.routeId, version=4):
            raise HTTPException(status_code=400)
        
        if not post_data.expireAt or not isinstance(post_data.expireAt, datetime):
            raise HTTPException(status_code=400)
        
        current_time = datetime.now(timezone.utc)
        if not isinstance(post_data.expireAt, datetime) or post_data.expireAt.replace(tzinfo=timezone.utc) <= current_time:
            return JSONResponse(status_code=412, content={"msg": "La fecha expiración no es válida"})


        
        posts_util = Posts()
        
        bearer_token = request.headers.get('Authorization').split(" ")[1]
        user_id = posts_util.authenticate_User(bearer_token)
        
        post_data.expireAt = datetime.date(post_data.expireAt).isoformat()
        
        new_post = posts_util.create_post(post_data, user_id, sess)
        response_body: CreatePostResponseSchema = CreatePostResponseSchema(
            id=str(new_post.id),
            userId = user_id,
            createdAt=datetime_to_str(new_post.createdAt)
        )
        response.status_code = 201
        return response_body
    
    except UniqueConstraintViolatedException:
        raise JSONResponse(status_code=412, content={
            "msg": "La fecha expiración no es válida"})


@router.get("/ping")
def ping():
    return Response(content="pong", media_type="application/text", status_code=200)

@router.get("/")
def get_posts(
    get_data: GetPostRequestSchema,
    request: Request,
    sess: Annotated[Session, Depends(get_session)]
) -> GetPostsResponseSchema:
    
    if not request.headers.get('Authorization') or 'Bearer ' not in request.headers.get('Authorization'):
            raise HTTPException(status_code=403, detail="")

    if get_data.expire is not None and not isinstance(get_data.expire, bool):
        raise HTTPException(status_code=400)

    if get_data.route and (not isinstance(get_data.route, str) or not uuid.UUID(get_data.route, version=4)):
        raise HTTPException(status_code=400)

    if get_data.owner and (not isinstance(get_data.owner, str) or (get_data.owner != "me" and not uuid.UUID(get_data.owner, version=4))):
        raise HTTPException(status_code=400)

    posts_util = Posts()
    
    bearer_token = request.headers.get('Authorization').split(" ")[1]
    user_id = posts_util.authenticate_User(bearer_token)
    
    response_data = posts_util.get_posts(get_data, user_id, sess)
    return response_data

@router.get("/{post_id}")
def get_post_by_id(
    post_id: str,
    sess: Annotated[Session, Depends(get_session)],
    request:Request
) -> GetSchema:
    
    if not request.headers.get('Authorization') or 'Bearer ' not in request.headers.get('Authorization'):
        raise HTTPException(status_code=403, detail="")

    try:
        uuid_obj = uuid.UUID(post_id, version=4)
    except ValueError:
        raise HTTPException(status_code=400, detail="El id no es un valor string con formato uuid")
    
    bearer_token = request.headers.get('Authorization').split(" ")[1]
    posts_util = Posts()
    user_id = posts_util.authenticate_User(bearer_token)
    
    response_data = posts_util.get_post(post_id, sess)
    return response_data


@router.delete("/{post_id}")
def delete_post(
    post_id: str,
    sess: Annotated[Session, Depends(get_session)],
    request: Request
):
    if not request.headers.get('Authorization') or 'Bearer ' not in request.headers.get('Authorization'):
            raise HTTPException(status_code=403, detail="")
        
    if not isinstance(post_id, str) or not uuid.UUID(post_id, version=4):
        raise HTTPException(status_code=400, detail="El id no es un valor string con formato uuid")
    
    bearer_token = request.headers.get('Authorization').split(" ")[1]
    posts_util = Posts()
    user_id = posts_util.authenticate_User(bearer_token)
    response = posts_util.delete_post(post_id, user_id, sess)
    return response



    


    

