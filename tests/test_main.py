import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import models, schemas, database, main  # Adjust import as needed
from datetime import datetime

# Setup in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the database tables
models.Base.metadata.create_all(bind=engine)

# Initialize the TestClient with the FastAPI app
app = main.app
client = TestClient(app)

@pytest.fixture(scope="module")
def db_session():
    """Fixture to provide a database session for tests."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="module")
def setup_database():
    """Fixture to create and drop tables in the in-memory database."""
    models.Base.metadata.create_all(bind=engine)
    yield
    models.Base.metadata.drop_all(bind=engine)

def test_get_weather_success(db_session, setup_database):
    """
    Test the `/weather` endpoint for retrieving weather data for a specific city and date.

    This test sends a GET request to the `/weather` endpoint with the query parameters 
    `city` set to "London" and `date` set to "2024-08-09". It asserts that the response 
    status code is 200, indicating a successful request. The test also checks that the 
    response JSON contains the expected keys: "city", "date", "min_temp", "max_temp", 
    and "avg_temp".

    Steps:
        1. Sends a GET request to the `/weather` endpoint with the query parameters 
        `city` set to "London" and `date` set to "2024-08-09".
        2. Asserts that the response status code is 200, indicating a successful request.
        3. Parses the JSON response data.
        4. Prints the response data for debugging purposes.
        5. Asserts that the response JSON contains the expected keys: "city", "date", 
        "min_temp", "max_temp", and "avg_temp".

    Assertions:
        - The response status code should be 200 (OK).
        - The response JSON should contain the keys "city", "date", "min_temp", 
          "max_temp", and "avg_temp".

    Example:
        Running this test might produce the following output in the console:

        data {
            "city": "London",
            "date": "2024-08-09",
            "min_temp": 15.2,
            "max_temp": 25.4,
            "avg_temp": 20.3
        }
    """
     
    response = client.get("/weather?city=London&date=2024-08-09")
    assert response.status_code == 200
    data = response.json()
    print('data', data)
    assert "city" in data
    assert "date" in data
    assert "min_temp" in data
    assert "max_temp" in data
    assert "avg_temp" in data

def test_get_weather_invalid_date_format(db_session, setup_database):
    """Test case for invalid date format."""
    response = client.get("/weather", params={"city": "Seattle", "date": "2024-08-32"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid date format. Use 'YYYY-MM-DD'."}

def test_get_weather_internal_server_error(db_session, setup_database, monkeypatch):
    """Test case for internal server error when fetching weather data."""
    def mock_get_weather(*args, **kwargs):
        raise Exception("Unexpected error")

    monkeypatch.setattr("app.weather.get_weather", mock_get_weather)

    response = client.get("/weather", params={"city": "Seattle", "date": "2024-08-08"})
    assert response.status_code == 500
    assert response.json() == {"detail": "Internal server error. Please try again later."}
