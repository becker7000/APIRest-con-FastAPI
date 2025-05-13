from app.database.mongo import db
from bson import ObjectId
from datetime import datetime, date
from fastapi import HTTPException

# Función para crear un libro
async def crear_libro(datos : dict):
    datos = convertir_fecha(datos)
    resultado = await db["libros"].insert_one(datos)
    return str(resultado.inserted_id)

async def listar_libros():
    libros = await db["libros"].find().to_list(100)
    libros = [convertir_objectid_a_str(libro) for libro in libros]
    return libros

async def obtener_libro_por_id(libro_id : str):
    if not ObjectId.is_valid(libro_id):
        raise HTTPException(status_code=400,detail="Id no encontrado o no válido")
    libro = await db["libros"].find_one({"_id": ObjectId(libro_id)})
    if libro:
        return convertir_objectid_a_str(libro)
    else:
        return None

async def actualizar_libro(libro_id : str, datos_actualizados : dict):
    if not ObjectId.is_valid(libro_id):
        raise HTTPException(status_code=400,detail="ID no válido")
    datos_actualizados = convertir_fecha(datos_actualizados)
    resultado = await db["libros"].update_one(
        {"_id":ObjectId(libro_id)},
        {"$set":datos_actualizados}
    )
    if resultado.matched_count == 0:
        raise HTTPException(status_code=404,detail="Libro no encontrado")

async def eliminar_libro(libro_id: str):
    if not ObjectId.is_valid(libro_id):
        raise HTTPException(status_code=400, detail="ID no válido")
    resultado = await db["libros"].delete_one({"_id": ObjectId(libro_id)})
    if resultado.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

# Función axiliar:
def convertir_fecha(libro : dict):
    if "fecha_publicacion" in libro and isinstance(libro["fecha_publicacion"],date):
        libro["fecha_publicacion"] = datetime.combine(libro["fecha_publicacion"],datetime.min.time())
    return libro

def convertir_objectid_a_str(libro):
    if "_id" in libro and isinstance(libro["_id"],ObjectId):
        libro["_id"] = str(libro["_id"])
    return libro

# Filtro para libros (autor, genero, editorial,disponibilidad, rangos de stock)
# Hacer primero una prueba desde Compass con los filtros
async def filtrar_libros(filtros: dict):
    consulta = {}

    if filtros.get("autor"):
        consulta["autor"] = filtros["autor"]
    if filtros.get("genero"):
        consulta["genero"] = filtros["genero"]
    if filtros.get("editorial"):
        consulta["editorial"] = filtros["editorial"]
    if filtros.get("disponible") is not None:
        consulta["disponible"] = filtros["disponible"]

    stock_filtro = {}
    if filtros.get("stock_min") is not None:
        stock_filtro["$gte"] = filtros["stock_min"]
    if filtros.get("stock_max") is not None:
        stock_filtro["$lte"] = filtros["stock_max"]
    if stock_filtro:
        consulta["stock"] = stock_filtro

    libros = await db["libros"].find(consulta).to_list(100)
    return [convertir_objectid_a_str(libro) for libro in libros]
