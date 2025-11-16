from sqlalchemy import Integer, Enum, Column, String, Date, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True)
    full_name = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    birth_date = Column(Date, nullable=False, index=True)
    address = Column(String(200), index=True, nullable=False)
    gender = Column(Enum("Мужской", "Женский", name='gender_enum'), index=True, nullable=False)
    hobby = Column(String(200), index=True, nullable=True)
    vk_profile = Column(Text, unique=True)
    blood_group = Column(Enum("1", "2", "3", "4", name="blood_type_enum"), index=True, nullable=False)
    rh_factor = Column(Enum("+", "-", name="rh_factor_enum"))