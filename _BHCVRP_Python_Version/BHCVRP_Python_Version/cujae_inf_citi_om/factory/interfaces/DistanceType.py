from enum import Enum

# Enumerado que indica los tipos de distancia

class DistanceType(Enum):
    Chebyshev = 0
    Euclidean = 1
    Haversine = 2
    Manhattan = 3
    Real = 4