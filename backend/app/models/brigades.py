from sqlalchemy import Integer, Column, String, Date, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base
from backend.app.models.importer import Importer

class Brigade(Base):
    __tablename__ = "brigades"

    id = Column(Integer, primary_key=True, index=True)
    
    importers = relationship('Importer', back_populates='brigade')
