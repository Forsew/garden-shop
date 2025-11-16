from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..schemas.schemas import (
    ProductCategoryCreate, ProductCategoryResponse,
    ProductCreate, ProductUpdate, ProductResponse
)
from ..models.products import ProductCategory, Product

router = APIRouter(prefix="/api/products", tags=["products"])

# Категории продукции
@router.post("/categories", response_model=ProductCategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(category: ProductCategoryCreate, db: Session = Depends(get_db)):
    """Создать категорию продукции"""
    existing = db.query(ProductCategory).filter(ProductCategory.name == category.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Категория с таким названием уже существует")
    
    db_category = ProductCategory(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@router.get("/categories", response_model=List[ProductCategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    """Получить все категории"""
    return db.query(ProductCategory).all()

@router.get("/categories/{category_id}", response_model=ProductCategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    """Получить категорию по ID"""
    category = db.query(ProductCategory).filter(ProductCategory.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    return category

# Продукция
@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """Создать продукт"""
    # Проверяем существование категории
    category = db.query(ProductCategory).filter(ProductCategory.id == product.category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.get("/", response_model=List[ProductResponse])
def get_products(category_id: int = None, db: Session = Depends(get_db)):
    """Получить все продукты (с фильтрацией по категории)"""
    query = db.query(Product)
    if category_id:
        query = query.filter(Product.category_id == category_id)
    return query.all()

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Получить продукт по ID"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Продукт не найден")
    return product

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product_update: ProductUpdate, db: Session = Depends(get_db)):
    """Обновить продукт"""
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Продукт не найден")
    
    update_data = product_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_product, key, value)
    
    db.commit()
    db.refresh(db_product)
    return db_product

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """Удалить продукт"""
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Продукт не найден")
    
    db.delete(db_product)
    db.commit()
    return None