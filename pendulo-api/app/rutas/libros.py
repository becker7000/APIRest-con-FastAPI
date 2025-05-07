from fastapi import APIRouter, HTTPException
from app.modelos.libro import LibroCrear, LibroActualizar
from app.servicios import servicio_libro

router = APIRouter(prefix="/libros", tags=["Libros"])

@router.get("/")
async def listar_libros():
    return await servicio_libro.listar_libros()

@router.post("/")
async def crear_libro(libro: LibroCrear):
    libro_id = await servicio_libro.crear_libro(libro.dict())
    return {"mensaje": "Libro creado", "id": libro_id}

@router.get("/{libro_id}")
async def obtener_libro(libro_id: str):
    libro = await servicio_libro.obtener_libro_por_id(libro_id)
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return libro

@router.put("/{libro_id}")
async def actualizar_libro(libro_id: str, libro: LibroActualizar):
    await servicio_libro.actualizar_libro(libro_id, libro.dict(exclude_unset=True))
    return {"mensaje": "Libro actualizado"}

@router.delete("/{libro_id}")
async def eliminar_libro(libro_id: str):
    await servicio_libro.eliminar_libro(libro_id)
    return {"mensaje": "Libro eliminado"}
