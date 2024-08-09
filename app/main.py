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

        This method checks if the provided date string matches the expected format 
        "YYYY-MM-DD". If the format is invalid, it raises a `ValueError`.

        Args:
            cls: The class that the validator is being applied to (used for class methods).
            value (str): The date string to be validated.

        Returns:
            str: The original date string if it matches the required format.

        Raises:
            ValueError: If the date string does not match the format "YYYY-MM-DD", 
            a `ValueError` is raised with a message indicating the format requirement.

        Example:
            >>> validate_date_format("2024-08-08")
            '2024-08-08'

            >>> validate_date_format("08-08-2024")
            ValueError: Invalid date format. Use 'YYYY-MM-DD'.
        """
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", value):
            raise ValueError("Invalid date format. Use 'YYYY-MM-DD'.")
        return value

# Initialize the database
database.init_db()

app = FastAPI()

@app.get("/weather/", response_model=schemas.WeatherResponse)
async def get_weather(city: str, date: str, db: Session = Depends(database.get_db)):
    """
    Retrieve weather data for a specific city and date.

    This function fetches weather data from the database for the specified city and date. 
    If the data is not found, it raises an HTTP 404 exception.

    Args:
        city (str): The name of the city for which to retrieve weather data.
        date (str): The date for which to retrieve weather data, in the format "YYYY-MM-DD".
        db (Session, optional): The database session dependency, automatically injected by FastAPI.

    Returns:
        dict: A dictionary containing the weather data for the specified city and date.

    Raises:
        HTTPException: If no weather data is found for the given city and date, a 404 error is raised.
    """
     
    date_obj = datetime.strptime(date, "%Y-%m-%d")
    weather_data = await weather.get_weather(db, city, date_obj)
    if not weather_data:
        raise HTTPException(status_code=404, detail="Weather data not found")

    return weather_data
