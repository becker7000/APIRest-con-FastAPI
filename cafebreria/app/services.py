from fastapi import HTTPException
from typing import List
from .models import Producto
from .database import menu


# Clase que contiene la lógica principal de negocio para productos.
# Esto sigue el principio de "separación de responsabilidades".
class ProductoService:

    def listar_productos(self) -> List[Producto]:
        # Devuelve la lista completa de productos
        return menu

    def agregar_producto(self, producto: Producto) -> Producto:
        # Evita duplicados verificando si ya existe un producto con el mismo ID
        if any(p.id == producto.id for p in menu):
            raise HTTPException(status_code=400, detail="El ID ya existe.")

        # Agrega el producto a la "base de datos"
        menu.append(producto)
        return producto

    def obtener_producto(self, producto_id: int) -> Producto:
        # Busca un producto por su ID y lo devuelve si existe
        for producto in menu:
            if producto.id == producto_id:
                return producto
        # Si no se encuentra, se lanza un error 404
        raise HTTPException(status_code=404, detail="Producto no encontrado.")

    def eliminar_producto(self, producto_id: int) -> dict:
        # Busca un producto por su ID y lo elimina si existe
        for producto in menu:
            if producto.id == producto_id:
                menu.remove(producto)
                return {"mensaje": f"Producto {producto_id} eliminado correctamente."}
        # Si no se encuentra, se lanza un error 404
        raise HTTPException(status_code=404, detail="Producto no encontrado.")
