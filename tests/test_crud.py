import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from app.database import Base
from app import models, schemas
from app.crud import get_weather_by_city_and_date, create_weather
from datetime import datetime
import logging

# Configure logging to capture log messages for testing
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

def test_get_weather_by_city_and_date(db_session):
    # Create and insert a weather record
    weather = models.Weather(
        city="Seattle",
        date=datetime(2024, 8, 8),
        min_temp=15.0,
        max_temp=25.0,
        avg_temp=20.0,
        humidity=70.0
    )
    db_session.add(weather)
    db_session.commit()

    # Test the retrieval function
    retrieved_weather = get_weather_by_city_and_date(db_session, "Seattle", datetime(2024, 8, 8))

    assert retrieved_weather is not None
    assert retrieved_weather.city == "Seattle"
    assert retrieved_weather.date == datetime(2024, 8, 8)
    assert retrieved_weather.min_temp == 15.0
    assert retrieved_weather.max_temp == 25.0
    assert retrieved_weather.avg_temp == 20.0
    assert retrieved_weather.humidity == 70.0

def test_get_weather_by_city_and_date_no_record(db_session):
    # Test retrieval when no record exists
    retrieved_weather = get_weather_by_city_and_date(db_session, "Nonexistent City", datetime(2024, 8, 8))

    assert retrieved_weather is None

def test_create_weather(db_session):
    # Create a WeatherCreate schema object
    weather_data = schemas.WeatherCreate(
        city="Los Angeles",
        date=datetime(2024, 8, 8),
        min_temp=18.0,
        max_temp=28.0,
        avg_temp=23.0,
        humidity=50.0
    )

    # Test the create function
    created_weather = create_weather(db_session, weather_data)

    assert created_weather.id is not None
    assert created_weather.city == "Los Angeles"
    assert created_weather.date == datetime(2024, 8, 8)
    assert created_weather.min_temp == 18.0
    assert created_weather.max_temp == 28.0
    assert created_weather.avg_temp == 23.0
    assert created_weather.humidity == 50.0

def test_create_weather_exception(db_session, monkeypatch):
    # Mock SQLAlchemyError to test exception handling
    def mock_add(*args, **kwargs):
        raise SQLAlchemyError("Database error")

    monkeypatch.setattr(db_session, 'add', mock_add)
    
    # Create a WeatherCreate schema object
    weather_data = schemas.WeatherCreate(
        city="Houston",
        date=datetime(2024, 8, 8),
        min_temp=22.0,
        max_temp=32.0,
        avg_temp=27.0,
        humidity=60.0
    )

    # Test the exception handling
    with pytest.raises(SQLAlchemyError):
        create_weather(db_session, weather_data)
