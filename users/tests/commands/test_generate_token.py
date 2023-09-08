from src.commands.generate_token import GenerateToken
from src.commands.create_user import CreateUser
from src.session import Session, engine
from src.models.model import Base
from src.models.user import User
from src.errors.errors import IncompleteParams, Unauthorized, UserNotFoundError

class TestGenerateToken():
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

  def test_generate_token_missing_field(self):
    try:
      GenerateToken({
        'username': self.data['username']
      }).execute()
      assert False
    except IncompleteParams:
      assert True

  def test_generate_token_wrong_password(self):
    try:
      GenerateToken({
        'username': self.data['username'],
        'password': 'wrong'
      }).execute()
      assert False
    except UserNotFoundError:
      assert True

  def test_generate_token_user_doesnt_exist(self):
    try:
      GenerateToken({
        'username': 'wrong',
        'password': 'wrong'
      }).execute()
      assert False
    except UserNotFoundError:
      assert True

  def test_generate_token(self):
    user = GenerateToken(self.data).execute()

    assert 'id' in user
    assert 'token' in user
    assert 'expireAt' in user
  
  def teardown_method(self):
    self.session.close()
    Base.metadata.drop_all(bind=engine)