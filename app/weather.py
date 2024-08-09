import httpx
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv
from app import crud, schemas
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class Config:
    WEATHER_API_URL = "http://api.weatherapi.com/v1/history.json"
    API_KEY = os.getenv("WEATHER_API_KEY")

    @staticmethod
    def validate():
        if not Config.API_KEY:
            raise ValueError("Weather API key is missing. Please set WEATHER_API_KEY in the environment variables.")

# Validate configuration
Config.validate()

async def fetch_weather_data(city: str, date: str) -> dict:
    """
    Fetch weather data from the external API.

    Args:
        city (str): The name of the city to fetch weather data for.
        date (str): The date to fetch weather data for, in 'YYYY-MM-DD' format.

    Returns:
        dict: The weather data in JSON format.

    Raises:
        httpx.HTTPStatusError: If the HTTP request to the weather API fails.
        ValueError: If the response does not contain expected data.
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                Config.WEATHER_API_URL,
                params={"key": Config.API_KEY, "q": city, "dt": date}
            )
            response.raise_for_status()
            data = response.json()
            
            # Check if the response has the expected structure
            if "forecast" not in data or "forecastday" not in data["forecast"]:
                logger.error("Unexpected response structure: %s", data)
                raise ValueError("Unexpected response structure from weather API.")
            
            return data
        except httpx.HTTPStatusError as e:
            logger.error("HTTP request failed: %s", e)
            raise
        except ValueError as e:
            logger.error("Data validation error: %s", e)
            raise

async def get_weather(db: Session, city: str, date: str) -> schemas.WeatherResponse:
    """
    Retrieve weather data from the database or fetch it from the API if not present.

    Args:
        db (Session): The database session object.
        city (str): The name of the city to get weather data for.
        date (str): The date to get weather data for, in 'YYYY-MM-DD' format.

    Returns:
        schemas.WeatherResponse: The weather data object.

    Raises:
        Exception: If there is an error fetching or storing weather data.
    """
    # Fetch weather from the database
    weather = crud.get_weather_by_city_and_date(db, city, date)
    if weather:
        return weather
    
    # Fetch weather from the external API
    data = await fetch_weather_data(city, date)
    forecast = data["forecast"]["forecastday"][0]["day"]
    
    # Create a weather data object
    weather_data = schemas.WeatherCreate(
        city=city,
        date=date,
        min_temp=forecast.get("mintemp_c"),
        max_temp=forecast.get("maxtemp_c"),
        avg_temp=forecast.get("avgtemp_c"),
        humidity=forecast.get("avghumidity")
    )
    
    # Store weather data in the database
    try:
        return crud.create_weather(db, weather_data)
    except Exception as e:
        logger.error("Error saving weather data to database: %s", e)
        raise
