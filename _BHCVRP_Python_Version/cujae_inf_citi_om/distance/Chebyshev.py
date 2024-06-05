from cujae_inf_citi_om import Distance
import math

# Clase que modela como calcular la distancia mediante la fórmula de Chebyshev

class Chebyshev(Distance):
    
    def __init__(self, axis_X_start, axis_Y_start, axis_X_end, axis_Y_end):
        super().__init__(axis_X_start, axis_Y_start, axis_X_end, axis_Y_end)
    
    def calculateDistance(self, axis_X_start, axis_Y_start, axis_X_end, axis_Y_end):
        distance = 0.0
        axis_X = 0.0
        axis_Y = 0.0
        
        axis_X = math.abs(axis_X_start - axis_X_end)
        axis_Y = math.abs(axis_Y_start - axis_Y_end)
        distance = math.max(axis_X, axis_Y)
        
        return distance