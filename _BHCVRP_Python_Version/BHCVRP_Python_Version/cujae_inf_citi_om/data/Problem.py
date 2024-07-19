from typing import List
import numpy as np
from data.Customer import Customer
from data.CustomerTTRP import CustomerTTRP
from data.Depot import Depot
from data.ProblemType import ProblemType
from exceptions.RequestException import RequestException
from exceptions.WithoutCapacityException import WithoutCapacityException

# Clase que modela los datos de un problema VRP.

class Problem:
    
    def __init__(self):
        self._list_customers: List[Customer] = []
        self._list_depots: List[Depot] = []
        self._type_problem: ProblemType = None
        self.set_cost_matrix(cost_matrix=None)
        self._list_capacities: List[float] = None

    @staticmethod # Método que implementa el Patrón Singleton
    def get_problem():
        if not hasattr(Problem, 'problem') or Problem.problem is None:
            Problem.problem = Problem()
        return Problem.problem

    def set_list_customers(self, list_customers: List[Customer]):
        self._list_customers = list_customers

    def get_list_customers(self) -> List[Customer]:
        return self._list_customers

    def set_list_depots(self, list_depots: List[Depot]):
        self._list_depots = list_depots

    def get_list_depots(self) -> List[Depot]:
        return self._list_depots

    def get_type_problem(self):
        return self._type_problem
    
    def set_type_problem(self, type_problem: ProblemType):
        self._type_problem = type_problem

    def set_type_problem_from_int(self, type_problem: int):
        if type_problem == 0:
            self._type_problem = ProblemType.CVRP
        elif type_problem == 1:
            self._type_problem = ProblemType.HFVRP
        elif type_problem == 2:
            self._type_problem = ProblemType.MDVRP
        elif type_problem == 3:
            self._type_problem = ProblemType.OVRP
        elif type_problem == 4:
            self._type_problem = ProblemType.TTRP
            
    def get_cost_matrix(self):
        return self._cost_matrix

    def set_cost_matrix(self, cost_matrix):
        self._cost_matrix = cost_matrix

    def get_list_capacities(self):
        return self._list_capacities

    def set_list_capacities(self, list_capacities):
        self._list_capacities = list_capacities

    # Método para obtener la lista de id de los clientes
    def get_list_id_customers(self):
        return [customer.id_customer for customer in self._list_customers]

    # Método que devuelve la demanda total
    def get_total_request(self):
        total_request = 0.0
        for customer in self._list_customers:
            total_request += customer.get_request_customer() 
        if total_request > 0:
            return total_request
        else:
            raise RequestException("La demanda total debe ser mayor que cero") 

    # Método que busca un cliente dado su identificador
    def get_customer_by_id_customer(self, id_customer):
        for customer in self._list_customers:
            if customer.get_id_customer() == id_customer:
                return customer
        return None

    # Método que devuelve el tipo de un cliente dado su identificador
    def get_type_by_id_customer(self, id_customer):
        for customer in self._list_customers:
            if isinstance(customer, CustomerTTRP) and customer._id_customer == id_customer:
                return customer.get_type_customer()
        return None

    # Método que devuelve la demanda de un cliente dado su identificador
    def get_request_by_id_customer(self, id_customer):
        request_customer = 0.0
        i = 0
        found = False
        count_customers = len(self._list_customers)
        
        while i < count_customers and not found:
            if self._list_customers[i].get_id_customer() == id_customer:
                request_customer = self._list_customers[i].get_request_customer()
                found = True
            else:
                i += 1
        if request_customer > 0:
            return request_customer
        else:
            raise RequestException("La demanda del cliente debe ser mayor que cero")

    def get_list_request_customers(self, list_customers):
        return [customer.get_request_customer() for customer in list_customers]

    def get_list_count_vehicles(self, list_depots):
        return [depot.get_list_fleets()[0].get_count_vehicles() for depot in list_depots]

    def get_list_capacity_vehicles(self, list_depots):
        return [depot.get_list_fleets()[0].get_capacity_vehicle() for depot in list_depots]
    
    # Método que dado un id (deposito o cliente) devuelve la posicion
    def get_pos_element(self, id_element):
        i = 0
        found = False
        pos_element = -1
        count_customers = len(self._list_customers)
        count_depots = len(self._list_depots)
        
        while i < count_depots and not found:
            if self._list_depots[i].get_id_depot() == id_element:
                pos_element = i + count_customers
                found = True
            else:
                i += 1
        
        i = 0
        while i < count_customers and not found:
            if self._list_customers[i].get_id_customer() == id_element:
                pos_element = i
                found = True
            else:
                i += 1
        
        return pos_element

    # Método que dado el id del deposito y del cliente devuelve la posicion
    def get_pos_element_by_id_depot(self, id_depot, id_customer, list_depots):
        found = False
        pos_element = -1
        i = 0
        count_depots = len(list_depots)
        
        while i < count_depots and not found:
            if list_depots[i].get_id_depot() == id_depot:
                j = 0
                count_assigned_customers = len(list_depots[i].get_list_assigned_customers())
                while j < count_assigned_customers and not found:
                    if list_depots[i].get_list_assigned_customers()[j] == id_customer:
                        pos_element = j
                        found = True
                    else:
                        j += 1
            else:
                i += 1
        
        return pos_element
    
    # Método que devuelve el id del depósito correspondiente a un cliente dado
    def get_id_depot_by_id_customer(self, id_customer):
        found = False
        id_depot = -1
        count_depots = len(self._list_depots)
        i = 0
        
        while i < count_depots and not found:
            j = 0
            count_assigned_customers = len(self._list_depots[i].get_list_assigned_customers())
            
            while j < count_assigned_customers and not found:
                if self._list_depots[i].get_list_assigned_customers()[j] == id_customer:
                    id_depot = self._list_depots[i].get_id_depot()
                    found = True
                else:
                    j += 1
            i += 1
        
        return id_depot

    # Método que devuelve la demanda de un depósito dado
    def current_request_by_depot(self, pos_depot, list_customers, list_depots):
        current_request = 0.0
        id_customer = -1
        count_customers = len(list_customers)
        count_assigned_customers = len(list_depots[pos_depot].get_list_assigned_customers())

        for i in range(count_assigned_customers):
            j = 0
            found = False
            id_customer = list_depots[pos_depot].get_list_assigned_customers()[i]
        
            while j < count_customers and not found:
                if id_customer == list_customers[j].get_id_customer():
                    current_request += list_customers[j].get_request_customer()
                    found = True
                j += 1
        if current_request > 0:
            return current_request
        else:
            raise RequestException("La demanda actual del depósito debe ser mayor que cero")
    
    # Método que devuelve la capacidad total de los vehículos de MDVRP
    def get_total_capacity(self):
        total_capacity = 0.0
        count_depots = len(self._list_depots)
        
        for i in range(count_depots):
            count_fleets = len(self._list_depots[i].get_list_fleets())
            
            for j in range(count_fleets):
                fleet = self._list_depots[i].get_list_fleets()[j]
                capacity_vehicle = fleet.get_capacity_vehicle()
                count_vehicles = int(fleet.get_count_vehicles())
                total_capacity += capacity_vehicle * count_vehicles
                
                if self._type_problem == ProblemType.TTRP or self._type_problem == 4:
                    capacity_trailer = fleet.get_capacity_trailer() 
                    count_trailers = fleet.get_count_trailers()
                    total_capacity += capacity_trailer * count_trailers
        
        if total_capacity > 0:
            return total_capacity
        else:
            raise WithoutCapacityException("La capacidad total de los vehículos de MDVRP debe ser mayor que cero")
    
    # Método que dice si hay o no capacidad disponible en los depósitos
    def exist_capacity_in_some_depot(self, list_depots):
        exist = False
        current_request = 0.0
        total_capacity = self.get_total_capacity(list_depots)
        count_depots = len(list_depots)
        
        for i in range(count_depots):
            current_request += self.current_request_by_depot(i, list_depots)
        
        if current_request == total_capacity:
            exist = True
        
        return exist
    
    # Método que dado el depósito devuelve la lista de clientes asignados
    def get_customers_assigned_by_id_depot(self, id_depot, list_customers, list_depots):
        list_customers_assigned = []
        count_customers = len(list_customers)
        pos_depot = self.get_pos_element(id_depot, list_customers, list_depots) - count_customers
        count_assigned_customers = len(list_depots[pos_depot].get_list_assigned_customers())

        for i in range(count_assigned_customers):
            j = 0
            found = False

            while j < count_customers and not found:
                if list_depots[pos_depot].get_list_assigned_customers()[i] == list_customers[j].get_id_customer():
                    list_customers_assigned.append(list_customers[j])
                    found = True
                else:
                    j += 1
        
        return list_customers_assigned

    # Método que llena la lista de capacidades de la flota de vehículos en HFVRP
    def fill_list_capacities(self, pos_depot):
        list_capacities = []

        for i in range(len(self._list_depots[pos_depot].get_list_fleets())):
            for j in range(int(self._list_depots[pos_depot].get_list_fleets()[i].get_count_vehicles())):
                list_capacities.append(self._list_depots[pos_depot].get_list_fleets()[i].get_capacity_vehicle())
        
        return list_capacities

    # Método que llena la lista de capacidades de la flota de vehículos en HFVRP
    def fill_list_capacities_test(self, list_depots):
        list_capacities = []

        for i in range(len(list_depots[0].get_list_fleets())):
            for j in range(list_depots[0].get_list_fleets()[i].get_count_vehicles()):
                list_capacities.append(list_depots[0].get_list_fleets()[i].get_capacity_vehicle())
        
        return list_capacities
    
    # Método para obtener la lista de los id de los depositos
    def get_list_id_depots(self, list_depots):
        count_depots = len(list_depots)
        list_id_depots = [depot.get_id_depot() for depot in list_depots]
        return list_id_depots

    # Método que determina si existen clientes que puedan ser asignado al depósito
    def is_full_depot(self, list_customers, pos_depot, list_depots):
        is_full = False
        capacity_total = (list_depots[pos_depot].get_list_fleets()[0].get_capacity_vehicle() * list_depots[pos_depot].get_list_fleets()[0].get_count_vehicles())
        request_depot = self.current_request_by_depot(pos_depot, list_customers, list_depots)
        ideal_request = capacity_total - request_depot

        if ideal_request != 0:
            i = 0
            while i < len(list_customers) and not is_full:
                if list_customers[i].get_request_customer() <= ideal_request:
                    is_full = True
                else:
                    i += 1
        
        return is_full