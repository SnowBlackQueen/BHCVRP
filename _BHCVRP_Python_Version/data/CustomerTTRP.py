from data import CustomerType

# Clase que modela los datos de un cliente en el TTRP

class CustomerTTRP(Customer):
    
    def __init__(self, type_customer=None, id_customer=None, request_customer=None, location_customer=None):
        super().__init__(id_customer, request_customer, location_customer)
        self._type_customer = type_customer

    def get_type_customer(self):
        return self._type_customer

    def set_type_customer(self, typeCustomer):
        self._type_customer = typeCustomer

    def set_type_customer(self, type_customer):
        if type_customer == 0:
            self._type_customer = CustomerType.VC
        elif type_customer == 1:
            self._type_customer = CustomerType.TC