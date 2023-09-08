from src.commands.delete_route import DeleteRoute
from src.commands.create_route import CreateRoute
from src.session import Session, engine
from src.models.model import Base
from src.models.route import Route
from src.errors.errors import InvalidParams, RouteNotFoundError
from datetime import datetime, timedelta
from tests.utils.constants import STATIC_FAKE_UUID

class TestDeleteRoute():
  def setup_method(self):
    Base.metadata.create_all(engine)
    self.session = Session()

    self.data = {
      'flightId': 'A2',
      'sourceAirportCode': 'LAX',
      'sourceCountry': 'USA',
      'destinyAirportCode': 'BOG',
      'destinyCountry': 'CO',
      'bagCost': 100,
      'plannedStartDate': datetime.utcnow().isoformat(),
      'plannedEndDate': (datetime.utcnow() + timedelta(days=2)).isoformat()
    }
    self.route = CreateRoute(self.data).execute()

  def test_delete_route(self):
    response = DeleteRoute(self.route['id']).execute()
    assert 'msg' in response

  def test_delete_route_invalid_id(self):
    try:
      DeleteRoute('1').execute()
      assert False
    except InvalidParams:
      assert True

  def test_delete_route_does_not_exist(self):
    try:
      DeleteRoute(STATIC_FAKE_UUID).execute()
      assert False
    except RouteNotFoundError:
      assert True

  def teardown_method(self):
    self.session.close()
    Base.metadata.drop_all(bind=engine)