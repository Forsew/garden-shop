from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import date
from ..database import get_db
from ..schemas.schemas import HarvestLogCreate, HarvestLogResponse, HarvestLogWithDetails
from ..models.harvest import HarvestLog
from ..models.collectors import Collector
from ..models.brigades import Brigade

router = APIRouter(prefix="/api/harvest", tags=["harvest"])

@router.post("/", response_model=HarvestLogResponse, status_code=status.HTTP_201_CREATED)
def create_harvest_log(log: HarvestLogCreate, db: Session = Depends(get_db)):
    """Создать запись о сборе урожая"""
    # Проверяем существование сборщика и бригады
    collector = db.query(Collector).filter(Collector.id == log.collector_id).first()
    if not collector:
        raise HTTPException(status_code=404, detail="Сборщик не найден")
    
    brigade = db.query(Brigade).filter(Brigade.id == log.brigade_id).first()
    if not brigade:
        raise HTTPException(status_code=404, detail="Бригада не найдена")
    
    # Проверяем, что сборщик состоит в указанной бригаде
    if collector.brigade_id != log.brigade_id:
        raise HTTPException(status_code=400, detail="Сборщик не состоит в указанной бригаде")
    
    db_log = HarvestLog(**log.dict())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

@router.get("/", response_model=List[HarvestLogWithDetails])
def get_harvest_logs(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    collector_id: Optional[int] = None,
    brigade_id: Optional[int] = None,
    crop_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Получить журнал сбора урожая с фильтрацией"""
    query = db.query(HarvestLog)
    
    if start_date:
        query = query.filter(HarvestLog.harvest_date >= start_date)
    if end_date:
        query = query.filter(HarvestLog.harvest_date <= end_date)
    if collector_id:
        query = query.filter(HarvestLog.collector_id == collector_id)
    if brigade_id:
        query = query.filter(HarvestLog.brigade_id == brigade_id)
    if crop_type:
        query = query.filter(HarvestLog.crop_type.ilike(f"%{crop_type}%"))
    
    logs = query.order_by(HarvestLog.harvest_date.desc()).all()
    
    # Добавляем информацию о сборщике и бригаде
    result = []
    for log in logs:
        log_dict = {
            "id": log.id,
            "collector_id": log.collector_id,
            "brigade_id": log.brigade_id,
            "harvest_date": log.harvest_date,
            "crop_type": log.crop_type,
            "quantity": log.quantity,
            "quality_grade": log.quality_grade,
            "notes": log.notes,
            "created_at": log.created_at,
            "collector_name": log.collector.full_name,
            "brigade_name": log.brigade.name
        }
        result.append(log_dict)
    
    return result

@router.get("/{log_id}", response_model=HarvestLogWithDetails)
def get_harvest_log(log_id: int, db: Session = Depends(get_db)):
    """Получить запись по ID"""
    log = db.query(HarvestLog).filter(HarvestLog.id == log_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Запись не найдена")
    
    return {
        "id": log.id,
        "collector_id": log.collector_id,
        "brigade_id": log.brigade_id,
        "harvest_date": log.harvest_date,
        "crop_type": log.crop_type,
        "quantity": log.quantity,
        "quality_grade": log.quality_grade,
        "notes": log.notes,
        "created_at": log.created_at,
        "collector_name": log.collector.full_name,
        "brigade_name": log.brigade.name
    }

@router.get("/stats/summary")
def get_harvest_stats(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """Получить статистику по сбору урожая"""
    query = db.query(HarvestLog)
    
    if start_date:
        query = query.filter(HarvestLog.harvest_date >= start_date)
    if end_date:
        query = query.filter(HarvestLog.harvest_date <= end_date)
    
    total_quantity = query.with_entities(func.sum(HarvestLog.quantity)).scalar() or 0
    total_logs = query.count()
    
    # Статистика по культурам
    crops_stats = query.with_entities(
        HarvestLog.crop_type,
        func.sum(HarvestLog.quantity).label('total')
    ).group_by(HarvestLog.crop_type).all()
    
    # Статистика по бригадам
    brigades_stats = query.with_entities(
        Brigade.name,
        func.sum(HarvestLog.quantity).label('total')
    ).join(Brigade).group_by(Brigade.name).all()
    
    return {
        "total_quantity": float(total_quantity),
        "total_logs": total_logs,
        "by_crop": [{"crop": c[0], "quantity": float(c[1])} for c in crops_stats],
        "by_brigade": [{"brigade": b[0], "quantity": float(b[1])} for b in brigades_stats]
    }

@router.delete("/{log_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_harvest_log(log_id: int, db: Session = Depends(get_db)):
    """Удалить запись"""
    log = db.query(HarvestLog).filter(HarvestLog.id == log_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Запись не найдена")
    
    db.delete(log)
    db.commit()
    return None