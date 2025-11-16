from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..schemas.schemas import (
    BrigadeCreate, BrigadeResponse, BrigadeWithCollectors,
    CollectorCreate, CollectorUpdate, CollectorResponse, CollectorWithBrigade
)
from ..models.brigades import Brigade
from ..models.collectors import Collector

router = APIRouter(prefix="/api/brigades", tags=["brigades"])

# Бригады
@router.post("/", response_model=BrigadeResponse, status_code=status.HTTP_201_CREATED)
def create_brigade(brigade: BrigadeCreate, db: Session = Depends(get_db)):
    """Создать бригаду"""
    existing = db.query(Brigade).filter(Brigade.name == brigade.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Бригада с таким названием уже существует")
    
    db_brigade = Brigade(**brigade.dict())
    db.add(db_brigade)
    db.commit()
    db.refresh(db_brigade)
    return db_brigade

@router.get("/", response_model=List[BrigadeWithCollectors])
def get_brigades(db: Session = Depends(get_db)):
    """Получить все бригады со сборщиками"""
    return db.query(Brigade).all()

@router.get("/{brigade_id}", response_model=BrigadeWithCollectors)
def get_brigade(brigade_id: int, db: Session = Depends(get_db)):
    """Получить бригаду по ID"""
    brigade = db.query(Brigade).filter(Brigade.id == brigade_id).first()
    if not brigade:
        raise HTTPException(status_code=404, detail="Бригада не найдена")
    return brigade

@router.delete("/{brigade_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_brigade(brigade_id: int, db: Session = Depends(get_db)):
    """Удалить бригаду"""
    db_brigade = db.query(Brigade).filter(Brigade.id == brigade_id).first()
    if not db_brigade:
        raise HTTPException(status_code=404, detail="Бригада не найдена")
    
    # Проверяем, есть ли сборщики в бригаде
    if db_brigade.collectors:
        raise HTTPException(status_code=400, detail="Нельзя удалить бригаду со сборщиками")
    
    db.delete(db_brigade)
    db.commit()
    return None

# Сборщики
@router.post("/collectors", response_model=CollectorResponse, status_code=status.HTTP_201_CREATED)
def create_collector(collector: CollectorCreate, db: Session = Depends(get_db)):
    """Создать сборщика"""
    # Проверяем существование бригады
    brigade = db.query(Brigade).filter(Brigade.id == collector.brigade_id).first()
    if not brigade:
        raise HTTPException(status_code=404, detail="Бригада не найдена")
    
    db_collector = Collector(**collector.dict())
    db.add(db_collector)
    db.commit()
    db.refresh(db_collector)
    return db_collector

@router.get("/collectors", response_model=List[CollectorWithBrigade])
def get_collectors(brigade_id: int = None, db: Session = Depends(get_db)):
    """Получить всех сборщиков (с фильтрацией по бригаде)"""
    query = db.query(Collector)
    if brigade_id:
        query = query.filter(Collector.brigade_id == brigade_id)
    
    collectors = query.all()
    result = []
    for collector in collectors:
        collector_dict = {
            "id": collector.id,
            "full_name": collector.full_name,
            "photo": collector.photo,
            "personal_characteristic": collector.personal_characteristic,
            "birth_year": collector.birth_year,
            "brigade_id": collector.brigade_id,
            "brigade_name": collector.brigade.name
        }
        result.append(collector_dict)
    return result

@router.get("/collectors/{collector_id}", response_model=CollectorResponse)
def get_collector(collector_id: int, db: Session = Depends(get_db)):
    """Получить сборщика по ID"""
    collector = db.query(Collector).filter(Collector.id == collector_id).first()
    if not collector:
        raise HTTPException(status_code=404, detail="Сборщик не найден")
    return collector

@router.put("/collectors/{collector_id}", response_model=CollectorResponse)
def update_collector(collector_id: int, collector_update: CollectorUpdate, db: Session = Depends(get_db)):
    """Обновить сборщика (в т.ч. перевести в другую бригаду)"""
    db_collector = db.query(Collector).filter(Collector.id == collector_id).first()
    if not db_collector:
        raise HTTPException(status_code=404, detail="Сборщик не найден")
    
    update_data = collector_update.dict(exclude_unset=True)
    
    # Если меняем бригаду, проверяем её существование
    if 'brigade_id' in update_data:
        brigade = db.query(Brigade).filter(Brigade.id == update_data['brigade_id']).first()
        if not brigade:
            raise HTTPException(status_code=404, detail="Бригада не найдена")
    
    for key, value in update_data.items():
        setattr(db_collector, key, value)
    
    db.commit()
    db.refresh(db_collector)
    return db_collector

@router.delete("/collectors/{collector_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_collector(collector_id: int, db: Session = Depends(get_db)):
    """Удалить сборщика"""
    db_collector = db.query(Collector).filter(Collector.id == collector_id).first()
    if not db_collector:
        raise HTTPException(status_code=404, detail="Сборщик не найден")
    
    db.delete(db_collector)
    db.commit()
    return None