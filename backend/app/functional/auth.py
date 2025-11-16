from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
import bcrypt
import jwt
import os

load_dotenv()
security = HTTPBearer()

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())

def create_token(user_id: int) -> str:
    return jwt.encode({"user_id": user_id}, os.SECRET_KEY, algorithm=os.ALGORITHM)

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, os.SECRET_KEY, algorithms=[os.ALGORITHM])
        return payload["user_id"]
    except:
        raise HTTPException(status_code=401, detail="Недействительный токен")