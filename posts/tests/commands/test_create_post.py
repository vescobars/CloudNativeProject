from src.commands.create_post import CreatePost
from src.session import Session, engine
from src.models.model import Base
from src.models.post import Post
from src.errors.errors import IncompleteParams, InvalidDate
from datetime import datetime, timedelta
import uuid

class TestCreatePost():
  def setup_method(self):
    Base.metadata.create_all(engine)
    self.session = Session()

  def test_create_post(self):
    data = {
      'routeId': str(uuid.uuid4()),
      'expireAt': (datetime.now() + timedelta(days=2)).isoformat()
    }
    userId = str(uuid.uuid4())
    post = CreatePost(data, userId).execute()

    assert post['userId'] == userId
    assert 'id' in post
    assert 'createdAt' in post

  def test_create_post_missing_fields(self):
    try:
      CreatePost({}).execute()
      assert False
    except IncompleteParams:
      assert True

  def test_create_post_past_date(self):
    try:
      data = {
        'routeId': str(uuid.uuid4()),
        'expireAt': (datetime.now() - timedelta(days=2)).isoformat()
      }
      userId = str(uuid.uuid4())
      CreatePost(data, userId).execute()
      assert False
    except InvalidDate:
      assert True

  def test_create_post_invalid_date(self):
    try:
      data = {
        'routeId': str(uuid.uuid4()),
        'expireAt': 'invalid'
      }
      userId = str(uuid.uuid4())
      CreatePost(data, userId).execute()
      assert False
    except InvalidDate:
      assert True

  def teardown_method(self):
    self.session.close()
    Base.metadata.drop_all(bind=engine)