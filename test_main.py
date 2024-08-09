import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_weather():
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
