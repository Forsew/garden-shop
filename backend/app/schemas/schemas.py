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
    username: str = Field(..., min_length=3, description="Username должен быть уникальным")
    full_name: str = Field(..., min_length=3, description="ФИО")
    password: str = Field(..., min_length=6, description="Пароль")
    birth_date: date = Field(..., description="Дата рождения")
    address: str = Field(..., min_length=5, description="Адрес")
    gender: str = Field(..., description="Пол: Мужской или Женский")
    hobby: Optional[str] = Field(None, description="Интересы")
    vk_profile: Optional[str] = Field(None, description="Ссылка на VK профиль")
    blood_group: str = Field(..., description="Группа крови: 1, 2, 3, 4")
    rh_factor: str = Field(..., description="Резус фактор: + или -")

    @validator('username')
    def validate_username(cls, value):
        if not re.match(r'^[a-zA-Z0-9_]+$', value):
            raise ValueError('Username может содержать только латинские буквы, цифры и подчеркивание')
        return value

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
    
    @validator('rh_factor')
    def validate_rh_factor(cls, value):
        if value not in ['+', '-']:
            raise ValueError('Резус фактор должен быть + или -')
        return value
    
    @validator('vk_profile')
    def validate_vk_profile(cls, value):
        if value and not value.startswith(('https://vk.com/', 'http://vk.com/', 'vk.com/')):
            raise ValueError('Неверная ссылка на VK')
        return value
    
class UserResponse(BaseModel):
    id: int
    username: str
    full_name: str
    birth_date: date
    address: str
    gender: str
    hobby: Optional[str]
    vk_profile: Optional[str]
    blood_group: str
    rh_factor: str

    class Config:
        from_attrinutes = True

class UserLogin(BaseModel):
    username: str
    password: str
