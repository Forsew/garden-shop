from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .database import init_db
from .routers import auth
import os

app = FastAPI(title=settings.app_name, debug=settings.debug)

# CORS - ВАЖНО: должен быть ДО всех роутеров!
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешаем все источники
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Роутеры API
app.include_router(auth.router)

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/")
def root():
    return {"message": "GardenSpace API работает"}

@app.get("/health")
def health_check():
    return {"status": "ok"}