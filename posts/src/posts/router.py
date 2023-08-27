from src.posts.schemas import GetPostRequestSchema, GetPostsResponseSchema, GetSchema
from src.posts.schemas import CreatePostRequestSchema, CreatePostResponseSchema
from fastapi import APIRouter, HTTPException, Response, Request, Depends, Header
from sqlalchemy.orm import Session
from typing import Annotated, Union
from src.database import get_session
from src.posts.utils import Posts
from src.constants import datetime_to_str
from src.exceptions import UniqueConstraintViolatedException
import uuid
from datetime import datetime, timezone, date


router = APIRouter()

@router.post("/")
def create_post(
        post_data: CreatePostRequestSchema, 
        response: Response,
        request:Request,
        sess: Annotated[Session, Depends(get_session)]
) -> CreatePostResponseSchema:
    try:
        if not request.headers.get('Authorization') or 'Bearer ' not in request.headers.get('Authorization'):
            raise HTTPException(status_code=403, detail=str(request.headers))
        
        if not post_data.routeId or not isinstance(post_data.routeId, str) or not uuid.UUID(post_data.routeId, version=4):
            raise HTTPException(status_code=400, detail="Alguno de los campos no esté presente en la solicitud, o no tengan el formato esperado.")
        
        if not post_data.expireAt or not isinstance(post_data.expireAt, datetime):
            raise HTTPException(status_code=400, detail="Alguno de los campos no esté presente en la solicitud, o no tengan el formato esperado.")
        
        if not isinstance(post_data.expireAt, datetime):
            raise HTTPException(status_code=412, detail={"msg": "La fecha expiración no es válida"})

        current_time = datetime.now(timezone.utc)
        if post_data.expireAt.replace(tzinfo=timezone.utc) <= current_time:
            raise HTTPException(status_code=412, detail={"msg": "La fecha expiración no es válida"})
        
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
    
    except UniqueConstraintViolatedException as e:
        print(e)
        raise HTTPException(status_code=412, detail="La fecha expiración no es válida")

@router.get("/ping")
def ping():
    return Response(content="pong", media_type="application/text", status_code=200)

@router.get("/")
def get_posts(
    get_data: GetPostRequestSchema,
    request: Request,
    sess: Annotated[Session, Depends(get_session)],
    Authorization: str = Header(None)
) -> GetPostsResponseSchema:
    
    if not request.headers.get('Authorization') or 'Bearer ' not in request.headers.get('Authorization'):
            raise HTTPException(status_code=403, detail="No hay token en la solicitud")

    if get_data.expire is not None and not isinstance(get_data.expire, bool):
        raise HTTPException(status_code=400, detail="Alguno de los campos de búsqueda no tiene el formato esperado")

    if get_data.route and (not isinstance(get_data.route, str) or not uuid.UUID(get_data.route, version=4)):
        raise HTTPException(status_code=400, detail="Alguno de los campos de búsqueda no tiene el formato esperado")

    if get_data.owner and (not isinstance(get_data.owner, str) or (get_data.owner != "me" and not uuid.UUID(get_data.owner, version=4))):
        raise HTTPException(status_code=400, detail="Alguno de los campos de búsqueda no tiene el formato esperado")

    posts_util = Posts()
    
    bearer_token = request.headers.get('Authorization').split(" ")[1]
    user_id = posts_util.authenticate_User(bearer_token)
    
    response_data = posts_util.get_posts(get_data, user_id, sess)
    return response_data

@router.get("/{post_id}")
def get_post_by_id(
    post_id: str,
    sess: Annotated[Session, Depends(get_session)],
    request:Request, 
    Authorization: str = Header(None)
) -> GetSchema:
    
    if not request.headers.get('Authorization') or 'Bearer ' not in request.headers.get('Authorization'):
        raise HTTPException(status_code=403, detail="No hay token en la solicitud")

    if not isinstance(post_id, str) or not uuid.UUID(post_id, version=4):
        raise HTTPException(status_code=400, detail="El id no es un valor string con formato uuid")
    
    bearer_token = request.headers.get('Authorization').split(" ")[1]
    posts_util = Posts()
    user_id = posts_util.authenticate_User(bearer_token)
    
    response_data = posts_util.get_post(post_id, sess)
    return response_data

@router.delete("/{post_id}")
def delete_post(
    post_id: str,
    request: Request,
    sess: Annotated[Session, Depends(get_session)]
):
    if not request.headers.get('Authorization') or 'Bearer ' not in request.headers.get('Authorization'):
            raise HTTPException(status_code=403, detail="No hay token en la solicitud")
        
    if not isinstance(post_id, str) or not uuid.UUID(post_id, version=4):
        raise HTTPException(status_code=400, detail="El id no es un valor string con formato uuid")
    
    posts_util = Posts()
    user_id = posts_util.authenticate_User(request.headers.get('Authorization'))
    response = posts_util.delete_post(post_id, user_id, sess)
    return response


@router.post("/reset")
def reset(sess: Session = Depends(get_session),
    Authorization: str = Header(None)):
    posts_util = Posts()
    user_id = posts_util.authenticate_User(Authorization)
    response = posts_util.hard_reset(sess)
    return response

    


    

