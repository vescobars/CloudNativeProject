from posts.src.posts.schemas import GetPostRequestSchema, GetPostsResponseSchema, GetSchema
from src.posts.schemas import CreatePostRequestSchema, CreatePostResponseSchema
from fastapi import APIRouter, HTTPException, Response, Depends, Header
from sqlalchemy.orm import Session
from typing import Annotated
from src.database import get_session
from src.posts.utils import Posts
from src.constants import datetime_to_str
from users.src.exceptions import UniqueConstraintViolatedException


router = APIRouter()

@router.post("/")
def create_post(
        post_data: CreatePostRequestSchema, 
        response: Response,
        sess: Annotated[Session, Depends(get_session)],
        Authorization: str = Header(None),
) -> CreatePostResponseSchema:
    try:
        posts_util = Posts()
        user_id = posts_util.authenticate_User(Authorization)
        new_post = posts_util.create_post(post_data, user_id, sess)
        response_body: CreatePostResponseSchema = CreatePostResponseSchema(
            id=str(new_post.id),
            userId = user_id,
            createdAt=datetime_to_str(new_post.createdAt),
        )
        response.status_code = 201
        return response_body
    except UniqueConstraintViolatedException as e:##TODO: Checkear la fecha, y no el uniqueness
        print(e)
        raise HTTPException(status_code=412, detail="La fecha expiración no es válida")


@router.get("/")
def get_posts(
    get_data: GetPostRequestSchema, 
    response: Response,
    sess: Annotated[Session, Depends(get_session)],
    Authorization: str = Header(None)
) -> GetPostsResponseSchema:
    posts_util = Posts()
    user_id = posts_util.authenticate_User(Authorization)
    response_data = posts_util.get_posts(get_data, user_id, sess)
    return response_data

@router.get("/{post_id}")
def get_post_by_id(
    post_id: str,
    sess: Annotated[Session, Depends(get_session)],
    Authorization: str = Header(None)
) -> GetSchema:
    posts_util = Posts()
    user_id = posts_util.authenticate_User(Authorization) ## Se necesita?
    response_data = posts_util.get_post(post_id, sess)
    return response_data

@router.delete("/{post_id}")
def delete_post(
    post_id: str,
    sess: Annotated[Session, Depends(get_session)],
    Authorization: str = Header(None)
):
    posts_util = Posts()
    user_id = posts_util.authenticate_User(Authorization)
    response = posts_util.delete_post(post_id, user_id, sess)
    return response


@router.get("/ping")
async def ping():
    return Response(content="pong", media_type="application/text", status_code=200)


@router.post("/reset")
async def reset(sess: Session = Depends(get_session),
    Authorization: str = Header(None)):
    posts_util = Posts()
    user_id = posts_util.authenticate_User(Authorization)
    response = posts_util.hard_reset(sess)
    return response

    


    

