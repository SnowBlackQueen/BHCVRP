from heuristic.Heuristic import Heuristic
from solution.Solution import Solution
from data.ProblemType import ProblemType
from data.Problem import Problem
from data.DepotMDVRP import DepotMDVRP
from data.Customer import Customer
from solution.Route import Route
from random import Random
from data.CustomerType import CustomerType
from solution.RouteType import RouteType
from solution.RouteTTRP import RouteTTRP

class RandomMethod(Heuristic):
    
    def __init__(self):
        super().__init__()
        
    def initialize_specifics(self):
        self.customer = self._get_random_customer(self.customers_to_visit)
        self.request_route = self.customer.get_request_customer()
        self.route.get_list_id_customers().append(self.customer.get_id_customer())
        self.customers_to_visit.remove(self.customer)

    def get_solution_inicial(self):
        
        self.execute()
            
        return self.solution
    
    # Método que devuelve un cliente de la lista de forma aleatoria
    def _get_random_customer(self, list_customers):
        customer = Customer()
        random = Random()
        index = -1
        
        index = random.nextInt(len(list_customers))
        customer = list_customers[index]
        
        return customer