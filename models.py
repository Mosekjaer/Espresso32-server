from sqlalchemy import Column, Float, Integer, BigInteger, Text
from pydantic import BaseModel
from database import Base

class SensorData(Base):
    __tablename__ = "sensor_data"
    id = Column(Integer, primary_key=True, index=True)
    timestamp_ms = Column(BigInteger)
    light = Column(Float)
    eco2 = Column(Integer)
    tvoc = Column(Integer)
    mic = Column(Integer)
    temp = Column(Float)
    humidity = Column(Float)
    should_open = Column(Integer)
    reason = Column(Text)
    
class AirQualityAdvice(BaseModel):
    should_open: bool
    reason: str