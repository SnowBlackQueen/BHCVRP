from data import Location
from exceptions.RequestException import RequestException

# Clase que modela los datos de un cliente en un VRP.

class Customer:
    
    def __init__(self, id_customer=None, request_customer=None, location_customer: Location = None):
        if id_customer is not None and request_customer is not None and location_customer is not None:
            # Constructor con tres argumentos
            self._id_customer = id_customer
            self._request_customer = request_customer
            self._location_customer = location_customer
        else:
            # Constructor sin argumentos (o con argumentos predeterminados)
            self.id_customer = 0
            self.request_customer = 0.0
            self.location_customer = None  # O crea una nueva instancia de Location con valores predeterminados si es necesario

    def __str__(self):
        return f"ID: {self.id_customer}, Request: {self.request_customer}, Location: {self.location_customer}"

    def get_id_customer(self):
        return self._id_customer

    def set_id_customer(self, id_customer):
        self._id_customer = id_customer

    def get_request_customer(self):
        return self._request_customer

    def set_request_customer(self, request_customer):
        if request_customer > 0:
            self._request_customer = request_customer
        else:
            raise RequestException("La demanda del cliente debe ser mayor que cero")

    def get_location_customer(self):
        return self._location_customer

    def set_location_customer(self, location_customer: Location):
        self._location_customer = location_customer