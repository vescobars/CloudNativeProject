from src.commands.get_post import GetPost
from src.commands.create_post import CreatePost
from src.session import Session, engine
from src.models.model import Base
from src.models.post import Post
from src.errors.errors import InvalidParams, PostNotFoundError
from datetime import datetime, timedelta
import uuid
from tests.utils.constants import STATIC_FAKE_UUID

class TestGetPost():
  def setup_method(self):
    Base.metadata.create_all(engine)
    self.session = Session()

    data = {
      'routeId': str(uuid.uuid4()),
      'expireAt': (datetime.now() + timedelta(days=2)).isoformat()
    }
    userId = str(uuid.uuid4())
    self.post = CreatePost(data, userId).execute()

  def test_get_post(self):
    post = GetPost(self.post['id']).execute()

    assert post['id'] == self.post['id']
    assert 'routeId' in post
    assert 'userId' in post
    assert 'expireAt' in post

  def test_get_post_invalid_id(self):
    try:
      GetPost('Invalid').execute()
      assert False
    except InvalidParams:
      assert True

  def test_get_post_doesnt_exist(self):
    try:
      GetPost(STATIC_FAKE_UUID).execute()
      assert False
    except PostNotFoundError:
      assert True

  def teardown_method(self):
    self.session.close()
    Base.metadata.drop_all(bind=engine)