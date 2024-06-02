from data import Location

# Clase que modela los datos de un depósito en un VRP

class Depot:
    
    def __init__(self, id_depot, location_depot: Location, list_fleets=None):
        self._id_depot = id_depot
        self._location_depot = location_depot
        self._list_fleets = list_fleets if list_fleets is not None else []

    def get_id_depot(self):
        return self._id_depot

    def set_id_depot(self, id_depot):
        self._id_depot = id_depot
        
    def get_list_fleets(self):
        return self._list_fleets

    def set_list_fleets(self, list_fleets):
        self._list_fleets = list_fleets

    def get_location_depot(self):
        return self._location_depot

    def set_location_depot(self, location_depot: Location):
        self._location_depot = location_depot

    