from pydantic import BaseModel, field_validator, ConfigDict
from datetime import datetime

class WeatherBase(BaseModel):
    city: str
    date: datetime
    min_temp: float
    max_temp: float
    avg_temp: float
    humidity: float

    model_config = ConfigDict(from_attributes=True)


    @field_validator('date', mode='before')
    def check_date(cls, value):
        if value > datetime.now():
            raise ValueError('Date cannot be in the future.')
        return value


class WeatherCreate(WeatherBase):
    pass

class WeatherResponse(WeatherBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
