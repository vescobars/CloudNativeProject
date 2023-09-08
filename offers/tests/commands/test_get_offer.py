from src.commands.create_offer import CreateOffer
from src.commands.get_offer import GetOffer
from src.session import Session, engine
from src.models.model import Base
from src.models.offer import Offer
from src.errors.errors import InvalidParam, OfferNotFoundError
from datetime import datetime, timedelta
from uuid import uuid4
from tests.utils.constants import STATIC_FAKE_UUID

class TestGetOffer():
  def setup_method(self):
    Base.metadata.create_all(engine)
    self.session = Session()
    self.userId = str(uuid4())
    self.data = {
      'postId': str(uuid4()),
      'description': 'My description',
      'size': 'LARGE',
      'fragile': True,
      'offer': 10
    }
    self.offer = CreateOffer(self.data, self.userId).execute()

  def test_get_offer(self):
    offer = GetOffer(self.offer['id']).execute()
    assert 'id' in offer
    assert 'createdAt' in offer
    assert 'postId' in offer
    assert 'description' in offer
    assert 'size' in offer
    assert 'fragile' in offer
    assert 'offer' in offer

  def test_get_offer_invalid_id(self):
    try:
      GetOffer('invalid').execute()
      assert False
    except InvalidParam:
      assert True

  def test_get_offer_doesnt_exist(self):
    try:
      GetOffer(STATIC_FAKE_UUID).execute()
      assert False
    except OfferNotFoundError:
      assert True

  def teardown_method(self):
    self.session.close()
    Base.metadata.drop_all(bind=engine)