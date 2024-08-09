from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from app import models, schemas
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_weather_by_city_and_date(db: Session, city: str, date: datetime):
    """
    Retrieve a weather record for a specific city and date from the database.

    It returns the first matching record, or `None` if no match is found.

    Args:
        db (Session): The SQLAlchemy session object used for database operations.
        city (str): The name of the city for which to retrieve the weather data.
        date (datetime): The specific date for which to retrieve the weather data.

    Returns:
        models.Weather or None: The weather record as a SQLAlchemy model instance if found, 
        otherwise `None`.
    """
    try:
        return db.query(models.Weather).filter(models.Weather.city == city, models.Weather.date == date).first()
    except SQLAlchemyError as e:
        logger.error(f"Error querying weather by city and date: {e}")
        raise

def create_weather(db: Session, weather: schemas.WeatherCreate):
    """
    Create a new weather record in the database.

    This function takes a SQLAlchemy database session and a `WeatherCreate` schema object,
    then creates and stores a new weather record in the database. The function commits 
    the transaction and refreshes the instance to ensure it contains any updates made by the 
    database (e.g., generated primary keys).

    Args:
        db (Session): The SQLAlchemy session object used for database operations.
        weather (schemas.WeatherCreate): The Pydantic schema object containing the weather data to be saved.

    Returns:
        models.Weather: The newly created weather record as a SQLAlchemy model instance.
    
    Raises:
        Exception: If there is an error creating the weather record.
    """
    db_weather = models.Weather(**weather.model_dump())
    
    try:
        db.add(db_weather)
        db.commit()
        db.refresh(db_weather)
        return db_weather
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error creating weather record: {e}")
        raise
