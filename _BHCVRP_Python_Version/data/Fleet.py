# Clase que modela los datos de una flota en un VRP

class Fleet:
    
    def __init__(self, count_vehicles, capacity_vehicle):
        self._count_vehicles = count_vehicles
        self._capacity_vehicle = capacity_vehicle

    def get_count_vehicles(self):
        return self._count_vehicles

    def set_count_vehicles(self, count_vehicles):
        self._count_vehicles = count_vehicles

    def get_capacity_vehicle(self):
        return self._capacity_vehicle

    def set_capacity_vehicle(self, capacity_vehicle):
        self._capacity_vehicle = capacity_vehicle