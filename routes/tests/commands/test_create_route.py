from src.commands.create_route import CreateRoute
from src.session import Session, engine
from src.models.model import Base
from src.models.route import Route
from src.errors.errors import IncompleteParams, FlightIdAlreadyExists, InvalidDates
from datetime import datetime, timedelta

class TestCreateRoute():
  def setup_method(self):
    Base.metadata.create_all(engine)
    self.session = Session()

  def test_create_route(self):
    data = {
      'flightId': 'A2',
      'sourceAirportCode': 'LAX',
      'sourceCountry': 'USA',
      'destinyAirportCode': 'BOG',
      'destinyCountry': 'CO',
      'bagCost': 100,
      'plannedStartDate': datetime.utcnow().isoformat(),
      'plannedEndDate': (datetime.utcnow() + timedelta(days=2)).isoformat()
    }
    route = CreateRoute(data).execute()

    assert 'id' in route
    assert 'createdAt' in route

  def test_create_route_missing_fields(self):
    data = {
      'sourceAirportCode': 'LAX',
    }
    try:
      CreateRoute(data).execute()
      assert False
    except IncompleteParams:
      assert len(self.session.query(Route).all()) == 0
      assert True

  def test_create_route_already_exist(self):
    data = {
      'flightId': 'A2',
      'sourceAirportCode': 'LAX',
      'sourceCountry': 'USA',
      'destinyAirportCode': 'BOG',
      'destinyCountry': 'CO',
      'bagCost': 100,
      'plannedStartDate': datetime.utcnow().isoformat(),
      'plannedEndDate': (datetime.utcnow() + timedelta(days=2)).isoformat()
    }
    CreateRoute(data).execute()

    try:
      CreateRoute(data).execute()
      assert False
    except FlightIdAlreadyExists:
      assert len(self.session.query(Route).all()) == 1
      assert True

  def test_create_route_start_date_invalid(self):
    data = {
        'flightId': 'A2',
        'sourceAirportCode': 'LAX',
        'sourceCountry': 'USA',
        'destinyAirportCode': 'BOG',
        'destinyCountry': 'CO',
        'bagCost': 100,
        'plannedStartDate': (datetime.utcnow() - timedelta(days=2)).isoformat(),
        'plannedEndDate': (datetime.utcnow() + timedelta(days=2)).isoformat()
    }
    try:
      CreateRoute(data).execute()
      assert False
    except InvalidDates:
      assert len(self.session.query(Route).all()) == 0
      assert True

  def test_create_route_end_date_invalid(self):
    data = {
        'flightId': 'A2',
        'sourceAirportCode': 'LAX',
        'sourceCountry': 'USA',
        'destinyAirportCode': 'BOG',
        'destinyCountry': 'CO',
        'bagCost': 100,
        'plannedStartDate': datetime.utcnow().isoformat(),
        'plannedEndDate': (datetime.utcnow() - timedelta(days=2)).isoformat()
    }
    try:
      CreateRoute(data).execute()
      assert False
    except InvalidDates:
      assert len(self.session.query(Route).all()) == 0
      assert True

  def test_create_route_both_start_and_end_date_invalid(self):
    data = {
        'flightId': 'A2',
        'sourceAirportCode': 'LAX',
        'sourceCountry': 'USA',
        'destinyAirportCode': 'BOG',
        'destinyCountry': 'CO',
        'bagCost': 100,
        'plannedStartDate': (datetime.utcnow() - timedelta(days=3)).isoformat(),
        'plannedEndDate': (datetime.utcnow() - timedelta(days=1)).isoformat()
    }
    try:
      CreateRoute(data).execute()
      assert False
    except InvalidDates:
      assert len(self.session.query(Route).all()) == 0
      assert True

  def teardown_method(self):
    self.session.close()
    Base.metadata.drop_all(bind=engine)