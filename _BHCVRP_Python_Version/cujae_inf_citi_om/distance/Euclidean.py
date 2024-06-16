from cujae_inf_citi_om.distance import Distance
import math

# Clase que modela como calcular la distancia mediante la fórmula de Euclideana

class Euclidean(Distance):
    
    def __init__(self, axis_X_start, axis_Y_start, axis_X_end, axis_Y_end):
        super().__init__(axis_X_start, axis_Y_start, axis_X_end, axis_Y_end)
    
    def calculateDistance(self, axis_X_start, axis_Y_start, axis_X_end, axis_Y_end):
        distance = 0.0
        axis_X = 0.0
        axis_Y = 0.0
        
        axis_X = math.pow((axis_X_start - axis_X_end), 2)
        axis_Y = math.pow((axis_Y_start - axis_Y_end), 2) 
        distance = math.sqrt((axis_X + axis_Y))
        
        return distance