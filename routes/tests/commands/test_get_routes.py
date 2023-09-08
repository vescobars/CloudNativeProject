from src.commands.get_routes import GetRoutes
from src.commands.create_route import CreateRoute
from src.session import Session, engine
from src.models.model import Base
from src.models.route import Route
from src.errors.errors import InvalidParams
from datetime import datetime, timedelta

class TestGetRoutes():
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
  
  def test_get_routes_by_flight_id(self):
    routes = GetRoutes({
      'flight': self.data['flightId']
    }).execute()

    assert len(routes) == 1
    assert routes[0]['id'] == self.route['id']

  def test_get_routes(self):
    routes = GetRoutes({}).execute()

    assert len(routes) == 1
    assert routes[0]['id'] == self.route['id']

  def test_get_routes_empty(self):
    routes = GetRoutes({
      'flight': f'{self.data["flightId"]}other'
    }).execute()
    assert len(routes) == 0

  def teardown_method(self):
    self.session.close()
    Base.metadata.drop_all(bind=engine)