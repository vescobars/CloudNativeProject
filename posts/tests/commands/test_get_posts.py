from src.commands.get_posts import GetPosts
from src.commands.create_post import CreatePost
from src.session import Session, engine
from src.models.model import Base
from src.models.post import Post
from src.errors.errors import InvalidParams
from datetime import datetime, timedelta
import uuid

class TestGetPosts():
  def setup_method(self):
    Base.metadata.create_all(engine)
    self.session = Session()
    self.post_data = {
      'routeId': str(uuid.uuid4()),
      'expireAt': (datetime.now() + timedelta(days=2)).isoformat()
    }
    self.userId = str(uuid.uuid4())
    self.post = CreatePost(self.post_data, self.userId).execute()

  def test_get_posts(self):
    data = {}
    posts = GetPosts(data, self.userId).execute()
    assert len(posts) == 1

  def test_get_posts_by_expire_true(self):
    data = {
      'expire': 'true'
    }
    posts = GetPosts(data, self.userId).execute()
    assert len(posts) == 0

  def test_get_posts_by_expire_false(self):
    data = {
      'expire': 'false'
    }
    posts = GetPosts(data, self.userId).execute()
    assert len(posts) == 1

  def test_get_posts_by_expire_invalid(self):
    data = {
      'expire': 'invalid'
    }
    try:
      GetPosts(data, self.userId).execute()
      assert False
    except InvalidParams:
      assert True

  def test_get_posts_by_route(self):
    data = {
      'route': self.post_data['routeId']
    }
    posts = GetPosts(data, self.userId).execute()
    assert len(posts) == 1
  
  def test_get_posts_by_my_owner(self):
    data = {
      'owner': 'me'
    }
    posts = GetPosts(data, self.userId).execute()
    assert len(posts) == 1

  def test_get_posts_by_other_owner(self):
    data = {
      'owner': str(uuid.uuid4())
    }
    posts = GetPosts(data, self.userId).execute()
    assert len(posts) == 0

  def test_get_posts_by_all_filters(self):
    data = {
      'route': self.post_data['routeId'],
      'expire': 'false',
      'owner': 'me'
    }
    posts = GetPosts(data, self.userId).execute()
    assert len(posts) == 1

  def teardown_method(self):
    self.session.close()
    Base.metadata.drop_all(bind=engine)