from abc import ABC, abstractmethod
import numpy as np
from generator.heuristic import Heuristic
from data.Problem import Problem
from data.ProblemType import ProblemType
from data.CustomerType import CustomerType
from generator.solution.Route import Route
from generator.solution.RouteTTRP import RouteTTRP
from generator.solution.RouteType import RouteType

class Save(Heuristic):
    parameterShape = 1

    def __init__(self):
        super().__init__()

    def fill_save_matrix(self, id_depot, customers_to_visit):
        count_customer = len(customers_to_visit)
        save_matrix = np.full((count_customer, count_customer), -np.inf)
        save = 0.0

        for i in range(count_customer):
            for j in range(i, count_customer):
                if i != j:
                    save = (Problem.get_problem().get_cost_matrix().item(
                                Problem.get_problem().get_pos_element(customers_to_visit[i].id_customer), 
                                Problem.get_problem().get_pos_element(id_depot)) + 
                            Problem.get_problem().get_cost_matrix().item(
                                Problem.get_problem().get_pos_element(id_depot), 
                                Problem.get_problem().get_pos_element(customers_to_visit[j].id_customer)) - 
                            (self.parameterShape * Problem.get_problem().get_cost_matrix().item(
                                Problem.get_problem().get_pos_element(customers_to_visit[i].id_customer), 
                                Problem.get_problem().get_pos_element(customers_to_visit[j].id_customer))))
                    save_matrix[i, j] = save
                    save_matrix[j, i] = save

        return save_matrix

    def get_position_route(self, list_routes, id_customer):
        index = -1
        stop = False
        i = 0

        while i < len(list_routes) and not stop:
            j = 0
            while j < len(list_routes[i].list_id_customers) and not stop:
                if list_routes[i].list_id_customers[j] == id_customer:
                    stop = True
                    index = i
                j += 1
            i += 1

        return index

    def create_initial_routes(self, list_customers):
        list_routes = []
        list_access_vc = []

        for customer in list_customers:
            route = Route()
            route.set_request_route(customer.request_customer)
            route.set_id_depot(Problem.get_problem().get_id_depot_by_id_customer(customer.id_customer))
            route.list_id_customers.append(customer.id_customer)

            if Problem.get_problem().get_type_problem() == ProblemType.TTRP:
                route = RouteTTRP(route.list_id_customers, route.request_route, 
                                  route.cost_route, route.id_depot, list_access_vc, 
                                  RouteType.PVR if customer.type_customer == CustomerType.VC else RouteType.PTR)

            list_routes.append(route)

        return list_routes

    def reduce_options(self, route, save_matrix):
        count_customers = len(Problem.get_problem().get_list_customers())

        for i in range(1, len(route.list_id_customers) - 1):
            if save_matrix[Problem.get_problem().get_pos_element(route.list_id_customers[i]), :].tolist().count(-np.inf) != count_customers:
                save_matrix[Problem.get_problem().get_pos_element(route.list_id_customers[i]), :] = -np.inf
                save_matrix[:, Problem.get_problem().get_pos_element(route.list_id_customers[i])] = -np.inf


