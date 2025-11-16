from sqlalchemy import Integer, Column, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from ..database import Base

class ProductCategory(Base):
    """Категории продукции (удобрения)"""
    __tablename__ = "product_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    
    products = relationship('Product', back_populates='category')

class Product(Base):
    """Продукция (удобрения)"""
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)  # Количество на складе
    category_id = Column(Integer, ForeignKey('product_categories.id'), nullable=False)
    image_url = Column(String(500), nullable=True)
    
    category = relationship('ProductCategory', back_populates='products')