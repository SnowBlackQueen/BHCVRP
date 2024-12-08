from data.Location import Location
from exceptions.BusStopCapacityException import BusStopCapacityException

# Clase que modela los datos de una parada en un SBRP

class BusStop:
    def __init__(
        self,
        id_bus_stop=None,
        capacity_bus_stop=None,
        location_bus_stop: Location = None,
        list_customers = None
    ):
        if (
            id_bus_stop is not None
            and capacity_bus_stop is not None
            and location_bus_stop is not None
            and list_customers is not None
        ):
            # Constructor con tres argumentos
            self._id_bus_stop = id_bus_stop
            self._capacity_bus_stop = capacity_bus_stop
            self._location_bus_stop = location_bus_stop
            self._list_customers = list_customers

        else:
            # Constructor sin argumentos (o con argumentos predeterminados)
            self._id_bus_stop = 0
            self._capacity_bus_stop = 0.0
            self._location_bus_stop = None  # O crea una nueva instancia de Location con valores predeterminados si es necesario
            self._list_customers = []

    def get_id_bus_stop(self):
        return self._id_bus_stop

    def set_id_bus_stop(self, id_bus_stop):
        self._id_bus_stop = id_bus_stop

    def get_capacity_bus_stop(self):
        return self._capacity_bus_stop

    def set_capacity_bus_stop(self, capacity_bus_stop):
        if capacity_bus_stop > 0:
            self._capacity_bus_stop = capacity_bus_stop
        else:
            raise BusStopCapacityException("La capacidad de la parada debe ser mayor que cero")

    def get_location_bus_stop(self):
        return self._location_bus_stop

    def set_location_bus_stop(self, location_bus_stop: Location):
        self._location_bus_stop = location_bus_stop

    def get_list_customers(self):
        return self._list_customers

    def set_list_customers(self, list_customers):
        self._list_customers = list_customers


