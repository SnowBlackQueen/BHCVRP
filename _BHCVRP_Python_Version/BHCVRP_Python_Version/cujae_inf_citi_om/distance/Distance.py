from abc import ABC, abstractmethod
# Clase que modela como calcular la distancia entre dos puntos

class Distance(ABC):
    
    @abstractmethod
    def calculate_distance(self, axis_X_start, axis_Y_start, axis_X_end, axis_Y_end):
        pass