from sqlalchemy import Integer, Column, String, Date, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base
from backend.app.models.collectors import Collector

class Brigade(Base):
    __tablename__ = "brigades"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, index=True)
    collectors = relationship('Collector', back_populates='brigade')
