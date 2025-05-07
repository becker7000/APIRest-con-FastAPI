from typing import List
from .models import Producto

# Esta lista actúa como nuestra "base de datos en memoria"
# Aquí se almacenan los productos agregados durante la ejecución.
menu: List[Producto] = []

"""
    Esta lista no genera una BD real solo se guarda 
    en memoria mientras la app está en ejecución, la lista
    se borrará después de que se termine la ejecución cuando el servidor se reinicia.
"""