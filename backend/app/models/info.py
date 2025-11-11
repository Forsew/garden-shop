from sqlalchemy import Integer, Column, String, Date, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base
from importer import Importer

class Info(Base):
    __tablename__ = 'info'

    id = Column(Integer, primary_key=True, index=True)
    importer_id = Column(Integer, ForeignKey('importer.id'), nullable=False, unique=True)
    address = Column(String(200), index=True, nullable=False)
    gender = Column(String(20), index=True, nullable=False)
    hobby = Column(String(200), index=True, nullable=True)
    vk = Column(Text, nullable=False, unique=True)
    blood_group = Column(Integer, index=True, nullable=False)
    rezus_factor = Column(String(20), index=True, nullable=False)


    importer = relationship('Importer', back_populates='info')