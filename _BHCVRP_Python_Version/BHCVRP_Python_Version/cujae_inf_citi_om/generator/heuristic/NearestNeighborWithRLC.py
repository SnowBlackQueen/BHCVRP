from generator.heuristic.Heuristic import Heuristic
from data.ProblemType import ProblemType
from data.Problem import Problem
from data.Customer import Customer
from generator.solution.Route import Route
from data.CustomerType import CustomerType
from generator.solution.RouteTTRP import RouteTTRP
from generator.solution.RouteType import RouteType
from random import Random
from generator.solution.Solution import Solution
from exceptions.RLC_Exception import RLC_Exception

class NearestNeighborWithRLC(Heuristic):
    size_rlc = 3

    def __init__(self):
        super().__init__()

    def initialize_specifics(self):
        if NearestNeighborWithRLC.size_rlc == 0:
            NearestNeighborWithRLC.size_rlc = 1
        elif NearestNeighborWithRLC.size_rlc > (Problem.get_problem().get_list_customers / 2):
            raise RLC_Exception("La lista de candidatos restringidos debe ser menor que la mitad del total de clientes")    
        
        self.customer = self._get_NN_customer(self.customers_to_visit, self.id_depot)
        self.request_route = self.customer.get_request_customer()
        self.route.get_list_id_customers().append(self.customer.get_id_customer())
        self.customers_to_visit.remove(self.customer) 
    
    def get_solution_inicial(self):
        self.execute()

        return self.solution

    # Método que devuelve el cliente más cercano al cliente referencia
    def _get_NN_customer(self, list_customers, reference):
        customer = Customer()
        RLC = -1

        if len(list_customers) == 1:
            customer = list_customers[0]
        else:
            list_nn = self._get_list_NN(list_customers, reference)
            list_rlc = []

            RLC = min(NearestNeighborWithRLC.size_rlc, len(list_customers))

            for i in range(RLC):
                list_rlc.append(list_nn[i])

            random = Random()
            index = random.randint(0, RLC - 1)
            customer = list_rlc.pop(index)

        return customer

    # Método que devuelve la lista de vecinos más cercanos
    def _get_list_NN(self, list_customers, reference):
        list_distances = []
        list_nn = []
        ref_distance = 0.0

        for i in range(len(list_customers)):
            ref_distance = Problem.get_problem().get_cost_matrix().item(Problem.get_problem().getPosElement(reference), Problem.get_problem().getPosElement(list_customers[i].get_id_customer()))
            list_distances.append(ref_distance)
            list_nn.append(list_customers[i])

        self._ascendent_ordenate(list_distances, list_nn)

        return list_nn


