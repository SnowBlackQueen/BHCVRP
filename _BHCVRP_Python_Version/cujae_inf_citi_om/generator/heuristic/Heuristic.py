import numpy as np

from data.Customer import Customer
from data.CustomerType import CustomerType
from data.Problem import Problem
from data.ProblemType import ProblemType
from generator.solution.Solution import Solution
from typing import List
from generator.heuristic.Metric import Metric
from generator.heuristic.FirstCustomerType import FirstCustomerType
import random
from random import Random
from abc import ABC, abstractmethod
from data.DepotMDVRP import DepotMDVRP
from generator.solution.Route import Route
from generator.solution.RouteType import RouteType
from generator.postoptimization.Operator_3opt import Operator_3opt
from generator.solution.RouteTTRP import RouteTTRP


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

        if Problem.get_problem().get_type_problem() == ProblemType.CVRP or Problem.get_problem().get_type_problem() == ProblemType.HFVRP or Problem.get_problem().get_type_problem() == ProblemType.OVRP or Problem.get_problem().get_type_problem() == ProblemType.TTRP:
            self.pos_depot = 0
            self.id_depot = Problem.get_problem().get_list_depots()[self.pos_depot].get_id_depot()
            self.customers_to_visit = list(Problem.get_problem().get_list_customers())
        else:
            i = 0
            self.found = False

            depots = Problem.get_problem().get_list_depots()

            while i < len(depots) and not self.found:
                if isinstance(depots[i], DepotMDVRP) or depots[i].get_list_assigned_customers():
                    self.pos_depot = i
                    self.id_depot = depots[self.pos_depot].get_id_depot() #VERIFICAR!!
                    customers_assigned_by_depot = Problem.get_problem().get_customers_assigned_by_id_depot(self.id_depot, Problem.get_problem()._list_customers, depots)
                    self.customers_to_visit = list(customers_assigned_by_depot)

                    self.found = True
                else:
                    i += 1

        self.capacity_vehicle = Problem.get_problem().get_list_depots()[self.pos_depot].get_list_fleets()[0].get_capacity_vehicle()
        self.count_vehicles = Problem.get_problem().get_list_depots()[self.pos_depot].get_list_fleets()[0].get_count_vehicles()

        self.customer = Customer()
        self.request_route = 0.0
        self.route = Route()

        self.type_problem = Problem.get_problem().get_type_problem()
        
        if self.type_problem == ProblemType.TTRP or self.type_problem == 4:
            self.route = RouteTTRP()

    @abstractmethod  # Método para ejecutar la variante específica del problema para cierta heurística
    def get_solution_inicial(self) -> Solution:
        pass

    def execute(self):
        if self.type_problem == ProblemType.CVRP or self.type_problem in [0, 3]:
            self.processing(self.customers_to_visit, self.count_vehicles, self.request_route,
                            self.route, self.id_depot, self.solution)


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
                                    self.request_route + self.customer.get_request_customer()):
                                self.solution.get_list_routes()[j].set_request_route(
                                    self.request_route + self.customer.get_request_customer())
                                self.solution.get_list_routes()[j].get_list_id_customers().append(
                                    self.customer.get_id_customer())
                                self.customers_to_visit.remove(self.customer)

                                found = True
                                # break
                            else:
                                j += 1
                                self.request_route = self.solution.get_list_routes()[j].get_request_route()
                        except StopIteration:
                            break

                    if not found:
                        self.route.get_list_id_customers().append(self.customer.get_id_customer())
                        self.route.set_request_route(
                            self.route.get_request_route() + self.customer.get_request_customer())
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
                    self.customers_to_visit = Problem.get_problem().get_customers_assigned_by_id_depot(self.id_depot, Problem.get_problem().get_list_customers(), Problem.get_problem().get_list_depots())
                    self.capacity_vehicle = depots[j].get_list_fleets()[0].get_capacity_vehicle()
                    self.count_vehicles = depots[j].get_list_fleets()[0].get_count_vehicles()

                    if self.customers_to_visit:
                        self.route = Route()
                        self.initialize_specifics()
                        self.request_route = self.customer.get_request_customer()
                        self.route.get_list_id_customers().append(self.customer.get_id_customer())
                        self.customers_to_visit.remove(self.customer)
                    else:
                        continue

                self.creating()

        elif self.type_problem == ProblemType.TTRP or self.type_problem == 4:
            self.is_TC = False
            self.capacity_trailer = Problem.get_problem().get_list_depots()[self.pos_depot].get_list_fleets()[0].get_capacity_trailer()

            self.type_customer = self.customer.get_type_customer()

            self.processing()

            self.route.set_request_route(self.request_route)

            if self.customer.get_type_customer() == CustomerType.TC or self.customer.get_type_customer() == 1:
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
    def creating(self, route=None, request_route=None, list_tau=None, list_metrics=None):
        created = False
        if self.type_problem == ProblemType.CVRP or self.type_problem == 0:
            if self.request_route + self.customer.get_request_customer() <= self.capacity_vehicle:
                self.request_route += self.customer.get_request_customer()
                self.route.get_list_id_customers().append(self.customer.get_id_customer())
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
                self.route.get_list_id_customers().append(self.customer.get_id_customer())
                self.request_route = self.customer.get_request_customer()
                self.customers_to_visit.remove(self.customer)
                created = True

            return created, self.route

        elif self.type_problem == ProblemType.HFVRP or self.type_problem == 1:
            while self.customers_to_visit:
                self.initialize_specifics()

                if self.capacity_vehicle >= (self.request_route + self.customer.get_request_customer()):
                    self.request_route += self.customer.get_request_customer()
                    self.route.get_list_id_customers().append(self.customer.get_id_customer())
                    self.customers_to_visit.remove(self.customer)  # Remueve el primer cliente procesado
                else:
                    self.route.set_request_route(self.request_route)
                    self.route.set_id_depot(self.id_depot)
                    self.solution.get_list_routes().append(self.route)

                    return False  # Indicando que se necesita un nuevo vehículo/ruta

            return True  # Indicando que el vehículo aún tiene capacidad

        elif self.type_problem == ProblemType.MDVRP or self.type_problem == 2:
            #routes = self.solution.get_list_routes()

            while self.customers_to_visit and self.count_vehicles > 0:
                self.initialize_specifics()

                if self.capacity_vehicle >= (self.request_route + self.customer.get_request_customer()):
                    self.request_route += self.customer.get_request_customer()
                    self.route.get_list_id_customers().append(self.customer.get_id_customer())
                    self.customers_to_visit.remove(self.customer)
                else:
                    self.route.set_request_route(self.request_route)
                    self.route.set_id_depot(self.id_depot)
                    self.solution.get_list_routes().append(self.route)
                    self.count_vehicles -= 1

                    if self.count_vehicles > 0:
                        self.route = Route()

                        self.route.get_list_id_customers().append(self.customer.get_id_customer())
                        self.request_route = self.customer.get_request_customer()
                        self.customers_to_visit.remove(self.customer)

            if self.route != None:
                self.route.set_request_route(self.request_route)
                self.route.set_id_depot(self.id_depot)
                #self.solution.get_list_routes().append(self.route)

            if self.customers_to_visit:
                self.route = Route()
                self.request_route = 0.0

                while(self.customers_to_visit):
                    k = 0
                    found = False
                    self.request_route = self.solution.get_list_routes()[k].get_request_route()

                    while k < len(self.solution.get_list_routes()) and not found:
                        if self.capacity_vehicle >= (self.request_route + self.customer.get_request_customer()):
                            self.solution.get_list_routes()[k].set_request_route(self.request_route + self.customer.get_request_customer())
                            self.solution.get_list_routes()[k].get_list_id_customers().append(self.customer.get_id_customer())
                            self.customers_to_visit.remove(self.customer)
                            found = True
                        else:
                            k += 1
                            self.request_route = self.solution.get_list_routes()[k].get_request_route()

                    if not found:
                        self.route.get_list_id_customers().append(self.customer.get_id_customer())
                        self.route.set_request_route(self.route.get_request_route() + self.customer.get_request_customer())
                        self.customers_to_visit.remove(self.customer)

                    if self.customers_to_visit:
                        self.initialize_specifics()

            if self.route.get_list_id_customers():
                self.route.set_id_depot(self.id_depot)
                self.solution.get_list_routes().append(self.route)

            #return self.solution.get_list_routes()

        elif self.type_problem == ProblemType.TTRP or self.type_problem == 4:
            if self.request_route + self.customer.get_request_customer() <= self.capacity_vehicle:
                self.request_route += self.customer.get_request_customer()
                self.route.get_list_id_customers().append(self.customer.get_id_customer())
                self.customers_to_visit.remove(self.customer)
            else:
                self.route.set_request_route(self.request_route)
                #self.route.set_type_route(RouteType.PTR.value)
                self.route.set_id_depot(self.id_depot)
                self.route = RouteTTRP(list_id_customers=self.route.get_list_id_customers(), request_route=self.route.get_request_route(), cost_route=self.route.get_cost_route(), id_depot=self.id_depot, list_access_vc=[], type_route=RouteType.PTR.value, maximum_distance=None)
                self.solution.get_list_routes().append(self.route)  #VERIFICAR!!

                self.route = RouteTTRP()

                self.request_route = self.customer.get_request_customer()
                self.type_customer = self.customer.get_type_customer()
                self.route.get_list_id_customers().append(self.customer.get_id_customer())
                self.customers_to_visit.remove(self.customer)

            created = True
            return created, self.route

    # Redefinir
    def processing(self, customers_to_visit=None, count_vehicles=None, request_route=None, route=None, id_depot=None,
                   solution=None):
        if self.type_problem == ProblemType.CVRP or self.type_problem == 0:
            cv = int(count_vehicles)
            while customers_to_visit and cv > 0:
                self.initialize_specifics()  # Para que customer sea tratado según la variante
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
                success = self.creating(self.route, self.request_route, self.customer,
                                        capacity_vehicle)

                if not success:
                    # Manejo cuando se agota la capacidad del vehículo actual
                    if self.list_capacities:
                        self.route = Route()

                        self.request_route = self.customer.get_request_customer()
                        self.route.get_list_id_customers().append(self.customer.get_id_customer())
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
                if self.customer.get_type_customer() == CustomerType.TC or self.customer.get_type_customer() == 1:
                    found, new_route = self.creating()
                else:
                    if self.customer.get_type_customer() == CustomerType.TC or self.customer.get_type_customer() == 1:
                        self.is_TC = True

                    if (self.capacity_vehicle + self.capacity_trailer) >= (
                            self.request_route + self.customer.get_request_customer()):
                        self.request_route += self.customer.get_request_customer()
                        self.route.get_list_id_customers().append(self.customer.get_id_customer())
                        self.customers_to_visit.remove(self.customer)
                    else:
                        self.route.set_request_route(self.request_route)

                        if self.is_TC:
                            route_ttrp = RouteTTRP(type_route=2, list_id_customers=self.route.get_list_id_customers(), request_route=self.route.get_request_route(), cost_route=self.route.get_cost_route(), id_depot=self.route.get_id_depot(), list_access_vc=[], maximum_distance=self.route.get_maximum_distance())
                            self.route = route_ttrp
                            self.route.set_type_route(RouteType.CVR.value)
                        else:
                            route_ttrp = RouteTTRP(type_route=1, list_id_customers=self.route.get_list_id_customers(), request_route=self.route.get_request_route(), cost_route=self.route.get_cost_route(), id_depot=self.route.get_id_depot(), list_access_vc=[], maximum_distance=self.route.get_maximum_distance())
                            self.route = route_ttrp
                            self.route.set_type_route(RouteType.PVR.value)

                        self.route.set_id_depot(self.id_depot)
                        self.solution.get_list_routes().append(self.route)
                        self.is_TC = False

                        self.route = RouteTTRP()

                        self.request_route = self.customer.get_request_customer()
                        self.type_customer = self.customer.get_type_customer()
                        self.route.get_list_id_customers().append(self.customer.get_id_customer())
                        self.customers_to_visit.remove(self.customer)

    def _get_customer_by_id(self, id_customer, list_customers):
        i = 0
        found = False
        customer = None

        while i < len(list_customers) and not found:
            if list_customers[i].get_id_customer() == id_customer:
                customer = list_customers[i]
                found = True
            else:
                i += 1

        return customer

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

    def _ascendent_ordenate_list_distances(self, list_distances, list_nn: List[Customer]):
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

    def _select_first_customer_in_mdvrp(self, customers_to_visit, first_customer_type, pos_matrix_depot):
        selected_customer = None
        current_index = -1
        current_cost = 0.0

        selected_customer = customers_to_visit[0]
        best_index = Problem.get_problem().get_pos_element(selected_customer.get_id_customer())
        best_cost = Problem.get_problem().get_cost_matrix().item(pos_matrix_depot, best_index)

        for i in range(1, len(customers_to_visit)):
            current_index = Problem.get_problem().get_pos_element(customers_to_visit[i].get_id_customer())
            current_cost = Problem.get_problem().get_cost_matrix().item(pos_matrix_depot, current_index)

            if first_customer_type == FirstCustomerType.FurthestCustomer:
                if current_cost > best_cost:
                    best_cost = current_cost
                    best_index = current_index
                    selected_customer = customers_to_visit[i]
            else:
                if first_customer_type == FirstCustomerType.NearestCustomer:
                    if current_cost < best_cost:
                        best_cost = current_cost
                        best_index = current_index
                        selected_customer = customers_to_visit[i]

        return selected_customer

    def _get_first_customer(self, customers_to_visit, first_customer_type, id_depot):
        first_customer = None
        index = -1
        pos_matrix_depot = -1
        rc = None

        if first_customer_type == FirstCustomerType.RandomCustomer:  # Replace with the actual condition
            index = random.randint(0, len(customers_to_visit) - 1)
            first_customer = customers_to_visit[index]
        else:
            pos_matrix_depot = Problem.get_problem().get_pos_element(id_depot)

            if Problem.get_problem().get_type_problem() == ProblemType.MDVRP:
                first_customer = self._select_first_customer_in_mdvrp(customers_to_visit, first_customer_type,
                                                                      pos_matrix_depot)
            else:
                if first_customer_type == FirstCustomerType.NearestCustomer:
                    cm = Problem.get_problem().get_cost_matrix()
                    submatrix = cm[pos_matrix_depot, :len(self.customers_to_visit)]
                    index = np.argmin(submatrix)
                elif first_customer_type == FirstCustomerType.FurthestCustomer:
                    cm = Problem.get_problem().get_cost_matrix()
                    submatrix = cm[pos_matrix_depot, :len(self.customers_to_visit)]
                    index = np.argmax(submatrix)

                first_customer = customers_to_visit[index]

        return first_customer

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
