from src.commands.create_offer import CreateOffer
from src.commands.get_offers import GetOffers
from src.session import Session, engine
from src.models.model import Base
from src.models.offer import Offer
from src.errors.errors import InvalidParam, IncompleteParams
from datetime import datetime, timedelta
from uuid import uuid4
from tests.utils.constants import STATIC_FAKE_UUID

class TestGetOffers():
  def setup_method(self):
    Base.metadata.create_all(engine)
    self.session = Session()
    self.userId = STATIC_FAKE_UUID
    self.data = {
      'postId': str(uuid4()),
      'description': 'My description',
      'size': 'LARGE',
      'fragile': True,
      'offer': 10
    }
    self.offer = CreateOffer(self.data, self.userId).execute()

  def test_get_offers(self):
    data = {}
    offers = GetOffers(data, self.userId).execute()
    assert len(offers) == 1
    assert 'id' in offers[0]
    assert 'createdAt' in offers[0]
    assert 'postId' in offers[0]
    assert 'description' in offers[0]
    assert 'size' in offers[0]
    assert 'fragile' in offers[0]
    assert 'offer' in offers[0]

  def test_get_offers_my_owner(self):
    data = {
      'owner': 'me'
    }
    offers = GetOffers(data, self.userId).execute()
    assert len(offers) == 1
    assert 'id' in offers[0]
    assert 'createdAt' in offers[0]
    assert 'postId' in offers[0]
    assert 'description' in offers[0]
    assert 'size' in offers[0]
    assert 'fragile' in offers[0]
    assert 'offer' in offers[0]

  def test_get_offers_other_owner(self):
    data = {
      'owner': str(uuid4())
    }
    offers = GetOffers(data, self.userId).execute()
    assert len(offers) == 0

  def test_get_offers_by_post(self):
    data = {
      'post': self.data['postId']
    }
    offers = GetOffers(data, self.userId).execute()
    assert len(offers) == 1
    assert 'id' in offers[0]
    assert 'createdAt' in offers[0]
    assert 'postId' in offers[0]
    assert 'description' in offers[0]
    assert 'size' in offers[0]
    assert 'fragile' in offers[0]
    assert 'offer' in offers[0]

  def test_get_offers_all_filters(self):
    data = {
      'post': self.data['postId'],
      'owner': 'me'
    }
    offers = GetOffers(data, self.userId).execute()
    assert len(offers) == 1
    assert 'id' in offers[0]
    assert 'createdAt' in offers[0]
    assert 'postId' in offers[0]
    assert 'description' in offers[0]
    assert 'size' in offers[0]
    assert 'fragile' in offers[0]
    assert 'offer' in offers[0]

  def test_get_offers_float_post_id(self):
    data = {
      'post': self.data['postId'],
      'owner': 'me'
    }
    offers = GetOffers(data, self.userId).execute()
    assert len(offers) == 1
    assert 'id' in offers[0]
    assert 'createdAt' in offers[0]
    assert 'postId' in offers[0]
    assert 'description' in offers[0]
    assert 'size' in offers[0]
    assert 'fragile' in offers[0]
    assert 'offer' in offers[0]

  def test_get_offers_invalid_post_id(self):
    try:
      data = {
        'post': 'invalid',
        'owner': 'me'
      }
      GetOffers(data, self.userId).execute()
      assert False
    except InvalidParam:
      assert True

  def teardown_method(self):
    self.session.close()
    Base.metadata.drop_all(bind=engine)