from pydantic_settings import BaseSettings
from typing import List
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    app_name: str = "Платформа учёта урожая"
    debug: bool = True
    database_url: str = os.getenv("DATABASE_URL")
    cors_origins: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ]
    static_dir: str = "static"
    images_dir: str = "static/images"

    class Config:
        env_file = ".env"

settings = Settings()