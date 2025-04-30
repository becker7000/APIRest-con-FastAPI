from fastapi import FastAPI

# Es el endpoint principal para nuestra API
# Enpoint es un punto de accesso
#app = FastAPI()
"""
@app.get("/") #ruta de acceso
async def root():
    return {"saludo":"Hola a todos usando FastAPI"}
"""
from fastapi import FastAPI
from .routes import router

# Creamos una instancia de FastAPI que actuará como el servidor principal
app = FastAPI(
    title="API de Cafetería",
    description="Un ejemplo básico de API usando FastAPI y programación orientada a objetos.",
    version="1.0"
)

# Registramos el router con todos los endpoints definidos en routes.py
app.include_router(router)



