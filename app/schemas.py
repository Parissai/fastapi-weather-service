from pydantic import BaseModel, ConfigDict
from datetime import datetime

class WeatherBase(BaseModel):
    city: str
    date: datetime
    min_temp: float
    max_temp: float
    avg_temp: float
    humidity: float

class WeatherCreate(WeatherBase):
    pass

class WeatherResponse(WeatherBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
