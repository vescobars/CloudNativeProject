from .base_command import BaseCommannd
from ..models.post import Post, PostSchema
from ..session import Session
from ..errors.errors import InvalidParams
from datetime import datetime
import uuid


class GetPosts(BaseCommannd):
    def __init__(self, data, userId=None):
        self.expire = data['expire'] if 'expire' in data else None
        self.route = data['route'] if 'route' in data else None
        if 'owner' in data:
            if data['owner'] == 'me':
                self.owner = userId
            else:
                self.owner = data['owner']
        else:
            self.owner = None

    def execute(self):
        session = Session()
        posts = session.query(Post).all()

        if self.owner != None:
            posts = [post for post in posts if post.userId ==
                     uuid.UUID(self.owner)]

        if self.route != None:
            posts = [post for post in posts if post.routeId ==
                     uuid.UUID(self.route)]

        if self.expire != None:
            if not self.is_boolean_string(self.expire):
                session.close()
                raise InvalidParams()

            if self.string_to_boolean(self.expire):
                posts = [post for post in posts if self.date_in_the_past(
                    post.expireAt.date())]
            else:
                posts = [post for post in posts if not self.date_in_the_past(
                    post.expireAt.date())]

        posts = PostSchema(many=True).dump(posts)
        session.close()

        return posts

    def date_in_the_past(self, date):
        current_utc_datetime = datetime.utcnow().date()
        return date < current_utc_datetime

    def is_boolean_string(self, s):
        return s.lower() == 'true' or s.lower() == 'false'

    def string_to_boolean(self, s):
        return s.lower() == 'true'
