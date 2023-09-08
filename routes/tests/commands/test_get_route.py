from src.commands.get_route import GetRoute
from src.commands.create_route import CreateRoute
from src.session import Session, engine
from src.models.model import Base
from src.models.route import Route
from src.errors.errors import InvalidParams, RouteNotFoundError
from datetime import datetime, timedelta
from tests.utils.constants import STATIC_FAKE_UUID

class TestGetRoute():
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

  def test_get_route(self):
    route = GetRoute(self.route['id']).execute()

    assert route['id'] == self.route['id']
    assert route['sourceAirportCode'] == self.data['sourceAirportCode']
    assert route['sourceCountry'] == self.data['sourceCountry']
    assert route['destinyAirportCode'] == self.data['destinyAirportCode']
    assert route['destinyCountry'] == self.data['destinyCountry']
    assert route['bagCost'] == self.data['bagCost']
    assert route['flightId'] == self.data['flightId']
    assert route['plannedStartDate'] == self.data['plannedStartDate']
    assert route['plannedEndDate'] == self.data['plannedEndDate']

  def test_get_route_invalid_id(self):
    try:
      GetRoute('non_number_id').execute()

      assert False
    except InvalidParams:
      assert True

  def test_get_route_doesnt_exist(self):
    try:
      GetRoute(STATIC_FAKE_UUID).execute()

      assert False
    except RouteNotFoundError:
      assert True

  
  def teardown_method(self):
    self.session.close()
    Base.metadata.drop_all(bind=engine)