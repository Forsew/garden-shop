from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import Dict
from ..database import get_db
from pydantic import BaseModel
from ..schemas.schemas import UserResponse, UserRegistration
from ..models.users import User
from ..functional.auth import verify_password, verify_token, hash_password, create_token

router = APIRouter(
    prefix="/api/auth",
    tags=["auth"]
)

@router.post("/reg", response_model=UserResponse, status_code=status.HTTP_200_OK)
def user_registration(user: UserRegistration, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Пользователь уже существует")
    
    db_user = User(
        username=user.username,
        full_name=user.full_name,
        password_hash=hash_password(user.password),
        birth_date=user.birth_date,
        address=user.address,
        gender=user.gender,
        hobby=user.hobby,
        vk_profile=user.vk_profile,
        blood_group=user.blood_type,
        blood_group=user.rh_factor
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user