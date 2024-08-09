import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models import Weather
from datetime import datetime

# Setup in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def setup_database():
    # Create tables
    Base.metadata.create_all(bind=engine)
    yield
    # Drop tables
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session(setup_database):
    # Create a new session for each test
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_create_weather(db_session):
    # Create an instance of Weather
    weather = Weather(
        city="New York",
        date=datetime(2024, 8, 8),
        min_temp=10.0,
        max_temp=25.0,
        avg_temp=18.0,
        humidity=65.0
    )
    # Add and commit the new Weather instance
    db_session.add(weather)
    db_session.commit()

    # Query the Weather instance
    queried_weather = db_session.query(Weather).filter_by(city="New York", date=datetime(2024, 8, 8)).first()
    
    assert queried_weather is not None
    assert queried_weather.city == "New York"
    assert queried_weather.date == datetime(2024, 8, 8)
    assert queried_weather.min_temp == 10.0
    assert queried_weather.max_temp == 25.0
    assert queried_weather.avg_temp == 18.0
    assert queried_weather.humidity == 65.0

def test_default_values(db_session):
    # Create an instance of Weather with defaults
    weather = Weather(
        city="San Francisco",
        date=datetime(2024, 8, 8)
    )
    db_session.add(weather)
    db_session.commit()

   
