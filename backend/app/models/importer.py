from sqlalchemy import Integer, Column, String, Date, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base
from brigades import Brigade

class Importer(Base):
    __tablename__ = "importers"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False, index=True)
    photo = Column(String, nullable=True)
    personal_characteristic = Column(String(500), nullable=False)
    birth_day = Column(Date, index=True, nullable=False)
    brigade_id = Column(Integer, ForeignKey('brigades.id'), nullable=False)

    brigade = relationship('Brigade', back_populates='importers')
    info = relationship('Info', uselist=False, back_populates='importer')
