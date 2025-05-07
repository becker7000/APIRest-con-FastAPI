from pydantic import BaseModel

# Modelo que representa un producto en la cafetería.
# Usamos Pydantic para validar los datos automáticamente.
class Producto(BaseModel):
    id: int                    # ID único del producto
    nombre: str                # Nombre del producto
    descripcion: str           # Breve descripción
    precio: float              # Precio del producto
    disponible: bool = True    # Estado de disponibilidad (por defecto: disponible)
