from sqlalchemy import Integer, Column, String, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class Collector(Base):
    __tablename__ = "collectors"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False, index=True)
    photo = Column(String, nullable=True)
    personal_characteristic = Column(String(500))
    birth_year = Column(Integer, index=True, nullable=False)
    brigade_id = Column(Integer, ForeignKey('brigades.id'), nullable=False)

    brigade = relationship('Brigade', back_populates='collectors')
