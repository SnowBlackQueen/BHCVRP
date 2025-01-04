from enum import Enum

# Enumerado que modela los tipos de forma de seleccionar el primer cliente de la ruta


class FirstElementType(Enum):
    Furthest = 0
    Nearest = 1
    Random = 2
