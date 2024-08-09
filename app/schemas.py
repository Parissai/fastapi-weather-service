from pydantic import BaseModel, Field, field_validator, ConfigDict
from datetime import datetime

class WeatherBase(BaseModel):
    city: str = Field(..., example="New York", min_length=1)
    date: datetime
    min_temp: float = Field(..., gt=-100.0, lt=100.0, example=10.5)
    max_temp: float = Field(..., gt=-100.0, lt=100.0, example=25.5)
    avg_temp: float = Field(..., gt=-100.0, lt=100.0, example=18.0)
    humidity: float = Field(..., ge=0.0, le=100.0, example=65.0)

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
