from pydantic_settings import BaseSettings

class Configuracion(BaseSettings):
    nombre_aplicacion: str = "API Cafebrería El Péndulo"
    url_mongo: str
    nombre_base_datos: str = "pendulo_db"

    class Config:
        env_file = ".env"

configuracion = Configuracion()
