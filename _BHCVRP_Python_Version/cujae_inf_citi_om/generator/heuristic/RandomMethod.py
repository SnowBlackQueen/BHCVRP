from generator.heuristic.Heuristic import Heuristic
from data.ProblemType import ProblemType
from data.Problem import Problem
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
            self.customer = self._get_random_customer(self.customers_to_visit)
            if self.type_problem == ProblemType.VRPTW:
                self.time_window = self.list_time_windows[self.customer.get_id_customer()]
            if not self.initialized:
                self.request_route = self.customer.get_request_customer()
                self.route.get_list_id_customers().append(self.customer.get_id_customer())
                self.customers_to_visit.remove(self.customer)
                if self.type_problem == ProblemType.VRPTW:
                    self.list_time_windows.remove(self.time_window)

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

