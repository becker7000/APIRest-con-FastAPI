from fastapi import FastAPI
from app.rutas import libros

app = FastAPI(title="API de la cafebrería El Péndulo")

app.include_router(libros.router)

"""
    1. libro.py
    2. .env
    3. config.py
    4. mongo.py
    5. servicio_libro.py
    6. libros.py
    7. main.py
"""