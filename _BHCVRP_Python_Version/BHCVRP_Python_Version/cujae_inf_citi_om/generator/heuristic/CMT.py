from generator.heuristic.Heuristic import Heuristic
from data.Problem import Problem
from generator.heuristic.Metric import Metric
from data.Customer import Customer
from generator.solution.Route import Route
from generator.postoptimization.Operator_3opt import Operator_3opt
from data.CustomerType import CustomerType
from generator.solution.Solution import Solution
from data.ProblemType import ProblemType
from data.DepotMDVRP import DepotMDVRP
from random import Random
from generator.solution.RouteTTRP import RouteTTRP
from generator.solution.RouteType import RouteType
from data.CustomerTTRP import CustomerTTRP
from generator.heuristic.FirstCustomerType import FirstCustomerType


class CMT(Heuristic):
    parameter_l = 1
    first_customer_type = FirstCustomerType.RandomCustomer

    def __init__(self):
        super().__init__()

    def initialize_specifics(self):
        if self.parameter_l <= 0:
            self.parameter_l = 1

        self.list_candidate_routes = []

        self.three_opt = Operator_3opt()

        self.random = Random()
        self.index = -1

        self.list_root_customers = []
        self.list_metrics_cmt_by_customer = None
        self.list_tau_costs = None
        self.route = None
        self.root_customer = None
        self.customer_to_insert = None
        self.request_route = 0.0
        self.pos_best_tau = -1

        if self.type_problem == ProblemType.HFVRP or self.type_problem == 1:
            self.list_capacities = list(Problem.get_problem().get_list_capacities())

    def creating(self, route, request_route, list_tau_costs, list_metrics_cmt_by_customer):
        if self.type_problem in [0, 1, 2,
                                 3] or self.type_problem == ProblemType.CVRP or self.type_problem == ProblemType.HFVRP or self.type_problem == ProblemType.MDVRP:
            if self.capacity_vehicle >= (request_route + self.customer_to_insert.get_request_customer()):
                request_route += self.customer_to_insert.get_request_customer()
                route.get_list_id_customers().append(self.customer_to_insert.get_id_customer())

                if len(route.get_list_id_customers()) >= 6:
                    self.three_opt.to_optimize(route)

                list_tau_costs.pop(self.pos_best_tau)
                self._delete_element(self.customer_to_insert.get_id_customer(), list_metrics_cmt_by_customer)
                self.customers_to_visit.remove(self.customer_to_insert)
            else:
                list_tau_costs.pop(self.pos_best_tau)
            return route

        elif self.type_problem == ProblemType.TTRP or self.type_problem == 4:
            if self.capacity_total >= (self.request_route + self.customer_to_insert.get_request_customer()):
                request_route += self.customer_to_insert.get_request_customer()
                route.get_list_id_customers().append(self.customer_to_insert.get_id_customer())

                if len(route.get_list_id_customers()) >= 6:
                    self.three_opt.to_optimize(route)

                list_tau_costs.remove(self.pos_best_tau)
                self._delete_element(self.customer_to_insert.get_id_customer(), list_metrics_cmt_by_customer)
                self.customers_to_visit.remove(self.customer_to_insert)

                if self.type_customer == CustomerType.VC and self.customer_to_insert.get_type_customer() == CustomerType.TC:
                    self.is_TC = True
            else:
                list_tau_costs.remove(self.pos_best_tau)
            return self.solution

    def processing(self, customers_to_visit, count_vehicles, request_route, route, id_depot, solution):
        if self.type_problem in [0, 2,
                                 3] or self.type_problem == ProblemType.CVRP or self.type_problem == ProblemType.MDVRP:
            while self.list_candidate_routes:
                self.list_metrics_cmt_by_customer = []
                self.list_metrics_cmt_by_customer = self._calculate_cost_cmt_by_customer(self.id_depot,
                                                                                         self.customers_to_visit,
                                                                                         self.list_candidate_routes)

                self.route = Route()

                self.index = self.random.randint(0, (len(self.list_candidate_routes) - 1))
                self.route = self.list_candidate_routes.pop(self.index)

                self.root_customer = self._get_customer_by_id(self.route.get_list_id_customers()[0],
                                                              self.list_root_customers)
                self.request_route = self.root_customer.get_request_customer()
                self.list_root_customers.remove(self.root_customer)
                self.route.set_id_depot(self.id_depot)

                self.list_tau_costs = []
                self.list_tau_costs = self._calculate_tau(self.list_metrics_cmt_by_customer, self.index)
                while self.list_tau_costs:
                    self.customer_to_insert = Customer()
                    self.pos_best_tau = len(self.list_tau_costs) - 1
                    self.customer_to_insert = self._get_customer_by_id(
                        self.list_tau_costs[self.pos_best_tau].get_id_element(), self.customers_to_visit)
                    self.route = self.creating(self.route, self.request_route, self.list_tau_costs,
                                               self.list_metrics_cmt_by_customer)
                self.route.set_request_route(self.request_route)
                self.solution.get_list_routes().append(self.route)
            return self.solution

        elif self.type_problem == ProblemType.HFVRP or self.type_problem == 1:
            while self.list_candidate_routes and self.list_capacities:
                list_metrics_cmt_by_customer = self._calculate_cost_cmt_by_customer(id_depot, customers_to_visit,
                                                                                    self.list_candidate_routes)

                route = Route()
                self.is_open = True

                index = self.random.randint(0, len(self.list_candidate_routes) - 1)
                route = self.list_candidate_routes.pop(index)

                root_customer = self._get_customer_by_id(route.get_list_id_customers()[0], self.list_root_customers)
                request_route = root_customer.get_request_customer()
                self.list_root_customers.remove(root_customer)
                route.set_id_depot(id_depot)

                list_tau_costs = self._calculate_tau(list_metrics_cmt_by_customer, index)

                while list_tau_costs:
                    pos_best_tau = len(list_tau_costs) - 1
                    self.customer_to_insert = self._get_customer_by_id(list_tau_costs[pos_best_tau].get_id_element(),
                                                                  customers_to_visit)

                    route = self.creating(route, request_route, list_tau_costs, list_metrics_cmt_by_customer)

                route.set_request_route(request_route)
                solution.get_list_routes().append(route)

                self.list_capacities.pop(0)
                self.is_open = False
            return self.is_open, solution

        elif self.type_problem == ProblemType.TTRP or self.type_problem == 4:
            list_access_vc = []
            while self.list_candidate_routes:
                list_metrics_CMT_by_customer = []
                list_metrics_CMT_by_customer = self._calculate_cost_cmt_by_customer(id_depot, customers_to_visit,
                                                                                    self.list_candidate_routes)

                route = Route()

                index = self.random.randint(len(self.list_candidate_routes))
                route = self.list_candidate_routes.remove(index)

                root_customer = Customer()
                root_customer = self._get_customer_by_id(route.get_list_id_customers()[0], self.list_root_customers)
                request_route = root_customer.get_request_customer()

                root_customer = CustomerTTRP(root_customer.get_id_customer(), root_customer.get_request_customer(),
                                             root_customer.get_location_customer(), self.type_customer)
                self.list_root_customers.remove(root_customer)
                route.set_id_depot(id_depot)

                if self.type_customer == CustomerType.TC:
                    capacity_total = self.capacity_vehicle
                else:
                    capacity_total = self.capacity_vehicle + self.capacity_trailer

                list_tau_costs = []
                list_tau_costs = self._calculate_tau(list_metrics_CMT_by_customer, index)

                while list_tau_costs:
                    customer_to_insert = Customer()
                    pos_best_tau = len(list_tau_costs) - 1
                    customer_to_insert = self._get_customer_by_id(list_tau_costs.get(pos_best_tau).get_id_element(),
                                                                  customers_to_visit)

                    route = self.creating(route, request_route, self.customer, self.capacity_vehicle, id_depot,
                                          solution, customers_to_visit)

                route.set_request_route(request_route)

                if self.type_customer == CustomerType.TC:
                    route = RouteTTRP(route.get_list_id_customers(), route.get_request_route(), route.get_cost_route(),
                                      route.get_id_depot(), list_access_vc, RouteType.PTR)
                else:
                    if self.is_TC:
                        route = RouteTTRP(route.get_list_id_customers(), route.get_request_route(),
                                          route.get_cost_route(), route.get_id_depot(), list_access_vc, RouteType.CVR)
                    else:
                        route = RouteTTRP(route.get_list_id_customers(), route.get_request_route(),
                                          route.get_cost_route(), route.get_id_depot(), list_access_vc, RouteType.PVR)

                solution.get_list_routes().append(route)
            return solution

    def execute(self):
        if self.type_problem == ProblemType.CVRP or self.type_problem in [0, 3]:
            while self.customers_to_visit:
                self.list_candidate_routes = self._do_first_phase(self.customers_to_visit, self.id_depot,
                                                                  self.pos_depot, self.capacity_vehicle,
                                                                  self.count_vehicles)
                self.list_root_customers = self._update_customers_to_visit(self.list_candidate_routes,
                                                                           self.customers_to_visit)
                self.solution = self.processing(self.customers_to_visit, self.count_vehicles, self.request_route,
                                                self.route, self.id_depot, self.solution)
                # break

        elif self.type_problem == ProblemType.HFVRP or self.type_problem == 1:
            self.capacity_vehicle = self.list_capacities[0]
            self.is_open = False

            while self.customers_to_visit and self.list_capacities:
                self.list_candidate_routes = self._do_first_phase(self.customers_to_visit, self.id_depot,
                                                                  self.pos_depot, self.capacity_vehicle,
                                                                  self.count_vehicles)
                self.list_root_customers = self._update_customers_to_visit(self.list_candidate_routes,
                                                                           self.customers_to_visit)
                self.is_open, self.solution = self.processing(self.customers_to_visit, self.count_vehicles,
                                                              self.request_route, self.route, self.id_depot,
                                                              self.solution)

                if self.is_open and self.customers_to_visit:
                    route.set_request_route(self.request_route)
                    route.set_id_depot(self.id_depot)
                    self.solution.get_list_routes().append(route)

                if self.customers_to_visit:
                    route = Route()
                    new_request = 0.0
                    route.set_id_depot(self.id_depot)

                    while self.customers_to_visit:
                        new_request += self.customers_to_visit[0].get_request_customer()
                        route.set_request_route(new_request)
                        route.get_list_id_customers().append(self.customers_to_visit[0].get_id_customer())
                        self.customers_to_visit.pop(0)

                    self.solution.get_list_routes().append(route)

                if self.is_open:
                    route.set_request_route(self.request_route)
                    route.set_id_depot(self.id_depot)
                    self.solution.get_list_routes().append(route)

        elif self.type_problem == ProblemType.MDVRP or self.type_problem == 2:
            for j in range(self.pos_depot, len(Problem.get_problem().get_list_depots())):
                if j != self.pos_depot:
                    id_depot = Problem.get_problem().get_list_depots()[j].get_id_depot()
                    customers_to_visit = list(Problem.get_problem().get_customers_assigned_by_id_depot(id_depot))

                    capacity_vehicle = Problem.get_problem().get_list_depots()[j].get_list_fleets()[
                        0].get_capacity_vehicle()
                    count_vehicles = Problem.get_problem().get_list_depots()[j].get_list_fleets()[
                        0].get_count_vehicles()

                while customers_to_visit:
                    self.list_candidate_routes = self._do_first_phase(customers_to_visit, id_depot, j, capacity_vehicle,
                                                                      count_vehicles)
                    self.list_root_customers = self._update_customers_to_visit(self.list_candidate_routes,
                                                                               customers_to_visit)
                    self.solution = self.processing(customers_to_visit, count_vehicles, self.request_route, self.route,
                                                    id_depot, self.solution)

        elif self.type_problem == ProblemType.TTRP or self.type_problem == 4:
            while self.customers_to_visit:
                self.is_TC = False
                self.capacity_trailer = Problem.get_problem().get_list_depots()[self.pos_depot].get_list_fleets()[
                    0].get_capacity_trailer()
                self.capacity_total = 0.0

                self.type_customer = CustomerType.TC  # ARREGLAR !!!

                self.list_candidate_routes = self._do_first_phase(customers_to_visit, id_depot, self.pos_depot,
                                                                  capacity_vehicle, count_vehicles)
                self.list_root_customers = self._update_customers_to_visit(self.list_candidate_routes,
                                                                           customers_to_visit)

                self.solution = self.processing(self.customers_to_visit, self.count_vehicles, self.request_route,
                                                self.route, self.id_depot, self.solution)

        return self.solution

    def get_solution_inicial(self):

        self.execute()

        return self.solution

    # Método que realiza la primera fase del algoritmo CMT
    def _do_first_phase(self, customers_to_visit, id_depot, pos_depot, capacity_vehicle, count_vehicles):
        list_routes = []
        list_customers = list(customers_to_visit)
        list_candidate_customers = None
        route = Route()
        request_route = 0.0

        three_opt = Operator_3opt()

        root_customer = self._get_first_customer(list_customers, self.first_customer_type, id_depot)
        request_route = root_customer.get_request_customer()
        route.get_list_id_customers().append(root_customer.get_id_customer())
        route.set_id_depot(id_depot)
        list_customers.remove(root_customer)

        type_problem = Problem.get_problem().get_type_problem()

        if type_problem in [ProblemType.CVRP, ProblemType.MDVRP]:
            if not list_customers:
                list_routes.append(route)
            else:
                while list_customers:
                    list_candidate_customers = []

                    for customer in list(list_customers):
                        metric_cmt = Metric()
                        if capacity_vehicle >= (request_route + customer.get_request_customer()):
                            metric_cmt.set_id_element(customer.get_id_customer())
                            metric_cmt.set_insertion_cost(
                                self._calculate_cost_of_cmt(id_depot, root_customer.get_id_customer(),
                                                            customer.get_id_customer()))
                            list_candidate_customers.append(metric_cmt)

                    self._ascendent_ordenate_list_without_order(list_candidate_customers)

                    while list_candidate_customers:
                        customer_to_insert = self._get_customer_by_id(list_candidate_customers[0].get_id_element(),
                                                                      list_customers)

                        if capacity_vehicle >= (request_route + customer_to_insert.get_request_customer()):
                            request_route += customer_to_insert.get_request_customer()
                            route.get_list_id_customers().append(customer_to_insert.get_id_customer())

                            if len(route.get_list_id_customers()) >= 6:
                                three_opt.to_optimize(route)

                            list_candidate_customers.pop(0)
                            list_customers.remove(customer_to_insert)
                        else:
                            list_candidate_customers.pop(0)

                    list_routes.append(route)

                    if list_customers:
                        route = Route()
                        request_route = 0.0

                        root_customer = self._get_first_customer(list_customers, self.first_customer_type, id_depot)
                        request_route = root_customer.get_request_customer()
                        route.get_list_id_customers().append(root_customer.get_id_customer())
                        route.set_id_depot(id_depot)
                        list_customers.remove(root_customer)

                        if not list_customers:
                            list_routes.append(route)

        elif type_problem == ProblemType.HFVRP:
            if not list_customers:
                list_routes.append(route)
            else:
                list_capacities = list(Problem.get_problem().get_list_capacities())
                capacity_vehicle = list_capacities[0]

                while list_customers and list_capacities:
                    list_candidate_customers = []

                    for customer in list(list_customers):
                        metric_cmt = Metric()
                        if capacity_vehicle >= (request_route + customer.get_request_customer()):
                            metric_cmt.set_id_element(customer.get_id_customer())
                            metric_cmt.set_insertion_cost(
                                self._calculate_cost_of_cmt(id_depot, root_customer.get_id_customer(),
                                                            customer.get_id_customer()))
                            list_candidate_customers.append(metric_cmt)

                    self._ascendent_ordenate_list_without_order(list_candidate_customers)

                    while list_candidate_customers:
                        customer_to_insert = self._get_customer_by_id(list_candidate_customers[0].get_id_element(),
                                                                      list_customers)

                        if capacity_vehicle >= (request_route + customer_to_insert.get_request_customer()):
                            request_route += customer_to_insert.get_request_customer()
                            route.get_list_id_customers().append(customer_to_insert.get_id_customer())
                            route.set_id_depot(id_depot)

                            if len(route.get_list_id_customers()) >= 6:
                                three_opt.to_optimize(route)

                            list_candidate_customers.pop(0)
                            list_customers.remove(customer_to_insert)
                        else:
                            list_candidate_customers.pop(0)

                    list_routes.append(route)
                    list_capacities.pop(0)

                    if list_customers:
                        route = Route()
                        request_route = 0.0

                        root_customer = self._get_first_customer(list_customers, self.first_customer_type, id_depot)
                        request_route = root_customer.get_request_customer()
                        route.get_list_id_customers().append(root_customer.get_id_customer())
                        route.set_id_depot(Problem.get_problem().get_list_depots()[pos_depot].get_id_depot())
                        list_customers.remove(root_customer)

                        if not list_capacities:
                            continue
                        else:
                            capacity_vehicle = list_capacities[0]

                        if not list_customers:
                            list_routes.append(route)

        elif type_problem == ProblemType.TTRP:
            capacity_total = 0.0
            capacity_trailer = Problem.get_problem().get_list_depots()[pos_depot].get_list_fleets()[
                0].get_capacity_trailer()

            if not list_customers:
                list_routes.append(route)
            else:
                while list_customers:
                    list_candidate_customers = []
                    type_customer = root_customer.get_type_customer()

                    if type_customer == CustomerType.TC:
                        capacity_total = capacity_vehicle
                    else:
                        capacity_total = capacity_vehicle + capacity_trailer

                    for customer in list(list_customers):
                        metric_cmt = Metric()
                        if capacity_total >= (request_route + customer.get_request_customer()):
                            metric_cmt.set_id_element(customer.get_id_customer())
                            metric_cmt.set_insertion_cost(
                                self._calculate_cost_of_cmt(id_depot, root_customer.get_id_customer(),
                                                            customer.get_id_customer()))
                            list_candidate_customers.append(metric_cmt)

                    self._ascendent_ordenate_list_without_order(list_candidate_customers)

                    while list_candidate_customers:
                        customer_to_insert = self._get_customer_by_id(list_candidate_customers[0].get_id_element(),
                                                                      list_customers)

                        if capacity_total >= (request_route + customer_to_insert.get_request_customer()):
                            request_route += customer_to_insert.get_request_customer()
                            route.get_list_id_customers().append(customer_to_insert.get_id_customer())
                            route.set_id_depot(Problem.get_problem().get_list_depots()[pos_depot].get_id_depot())

                            if len(route.get_list_id_customers()) >= 6:
                                three_opt.to_optimize(route)

                            list_candidate_customers.pop(0)
                            list_customers.remove(customer_to_insert)
                        else:
                            list_candidate_customers.pop(0)

                    list_routes.append(route)

                    if list_customers:
                        route = Route()
                        request_route = 0.0

                        root_customer = self._get_first_customer(list_customers, self.first_customer_type, id_depot)
                        request_route = root_customer.get_request_customer()
                        route.get_list_id_customers().append(root_customer.get_id_customer())
                        route.set_id_depot(Problem.get_problem().get_list_depots()[pos_depot].get_id_depot())
                        list_customers.remove(root_customer)

                        if not list_customers:
                            list_routes.append(route)

        self._empty_routes(list_routes)
        return list_routes

    # Método que calcula el costo de insertar un cliente en la ruta
    def _calculate_cost_of_cmt(self, id_depot, current_element, next_element):
        cost_depot_to_next = Problem.get_problem().get_cost_matrix()[
            Problem.get_problem().get_pos_element(id_depot), Problem.get_problem().get_pos_element(next_element)]
        cost_next_to_current = Problem.get_problem().get_cost_matrix()[
            Problem.get_problem().get_pos_element(next_element), Problem.get_problem().get_pos_element(current_element)]

        return (cost_depot_to_next + (self.parameter_l * cost_next_to_current))

    # Método que vacia la lista de rutas dejando solo el primer cliente en cada una
    def _empty_routes(self, list_routes):
        for i in range(len(list_routes)):
            j = 1

            while j < len(list_routes[i].get_list_id_customers()):
                list_routes[i].get_list_id_customers().pop(j)

    # Método que devuelve en una lista los clientes a eliminar que ya pertenecen a una ruta
    def _update_customers_to_visit(self, list_routes, customers_to_visit):
        """
        Actualiza la lista de clientes a visitar, eliminando aquellos que ya están en las rutas dadas.

        :param list_routes: Lista de rutas, donde cada ruta contiene una lista de IDs de clientes.
        :param customers_to_visit: Lista de clientes a visitar.
        :return: Lista de clientes raíz que se han eliminado de la lista de clientes a visitar.
        """
        list_root_customers = []

        for route in list_routes:
            root_customer_id = route.get_list_id_customers()[0]
            for customer in customers_to_visit:
                if customer.get_id_customer() == root_customer_id:
                    list_root_customers.append(customer)
                    customers_to_visit.remove(customer)
                    break  # Salir del bucle una vez que se ha encontrado y eliminado el cliente

        return list_root_customers

    # Método que retorna la lista ordenada con los costos CMT en cada ruta para cada cliente
    def _calculate_cost_cmt_by_customer(self, id_depot, list_customers, list_routes):
        list_metrics_cmt_by_customer = []

        for i in range(len(list_customers)):
            list_metric_cmt = []

            for j in range(len(list_routes)):
                metric_cmt = Metric()
                metric_cmt.set_id_element(list_customers[i].get_id_customer())
                metric_cmt.set_insertion_cost(
                    self._calculate_cost_of_cmt(id_depot, list_routes[j].get_list_id_customers()[0],
                                                list_customers[i].get_id_customer()))
                metric_cmt.set_index(j)
                list_metric_cmt.append(metric_cmt)

            if len(list_routes) > 1:
                self._ascendent_ordenate_list_without_order(list_metric_cmt)

            list_metrics_cmt_by_customer.append(list_metric_cmt)

        return list_metrics_cmt_by_customer

    # Método que devuelve listado de clientes con el TAU calculado y ordenado
    def _calculate_tau(self, list_metrics_cmt_by_customer, pos_route):
        list_tau_costs = []
        first_cost = 0.0
        second_cost = 0.0

        for i in range(len(list_metrics_cmt_by_customer)):
            j = 0

            if list_metrics_cmt_by_customer[i][0].get_index() == pos_route:
                metric_cmt = Metric()
                metric_cmt.set_id_element(list_metrics_cmt_by_customer[i][j].get_id_element())

                first_cost = list_metrics_cmt_by_customer[i][j].get_insertion_cost()

                if len(list_metrics_cmt_by_customer[i]) > 1:
                    second_cost = list_metrics_cmt_by_customer[i][j + 1].get_insertion_cost()
                    tau_cost = second_cost - first_cost
                else:
                    tau_cost = first_cost

                metric_cmt.set_insertion_cost(tau_cost)

                list_tau_costs.append(metric_cmt)

        if len(list_tau_costs) > 1:
            self._ascendent_ordenate_list_without_order(list_tau_costs)

        return list_tau_costs

    # Método que elimina un cliente de la lista ordenada de los costos
    def _delete_element(self, id_customer, list_metrics_cmt_by_customer):
        deleted = False
        i = 0

        while i < len(list_metrics_cmt_by_customer) and not deleted:
            if list_metrics_cmt_by_customer[i][0].get_id_element() == id_customer:
                list_metrics_cmt_by_customer.pop(i)
                deleted = True
            else:
                i += 1
