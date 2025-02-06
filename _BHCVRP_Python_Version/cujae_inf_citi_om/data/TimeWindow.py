from exceptions.ServiceTimeException import ServiceTimeException
from exceptions.TimeWindowException import TimeWindowException

# Clase que modela una ventana de tiempo para la variante VRPTW

class TimeWindow:
    def __init__(self, initial_node=None, end_node=None, service_time=None):
        if (
            initial_node is not None
            and end_node is not None
            and service_time is not None
        ):
            # Constructor con tres argumentos
            self._initial_node = initial_node
            self._end_node = end_node
            self._service_time = service_time

        else:
            # Constructor sin argumentos (o con argumentos predeterminados)
            self._initial_node = 0.0
            self._end_node = 0.0
            self._service_time = 0.0

    def get_initial_node(self):
        return self._initial_node

    def set_initial_node(self, initial_node):
        if initial_node >= 0:
            self._initial_node = initial_node
        else:
            raise TimeWindowException("La ventana de tiempo no puede ser negativa")

    def get_end_node(self):
        return self._end_node

    def set_end_node(self, end_node):
        if end_node >= 0:
            self._end_node = end_node
        else:
            raise TimeWindowException("La ventana de tiempo no puede ser negativa")

    def get_service_time(self):
        return self._service_time

    def set_service_time(self, service_time):
        if service_time >= 0:
            self._service_time = service_time
        else:
            raise ServiceTimeException("El tiempo de servicio no puede ser negativo")