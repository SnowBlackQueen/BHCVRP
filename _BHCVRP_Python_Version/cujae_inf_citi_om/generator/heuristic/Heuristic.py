import random
import numpy as np

from typing import List
from abc import ABC, abstractmethod
from random import Random

from data.Customer import Customer
from data.CustomerType import CustomerType
from data.BusStop import BusStop
from data.TimeWindow import TimeWindow
from data.Problem import Problem
from data.ProblemType import ProblemType
from data.DepotMDVRP import DepotMDVRP
from solution.Solution import Solution
from solution.Route import Route
from solution.RouteType import RouteType
from solution.RouteTTRP import RouteTTRP
from generator.heuristic.Metric import Metric
from generator.heuristic.FirstElementType import FirstElementType

from generator.postoptimization.Operator_3opt import Operator_3opt

# Clase abstracta que modela una heurística de construcción


class Heuristic(ABC):
    def __init__(self):
        self.initialized = False

    # Template Method
    def template_method(self) -> Solution:
        self.comun_initialize()
        self.initialize_specifics()
        self.initialized = True
        return self.get_solution_inicial()

    @abstractmethod  # Método para inicializar parámetros específicos de algunas heurísticas
    def initialize_specifics(self):
        pass

        # Método que inicializa todo los parámetros en común de las HC

    def comun_initialize(self):
        self.solution = Solution()
        self.customers_to_visit = None
        self.id_depot = -1
        self.pos_depot = -1

        if (
            Problem.get_problem().get_type_problem() == ProblemType.CVRP
            or Problem.get_problem().get_type_problem() == ProblemType.HFVRP
            or Problem.get_problem().get_type_problem() == ProblemType.OVRP
            or Problem.get_problem().get_type_problem() == ProblemType.TTRP
            or Problem.get_problem().get_type_problem() == ProblemType.SBRP
            or Problem.get_problem().get_type_problem() == ProblemType.VRPTW
        ):
            self.pos_depot = 0
            self.id_depot = (
                Problem.get_problem().get_list_depots()[self.pos_depot].get_id_depot()
            )
            if Problem.get_problem().get_type_problem() == ProblemType.SBRP:
                self.list_bus_stops = list(Problem.get_problem().get_list_buses_stop())
                self.bus_stop = BusStop()

            else:
                self.customers_to_visit = list(Problem.get_problem().get_list_customers())
                if Problem.get_problem().get_type_problem() == ProblemType.VRPTW:
                    # self.list_time_windows = list(Problem.get_problem().get_list_time_windows())
                    self.feasible_customers = []
        else:
            i = 0
            self.found = False

            depots = Problem.get_problem().get_list_depots()

            while i < len(depots) and not self.found:
                if (
                    isinstance(depots[i], DepotMDVRP)
                    or depots[i].get_list_assigned_customers()
                ):
                    self.pos_depot = i
                    self.id_depot = depots[self.pos_depot].get_id_depot()  # VERIFICAR!!
                    customers_assigned_by_depot = (
                        Problem.get_problem().get_customers_assigned_by_id_depot(
                            self.id_depot, Problem.get_problem()._list_customers, depots
                        )
                    )
                    self.customers_to_visit = list(customers_assigned_by_depot)

                    self.found = True
                else:
                    i += 1

        self.capacity_vehicle = (
            Problem.get_problem()
            .get_list_depots()[self.pos_depot]
            .get_list_fleets()[0]
            .get_capacity_vehicle()
        )
        self.count_vehicles = (
            Problem.get_problem()
            .get_list_depots()[self.pos_depot]
            .get_list_fleets()[0]
            .get_count_vehicles()
        )

        self.customer = Customer()
        self.request_route = 0.0
        self.time_route = 0.0
        self.route = Route()

        self.type_problem = Problem.get_problem().get_type_problem()

        if self.type_problem == ProblemType.TTRP or self.type_problem == 4:
            self.route = RouteTTRP()


    @abstractmethod  # Método para ejecutar la variante específica del problema para cierta heurística
    def get_solution_inicial(self) -> Solution:
        pass

    def execute(self):
        if self.type_problem == ProblemType.CVRP or self.type_problem == ProblemType.SBRP or self.type_problem == ProblemType.VRPTW or self.type_problem in [0, 3, 5]:
            self.processing(
                self.customers_to_visit,
                self.count_vehicles,
                self.request_route,
                self.route,
                self.id_depot,
                self.solution,
            )

        elif self.type_problem == ProblemType.HFVRP or self.type_problem == 1:
            self.processing()
            if self.customers_to_visit:
                self.route = Route()
                self.list_capacities = list(Problem.get_problem().get_list_capacities())
                iterator_cap_vehicle = iter(self.list_capacities)
                while self.customers_to_visit:
                    j = 0
                    found = False

                    while not found:
                        try:
                            if next(iterator_cap_vehicle) >= (
                                self.request_route
                                + self.customer.get_request_customer()
                            ):
                                self.solution.get_list_routes()[j].set_request_route(
                                    self.request_route
                                    + self.customer.get_request_customer()
                                )
                                self.solution.get_list_routes()[
                                    j
                                ].get_list_id_customers().append(
                                    self.customer.get_id_customer()
                                )
                                self.customers_to_visit.remove(self.customer)

                                found = True
                                # break
                            else:
                                j += 1
                                self.request_route = self.solution.get_list_routes()[
                                    j
                                ].get_request_route()
                        except StopIteration:
                            break

                    if not found:
                        self.route.get_list_id_customers().append(
                            self.customer.get_id_customer()
                        )
                        self.route.set_request_route(
                            self.route.get_request_route()
                            + self.customer.get_request_customer()
                        )
                        self.customers_to_visit.remove(self.customer)

                    if self.customers_to_visit:
                        self.initialize_specifics()

                # if self.route.get_list_id_customers():
                #     self.route.set_id_depot(self.id_depot)
                #     self.solution.get_list_routes().append(self.route)

        elif self.type_problem == ProblemType.MDVRP or self.type_problem == 2:
            depots = Problem.get_problem().get_list_depots()
            for j in range(self.pos_depot, len(depots)):
                if j != self.pos_depot:
                    self.id_depot = depots[j].get_id_depot()
                    self.customers_to_visit = (
                        Problem.get_problem().get_customers_assigned_by_id_depot(
                            self.id_depot,
                            Problem.get_problem().get_list_customers(),
                            Problem.get_problem().get_list_depots(),
                        )
                    )
                    self.capacity_vehicle = (
                        depots[j].get_list_fleets()[0].get_capacity_vehicle()
                    )
                    self.count_vehicles = (
                        depots[j].get_list_fleets()[0].get_count_vehicles()
                    )

                    if self.customers_to_visit:
                        self.route = Route()
                        self.initialize_specifics()
                        self.request_route = self.customer.get_request_customer()
                        self.route.get_list_id_customers().append(
                            self.customer.get_id_customer()
                        )
                        self.customers_to_visit.remove(self.customer)
                    else:
                        continue

                self.creating()

        elif self.type_problem == ProblemType.TTRP or self.type_problem == 4:
            self.is_TC = False
            self.capacity_trailer = (
                Problem.get_problem()
                .get_list_depots()[self.pos_depot]
                .get_list_fleets()[0]
                .get_capacity_trailer()
            )

            self.type_customer = self.customer.get_type_customer()

            self.processing()

            self.route.set_request_route(self.request_route)

            if (
                self.customer.get_type_customer() == CustomerType.TC
                or self.customer.get_type_customer() == 1
            ):
                self.route.set_type_route(RouteType.PTR.value)
            else:
                if self.is_TC:
                    self.route.set_type_route(RouteType.CVR.value)
                else:
                    self.route.set_type_route(RouteType.PVR.value)

            self.route.set_id_depot(self.id_depot)
            self.solution.get_list_routes().append(self.route)

        return self.solution

    # Redefinir
    def creating(
        self, route=None, request_route=None, list_tau=None, list_metrics=None
    ):
        created = False
        if self.type_problem == ProblemType.SBRP:
            # Logic for SBRP variant
            while self.list_bus_stops:
                self.initialize_specifics()  # Initialize bus stop specifics

                # Get the current bus stop
                bus_stop = self.bus_stop  # Assuming self.bus_stop is set correctly

                # Check if adding this bus stop exceeds vehicle capacity
                if (self.request_route + bus_stop.get_capacity_bus_stop() <= self.capacity_vehicle):
                    self.request_route += bus_stop.get_capacity_bus_stop()  # Update request_route
                    self.route.get_list_bus_stops().append(bus_stop.get_id_bus_stop())  # Add bus stop to route
                    self.list_bus_stops.remove(bus_stop)  # Remove bus stop from the list
                else:
                    # If capacity is exceeded, finalize the current route
                    self.route.set_request_route(self.request_route)
                    self.route.set_id_depot(self.id_depot)
                    self.solution.get_list_routes().append(self.route)

                    # Reset for the next route
                    self.route = Route()  # Create a new route
                    self.request_route = 0.0  # Reset request_route for the new route

            # Finalize the last route if it has bus stops
            if self.route.get_list_bus_stops():
                self.route.set_request_route(self.request_route)
                self.route.set_id_depot(self.id_depot)
                self.solution.get_list_routes().append(self.route)

            created = True  # Indicate that a route was created
            return created, self.route
        else:
            if self.type_problem == ProblemType.CVRP or self.type_problem == 0:
                if (
                    self.request_route + self.customer.get_request_customer()
                    <= self.capacity_vehicle
                ):
                    self.request_route += self.customer.get_request_customer()
                    self.route.get_list_id_customers().append(
                        self.customer.get_id_customer()
                    )
                    self.customers_to_visit.remove(self.customer)
                    if not self.customers_to_visit:
                        self.route.set_request_route(self.request_route)
                        self.route.set_id_depot(self.id_depot)
                        self.solution.get_list_routes().append(self.route)
                else:
                    self.route.set_request_route(self.request_route)
                    self.route.set_id_depot(self.id_depot)
                    self.solution.get_list_routes().append(self.route)
                    self.route = Route()
                    self.route.get_list_id_customers().append(
                        self.customer.get_id_customer()
                    )
                    self.request_route = self.customer.get_request_customer()
                    self.customers_to_visit.remove(self.customer)
                    created = True

                return created, self.route

            elif self.type_problem == ProblemType.HFVRP or self.type_problem == 1:
                while self.customers_to_visit:
                    self.initialize_specifics()

                    if self.capacity_vehicle >= (
                        self.request_route + self.customer.get_request_customer()
                    ):
                        self.request_route += self.customer.get_request_customer()
                        self.route.get_list_id_customers().append(
                            self.customer.get_id_customer()
                        )
                        self.customers_to_visit.remove(
                            self.customer
                        )  # Remueve el primer cliente procesado
                    else:
                        self.route.set_request_route(self.request_route)
                        self.route.set_id_depot(self.id_depot)
                        self.solution.get_list_routes().append(self.route)

                        return False  # Indicando que se necesita un nuevo vehículo/ruta

                return True  # Indicando que el vehículo aún tiene capacidad

            elif self.type_problem == ProblemType.MDVRP or self.type_problem == 2:
                # routes = self.solution.get_list_routes()

                while self.customers_to_visit and self.count_vehicles > 0:
                    self.initialize_specifics()

                    if self.capacity_vehicle >= (
                        self.request_route + self.customer.get_request_customer()
                    ):
                        self.request_route += self.customer.get_request_customer()
                        self.route.get_list_id_customers().append(
                            self.customer.get_id_customer()
                        )
                        self.customers_to_visit.remove(self.customer)
                    else:
                        self.route.set_request_route(self.request_route)
                        self.route.set_id_depot(self.id_depot)
                        self.solution.get_list_routes().append(self.route)
                        self.count_vehicles -= 1

                        if self.count_vehicles > 0:
                            self.route = Route()

                            self.route.get_list_id_customers().append(
                                self.customer.get_id_customer()
                            )
                            self.request_route = self.customer.get_request_customer()
                            self.customers_to_visit.remove(self.customer)

                if self.route != None:
                    self.route.set_request_route(self.request_route)
                    self.route.set_id_depot(self.id_depot)
                    # self.solution.get_list_routes().append(self.route)

                if self.customers_to_visit:
                    self.route = Route()
                    self.request_route = 0.0

                    while self.customers_to_visit:
                        k = 0
                        found = False
                        self.request_route = self.solution.get_list_routes()[
                            k
                        ].get_request_route()

                        while k < len(self.solution.get_list_routes()) and not found:
                            if self.capacity_vehicle >= (
                                self.request_route + self.customer.get_request_customer()
                            ):
                                self.solution.get_list_routes()[k].set_request_route(
                                    self.request_route
                                    + self.customer.get_request_customer()
                                )
                                self.solution.get_list_routes()[
                                    k
                                ].get_list_id_customers().append(
                                    self.customer.get_id_customer()
                                )
                                self.customers_to_visit.remove(self.customer)
                                found = True
                            else:
                                k += 1
                                self.request_route = self.solution.get_list_routes()[
                                    k
                                ].get_request_route()

                        if not found:
                            self.route.get_list_id_customers().append(
                                self.customer.get_id_customer()
                            )
                            self.route.set_request_route(
                                self.route.get_request_route()
                                + self.customer.get_request_customer()
                            )
                            self.customers_to_visit.remove(self.customer)

                        if self.customers_to_visit:
                            self.initialize_specifics()

                if self.route.get_list_id_customers():
                    self.route.set_id_depot(self.id_depot)
                    self.solution.get_list_routes().append(self.route)

                # return self.solution.get_list_routes()

            elif self.type_problem == ProblemType.TTRP or self.type_problem == 4:
                if (
                    self.request_route + self.customer.get_request_customer()
                    <= self.capacity_vehicle
                ):
                    self.request_route += self.customer.get_request_customer()
                    self.route.get_list_id_customers().append(
                        self.customer.get_id_customer()
                    )
                    self.customers_to_visit.remove(self.customer)
                else:
                    self.route.set_request_route(self.request_route)
                    # self.route.set_type_route(RouteType.PTR.value)
                    self.route.set_id_depot(self.id_depot)
                    self.route = RouteTTRP(
                        list_id_customers=self.route.get_list_id_customers(),
                        request_route=self.route.get_request_route(),
                        cost_route=self.route.get_cost_route(),
                        id_depot=self.id_depot,
                        list_access_vc=[],
                        type_route=RouteType.PTR.value,
                        maximum_distance=None,
                    )
                    self.solution.get_list_routes().append(self.route)  # VERIFICAR!!

                    self.route = RouteTTRP()

                    self.request_route = self.customer.get_request_customer()
                    self.type_customer = self.customer.get_type_customer()
                    self.route.get_list_id_customers().append(
                        self.customer.get_id_customer()
                    )
                    self.customers_to_visit.remove(self.customer)

            elif self.type_problem == ProblemType.VRPTW or self.type_problem == 6:

                if self.feasible_customers:
                    self.request_route += self.customer.get_request_customer()
                    self.route.get_list_id_customers().append(
                        self.customer.get_id_customer()
                    )
                    self.customers_to_visit.remove(self.customer)
                    if not self.customers_to_visit:
                        self.route.set_request_route(self.request_route)
                        self.route.set_id_depot(self.id_depot)
                        self.solution.get_list_routes().append(self.route)
                else:
                    self.route.set_request_route(self.request_route)
                    self.route.set_id_depot(self.id_depot)
                    self.solution.get_list_routes().append(self.route)
                    self.route = Route()
                    # self.route.get_list_id_customers().append(
                    #     self.customer.get_id_customer()
                    # )
                    # self.request_route = self.customer.get_request_customer()
                    # self.customers_to_visit.remove(self.customer)
                    self.request_route = 0.0
                    self.time_route = 0.0
                    created = True

                return created, self.route

            created = True
            return created, self.route

    # Redefinir
    def processing(
        self,
        customers_to_visit=None,
        count_vehicles=None,
        request_route=None,
        route=None,
        id_depot=None,
        solution=None,
    ):
        if self.type_problem == ProblemType.CVRP or self.type_problem == ProblemType.VRPTW or self.type_problem == 0:
            cv = int(count_vehicles)
            while customers_to_visit and cv > 0:
                self.initialize_specifics()  # Para que customer sea tratado según la variante
                found, new_route = self.creating()
                if found:
                    route = new_route
                    cv -= 1

        elif self.type_problem == ProblemType.SBRP or self.type_problem == 5:
            cv = int(count_vehicles)
            while self.list_bus_stops and cv > 0:
                self.initialize_specifics()  # Para que bus_stop sea tratado según la variante
                found, new_route = self.creating()
                if found:
                    route = new_route
                    cv -= 1

        elif self.type_problem == ProblemType.HFVRP or self.type_problem == 1:
            self.list_capacities = list(Problem.get_problem().get_list_capacities())
            capacity_vehicle = self.list_capacities[0]
            is_open = True

            while self.customers_to_visit and self.list_capacities:
                # self.route = Route()
                success = self.creating(
                    self.route, self.request_route, self.customer, capacity_vehicle
                )

                if not success:
                    # Manejo cuando se agota la capacidad del vehículo actual
                    if self.list_capacities:
                        self.route = Route()

                        self.request_route = self.customer.get_request_customer()
                        self.route.get_list_id_customers().append(
                            self.customer.get_id_customer()
                        )
                        self.customers_to_visit.remove(self.customer)

                        capacity_vehicle = self.list_capacities.pop(0)
                        is_open = True
                    else:
                        is_open = False

                # if is_open:
                #     self.route.set_request_route(self.request_route)
                #     self.route.set_id_depot(self.id_depot)
                #     self.solution.get_list_routes().append(self.route)

        elif self.type_problem == ProblemType.TTRP or self.type_problem == 4:
            while self.customers_to_visit:
                self.initialize_specifics()
                found = False
                if (
                    self.customer.get_type_customer() == CustomerType.TC
                    or self.customer.get_type_customer() == 1
                ):
                    found, new_route = self.creating()
                else:
                    if (
                        self.customer.get_type_customer() == CustomerType.TC
                        or self.customer.get_type_customer() == 1
                    ):
                        self.is_TC = True

                    if (self.capacity_vehicle + self.capacity_trailer) >= (
                        self.request_route + self.customer.get_request_customer()
                    ):
                        self.request_route += self.customer.get_request_customer()
                        self.route.get_list_id_customers().append(
                            self.customer.get_id_customer()
                        )
                        self.customers_to_visit.remove(self.customer)
                    else:
                        self.route.set_request_route(self.request_route)

                        if self.is_TC:
                            route_ttrp = RouteTTRP(
                                type_route=2,
                                list_id_customers=self.route.get_list_id_customers(),
                                request_route=self.route.get_request_route(),
                                cost_route=self.route.get_cost_route(),
                                id_depot=self.route.get_id_depot(),
                                list_access_vc=[],
                                maximum_distance=self.route.get_maximum_distance(),
                            )
                            self.route = route_ttrp
                            self.route.set_type_route(RouteType.CVR.value)
                        else:
                            route_ttrp = RouteTTRP(
                                type_route=1,
                                list_id_customers=self.route.get_list_id_customers(),
                                request_route=self.route.get_request_route(),
                                cost_route=self.route.get_cost_route(),
                                id_depot=self.route.get_id_depot(),
                                list_access_vc=[],
                                maximum_distance=self.route.get_maximum_distance(),
                            )
                            self.route = route_ttrp
                            self.route.set_type_route(RouteType.PVR.value)

                        self.route.set_id_depot(self.id_depot)
                        self.solution.get_list_routes().append(self.route)
                        self.is_TC = False

                        self.route = RouteTTRP()

                        self.request_route = self.customer.get_request_customer()
                        self.type_customer = self.customer.get_type_customer()
                        self.route.get_list_id_customers().append(
                            self.customer.get_id_customer()
                        )
                        self.customers_to_visit.remove(self.customer)

    def _get_element_by_id(self, id_element, list_elements):
        i = 0
        found = False
        element = None

        while i < len(list_elements) and not found:
            if Problem.get_problem().get_type_problem() == ProblemType.SBRP:
                if list_elements[i].get_id_bus_stop() == id_element:
                    element = list_elements[i]
                    found = True
                else:
                    i += 1
            else:
                if list_elements[i].get_id_customer() == id_element:
                    element = list_elements[i]
                    found = True
                else:
                    i += 1

        return element

    def _ascendent_ordenate_list_without_order(self, list_without_order: List[Metric]):
        for i in range(len(list_without_order)):
            minor_insertion_cost = list_without_order[i].get_insertion_cost()
            minor_metric = list_without_order[i]
            reference_pos = i

            current_metric = None
            current_pos = -1

            for j in range(i + 1, len(list_without_order)):
                if list_without_order[j].get_insertion_cost() < minor_insertion_cost:
                    minor_insertion_cost = list_without_order[j].get_insertion_cost()
                    current_metric = list_without_order[j]
                    current_pos = j

            if current_pos != -1:
                list_without_order[reference_pos] = current_metric
                list_without_order[current_pos] = minor_metric

    def _ascendent_ordenate_list_distances(
        self, list_distances, list_nn: List[Customer]
    ):
        for i in range(len(list_distances)):
            minor_distance = list_distances[i]
            customer_nn = list_nn[i]
            reference_pos = i

            current_distance = 0.0
            current_customer = None
            current_pos = -1

            for j in range(i + 1, len(list_distances)):
                if minor_distance > list_distances[j]:
                    current_distance = list_distances[j]
                    current_customer = list_nn[j]
                    current_pos = j

            if current_pos != -1:
                list_distances[reference_pos] = current_distance
                list_distances[current_pos] = minor_distance

                list_nn[reference_pos] = current_customer
                list_nn[current_pos] = customer_nn

    def _select_first_customer_in_mdvrp(
        self, customers_to_visit, first_customer_type, pos_matrix_depot
    ):
        selected_customer = None
        current_index = -1
        current_cost = 0.0

        selected_customer = customers_to_visit[0]
        best_index = Problem.get_problem().get_pos_element(
            selected_customer.get_id_customer()
        )
        best_cost = (
            Problem.get_problem().get_cost_matrix().item(pos_matrix_depot, best_index)
        )

        for i in range(1, len(customers_to_visit)):
            current_index = Problem.get_problem().get_pos_element(
                customers_to_visit[i].get_id_customer()
            )
            current_cost = (
                Problem.get_problem()
                .get_cost_matrix()
                .item(pos_matrix_depot, current_index)
            )

            if first_customer_type == FirstElementType.Furthest:
                if current_cost > best_cost:
                    best_cost = current_cost
                    best_index = current_index
                    selected_customer = customers_to_visit[i]
            else:
                if first_customer_type == FirstElementType.Nearest:
                    if current_cost < best_cost:
                        best_cost = current_cost
                        best_index = current_index
                        selected_customer = customers_to_visit[i]

        return selected_customer

    def _get_first_element(self, elements_to_visit, first_element_type, id_depot):
        first_element = None
        index = -1
        pos_matrix_depot = -1
        rc = None

        if (
            first_element_type == FirstElementType.Random
        ):  # Replace with the actual condition
            index = random.randint(0, len(elements_to_visit) - 1)
            first_element = elements_to_visit[index]
        else:
            pos_matrix_depot = Problem.get_problem().get_pos_element(id_depot)

            if Problem.get_problem().get_type_problem() == ProblemType.MDVRP:
                first_element = self._select_first_customer_in_mdvrp(
                    elements_to_visit, first_element_type, pos_matrix_depot
                )
            else:
                if first_element_type == FirstElementType.Nearest:
                    cm = Problem.get_problem().get_cost_matrix()
                    submatrix = cm[pos_matrix_depot, : len(elements_to_visit)]
                    index = np.argmin(submatrix)
                elif first_element_type == FirstElementType.Furthest:
                    cm = Problem.get_problem().get_cost_matrix()
                    submatrix = cm[pos_matrix_depot, : len(elements_to_visit)]
                    index = np.argmax(submatrix)

                first_element = elements_to_visit[index]

        return first_element

    def get_feasible_customers(self, current_node_id):
        feasible_customers = []
        time_matrix = Problem.get_problem().get_time_matrix()

        for cust in self.customers_to_visit:
            travel_time = time_matrix[current_node_id, cust.get_id_customer()]
            arrival_time = self.time_route + travel_time
            # Si se llega antes del ready_time, se espera
            effective_time = max(arrival_time, cust.get_time_window().get_initial_node())
            # Verificamos la ventana de tiempo del cliente
            if effective_time > cust.get_time_window().get_end_node():
                continue  # No es factible por ventana de tiempo
            # Verificamos la capacidad
            if self.request_route + cust.get_request_customer() > self.capacity_vehicle:
                continue
            feasible_customers.append(cust)

        return feasible_customers

    """# Cómo usar el patrón Template 
    def execute(self):
        self.step1()
        self.step2()
        self.step3()
        self.common_step()

    @abstractmethod
    def step1(self):
        pass

    @abstractmethod
    def step2(self):
        pass

    @abstractmethod
    def step3(self):
        pass

    def common_step(self):
        print("Executing common step")

    class HeuristicA(Heuristic):
        def step1(self):
            print("HeuristicA Step 1")

        def step2(self):
            print("HeuristicA Step 2")

        def step3(self):
            print("HeuristicA Step 3")

    class HeuristicB(Heuristic):
        def step1(self):
            print("HeuristicB Step 1")

        def step2(self):
            print("HeuristicB Step 2")

        def step3(self):
            print("HeuristicB Step 3")

    # Example usage
    heuristic_a = HeuristicA()
    heuristic_a.execute()

    heuristic_b = HeuristicB()
    heuristic_b.execute() 
    
    # Aquí empieza el código original"""
