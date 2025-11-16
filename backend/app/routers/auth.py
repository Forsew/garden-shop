from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from ..database import get_db
from ..schemas.schemas import UserResponse, UserRegistration, UserLogin
from ..models.users import User
from ..functional.auth import verify_password, verify_token, hash_password, create_token

router = APIRouter(
    prefix="/api/auth",
    tags=["auth"]
)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: dict

@router.post("/reg", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def user_registration(user: UserRegistration, db: Session = Depends(get_db)):
    """Регистрация нового пользователя"""
    
    # Проверка существования пользователя
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Пользователь с таким username уже существует")
    
    if user.vk_profile and db.query(User).filter(User.vk_profile == user.vk_profile).first():
        raise HTTPException(status_code=400, detail="Этот VK профиль уже привязан к другому аккаунту")
    
    # Создание нового пользователя
    db_user = User(
        username=user.username,
        full_name=user.full_name,
        password_hash=hash_password(user.password),
        birth_date=user.birth_date,
        address=user.address,
        gender=user.gender,
        hobby=user.hobby,
        vk_profile=user.vk_profile,
        blood_group=user.blood_group,
        rh_factor=user.rh_factor
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Создание токена
    token = create_token(db_user.id)
    
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user={
            "id": db_user.id,
            "username": db_user.username,
            "full_name": db_user.full_name
        }
    )

@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
def user_login(user: UserLogin, db: Session = Depends(get_db)):
    """Авторизация пользователя"""
    
    db_user = db.query(User).filter(User.username == user.username).first()
    
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный username или пароль"
        )
    
    token = create_token(db_user.id)
    
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user={
            "id": db_user.id,
            "username": db_user.username,
            "full_name": db_user.full_name
        }
    )

@router.get("/profile", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_user_profile(user_id: int = Depends(verify_token), db: Session = Depends(get_db)):
    """Получение профиля пользователя"""
    
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    return user