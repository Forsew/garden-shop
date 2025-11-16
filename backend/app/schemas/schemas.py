from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime, date
import re

class BrigadeCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)

class BrigadeResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class CollectorCreate(BaseModel):
    full_name: str = Field(..., min_length=3, max_length=100)
    photo: Optional[str] = None
    personal_characteristic: Optional[str] = Field(None, max_length=500)
    birth_year: int = Field(..., ge=1950, le=2010)
    brigade_id: int

class CollectorUpdate(BaseModel):
    full_name: Optional[str] = None
    photo: Optional[str] = None
    personal_characteristic: Optional[str] = None
    birth_year: Optional[int] = Field(None, ge=1950, le=2010)
    brigade_id: Optional[int] = None

class CollectorResponse(BaseModel):
    id: int
    full_name: str
    photo: Optional[str]
    personal_characteristic: Optional[str]
    birth_year: int
    brigade_id: int

    class Config:
        from_attributes = True

class CollectorWithBrigade(CollectorResponse):
    brigade_name: str

class BrigadeWithCollectors(BrigadeResponse):
    collectors: List[CollectorResponse] = []


# === ПРОДУКЦИЯ ===
class ProductCategoryCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = None

class ProductCategoryResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    class Config:
        from_attributes = True

class ProductCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=200)
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    stock: int = Field(default=0, ge=0)
    category_id: int
    image_url: Optional[str] = None

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    category_id: Optional[int] = None
    image_url: Optional[str] = None

class ProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    stock: int
    category_id: int
    image_url: Optional[str]
    category: ProductCategoryResponse
    class Config:
        from_attributes = True

# === БРИГАДЫ (обновленные) ===
class BrigadeWithCollectors(BrigadeResponse):
    collectors: List['CollectorResponse'] = []

class CollectorWithBrigade(CollectorResponse):
    brigade_name: str

# === ЖУРНАЛ УРОЖАЯ ===
class HarvestLogCreate(BaseModel):
    collector_id: int
    brigade_id: int
    harvest_date: date
    crop_type: str = Field(..., min_length=2, max_length=100)
    quantity: float = Field(..., gt=0)
    quality_grade: str = Field(..., pattern="^[ABC]$")
    notes: Optional[str] = Field(None, max_length=500)

    @validator('quality_grade')
    def validate_quality(cls, v):
        if v not in ['A', 'B', 'C']:
            raise ValueError('Качество должно быть A, B или C')
        return v

class HarvestLogResponse(BaseModel):
    id: int
    collector_id: int
    brigade_id: int
    harvest_date: date
    crop_type: str
    quantity: float
    quality_grade: str
    notes: Optional[str]
    created_at: datetime
    class Config:
        from_attributes = True

class HarvestLogWithDetails(HarvestLogResponse):
    collector_name: str
    brigade_name: str

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


