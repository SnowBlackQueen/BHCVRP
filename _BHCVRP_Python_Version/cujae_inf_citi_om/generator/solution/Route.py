import numpy as np
from data.Problem import Problem
from exceptions.RequestException import RequestException
from exceptions.CostException import CostException
from exceptions.DistanceNotAccessibleException import DistanceNotAccessibleException

class Route:
    
    def __init__(self, list_id_customers=None, request_route=None, cost_route=None, id_depot=None, list_access_vc=None, maximum_distance=None):
        if list_id_customers is not None and request_route is not None and cost_route is not None and id_depot is not None:
            self.list_id_customers = list(list_id_customers)
            self.request_route = request_route
            self.cost_route = 0.0
            self.id_depot = id_depot
            self.list_access_vc = []
            self.maximum_distance = maximum_distance
        else:
            self.list_id_customers = []
            self.request_route = 0.0
            self.cost_route = 0.0
            self.id_depot = -1
            self.maximum_distance = 0.0

    def get_list_id_customers(self):
        return self.list_id_customers

    def set_list_id_customers(self, list_id_customers):
        self.list_id_customers = list_id_customers

    def get_request_route(self):
        return self.request_route

    def set_request_route(self, request_route):
        if request_route > 0:
            self.request_route = request_route
        else:
            raise RequestException("La demanda de la ruta debe ser mayor que cero")

    def get_cost_route(self):
        return self.cost_route

    def set_cost_route(self, cost_route):
        if cost_route > 0:
            self.cost_route = cost_route
        else:
            raise CostException("El costo de la ruta debe ser mayor que cero")

    def get_id_depot(self):
        return self.id_depot

    def set_id_depot(self, id_depot):
        self.id_depot = id_depot
        
    def get_maximum_distance(self):
        return self.maximum_distance
    
    def set_maximum_distance(self, maximum_distance):
        if maximum_distance > 0 & maximum_distance < 99999:
            self.maximum_distance = maximum_distance
        else:
            raise DistanceNotAccessibleException("La distancia no es accesible")

    def get_cost_single_route(self):
        cost_route = 0.0
        customer_ini = self.list_id_customers[0]
        pos_customer_ini = Problem.get_problem().get_pos_element(customer_ini)

        cost_matrix = Problem.get_problem().get_cost_matrix()

        # Obtener los índices de self.id_depot y pos_customer_ini
        depot_index = Problem.get_problem().get_pos_element(self.id_depot)
        customer_ini_index = Problem.get_problem().get_pos_element(pos_customer_ini)

        # Calcular el costo y sumarlo a cost_route
        cost_route += cost_matrix[depot_index][customer_ini_index]
        
        for i in range(1, len(self.list_id_customers)):
            customer_next = self.list_id_customers[i]
            pos_customer_next = Problem.get_problem().get_pos_element(customer_next)
            cost_route += Problem.get_problem().get_cost_matrix().item(pos_customer_ini, pos_customer_next)
            customer_ini = customer_next
            pos_customer_ini = pos_customer_next

        cost_route += cost_matrix[pos_customer_ini][depot_index]
        
        self.set_cost_route(cost_route)
        return cost_route

