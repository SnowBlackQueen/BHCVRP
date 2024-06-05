from _vrp_data import Depot

# Clase que modela los datos de un depósito en el MDVRP

class DepotMDVRP(Depot):
    
    def __init__(self, list_assigned_customers=None):
        super().__init__()
        self._list_assigned_customers = list_assigned_customers if list_assigned_customers is not None else []

    def get_list_assigned_customers(self):
        return self._list_assigned_customers

    def set_list_assigned_customers(self, list_assigned_customers):
        self._list_assigned_customers = list_assigned_customers