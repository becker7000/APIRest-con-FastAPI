from fastapi import FastAPI
from app.rutas import libros

app = FastAPI(title="API Cafebrería El Péndulo")

app.include_router(libros.router)
