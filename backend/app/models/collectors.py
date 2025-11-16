from sqlalchemy import Integer, Column, String, Date, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base
from brigades import Brigade

class Collector(Base):
    __tablename__ = "collectors"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False, index=True)
    photo = Column(String, nullable=True)
    personal_characteristic = Column(String(500))
    birth_year = Column(Integer, index=True, nullable=False)
    brigade_id = Column(Integer, ForeignKey('brigades.id'), nullable=False)

    brigade = relationship('Brigade', back_populates='collectors')
