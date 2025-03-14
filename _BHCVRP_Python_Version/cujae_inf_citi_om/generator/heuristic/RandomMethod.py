from generator.heuristic.Heuristic import Heuristic
from data.ProblemType import ProblemType
from data.Problem import Problem
from data.DepotMDVRP import DepotMDVRP
from data.Customer import Customer
from data.BusStop import BusStop
from random import Random


class RandomMethod(Heuristic):

    def __init__(self):
        super().__init__()

    def initialize_specifics(self):
        if Problem.get_problem().get_type_problem() == ProblemType.SBRP:
            self.bus_stop = self._get_random_bus_stop(self.list_bus_stops)
            if not self.initialized:
                self.route.get_list_bus_stops().append(self.bus_stop.get_id_bus_stop())
                self.list_bus_stops.remove(self.bus_stop)
        else:
            if self.type_problem == ProblemType.VRPTW:
                current_node_id = self.customer.get_id_customer()
                self.feasible_customers = self.get_feasible_customers(current_node_id)
                if self.feasible_customers:
                    self.customer = self._get_random_customer(self.feasible_customers)

                    time_matrix = Problem.get_problem().get_time_matrix()
                    current_time = time_matrix[current_node_id, self.customer.get_id_customer()]
                    customer_ready_time = self.customer.get_time_window().get_initial_node()
                    customer_service_time = self.customer.get_time_window().get_service_time()
                    self.time_route = max(current_time, customer_ready_time) + customer_service_time
            else:
                self.customer = self._get_random_customer(self.customers_to_visit)
            if not self.initialized:
                if self.type_problem == ProblemType.VRPTW:
                    self.request_route = self.customer.get_request_customer()
                    self.route.get_list_id_customers().append(self.customer.get_id_customer())
                    self.customers_to_visit.remove(self.customer)


                else:
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

        index = random.randint(0, len(list_customers) - 1)
        customer = list_customers[index]
        # customer = list_customers[13]

        return customer

    def _get_random_bus_stop(self, list_bus_stops):
        bus_stop = BusStop()
        random = Random()
        index = -1

        index = random.randint(0, len(list_bus_stops) - 1)
        bus_stop = list_bus_stops[index]
        # customer = list_customers[13]

        return bus_stop

