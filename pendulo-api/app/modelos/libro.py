# Importa BaseModel y Field desde Pydantic para definir esquemas de validación de datos
from pydantic import BaseModel, Field

# Importa Optional para indicar que algunos campos pueden ser opcionales
from typing import Optional

# Importa el tipo date para representar fechas
from datetime import date

# Clase base que define los campos comunes para un libro
class LibroBase(BaseModel):
    titulo: str                      # Título del libro (requerido)
    autor: str                       # Autor del libro (requerido)
    genero: str                      # Género o categoría (requerido)
    editorial: str                   # Editorial del libro (requerido)
    fecha_publicacion: Optional[date]  # Fecha de publicación (opcional)
    descripcion: Optional[str]         # Breve descripción del libro (opcional)
    stock: int                        # Cantidad disponible en inventario (requerido)
    disponible: bool = True           # Indica si está disponible (por defecto: True)

# Modelo usado al crear un nuevo libro (iguala a LibroBase, sin cambios adicionales)
class LibroCrear(LibroBase):
    pass

# Modelo para actualizar parcialmente un libro (todos los campos son opcionales)
class LibroActualizar(BaseModel):
    titulo: Optional[str]
    autor: Optional[str]
    genero: Optional[str]
    editorial: Optional[str]
    fecha_publicacion: Optional[date]
    descripcion: Optional[str]
    stock: Optional[int]
    disponible: Optional[bool]

# Modelo para representar un libro obtenido desde la base de datos
# Incluye todos los campos de LibroBase más el campo `id` como string
class LibroEnDB(LibroBase):
    id: str  # Este campo representa el `_id` de MongoDB convertido a string
