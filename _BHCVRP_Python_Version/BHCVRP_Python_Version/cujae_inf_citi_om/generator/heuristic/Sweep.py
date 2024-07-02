from generator.heuristic.Heuristic import Heuristic
from data.Customer import Customer
from generator.solution.Solution import Solution
from data.Problem import Problem
from data.ProblemType import ProblemType
from data.DepotMDVRP import DepotMDVRP
from generator.solution.Route import Route
from random import Random
from data.CustomerType import CustomerType
from generator.solution.RouteType import RouteType

class Sweep(Heuristic):
    
    def __init__(self):
        super().__init__()
        
    def initialize_specifics(self):
        self.random = Random()
        self.index = -1

        self.bubble_method(self.customers_to_visit)

        self.index = self.random.randint(0, len(self.customers_to_visit) - 1)
        
        if self.index == len(self.customers_to_visit):
            self.index = 0
            
        self.customer = self.customers_to_visit[self.index]
        self.request_route = self.customer.get_request_customer()
        self.route.get_list_id_customers().append(self.customer.get_id_customer())
        self.customers_to_visit.remove(self.customer)

    def get_solution_inicial(self):
        self.execute()
        
        return self.solution
    
    # Método de ordenamiento Burbujas utilizando las coordenadas polares
    def bubble_method(self, list_customers):
        value_theta_one = 0.0
        value_rho_one = 0.0
        value_theta_two = 0.0
        value_rho_two = 0.0

        for i in range(len(list_customers) - 1):
            value_theta_one = list_customers[i].get_location_customer().get_polar_theta()

            for j in range(i + 1, len(list_customers)):
                customer = Customer()

                value_theta_two = list_customers[j].get_location_customer().get_polar_theta()

                if value_theta_one > value_theta_two:
                    customer = list_customers[i]
                    list_customers[i] = list_customers[j]
                    list_customers[j] = customer

                    value_theta_one = value_theta_two
                else:
                    if value_theta_one == value_theta_two:
                        value_rho_one = list_customers[i].get_location_customer().get_polar_rho()
                        value_rho_two = list_customers[j].get_location_customer().get_polar_rho()

                        if value_rho_one > value_rho_two:
                            customer = list_customers[i]
                            list_customers[i] = list_customers[j]
                            list_customers[j] = customer

                            value_theta_one = value_theta_two
        return list_customers