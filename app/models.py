from sqlalchemy import Column, Integer, String, Float, DateTime
from app.database import Base

class Weather(Base):
    __tablename__ = "weather"
    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, index=True)
    date = Column(DateTime, index=True)
    min_temp = Column(Float)
    max_temp = Column(Float)
    avg_temp = Column(Float)
    humidity = Column(Float)
