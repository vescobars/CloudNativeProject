from src.commands.create_offer import CreateOffer
from src.session import Session, engine
from src.models.model import Base
from src.models.offer import Offer
from src.errors.errors import IncompleteParams, InvalidParamFormat
from datetime import datetime, timedelta
from uuid import uuid4

class TestCreateOffer():
  def setup_method(self):
    Base.metadata.create_all(engine)
    self.session = Session()
    self.userId = str(uuid4())

  def test_create_offer(self):
    data = {
      'postId': str(uuid4()),
      'description': 'My description',
      'size': 'LARGE',
      'fragile': True,
      'offer': 10
    }
    offer = CreateOffer(data, self.userId).execute()
    assert 'id' in offer
    assert offer['userId'] == self.userId
    assert 'createdAt' in offer

  def test_create_offer_lowercase_size(self):
    data = {
      'postId': str(uuid4()),
      'description': 'My description',
      'size': 'medium',
      'fragile': True,
      'offer': 10
    }
    offer = CreateOffer(data, self.userId).execute()
    assert 'id' in offer
    assert offer['userId'] == self.userId
    assert 'createdAt' in offer

  def test_create_offer_missing_fields(self):
    try:
      data = {
        'postId': str(uuid4()),
        'description': 'My description'
      }
      CreateOffer(data, self.userId).execute()
      assert False
    except IncompleteParams:
      assert True
    
  def test_create_offer_invalid_size(self):
    try:
      data = {
        'postId': str(uuid4()),
        'description': 'My description',
        'size': 'invalid',
        'fragile': True,
        'offer': 10
      }
      CreateOffer(data, self.userId).execute()
      assert False
    except InvalidParamFormat:
      assert True

  def test_create_negative_offer(self):
    try:
      data = {
        'postId': str(uuid4()),
        'description': 'My description',
        'size': 'SMALL',
        'fragile': True,
        'offer': -10
      }
      CreateOffer(data, self.userId).execute()
      assert False
    except InvalidParamFormat:
      assert True

  def teardown_method(self):
    self.session.close()
    Base.metadata.drop_all(bind=engine)