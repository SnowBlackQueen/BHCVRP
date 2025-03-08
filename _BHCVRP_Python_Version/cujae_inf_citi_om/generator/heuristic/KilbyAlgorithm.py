from generator.heuristic.Heuristic import Heuristic
from data.Problem import Problem
from data.ProblemType import ProblemType
from generator.heuristic.Metric import Metric
from solution.Route import Route
from solution.RouteType import RouteType
from solution.RouteTTRP import RouteTTRP
from data.Customer import Customer
from data.CustomerType import CustomerType
from data.CustomerTTRP import CustomerTTRP
from data.BusStop import BusStop
from generator.postoptimization.Operator_3opt import Operator_3opt


class KilbyAlgorithm(Heuristic):

    def __init__(self):
        super().__init__()

    def initialize_specifics(self):
        self.list_candidate_routes = []
        self.list_kilby_costs = None

        self.count_trailers = 0
        self.type_customer = CustomerType.TC
        self.list_access_vc = []

        if Problem.get_problem().get_type_problem() == ProblemType.TTRP:
            self.count_trailers = (
                Problem.get_problem()
                .get_list_depots()[self.pos_depot]
                .get_list_fleets()[0]
                .get_count_trailers()
            )

        elif Problem.get_problem().get_type_problem() == ProblemType.HFVRP:
            self.count_vehicles = len(
                Problem.get_problem().fill_list_capacities(self.pos_depot)
            )
        else:
            self.count_vehicles = (
                Problem.get_problem()
                .get_list_depots()[self.pos_depot]
                .get_list_fleets()[0]
                .get_count_vehicles()
            )

        self.three_opt = Operator_3opt()
        # Operator_2opt stepOptimizacion1 = new Operator_2opt();
        # Operator_Relocate stepOptimizacion2 = new Operator_Relocate();
        # Operator_Exchange stepOptimizacion3 = new Operator_Exchange();

        self.metric_kilby = None
        self.pos_route = -1
        self.is_route_full = True
        self.routes_with_elements = 0

        for i in range(self.count_vehicles):
            if self.type_problem == 4 or self.type_problem == ProblemType.TTRP:
                self.route = RouteTTRP()
            else:
                self.route = Route()
            self.list_candidate_routes.append(self.route)

        self.list_route_opt = []

    def creating(
        self, route=None, request_route=None, list_tau=None, list_metrics=None
    ):
        if (
            self.type_problem in [0, 1, 2, 3, 4, 5, 6]
            or self.type_problem == ProblemType.CVRP
            or self.type_problem == ProblemType.OVRP
            or self.type_problem == ProblemType.HFVRP
            or self.type_problem == ProblemType.MDVRP
            or self.type_problem == ProblemType.TTRP
            or self.type_problem == ProblemType.SBRP
            or self.type_problem == ProblemType.VRPTW
        ):
            print("entra a creating")
            while self.list_kilby_costs:
                i = 0
                while i < len(self.list_candidate_routes) and self.list_kilby_costs:
                    if self.type_problem == ProblemType.SBRP:
                        self.bus_stop = BusStop()
                        self.bus_stop = self._get_element_by_id(
                            self.list_kilby_costs[0].get_id_element(),
                            self.list_bus_stops,
                        )
                        self.request_route = self.bus_stop.get_capacity_bus_stop()

                        self.list_candidate_routes[i].get_list_bus_stops().append(
                            self.bus_stop
                        )
                    else:
                        self.customer = Customer()
                        self.customer = self._get_element_by_id(
                            self.list_kilby_costs[0].get_id_element(),
                            self.customers_to_visit,
                        )
                        self.request_route = self.customer.get_request_customer()

                        self.list_candidate_routes[i].get_list_id_customers().append(
                            self.customer.get_id_customer()
                        )

                    self.list_candidate_routes[i].set_request_route(self.request_route)
                    self.list_candidate_routes[i].set_id_depot(self.id_depot)
                    self.list_kilby_costs.pop(0)

                    if self.type_problem == ProblemType.SBRP:
                        self.list_bus_stops.remove(self.bus_stop)
                    else:
                        self.customers_to_visit.remove(self.customer)
                    self.routes_with_elements += 1

                    if self.type_problem == ProblemType.TTRP:
                        if (
                            self.customer.get_type_customer() == CustomerType.TC
                            or self.customer.get_type_customer() == 1
                        ):
                            self.capacity_total = self.capacity_vehicle
                        else:
                            self.capacity_total = (
                                self.capacity_vehicle + self.capacity_trailer
                            )

                    i += 1

                    if self.type_problem == ProblemType.HFVRP:
                        self.is_open = True

            j = self.routes_with_elements
            # print("creating1")

            while self.routes_with_elements < len(self.list_candidate_routes):
                self.list_candidate_routes.pop(j)
            # print("creating2")
            print("termina creating")

    def processing(
        self,
        customers_to_visit=None,
        count_vehicles=None,
        request_route=None,
        route=None,
        id_depot=None,
        solution=None,
    ):
        if self.type_problem == 5 or self.type_problem == ProblemType.SBRP:
            while self.list_candidate_routes and self.list_bus_stops:
                self.metric_kilby = Metric()
                self.metric_kilby = self.get_best_element(
                    self.id_depot,
                    self.list_bus_stops,
                    self.list_candidate_routes,
                    self.capacity_vehicle,
                    self.count_trailers,
                )

                if self.metric_kilby is None:
                    self.pos_route = self.close_route(self.list_candidate_routes)
                    self.is_route_full = False
                else:
                    bus_stop_insert = BusStop()
                    bus_stop_insert = self._get_element_by_id(
                        self.metric_kilby.get_id_element(), self.list_bus_stops
                    )

                    self.pos_route = self.metric_kilby.get_index()
                    self.request_route = (
                        self.list_candidate_routes[
                            self.metric_kilby.get_index()
                        ].get_request_route()
                        + bus_stop_insert.get_capacity_bus_stop()
                    )

                    self.list_candidate_routes[
                        self.pos_route
                    ].get_list_bus_stops().append(bus_stop_insert)
                    self.list_candidate_routes[self.pos_route].set_request_route(
                        self.request_route
                    )
                    self.list_candidate_routes[self.pos_route].set_id_depot(
                        self.id_depot
                    )
                    self.list_bus_stops.remove(bus_stop_insert)

                    self.is_route_full = self.request_perfect(
                        self.list_bus_stops,
                        self.capacity_vehicle,
                        self.request_route,
                    )

                if not self.is_route_full:
                    # if len(self.list_candidate_routes[self.pos_route].get_list_id_customers()) >= 6:
                    #   self.three_opt.to_optimize(self.list_candidate_routes[self.pos_route])
                    self.list_route_opt.append(
                        self.list_candidate_routes[self.pos_route]
                    )
                    self.list_candidate_routes.pop(self.pos_route)

            while self.list_candidate_routes:
                self.pos_route = 0
                # if len(self.list_candidate_routes[self.pos_route].get_list_id_customers()) >= 6:
                #   self.three_opt.to_optimize(self.list_candidate_routes[self.pos_route])
                self.list_route_opt.append(self.list_candidate_routes[self.pos_route])
                self.list_candidate_routes.pop(self.pos_route)

        else:
            print("entra a processing")
            while self.list_candidate_routes and self.customers_to_visit:
                self.metric_kilby = Metric()
                self.metric_kilby = self.get_best_element(
                    self.id_depot,
                    self.customers_to_visit,
                    self.list_candidate_routes,
                    self.capacity_vehicle,
                    self.count_trailers,
                )
                print("sale de get_best_element")

                if self.metric_kilby is None:
                    self.pos_route = self.close_route(self.list_candidate_routes)
                    self.is_route_full = False
                else:
                    customer_insert = Customer()
                    customer_insert = self._get_element_by_id(
                        self.metric_kilby.get_id_element(), self.customers_to_visit
                    )

                    self.pos_route = self.metric_kilby.get_index()
                    self.request_route = (
                        self.list_candidate_routes[
                            self.metric_kilby.get_index()
                        ].get_request_route()
                        + customer_insert.get_request_customer()
                    )

                    self.list_candidate_routes[
                        self.pos_route
                    ].get_list_id_customers().append(customer_insert.get_id_customer())
                    self.list_candidate_routes[self.pos_route].set_request_route(
                        self.request_route
                    )
                    self.list_candidate_routes[self.pos_route].set_id_depot(
                        self.id_depot
                    )
                    self.customers_to_visit.remove(customer_insert)

                    self.is_route_full = self.request_perfect(
                        self.customers_to_visit,
                        self.capacity_vehicle,
                        self.request_route,
                    )

                    if self.type_problem == 4 or self.type_problem == ProblemType.TTRP:
                        # Verificar si va aquí
                        if (
                            self.customer.get_type_customer() == CustomerType.VC
                            and customer_insert.get_type_customer() == CustomerType.TC
                            or self.customer.get_type_customer() == 0
                            and customer_insert.get_type_customer() == 1
                        ):
                            self.is_TC = True

                # Verificar si va aquí
                if self.type_problem == 4 or self.type_problem == ProblemType.TTRP:
                    if (
                        self.customer.get_type_customer() == CustomerType.TC
                        or self.customer.get_type_customer() == 1
                    ):
                        self.route = RouteTTRP(
                            list_id_customers=self.list_candidate_routes[
                                self.pos_route
                            ].get_list_id_customers(),
                            request_route=self.request_route,
                            cost_route=self.list_candidate_routes[
                                self.pos_route
                            ].get_cost_route(),
                            id_depot=self.id_depot,
                            list_access_vc=self.list_access_vc,
                            maximum_distance=None,
                            type_route=RouteType.PTR,
                        )
                    else:
                        if self.is_TC:
                            self.route = RouteTTRP(
                                self.list_candidate_routes[
                                    self.pos_route
                                ].get_list_id_customers(),
                                self.request_route,
                                self.list_candidate_routes[
                                    self.pos_route
                                ].get_cost_route(),
                                self.id_depot,
                                self.list_access_vc,
                                None,
                                RouteType.CVR,
                            )
                        else:
                            self.route = RouteTTRP(
                                self.list_candidate_routes[
                                    self.pos_route
                                ].get_list_id_customers(),
                                self.request_route,
                                self.list_candidate_routes[
                                    self.pos_route
                                ].get_cost_route(),
                                self.id_depot,
                                self.list_access_vc,
                                None,
                                RouteType.PVR,
                            )

                if not self.is_route_full:
                    # if len(self.list_candidate_routes[self.pos_route].get_list_id_customers()) >= 6:
                    #   self.three_opt.to_optimize(self.list_candidate_routes[self.pos_route])
                    self.list_route_opt.append(
                        self.list_candidate_routes[self.pos_route]
                    )
                    self.list_candidate_routes.pop(self.pos_route)

                    # if listCandidateRoutes[posRoute].getListIdCustomers().size() >= 4:
                    #     stepOptimizacion1.stepOptimizacion(listCandidateRoutes[posRoute], variant)
                    #
                    # if listCandidateRoutes[posRoute].getListIdCustomers().size() >= 2:
                    #     stepOptimizacion2.stepOptimizacion(listCandidateRoutes[posRoute], variant)
                    #     stepOptimizacion3.stepOptimizacion(listCandidateRoutes[posRoute], variant)
                    #
                    # listRouteOpt.append(listCandidateRoutes[posRoute])
                    # routesCandidates.remove(posRoute)

                if self.type_problem == 4 or self.type_problem == ProblemType.TTRP:
                    if not self.list_candidate_routes:
                        for i in range(self.count_vehicles):
                            self.route = RouteTTRP()
                            self.list_candidate_routes.append(self.route)
                        self.list_kilby_costs = self.select_best_cost(
                            self.count_vehicles,
                            self.count_trailers,
                            self.id_depot,
                            self.customers_to_visit,
                        )
                        self.creating()
                print("processing1")

            while self.list_candidate_routes:
                self.pos_route = 0
                # if len(self.list_candidate_routes[self.pos_route].get_list_id_customers()) >= 6:
                #   self.three_opt.to_optimize(self.list_candidate_routes[self.pos_route])
                self.list_route_opt.append(self.list_candidate_routes[self.pos_route])
                self.list_candidate_routes.pop(self.pos_route)

                # if listCandidateRoutes[posRoute].getListIdCustomers().size() >= 4:
                #     stepOptimizacion1.stepOptimizacion(listCandidateRoutes[posRoute], variant)
                #
                # if listCandidateRoutes[posRoute].getListIdCustomers().size() >= 2:
                #     stepOptimizacion2.stepOptimizacion(listCandidateRoutes[posRoute], variant)
                #     stepOptimizacion3.stepOptimizacion(listCandidateRoutes[posRoute], variant)
                #
                # listRouteOpt.append(listCandidateRoutes[posRoute])
                # listCandidateRoutes.remove(posRoute)
            print("termina processing")

    def execute(self):
        if self.type_problem in [0, 3] or self.type_problem == ProblemType.CVRP or self.type_problem == ProblemType.OVRP or self.type_problem == 5 or self.type_problem == ProblemType.SBRP or self.type_problem == ProblemType.VRPTW or self.type_problem == 6:
            if self.type_problem == ProblemType.SBRP:
                if self.list_bus_stops:
                    self.list_kilby_costs = []
                    self.list_kilby_costs = self.select_best_cost(
                        self.count_vehicles,
                        self.count_trailers,
                        self.id_depot,
                        self.list_bus_stops,
                    )

                    self.creating()

                    self.processing(
                        self.list_bus_stops,
                        self.count_vehicles,
                        self.request_route,
                        self.route,
                        self.id_depot,
                        self.solution,
                    )
            else:
                if self.customers_to_visit:
                    self.list_kilby_costs = []
                    self.list_kilby_costs = self.select_best_cost(
                        self.count_vehicles,
                        self.count_trailers,
                        self.id_depot,
                        self.customers_to_visit,
                    )

                    print("entra al execute, va para creating")
                    self.creating()

                    print("va pal processing")
                    self.processing(
                        self.customers_to_visit,
                        self.count_vehicles,
                        self.request_route,
                        self.route,
                        self.id_depot,
                        self.solution,
                    )
                    print("termina processing")

            self.solution.set_list_routes(self.list_route_opt)
            print("devuelve la solución")

        elif self.type_problem == 1 or self.type_problem == ProblemType.HFVRP:
            list_capacities = list(Problem.get_problem().get_list_capacities())
            self.capacity_vehicle = list_capacities[0]
            is_open = True

            if self.customers_to_visit:
                self.list_kilby_costs = []
                self.list_kilby_costs = self.select_best_cost(
                    self.count_vehicles,
                    self.count_trailers,
                    self.id_depot,
                    self.customers_to_visit,
                )

                self.creating()

                self.processing()

                while self.list_candidate_routes:
                    self.pos_route = 0
                    if (
                        len(
                            self.list_candidate_routes[
                                self.pos_route
                            ].get_list_id_customers()
                        )
                        >= 6
                    ):
                        self.three_opt.to_optimize(
                            self.list_candidate_routes[self.pos_route]
                        )
                    self.list_route_opt.append(
                        self.list_candidate_routes[self.pos_route]
                    )
                    self.list_candidate_routes.remove(self.pos_route)

            self.solution.set_list_routes(self.list_route_opt)
            # Verificar
            list_capacities.pop(0)
            is_open = False

            if is_open and self.customers_to_visit:
                self.route.set_request_route(self.request_route)
                self.route.set_id_depot(self.id_depot)
                self.solution.get_list_routes().append(self.route)

            if self.customers_to_visit:
                self.route = Route()
                new_request = 0.0
                self.route.set_id_depot(self.id_depot)

                while self.customers_to_visit:
                    new_request += self.customers_to_visit[0].get_request_customer()
                    self.route.set_request_route(new_request)
                    self.route.get_list_id_customers().append(
                        self.customers_to_visit[0].get_id_customer()
                    )
                    self.customers_to_visit.pop(0)

                self.solution.get_list_routes().append(self.route)

            if is_open:
                self.route.set_request_route(self.request_route)
                self.route.set_id_depot(self.id_depot)
                self.solution.get_list_routes().append(self.route)

        elif self.type_problem == 2 or self.type_problem == ProblemType.MDVRP:
            for j in range(
                self.pos_depot, len(Problem.get_problem().get_list_depots())
            ):
                print("first")
                if j != self.pos_depot:
                    self.id_depot = (
                        Problem.get_problem().get_list_depots()[j].get_id_depot()
                    )
                    self.customers_to_visit = list(
                        Problem.get_problem().get_customers_assigned_by_id_depot(
                            self.id_depot,
                            Problem.get_problem().get_list_customers(),
                            Problem.get_problem().get_list_depots(),
                        )
                    )

                    self.capacity_vehicle = (
                        Problem.get_problem()
                        .get_list_depots()[j]
                        .get_list_fleets()[0]
                        .get_capacity_vehicle()
                    )
                    self.count_vehicles = (
                        Problem.get_problem()
                        .get_list_depots()[j]
                        .get_list_fleets()[0]
                        .get_count_vehicles()
                    )

                if self.customers_to_visit:
                    self.list_kilby_costs = []
                    self.list_kilby_costs = self.select_best_cost(
                        self.count_vehicles,
                        self.count_trailers,
                        self.id_depot,
                        self.customers_to_visit,
                    )

                    self.creating()

                    self.processing()

                    print("asd")
                self.solution.set_list_routes(self.list_route_opt)
                print("solution")

                for i in range(self.count_vehicles):
                    self.route = Route()
                    self.list_candidate_routes.append(self.route)

            print("Fin")

        elif self.type_problem == 4 or self.type_problem == ProblemType.TTRP:
            self.list_access_vc = []
            if self.customers_to_visit:
                self.is_TC = False
                self.capacity_trailer = (
                    Problem.get_problem()
                    .get_list_depots()[self.pos_depot]
                    .get_list_fleets()[0]
                    .get_capacity_trailer()
                )
                self.capacity_total = 0.0
                self.type_customer = CustomerType.TC

                self.list_kilby_costs = []
                self.list_kilby_costs = self.select_best_cost(
                    self.count_vehicles,
                    self.count_trailers,
                    self.id_depot,
                    self.customers_to_visit,
                )

                self.creating()

                self.processing()

            self.solution.set_list_routes(self.list_route_opt)

    def get_solution_inicial(self):

        self.execute()

        return self.solution

    # Método que devuelve una lista de los n mejores para las n rutas
    def select_best_cost(self, count_vehicles, count_trailers, id_depot, list_element):
        list_kilby_costs = []
        metric_kilby = None
        cost_kilby = 0.0

        count_routes_pvr = count_trailers
        count_routes_ptr = count_vehicles - count_trailers
        type_customer = None

        for i in range(len(list_element)):
            metric_kilby = Metric()

            if Problem.get_problem().get_type_problem() == ProblemType.SBRP:
                cost_kilby = self.calculate_cost_of_kilby(
                    id_depot, id_depot, list_element[i].get_id_bus_stop()
                )

                if len(list_kilby_costs) < count_vehicles:
                    metric_kilby.set_id_element(list_element[i].get_id_bus_stop())
                    metric_kilby.set_insertion_cost(cost_kilby)
                    list_kilby_costs.append(metric_kilby)

                else:
                    pos_max_cost = self.find_max_cost(
                        list_kilby_costs, list_element, type_customer
                    )

                    if cost_kilby < list_kilby_costs[pos_max_cost].get_insertion_cost():
                        metric_kilby.set_id_element(list_element[i].get_id_bus_stop())
                        metric_kilby.set_insertion_cost(cost_kilby)

                        list_kilby_costs.pop(pos_max_cost)
                        list_kilby_costs.append(metric_kilby)
            else:
                if isinstance(list_element[i], CustomerTTRP):
                    type_customer = list_element[i].get_type_customer()
                else:
                    type_customer = CustomerType.TC

                cost_kilby = self.calculate_cost_of_kilby(
                    id_depot, id_depot, list_element[i].get_id_customer()
                )

                if len(list_kilby_costs) < count_vehicles:
                    if (
                        (
                            type_customer == CustomerType.VC
                            or type_customer == CustomerType.VC.value
                        )
                        and count_routes_pvr != 0
                    ) or (
                        (
                            type_customer == CustomerType.TC
                            or type_customer == CustomerType.TC.value
                        )
                        and count_routes_ptr != 0
                    ):
                        metric_kilby.set_id_element(list_element[i].get_id_customer())
                        metric_kilby.set_insertion_cost(cost_kilby)

                        list_kilby_costs.append(metric_kilby)

                        if (
                            type_customer == CustomerType.VC
                            or type_customer == CustomerType.VC.value
                        ):
                            count_routes_pvr -= 1
                        else:
                            count_routes_ptr -= 1
                else:
                    pos_max_cost = self.find_max_cost(
                        list_kilby_costs, list_element, type_customer
                    )

                    if cost_kilby < list_kilby_costs[pos_max_cost].get_insertion_cost():
                        metric_kilby.set_id_element(list_element[i].get_id_customer())
                        metric_kilby.set_insertion_cost(cost_kilby)

                        list_kilby_costs.pop(pos_max_cost)
                        list_kilby_costs.append(metric_kilby)

        return list_kilby_costs

    # Método que calcula el costo de insertar un cliente en la ruta
    def calculate_cost_of_kilby(self, id_depot, current_element, next_element):
        #if Problem.get_problem().get_type_problem() == ProblemType.SBRP:
         #   current_element = current_element[0].get_id_bus_stop()

        cost_actual_to_next = Problem.get_problem().get_cost_matrix()[
            Problem.get_problem().get_pos_element(current_element),
            Problem.get_problem().get_pos_element(next_element),
        ]
        cost_next_to_depot = Problem.get_problem().get_cost_matrix()[
            Problem.get_problem().get_pos_element(next_element),
            Problem.get_problem().get_pos_element(id_depot),
        ]
        cost_actual_to_depot = Problem.get_problem().get_cost_matrix()[
            Problem.get_problem().get_pos_element(current_element),
            Problem.get_problem().get_pos_element(id_depot),
        ]

        return cost_actual_to_next + cost_next_to_depot - cost_actual_to_depot

    # Método que devuelve la posición del mayor costo de la lista
    def find_max_cost(self, list_kilby_costs, list_elements, type_customer):
        pos_max_cost = -1
        max_cost = 0.0
        current_cost = 0.0
        current_type_customer = None

        case = Problem.get_problem().get_type_problem()

        if case in [0, 1, 2, 3, 5]:
            pos_max_cost = 0
            max_cost = list_kilby_costs[pos_max_cost].get_insertion_cost()

            for i in range(1, len(list_kilby_costs)):
                current_cost = list_kilby_costs[i].get_insertion_cost()

                if max_cost < current_cost:
                    max_cost = current_cost
                    pos_max_cost = i

        elif case == 4:
            pos_max_cost = self.find_first_customer_equals_access(
                type_customer, list_kilby_costs, list_elements
            )
            max_cost = list_kilby_costs[pos_max_cost].get_insertion_cost()

            for i in range(pos_max_cost + 1, len(list_kilby_costs)):
                current_cost = list_kilby_costs[i].get_insertion_cost()
                current_type_customer = self.get_customer_by_id(
                    list_kilby_costs[i].get_id_element(), list_elements
                ).get_type_customer()

                if max_cost < current_cost and current_type_customer == type_customer:
                    max_cost = current_cost
                    pos_max_cost = i

        return pos_max_cost

    # Método que devuelve la posición del primer cliente con un acceso dado
    def find_first_customer_equals_access(
        self, type_customer, list_kilby_costs, list_customers
    ):
        i = 0
        found = False
        new_type_customer = None
        pos = -1

        while i < len(list_kilby_costs) and not found:
            new_type_customer = self.get_customer_by_id(
                list_kilby_costs[i].get_id_element(), list_customers
            ).get_type_customer()

            if new_type_customer == type_customer:
                pos = i
                found = True

            i += 1

        return pos

    # Método que devuelve el mejor cliente
    def get_best_element(
        self, id_depot, list_element, list_routes, capacity_truck, capacity_trailer
    ):
        best_metric_kilby = None

        best_cost = 0.0
        best_id_element = -1
        best_route = -1
        current_cost = 0.0
        request_route = 0.0
        request_analice = 0.0
        total_capacity = 0.0
        found = False
        i = 0

        print("entra al get_best_element")
        while i < len(list_element) and not found:
            if (
                Problem.get_problem().get_type_problem() == ProblemType.CVRP
                or Problem.get_problem().get_type_problem() == ProblemType.OVRP
                or Problem.get_problem().get_type_problem() == ProblemType.HFVRP
                or Problem.get_problem().get_type_problem() == ProblemType.OVRP
                or Problem.get_problem().get_type_problem() == ProblemType.MDVRP
                or Problem.get_problem().get_type_problem() == ProblemType.SBRP
                or Problem.get_problem().get_type_problem() == ProblemType.VRPTW
                or (
                    Problem.get_problem().get_type_problem() == ProblemType.TTRP
                    and isinstance(list_routes[0], RouteTTRP)
                    and list_routes[0]._type_route == 0
                    or list_routes[0]._type_route == RouteType.PTR
                )
            ):
                total_capacity = capacity_truck
            else:
                total_capacity = capacity_truck + capacity_trailer

            j = 0
            while j < len(list_routes) and not found:
                if Problem.get_problem().get_type_problem() == ProblemType.SBRP:
                    if (
                        list_routes[j].get_request_route()
                        + list_element[i].get_capacity_bus_stop()
                        <= total_capacity
                    ):
                        best_id_element = list_element[i].get_id_bus_stop()
                        best_cost = self.calculate_cost_of_kilby(
                            id_depot,
                            list_routes[0].get_list_bus_stops()[0],
                            list_element[0].get_id_bus_stop(),
                        )
                        best_route = j
                        found = True
                    else:
                        j += 1
                else:
                    if (
                        list_routes[j].get_request_route()
                        + list_element[i].get_request_customer()
                        <= total_capacity
                    ):
                        tw_flag = True
                        if self.type_problem == ProblemType.VRPTW:
                            print("entra a TW")
                            self.time_route = self.get_time_route(list_routes[j].get_list_id_customers())
                            self.feasible_customers = self.get_feasible_customers(
                                list_routes[j].get_list_id_customers()[-1])
                            if list_element[i] in self.feasible_customers:
                                time_matrix = Problem.get_problem().get_time_matrix()
                                current_time = time_matrix[
                                    list_routes[j].get_list_id_customers()[-1], list_element[i].get_id_customer()]
                                customer_ready_time = list_element[i].get_time_window().get_initial_node()
                                customer_service_time = list_element[i].get_time_window().get_service_time()
                                self.time_route = max(current_time, customer_ready_time) + customer_service_time
                                print("tw")
                            else:
                                tw_flag = False
                                best_cost = self.calculate_cost_of_kilby(
                                    id_depot,
                                    list_routes[0].get_list_id_customers()[0],
                                    list_element[0].get_id_customer(),
                                )
                                j += 1
                        if tw_flag:
                            best_id_element = list_element[i].get_id_customer()
                            best_cost = self.calculate_cost_of_kilby(
                                id_depot,
                                list_routes[0].get_list_id_customers()[0],
                                list_element[0].get_id_customer(),
                            )
                            best_route = j
                            found = True
                    else:
                        j += 1

            i += 1

        for k in range(len(list_element)):
            for l in range(
                len(list_routes)
            ):  # this loop started at 1, had to change it
                if (
                    Problem.get_problem().get_type_problem() == ProblemType.CVRP
                    or Problem.get_problem().get_type_problem() == ProblemType.OVRP
                    or Problem.get_problem().get_type_problem() == ProblemType.HFVRP
                    or Problem.get_problem().get_type_problem() == ProblemType.OVRP
                    or Problem.get_problem().get_type_problem() == ProblemType.MDVRP
                    or Problem.get_problem().get_type_problem() == ProblemType.SBRP
                    or Problem.get_problem().get_type_problem() == ProblemType.VRPTW
                    or (
                        Problem.get_problem().get_type_problem() == ProblemType.TTRP
                        and isinstance(list_routes[l], RouteTTRP)
                        and list_routes[l]._type_route == 0
                        or list_routes[l]._type_route == RouteType.PTR
                    )
                ):
                    total_capacity = capacity_truck
                else:
                    total_capacity = capacity_truck + capacity_trailer

                request_route = list_routes[l].get_request_route()

                if Problem.get_problem().get_type_problem() == ProblemType.SBRP:
                    current_cost = self.calculate_cost_of_kilby(
                        id_depot,
                        list_routes[l].get_list_bus_stops()[0],
                        list_element[k].get_id_bus_stop(),
                    )
                    request_analice = (
                            request_route + list_element[k].get_capacity_bus_stop()
                    )
                else:
                    current_cost = self.calculate_cost_of_kilby(
                        id_depot,
                        list_routes[l].get_list_id_customers()[0],
                        list_element[k].get_id_customer(),
                    )
                    request_analice = (
                            request_route + list_element[k].get_request_customer()
                    )

                if current_cost < best_cost and request_analice <= total_capacity:
                    best_cost = current_cost
                    if Problem.get_problem().get_type_problem() == ProblemType.SBRP:
                        best_id_element = list_element[k].get_id_bus_stop()
                    else:
                        best_id_element = list_element[k].get_id_customer()
                    best_route = l

        if found:
            best_metric_kilby = Metric()
            best_metric_kilby.set_id_element(best_id_element)
            best_metric_kilby.set_insertion_cost(best_cost)
            best_metric_kilby.set_index(best_route)

        return best_metric_kilby

    # Método que devuelve la ruta con demanda más cercana a la capacidad
    def close_route(self, list_routes):
        pos_route = 0

        max_capacity = list_routes[0].get_request_route()

        for i in range(1, len(list_routes)):
            if list_routes[i].get_request_route() > max_capacity:
                max_capacity = list_routes[i].get_request_route()
                pos_route = i

        return pos_route

    # Método que determina si una ruta está llena
    def request_perfect(self, elements_to_visit, capacity_total, request_route):
        pass_val = False
        ideal_request = capacity_total - request_route

        if ideal_request != 0:
            i = 0

            while i < len(elements_to_visit) and not pass_val:
                if Problem.get_problem().get_type_problem() == ProblemType.SBRP:
                    if elements_to_visit[i].get_capacity_bus_stop() <= ideal_request:
                        pass_val = True
                    else:
                        i += 1
                else:
                    if elements_to_visit[i].get_request_customer() <= ideal_request:
                        pass_val = True
                    else:
                        i += 1

        return pass_val
