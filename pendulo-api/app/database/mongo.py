from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import configuracion

cliente_mongo = AsyncIOMotorClient(configuracion.url_mongo)
db = cliente_mongo[configuracion.nombre_base_datos]
