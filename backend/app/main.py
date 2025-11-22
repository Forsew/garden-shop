from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .database import init_db
from .routers import auth, products, brigades, harvest
import os

# ВАЖНО: Импортируем все модели для создания таблиц
from .models import users, brigades as brigades_model, collectors, products as products_model, harvest as harvest_model

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
app.include_router(products.router)
app.include_router(brigades.router)
app.include_router(harvest.router)

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/")
def root():
    return {"message": "GardenSpace API работает"}

@app.get("/health")
def health_check():
    return {"status": "ok"}