from sqlalchemy import Integer, Column, String
from sqlalchemy.orm import relationship
from ..database import Base

class Brigade(Base):
    __tablename__ = "brigades"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, index=True)
    collectors = relationship('Collector', back_populates='brigade')