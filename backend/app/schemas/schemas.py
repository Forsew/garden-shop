from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime, date
import re

class BrigadeCreate(BaseModel):
    name: str

class BrigadeResponse(BrigadeCreate):
    id: int

    class Config:
        from_attributes = True

class CollectorCreate(BaseModel):
    full_name: str
    photo: Optional[str] = None
    personal_characteristic: Optional[str] = None
    birth_year: int
    brigade_id: int

class CollectorResponse(CollectorCreate):
    id: int

    class Config:
        from_attributes = True

class UserRegistration(BaseModel):
    username: str
    full_name: str
    password: str
    birth_date: date
    address: str
    gender: str
    hobby: Optional[str] = None
    vk_profile: Optional[str] = None
    blood_group: str
    rh_factor: str

    @validator('password')
    def validate_password(cls, value):
        if len(value) < 6:
           raise ValueError('Пароль должен быть длиннее 6 символов')
        if not re.search(r'[A-Z]', value):
            raise ValueError('Пароль должен содержать заглавные латинские буквы')
        if not re.search(r'[a-z]', value):
            raise ValueError('Пароль должен содержать строчные латинские буквы')
        if not re.search(r'[0-9]', value):
            raise ValueError('Пароль должен содержать цифры')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>+=\[\]\\/;\'`~]', value):
            raise ValueError('Пароль должен содержать спецсимволы')
        if not re.search(r'[ \-_]', value):
            raise ValueError('Пароль должен содержать пробел, дефис или подчеркивание')
        if re.search(r'[а-яА-ЯёЁ]', value):
            raise ValueError('Пароль не должен содержать русские буквы')
        return value
    
class UserResponse(UserRegistration):
    id: int

    class Config:
        from_attrinutes = True

class UserLogin(BaseModel):
    username: str
    password: str
