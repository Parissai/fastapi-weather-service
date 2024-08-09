from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from pydantic import BaseModel, field_validator
import re
from app import weather, schemas, database

class WeatherRequest(BaseModel):
    city: str
    date: str

    @field_validator("date")
    def validate_date_format(cls, value):
        """
        Validate the format of a date string.

        Checks if the provided date string matches the expected format "YYYY-MM-DD".
        Raises a `ValueError` if the format is invalid.

        Args:
            cls: The class method context (not used here).
            value (str): The date string to be validated.

        Returns:
            str: The original date string if it matches the required format.

        Raises:
            ValueError: If the date string does not match the format "YYYY-MM-DD".
        """
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", value):
            raise ValueError("Invalid date format. Use 'YYYY-MM-DD'.")
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid date. Please ensure the date exists.")
        return value

# Initialize the database
database.init_db()

app = FastAPI()

@app.get("/weather", response_model=schemas.WeatherResponse)
async def get_weather(city: str, date: str, db: Session = Depends(database.get_db)):
    """
    Retrieve weather data for a specific city and date.

    Fetches weather data from the database for the specified city and date.
    Raises a 404 error if the data is not found.

    Args:
        city (str): The name of the city.
        date (str): The date in the format "YYYY-MM-DD".
        db (Session, optional): Database session dependency.

    Returns:
        schemas.WeatherResponse: The weather data for the city and date.

    Raises:
        HTTPException: 404 if weather data is not found.
    """
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use 'YYYY-MM-DD'.")

    weather_data = await weather.get_weather(db, city, date_obj)
    if not weather_data:
        raise HTTPException(status_code=404, detail="Weather data not found")

    return weather_data
