import math

# Clase que modela la ubicación geográfica de un cliente VRP o depósito a partir de sus coordenadas cartesianas

class Location:
    
    def __init__(self, axis_X, axis_Y):
        self._axis_X = axis_X
        self._axis_Y = axis_Y

    def get_axisX(self):
        return self._axis_X

    def set_axisX(self, axis_X):
        self._axis_X = axis_X

    def get_axisY(self):
        return self._axis_Y

    def set_axisY(self, axis_Y):
        self._axis_Y = axis_Y

    # Método que devuelve para un punto su coordenada polar Theta 
    def get_polar_theta(self):
        return math.atan(self._axis_Y / self._axis_X)

    # Método que devuelve para un punto su coordenada Rho
    def get_polar_rho(self):
        return math.sqrt(self._axis_X ** 2 + self._axis_Y ** 2)