import datetime
import uuid
from typing import Optional, Annotated

from pydantic import BaseModel, EmailStr, Field, AfterValidator

from src.schemas import UserStatusEnum

def check_uuid4(v: str) -> str:
    uuid.UUID(v)
    return v

class CreatePostRequestSchema(BaseModel):
    routeId: str = Field(min_length=1)
    expireAt: datetime = Field(min_length=1)
        
class CreatePostResponseSchema(BaseModel):
    id: str = Annotated[str, AfterValidator(check_uuid4)]
    userId : str
    createdAt: str
     
class GetPostRequestSchema(BaseModel):
    expire: Optional[bool]
    route:Optional[str]
    owner:Optional[str]

class PostSchema(BaseModel):
    id: str
    userId:str
    createdAt: str
    
class GetSchema(BaseModel):
    id: str
    routeId: str
    userId: str
    expireAt: str
    createdAt: str

class GetPostsResponseSchema(BaseModel):
    posts: list[GetSchema]