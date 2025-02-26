from abc import ABC, abstractmethod
import numpy as np
from generator.heuristic.Heuristic import Heuristic
from data.Problem import Problem
from data.ProblemType import ProblemType
from data.CustomerType import CustomerType
from solution.Route import Route
from solution.RouteTTRP import RouteTTRP
from solution.RouteType import RouteType
from generator.postoptimization.Operator_3opt import Operator_3opt


class Save(Heuristic):
    parameter_shape = 1

    def __init__(self):
        super().__init__()

    @abstractmethod
    def initialize_specifics(self):
        if self.parameter_shape <= 0:
            self.parameter_shape = 1

        self.three_opt = Operator_3opt()

        # self.list_routes = list(Route)()
        if self.type_problem == ProblemType.SBRP:
            self.list_routes = self.create_initial_routes(self.list_bus_stops)
            self.cant_bus_stops = len(self.list_bus_stops)
            self.save_matrix = np.zeros((self.cant_bus_stops, self.cant_bus_stops))
            self.save_matrix = self.fill_save_matrix(self.id_depot, self.list_bus_stops)
        else:
            self.list_routes = self.create_initial_routes(self.customers_to_visit)

            self.cant_customers = len(self.customers_to_visit)
            self.save_matrix = np.zeros((self.cant_customers, self.cant_customers))
            self.save_matrix = self.fill_save_matrix(self.id_depot, self.customers_to_visit)

    # Método que construye la matriz de ahorro
    def fill_save_matrix(self, id_depot, elements_to_visit):
        count_element = len(elements_to_visit)
        save_matrix = np.full((count_element, count_element), -np.inf)
        save = 0.0

        for i in range(count_element):
            for j in range(i, count_element):
                if i != j:
                    if self.type_problem == ProblemType.SBRP:
                        save = (
                                Problem.get_problem().get_cost_matrix()[
                                    Problem.get_problem().get_pos_element(
                                        elements_to_visit[i].get_id_bus_stop()
                                    ),
                                    Problem.get_problem().get_pos_element(id_depot),
                                ]
                                + Problem.get_problem().get_cost_matrix()[
                                    Problem.get_problem().get_pos_element(id_depot),
                                    Problem.get_problem().get_pos_element(
                                        elements_to_visit[j].get_id_bus_stop()
                                    ),
                                ]
                                - (
                                        self.parameter_shape
                                        * Problem.get_problem().get_cost_matrix()[
                                            Problem.get_problem().get_pos_element(
                                                elements_to_visit[i].get_id_bus_stop()
                                            ),
                                            Problem.get_problem().get_pos_element(
                                                elements_to_visit[j].get_id_bus_stop()
                                            ),
                                        ]
                                )
                        )
                    else:
                        save = (
                            Problem.get_problem().get_cost_matrix()[
                                Problem.get_problem().get_pos_element(
                                    elements_to_visit[i].get_id_customer()
                                ),
                                Problem.get_problem().get_pos_element(id_depot),
                            ]
                            + Problem.get_problem().get_cost_matrix()[
                                Problem.get_problem().get_pos_element(id_depot),
                                Problem.get_problem().get_pos_element(
                                    elements_to_visit[j].get_id_customer()
                                ),
                            ]
                            - (
                                self.parameter_shape
                                * Problem.get_problem().get_cost_matrix()[
                                    Problem.get_problem().get_pos_element(
                                        elements_to_visit[i].get_id_customer()
                                    ),
                                    Problem.get_problem().get_pos_element(
                                        elements_to_visit[j].get_id_customer()
                                    ),
                                ]
                            )
                        )
                    save_matrix[i, j] = save
                    save_matrix[j, i] = save

        return save_matrix

    # Método que devuelve la posición de una ruta
    def get_position_route(self, list_routes, id_element):
        index = -1
        stop = False
        i = 0

        while i < len(list_routes) and not stop:
            j = 0

            if self.type_problem == ProblemType.SBRP:
                while j < len(list_routes[i].get_list_bus_stops()) and not stop:
                    bus_stop = list_routes[i].get_list_bus_stops()[j]
                    if bus_stop.get_id_bus_stop() == id_element:
                        stop = True
                        index = i
                    j += 1
            else:
                while j < len(list_routes[i].get_list_id_customers()) and not stop:
                    if list_routes[i].get_list_id_customers()[j] == id_element:
                        stop = True
                        index = i
                    j += 1
            i += 1

        return index

    # Método para crear las rutas iniciales
    def create_initial_routes(self, list_elements):
        list_routes = []
        list_access_vc = []

        for element in list_elements:
            route = Route()

            if self.type_problem == ProblemType.SBRP:
                route.set_request_route(element.get_capacity_bus_stop())
                route.set_id_depot(self.id_depot)
                route.list_bus_stops.append(element)

            else:
                route.set_request_route(element.get_request_customer())
                route.set_id_depot(
                    Problem.get_problem().get_id_depot_by_id_customer(
                        element.get_id_customer()
                    )
                )
                route.list_id_customers.append(element.get_id_customer())

                if Problem.get_problem().get_type_problem() == ProblemType.TTRP:
                    route = RouteTTRP(
                        list_id_customers=route.list_id_customers,
                        request_route=route.request_route,
                        cost_route=route.cost_route,
                        id_depot=route.id_depot,
                        list_access_vc=list_access_vc,
                        type_route=(
                            RouteType.PVR
                            if element.get_type_customer() == CustomerType.VC.value
                            else RouteType.PTR
                        ),
                    )

            list_routes.append(route)

        return list_routes

    def reduce_options(self, route, save_matrix):
        if self.type_problem == ProblemType.SBRP:
            count_bus_stops = len(Problem.get_problem().get_list_buses_stop())

            for i in range(1, len(route.get_list_bus_stops()) - 1):
                if (
                    save_matrix[
                        Problem.get_problem().get_pos_element(
                            route.get_list_bus_stops()[i]
                        ),
                        :,
                    ]
                    .tolist()
                    .count(-np.inf)
                    != count_bus_stops
                ):
                    save_matrix[
                        Problem.get_problem().get_pos_element(
                            route.get_list_bus_stops()[i]
                        ),
                        :,
                    ] = -np.inf
                    save_matrix[
                        :,
                        Problem.get_problem().get_pos_element(
                            route.get_list_bus_stops()[i]
                        ),
                    ] = -np.inf

        else:
            count_customers = len(Problem.get_problem().get_list_customers())

            for i in range(1, len(route.get_list_id_customers()) - 1):
                if (
                    save_matrix[
                        Problem.get_problem().get_pos_element(
                            route.get_list_id_customers()[i]
                        ),
                        :,
                    ]
                    .tolist()
                    .count(-np.inf)
                    != count_customers
                ):
                    save_matrix[
                        Problem.get_problem().get_pos_element(
                            route.get_list_id_customers()[i]
                        ),
                        :,
                    ] = -np.inf
                    save_matrix[
                        :,
                        Problem.get_problem().get_pos_element(
                            route.get_list_id_customers()[i]
                        ),
                    ] = -np.inf
