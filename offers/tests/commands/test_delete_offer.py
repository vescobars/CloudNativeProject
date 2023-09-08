from src.commands.delete_offer import DeleteOffer
from src.commands.create_offer import CreateOffer
from src.session import Session, engine
from src.models.model import Base
from src.errors.errors import InvalidParam, OfferNotFoundError
from datetime import datetime, timedelta
from uuid import uuid4
from tests.utils.constants import STATIC_FAKE_UUID

class TestDeleteOffer():
  def setup_method(self):
    Base.metadata.create_all(engine)
    self.session = Session()
    self.data = {
      'postId': str(uuid4()),
      'description': 'My description',
      'size': 'LARGE',
      'fragile': True,
      'offer': 10
    }
    userId = str(uuid4())
    self.offer = CreateOffer(self.data, userId).execute()

  def test_delete_offer(self):
    response = DeleteOffer(self.offer['id']).execute()
    assert 'msg' in response

  def test_delete_offer_invalid_id(self):
    try:
      DeleteOffer('1').execute()
      assert False
    except InvalidParam:
      assert True

  def test_delete_offer_does_not_exist(self):
    try:
      DeleteOffer(STATIC_FAKE_UUID).execute()
      assert False
    except OfferNotFoundError:
      assert True

  def teardown_method(self):
    self.session.close()
    Base.metadata.drop_all(bind=engine)