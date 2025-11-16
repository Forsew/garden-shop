from sqlalchemy import Integer, Column, String, Float, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class HarvestLog(Base):
    """Журнал учета сбора урожая"""
    __tablename__ = "harvest_logs"

    id = Column(Integer, primary_key=True, index=True)
    collector_id = Column(Integer, ForeignKey('collectors.id'), nullable=False)
    brigade_id = Column(Integer, ForeignKey('brigades.id'), nullable=False)
    harvest_date = Column(Date, nullable=False, index=True)
    crop_type = Column(String(100), nullable=False)  # Вид культуры
    quantity = Column(Float, nullable=False)  # Количество (кг)
    quality_grade = Column(String(20), nullable=False)  # Класс качества (A, B, C)
    notes = Column(String(500), nullable=True)  # Примечания
    created_at = Column(DateTime, default=datetime.utcnow)
    
    collector = relationship('Collector', backref='harvest_logs')
    brigade = relationship('Brigade', backref='harvest_logs')