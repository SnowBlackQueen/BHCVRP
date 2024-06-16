import numpy as np
from cujae_inf_citi_om.data import Problem

class Route:
    def __init__(self):
        self.list_id_customers = []
        self.request_route = 0.0
        self.cost_route = 0.0
        self.id_depot = -1

    def __init__(self, list_id_customers, request_route, cost_route, id_depot, list_access_vc):
        self.list_id_customers = list(list_id_customers)
        self.request_route = request_route
        self.cost_route = 0.0
        self.id_depot = id_depot
        self.list_access_vc = []

    def get_list_id_customers(self):
        return self.list_id_customers

    def set_list_id_customers(self, list_id_customers):
        self.list_id_customers = list_id_customers

    def get_request_route(self):
        return self.request_route

    def set_request_route(self, request_route):
        self.request_route = request_route

    def get_cost_route(self):
        return self.cost_route

    def set_cost_route(self, cost_route):
        self.cost_route = cost_route

    def get_id_depot(self):
        return self.id_depot

    def set_id_depot(self, id_depot):
        self.id_depot = id_depot

    def get_cost_single_route(self):
        cost_route = 0.0
        customer_ini = self.list_id_customers[0]
        pos_customer_ini = Problem.get_problem().get_pos_element(customer_ini)

        # cost_route += Problem.get_problem().get_cost_matrix().item(Problem.get_problem().get_pos_element(self.id_depot), pos_customer_ini)

        for i in range(1, len(self.list_id_customers)):
            customer_next = self.list_id_customers[i]
            pos_customer_next = Problem.get_problem().get_pos_element(customer_next)
            # cost_route += Problem.get_problem().get_cost_matrix().item(pos_customer_ini, pos_customer_next)
            customer_ini = customer_next
            pos_customer_ini = pos_customer_next

        # cost_route += Problem.get_problem().get_cost_matrix().item(pos_customer_ini, Problem.get_problem().get_pos_element(self.id_depot))
        self.set_cost_route(cost_route)
        return cost_route

