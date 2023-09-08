from src.commands.delete_post import DeletePost
from src.commands.create_post import CreatePost
from src.session import Session, engine
from src.models.model import Base
from src.errors.errors import InvalidParams, PostNotFoundError
from datetime import datetime, timedelta
import uuid
from tests.utils.constants import STATIC_FAKE_UUID

class TestDeletePost():
  def setup_method(self):
    Base.metadata.create_all(engine)
    self.session = Session()
    self.data = {
      'routeId': str(uuid.uuid4()),
      'expireAt': (datetime.now() + timedelta(days=2)).isoformat()
    }
    userId = str(uuid.uuid4())
    self.post = CreatePost(self.data, userId).execute()

  def test_delete_post(self):
    response = DeletePost(self.post['id']).execute()
    assert 'msg' in response

  def test_delete_post_invalid_id(self):
    try:
      DeletePost('1').execute()
      assert False
    except InvalidParams:
      assert True

  def test_delete_post_does_not_exist(self):
    try:
      DeletePost(STATIC_FAKE_UUID).execute()
      assert False
    except PostNotFoundError:
      assert True

  def teardown_method(self):
    self.session.close()
    Base.metadata.drop_all(bind=engine)