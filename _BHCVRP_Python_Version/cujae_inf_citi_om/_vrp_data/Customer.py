from _vrp_data import Location

# Clase que modela los datos de un cliente en un VRP.

class Customer:
    
    def __init__(self, id_customer, request_customer, location_customer: Location):
        self._id_customer = id_customer
        self._request_customer = request_customer
        self._location_customer = location_customer

    def get_id_customer(self):
        return self._id_customer

    def set_id_customer(self, id_customer):
        self._id_customer = id_customer

    def get_request_customer(self):
        return self._request_customer

    def set_request_customer(self, request_customer):
        self._request_customer = request_customer

    def get_location_customer(self):
        return self._location_customer

    def set_location_customer(self, location_customer: Location):
        self._location_customer = location_customer