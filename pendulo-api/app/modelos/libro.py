from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class LibroBase(BaseModel):
    titulo : str
    autor : str
    genero : str
    editorial : str
    fecha_publicacion : Optional[date]
    descripcion : Optional[str]
    stock : int
    disponible : bool = True

class LibroCrear(LibroBase):
    pass

class LibroActualizar(BaseModel):
    titulo : Optional[str]
    autor : Optional[str]
    genero : Optional[str]
    editorial : Optional[str]
    fecha_publicacion : Optional[date]
    descripcion : Optional[str]
    stock : Optional[int]
    disponible : Optional[bool]

class LibroEnDB(LibroBase):
    id : str # Es el ObjectId de mongo pero en string

# Esto te permite validar las query params de manera tipada y ordenada:
# Pydantic se usa en FastAPI para validar, transformar y documentar datos de entrada
# (como query params, body, headers, etc.).
class FiltroLibro(BaseModel):
    autor: Optional[str] = None
    genero: Optional[str] = None
    editorial: Optional[str] = None
    disponible: Optional[bool] = None
    stock_min: Optional[int] = None
    stock_max: Optional[int] = None
