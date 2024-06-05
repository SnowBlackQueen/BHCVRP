from enum import Enum

# Enumerado que modela los tipos de forma de seleccionar el primer cliente de la ruta

class FirstCustomerType(Enum):
    FurthestCustomer = 0
    NearestCustomer = 1
    RandomCustomer = 2