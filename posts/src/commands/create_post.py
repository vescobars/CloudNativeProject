from .base_command import BaseCommannd
from ..models.post import Post, PostSchema, CreatedPostSchema
from ..session import Session
from ..errors.errors import IncompleteParams, InvalidDate
from datetime import datetime

class CreatePost(BaseCommannd):
    def __init__(self, data, userId=None):
        self.data = data
        if userId != None:
            self.data['userId'] = userId

    def execute(self):
        try:
            if 'expireAt' in self.data and self.data['expireAt'] != None and not self.valid_date():
                raise InvalidDate()

            posted_post = PostSchema(
                only=('routeId', 'userId', 'expireAt')
            ).load(self.data)
            post = Post(**posted_post)

            session = Session()

            session.add(post)
            session.commit()

            new_post = CreatedPostSchema().dump(post)
            session.close()

            return new_post
        except TypeError as posi:
            raise IncompleteParams

    def valid_date(self):
        try:
            # If last character is a Z remove it
            expireAt = self.data['expireAt'][:-1] if self.data['expireAt'][-1] == 'Z' else self.data['expireAt']
            date_obj = datetime.fromisoformat(expireAt).date()
            current_utc_datetime = datetime.utcnow().date()
            return date_obj > current_utc_datetime
        except:
            return False
