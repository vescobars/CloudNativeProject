from sqlite3 import IntegrityError

from fastapi import HTTPException
from src.constants import USERS_PATH
from src.posts.schemas import CreatePostRequestSchema, GetPostRequestSchema, GetPostsResponseSchema, GetSchema, PostSchema
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from src.models import Post
from src.exceptions import UniqueConstraintViolatedException
import os
import requests
from sqlalchemy import select
from src.constants import datetime_to_str
from sqlalchemy import delete

    
class Posts:
    
    @staticmethod
    def authenticate_User(bearer_token: str) -> str:
        headers = {"Authorization" : 'Bearer ' + bearer_token}
        url = USERS_PATH.rstrip('/') + "/users/me"
        print(url)
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            user_data = response.json()
            user_id = user_data["id"]
            return user_id
        else:
            raise HTTPException(status_code=401)


    @staticmethod
    def create_post(data: CreatePostRequestSchema, user_id: str, session: Session) -> PostSchema:
        """
        Insert a new post into the Posts table
        """
        new_post = None
        with session:
            current_time = datetime.now(timezone.utc)
            try:
                new_post = Post(
                    routeId=data.routeId,
                    expireAt=data.expireAt,
                    createdAt=current_time,
                    userId = user_id
                )

                session.add(new_post)
                session.commit()
            except IntegrityError as e:
                raise UniqueConstraintViolatedException(e)
        return new_post
    
    @staticmethod
    def get_posts(data: GetPostRequestSchema, user_id: str, sess: Session):
        filters = []

        if data.expire is not None:
            filters.append(Post.expireAt.isnot(None) if data.expire else Post.expireAt.is_(None))

        if data.route:
            filters.append(Post.routeId == data.route)

        if data.owner:
            filters.append(Post.userId == data.owner)
        else:
            filters.append(True)

        posts = sess.execute(
            select(Post).filter(*filters)
        ).scalars().all()

        posts_list = [
            {
                "id": str(post.id),
                "routeId": post.routeId,
                "userId": post.userId,
                "expireAt": post.expireAt,
                "createdAt": datetime_to_str(post.createdAt)
            }
            for post in posts
        ]
        response_data = GetPostsResponseSchema(posts=posts_list)

        return response_data

    
    @staticmethod
    def get_post(post_id: str, sess: Session):
        post = sess.execute( 
            select(Post).where(Post.id == post_id) 
        ).scalar()
        
        if post is None:
            raise HTTPException(status_code=404)
        
        response_data = GetSchema(
            id=post.id,
            userId=post.userId,
            routeId=post.routeId,
            expireAt=post.expireAt,
            createdAt=datetime_to_str(post.createdAt)
        )
        
        return response_data
    
    @staticmethod
    def delete_post(post_id: str, user_id:str, sess: Session):
        post = sess.execute( 
            select(Post).where(Post.id == post_id) 
        ).scalar()
        if post is None:
            raise HTTPException(status_code=404)
        sess.delete(post)
        sess.commit()
        return {"msg": "The post was successfully deleted"}
    
    @staticmethod
    def hard_reset(user_id:str, sess: Session):
        statement = delete(Post)
        with sess:
            sess.execute(statement)
            sess.commit()
        return {"msg": "Todos los datos fueron eliminados"}
        
        
        
        

        