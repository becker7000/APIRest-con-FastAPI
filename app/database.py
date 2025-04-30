from typing import List
from .models import Producto

# Esta lista actúa como nuestra "base de datos en memoria"
# Aquí se almacenan los productos agregados durante la ejecución.
menu: List[Producto] = []
