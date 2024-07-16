from data.CustomerType import CustomerType
from data.Customer import Customer

# Clase que modela los datos de un cliente en el TTRP

class CustomerTTRP(Customer):
    
    def __init__(self, type_customer=None, id_customer=None, request_customer=None, location_customer=None):
        super().__init__(id_customer, request_customer, location_customer)  
        self.type_customer = type_customer
        
    def __init__(self,type_customer=None, id_customer=None, request_customer=None, location_customer=None):
        super().__init__(id_customer, request_customer, location_customer)  
        self.type_customer = type_customer
        self._id_customer = id_customer
        self._request_customer = request_customer
        self._location_customer = location_customer

    def get_type_customer(self):
        return self.type_customer

    def set_type_customer(self, type_customer):
        self.type_customer = type_customer

    def set_type_customer_int(self, type_customer_int):
        if type_customer_int == CustomerType.VC.value:
            self.type_customer = CustomerType.VC
        elif type_customer_int == CustomerType.TC.value:
            self.type_customer = CustomerType.TC
        else:
            raise ValueError("Invalid customer type integer")