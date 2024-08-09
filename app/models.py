from sqlalchemy import Column, Integer, String, Float, DateTime
from app.database import Base

class Weather(Base):
    __tablename__ = "weather"
    
    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, index=True, nullable=False)
    date = Column(DateTime, index=True, nullable=False)
    min_temp = Column(Float, default=0.0)
    max_temp = Column(Float, default=0.0)
    avg_temp = Column(Float, default=0.0)
    humidity = Column(Float, default=0.0)

    def __repr__(self):
        return f"<Weather(id={self.id}, city='{self.city}', date={self.date}, min_temp={self.min_temp}, max_temp={self.max_temp}, avg_temp={self.avg_temp}, humidity={self.humidity})>"
