from typing import List
import numpy as np

# Clase que modela los datos de un problema VRP.

class Problem:
    
    def __init__(self):
        self._list_customers: List[Customer] = []
        self._list_depots: List[Depot] = []
        self._type_problem: ProblemType = None
        # self._cost_matrix: NumericMatrix = NumericMatrix()
        self._list_capacities: List[float] = None

    @staticmethod
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
            
    # def getCostMatrix(self):
      #  return self.cost_matrix.getCostMatrix()

    # def setCostMatrix(self, cost_matrix):
      #  self.cost_matrix.setCostMatrix(cost_matrix)

    def get_list_capacities(self):
        return self._list_capacities

    def set_list_capacities(self, list_capacities):
        self._list_capacities = list_capacities

    def get_list_id_customers(self):
        return [customer.id_customer for customer in self.list_customers]

    def get_total_request(self):
        return sum(customer.request_customer for customer in self.list_customers)

    def get_customer_by_id_customer(self, id_customer):
        for customer in self.list_customers:
            if customer.id_customer == id_customer:
                return customer
        return None

    def get_type_by_id_customer(self, id_customer):
        for customer in self.list_customers:
            if isinstance(customer, CustomerTTRP) and customer.id_customer == id_customer:
                return customer.getTypeCustomer()
        return None
