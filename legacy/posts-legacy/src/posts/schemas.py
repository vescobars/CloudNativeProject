from datetime import datetime, timezone
import uuid
from typing import Optional, Annotated
from pydantic import BaseModel, Field, AfterValidator, validator


def check_uuid4(v: str) -> str:
    uuid.UUID(v)
    return v

def date_validation(d:datetime):
    current_date = datetime.now(timezone.utc)
    if d < current_date:
        raise ValueError("Date cannot be before the current date")
    return d

class CreatePostRequestSchema(BaseModel):
    routeId: str = Field(min_length=1)
    expireAt: datetime

class CreatePostResponseSchema(BaseModel):
    id: str = Annotated[str, AfterValidator(check_uuid4)]
    userId : str
    createdAt: datetime
     
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
    expireAt: datetime
    createdAt: datetime

    @validator("id", "routeId", "userId", pre=True)
    def validate_uuid_to_str(cls, value):
        if isinstance(value, uuid.UUID):
            return str(value)
        return value

class GetPostsResponseSchema(BaseModel):
    posts: list[GetSchema]