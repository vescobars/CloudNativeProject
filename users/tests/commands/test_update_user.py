from src.session import Session, engine
from src.models.model import Base
from src.models.user import User
from src.main import app
from src.commands.create_user import CreateUser
from src.errors.errors import UserNotFoundError
from src.commands.update_user import UpdateUser, IncompleteParams
import json
from datetime import datetime, timedelta
from tests.utils.constants import STATIC_FAKE_UUID

class TestUpdateUser():
  def setup_method(self):
    Base.metadata.create_all(engine)
    self.session = Session()
    
    self.data = {
      'username': 'william',
      'email': 'william@gmail.com',
      'password': '123456',
      "dni": "123456",
      "fullName": "william",
      "phoneNumber": "300000000"
    }
    self.user = CreateUser(self.data).execute()

  def test_update_user(self):
    data = {
      "phoneNumber": "400000000",
      "fullName": "william",
      "dni": "654321",
      "status": "VERIFICADO"
    }
    response = UpdateUser(self.user['id'], data).execute()

    assert 'msg' in response

  def test_update_user_that_does_not_exist(self):
    data = {
      "phoneNumber": "400000000",
      "fullName": "william",
      "dni": "654321",
      "status": "VERIFICADO"
    }
    try:
      UpdateUser(STATIC_FAKE_UUID, data).execute()
      assert False
    except UserNotFoundError:
      assert True

  def test_update_user_missing_fields(self):
    data = {
      'username': 'william',
    }
    try:
      UpdateUser(self.user['id'], data).execute()
      assert False
    except IncompleteParams:
      assert True

  def teardown_method(self):
    self.session.close()
    Base.metadata.drop_all(bind=engine)