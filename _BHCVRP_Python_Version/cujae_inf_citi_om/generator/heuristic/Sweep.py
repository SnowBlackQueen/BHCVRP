from generator.heuristic.Heuristic import Heuristic
from data.Customer import Customer
from data.BusStop import BusStop
from data.Problem import Problem
from data.ProblemType import ProblemType
from random import Random


class Sweep(Heuristic):

    def __init__(self):
        super().__init__()

    def initialize_specifics(self):
        self.random = Random()
        self.index = -1

        if Problem.get_problem().get_type_problem() == ProblemType.SBRP:
            self.bubble_method(self.list_bus_stops)

            self.index = self.random.randint(0, len(self.list_bus_stops) - 1)

            if self.index == len(self.list_bus_stops):
                self.index = 0

            self.bus_stop = self.list_bus_stops[self.index]
            if not self.initialized:
                self.route.get_list_bus_stops().append(self.bus_stop.get_id_bus_stop())
                self.list_bus_stops.remove(self.bus_stop)
        else:
            if self.type_problem == ProblemType.VRPTW:
                current_node_id = self.customer.get_id_customer()
                self.feasible_customers = self.get_feasible_customers(current_node_id)
                if self.feasible_customers:
                    self.bubble_method(self.feasible_customers)

                    self.index = self.random.randint(0, len(self.feasible_customers) - 1)

                    if self.index == len(self.feasible_customers):
                        self.index = 0

                    self.customer = self.feasible_customers[self.index]

                    time_matrix = Problem.get_problem().get_time_matrix()
                    current_time = time_matrix[current_node_id, self.customer.get_id_customer()]
                    customer_ready_time = self.customer.get_time_window().get_initial_node()
                    customer_service_time = self.customer.get_time_window().get_service_time()
                    self.time_route = max(current_time, customer_ready_time) + customer_service_time

            else:
                self.bubble_method(self.customers_to_visit)

                self.index = self.random.randint(0, len(self.customers_to_visit) - 1)

                if self.index == len(self.customers_to_visit):
                    self.index = 0

                self.customer = self.customers_to_visit[self.index]
            if not self.initialized:
                self.request_route = self.customer.get_request_customer()
                self.route.get_list_id_customers().append(self.customer.get_id_customer())
                self.customers_to_visit.remove(self.customer)

    def get_solution_inicial(self):
        self.execute()

        return self.solution

    # Método de ordenamiento Burbujas utilizando las coordenadas polares
    def bubble_method(self, list_elements):
        value_theta_one = 0.0
        value_rho_one = 0.0
        value_theta_two = 0.0
        value_rho_two = 0.0

        for i in range(len(list_elements) - 1):
            if Problem.get_problem().get_type_problem() == ProblemType.SBRP:
                value_theta_one = (
                    list_elements[i].get_location_bus_stop().get_polar_theta()
                )

                for j in range(i + 1, len(list_elements)):
                    bus_stop = BusStop()

                    value_theta_two = (
                        list_elements[j].get_location_bus_stop().get_polar_theta()
                    )

                    if value_theta_one > value_theta_two:
                        bus_stop = list_elements[i]
                        list_elements[i] = list_elements[j]
                        list_elements[j] = bus_stop

                        value_theta_one = value_theta_two
                    else:
                        if value_theta_one == value_theta_two:
                            value_rho_one = (
                                list_elements[i].get_location_bus_stop().get_polar_rho()
                            )
                            value_rho_two = (
                                list_elements[j].get_location_bus_stop().get_polar_rho()
                            )

                            if value_rho_one > value_rho_two:
                                bus_stop = list_elements[i]
                                list_elements[i] = list_elements[j]
                                list_elements[j] = bus_stop

                                value_theta_one = value_theta_two
            else:
                value_theta_one = (
                    list_elements[i].get_location_customer().get_polar_theta()
                )

                for j in range(i + 1, len(list_elements)):
                    customer = Customer()

                    value_theta_two = (
                        list_elements[j].get_location_customer().get_polar_theta()
                    )

                    if value_theta_one > value_theta_two:
                        customer = list_elements[i]
                        list_elements[i] = list_elements[j]
                        list_elements[j] = customer

                        value_theta_one = value_theta_two
                    else:
                        if value_theta_one == value_theta_two:
                            value_rho_one = (
                                list_elements[i].get_location_customer().get_polar_rho()
                            )
                            value_rho_two = (
                                list_elements[j].get_location_customer().get_polar_rho()
                            )

                            if value_rho_one > value_rho_two:
                                customer = list_elements[i]
                                list_elements[i] = list_elements[j]
                                list_elements[j] = customer

                                value_theta_one = value_theta_two
        return list_elements
