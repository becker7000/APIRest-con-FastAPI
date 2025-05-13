from fastapi import APIRouter, HTTPException
from app.modelos.libro import LibroCrear, LibroActualizar
from app.servicios import servicio_libro
from app.modelos.libro import FiltroLibro # Nuevo import para el filtro
from fastapi import Query
from typing import Optional

router = APIRouter(prefix="/libros",tags=["Libros"])

""" # Método anterior de listar libros
@router.get("/")
async def listar_libros():
    return await servicio_libro.listar_libros()
"""
# Nuevo mé_todo listar_libros()
# Ruteo para filtro por autor, genero, editorial, disponibilidad y rangos de stock:
@router.get("/")
async def listar_libros(
    autor: Optional[str] = Query(None),
    genero: Optional[str] = Query(None),
    editorial: Optional[str] = Query(None),
    disponible: Optional[bool] = Query(None),
    stock_min: Optional[int] = Query(None, ge=0), # ge = mayor o igual que
    stock_max: Optional[int] = Query(None, ge=0)
):
    filtros = {
        "autor": autor,
        "genero": genero,
        "editorial": editorial,
        "disponible": disponible,
        "stock_min": stock_min,
        "stock_max": stock_max,
    }
    return await servicio_libro.filtrar_libros(filtros)
"""
Te ahorra validaciones manuales.
Evita errores lógicos (como buscar libros con stock mínimo negativo, lo cual no tiene sentido).
Mejora la documentación Swagger mostrando los límites aceptables.
"""

@router.post("/")
async def crear_libro(libro : LibroCrear):
    libro_id = await servicio_libro.crear_libro(libro.dict())
    return {"mensaje":"Libro creado correctamente", "id":libro_id}

@router.get("/{libro_id}")
async def obtener_libro(libro_id : str):
    libro = await servicio_libro.obtener_libro_por_id(libro_id)
    if not libro:
        raise HTTPException(status_code=404,detail="Libro no encontrado")
    return libro

@router.put("/{libro_id}")
async def actualizar_libro(libro_id : str, libro : LibroActualizar):
    await servicio_libro.actualizar_libro(libro_id,libro.dict(exclude_unset=True))
    return {"mensaje":"Libro actualizado correctamente"}

@router.delete("/{libro_id}")
async def eliminar_libro(libro_id: str):
    await servicio_libro.eliminar_libro(libro_id)
    return {"mensaje": "Libro eliminado"}

"""
Probar de esta forma: (hacer combinaciones de estas formas)
GET /libros?autor=Gabriel García Márquez
GET /libros?genero=Ficción&editorial=Sudamericana
GET /libros?disponible=true
GET /libros?stock_min=5&stock_max=20
GET /libros?autor=Borges&disponible=true&stock_min=1

"""

