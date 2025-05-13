from pydantic_settings import BaseSettings

class Configuracion(BaseSettings):
    nombre_aplicacion : str = "API de la cafebrería El Péndulo"
    url_mongo : str
    nombre_base_datos : str = "pendulo_db"

    class Config:
        env_file = ".env"

# Se crea un objeto de configuración
configuracion = Configuracion()