from .base_command import BaseCommannd
from ..models.post import Post, PostSchema
from ..session import Session
from ..errors.errors import InvalidParams, PostNotFoundError


class GetPost(BaseCommannd):
    def __init__(self, post_id):
        if self.is_uuid(post_id):
            self.post_id = post_id
        else:
            raise InvalidParams()

    def execute(self):
        session = Session()
        if len(session.query(Post).filter_by(id=self.post_id).all()) <= 0:
            session.close()
            raise PostNotFoundError()

        post = session.query(Post).filter_by(id=self.post_id).one()
        schema = PostSchema()
        post = schema.dump(post)

        session.close()

        return post
