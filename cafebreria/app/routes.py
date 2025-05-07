from fastapi import APIRouter
from typing import List
from .models import Producto
from .services import ProductoService

# Creamos un router que contendrá los endpoints relacionados al menú
router = APIRouter()

# Instanciamos la clase de servicio que manejará la lógica del producto
servicio = ProductoService()

@router.get("/", tags=["Inicio"])
def inicio():
    # Endpoint raíz para verificar que la API esté corriendo
    return {"mensaje": "Bienvenido a la API de la Cafetería"}

@router.get("/menu", response_model=List[Producto], tags=["Menú"])
def obtener_menu():
    # Devuelve todos los productos del menú
    return servicio.listar_productos()

@router.post("/menu", response_model=Producto, tags=["Menú"])
def agregar_producto(producto: Producto):
    # Agrega un nuevo producto al menú
    return servicio.agregar_producto(producto)

@router.get("/menu/{producto_id}", response_model=Producto, tags=["Menú"])
def obtener_producto(producto_id: int):
    # Devuelve un producto específico por ID
    return servicio.obtener_producto(producto_id)

@router.delete("/menu/{producto_id}", tags=["Menú"])
def eliminar_producto(producto_id: int):
    # Elimina un producto por su ID
    return servicio.eliminar_producto(producto_id)
