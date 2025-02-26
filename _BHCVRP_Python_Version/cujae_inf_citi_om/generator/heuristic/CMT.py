from generator.heuristic.Heuristic import Heuristic
from data.Problem import Problem
from generator.heuristic.Metric import Metric
from data.Customer import Customer
from data.BusStop import BusStop
from solution.Route import Route
from generator.postoptimization.Operator_3opt import Operator_3opt
from data.CustomerType import CustomerType
from data.ProblemType import ProblemType
from random import Random
from solution.RouteTTRP import RouteTTRP
from solution.RouteType import RouteType
from generator.heuristic.FirstElementType import FirstElementType


class CMT(Heuristic):
    parameter_l = 1
    first_element_type = FirstElementType.Random

    def __init__(self):
        super().__init__()

    def initialize_specifics(self):
        if self.parameter_l <= 0:
            self.parameter_l = 1

        self.list_candidate_routes = []

        self.three_opt = Operator_3opt()

        self.random = Random()
        self.index = -1

        self.list_root_elements = []
        self.list_metrics_cmt_by_element = None
        self.list_tau_costs = None
        self.route = None
        self.root_element = None
        self.element_to_insert = None
        self.request_route = 0.0
        self.pos_best_tau = -1

        if self.type_problem == ProblemType.HFVRP or self.type_problem == 1:
            self.list_capacities = list(Problem.get_problem().get_list_capacities())

    def creating(
        self,
        route=None,
        request_route=None,
        list_tau_costs=None,
        list_metrics_cmt_by_customer=None,
    ):
        if (
            self.type_problem in [0, 1, 2, 3, 5]
            or self.type_problem == ProblemType.CVRP
            or self.type_problem == ProblemType.HFVRP
            or self.type_problem == ProblemType.MDVRP
            or self.type_problem == ProblemType.SBRP
        ):
            if self.type_problem == ProblemType.SBRP or self.type_problem == 5:
                if self.capacity_vehicle >= (
                        request_route + self.bus_stop.get_capacity_bus_stop()
                ):
                    request_route += self.bus_stop.get_capacity_bus_stop()
                    route.get_list_bus_stops().append(self.bus_stop.get_id_bus_stop())

                    # if len(route.get_list_id_customers()) >= 6:
                    #   self.three_opt.to_optimize(route)

                    list_tau_costs.pop(self.pos_best_tau)
                    self._delete_element(
                        self.bus_stop.get_id_bus_stop(),
                        list_metrics_cmt_by_customer,
                    )
                    self.list_bus_stops.remove(self.element_to_insert)
                else:
                    list_tau_costs.pop(self.pos_best_tau)
            else:
                if self.capacity_vehicle >= (
                    request_route + self.element_to_insert.get_request_customer()
                ):
                    request_route += self.element_to_insert.get_request_customer()
                    route.get_list_id_customers().append(
                        self.element_to_insert.get_id_customer()
                    )

                    # if len(route.get_list_id_customers()) >= 6:
                    #   self.three_opt.to_optimize(route)

                    list_tau_costs.pop(self.pos_best_tau)
                    self._delete_element(
                        self.element_to_insert.get_id_customer(),
                        list_metrics_cmt_by_customer,
                    )
                    self.customers_to_visit.remove(self.element_to_insert)
                else:
                    list_tau_costs.pop(self.pos_best_tau)
            return route

        elif self.type_problem == ProblemType.TTRP or self.type_problem == 4:
            if self.capacity_total >= (
                self.request_route + self.element_to_insert.get_request_customer()
            ):
                self.request_route += self.element_to_insert.get_request_customer()
                self.route.get_list_id_customers().append(
                    self.element_to_insert.get_id_customer()
                )

                if len(self.route.get_list_id_customers()) >= 6:
                    self.three_opt.to_optimize(self.route)

                self.list_tau_costs.pop(self.pos_best_tau)
                self._delete_element(
                    self.element_to_insert.get_id_customer(),
                    self.list_metrics_CMT_by_customer,
                )
                self.customers_to_visit.remove(self.element_to_insert)

                if (
                    self.type_customer == CustomerType.VC.value
                    and self.element_to_insert.get_type_customer()
                    == CustomerType.TC.value
                ):
                    self.is_TC = True
            else:
                self.list_tau_costs.pop(self.pos_best_tau)
            return self.route

    def processing(
        self,
        customers_to_visit,
        count_vehicles,
        request_route,
        route,
        id_depot,
        solution,
    ):
        if (
            self.type_problem in [0, 2, 3, 5]
            or self.type_problem == ProblemType.CVRP
            or self.type_problem == ProblemType.MDVRP
            or self.type_problem == ProblemType.SBRP
        ):
            while self.list_candidate_routes:
                self.list_metrics_cmt_by_element = []

                if self.type_problem == ProblemType.SBRP:
                    self.list_metrics_cmt_by_element = (self._calculate_cost_cmt_by_element(self.id_depot,
                                                                                            self.list_bus_stops,
                                                                                            self.list_candidate_routes))
                else:
                    self.list_metrics_cmt_by_element = (self._calculate_cost_cmt_by_element(self.id_depot,
                                                                                            self.customers_to_visit,
                                                                                            self.list_candidate_routes))

                self.route = Route()

                self.index = self.random.randint(
                    0, (len(self.list_candidate_routes) - 1)
                )
                self.route = self.list_candidate_routes.pop(self.index)

                if self.type_problem == ProblemType.SBRP:
                    self.bus_stop = self.route.get_list_bus_stops()[0]
                    self.root_element = self._get_element_by_id(self.bus_stop.get_id_bus_stop(), self.list_root_elements)
                    self.request_route = self.root_element.get_capacity_bus_stop()
                else:
                    self.root_element = self._get_element_by_id(
                        self.route.get_list_id_customers()[0], self.list_root_elements
                    )
                    self.request_route = self.root_element.get_request_customer()

                self.list_root_elements.remove(self.root_element)
                self.route.set_id_depot(self.id_depot)

                self.list_tau_costs = []
                self.list_tau_costs = self._calculate_tau(
                    self.list_metrics_cmt_by_element, self.index
                )
                while self.list_tau_costs:
                    if self.type_problem == ProblemType.SBRP:
                        self.element_to_insert = BusStop()
                        self.pos_best_tau = len(self.list_tau_costs) - 1
                        self.element_to_insert = self._get_element_by_id(self.list_tau_costs[self.pos_best_tau].get_id_element(),
                                                                         self.list_bus_stops)
                    else:
                        self.element_to_insert = Customer()
                        self.pos_best_tau = len(self.list_tau_costs) - 1
                        self.element_to_insert = self._get_element_by_id(
                            self.list_tau_costs[self.pos_best_tau].get_id_element(),
                            self.customers_to_visit,
                        )
                    self.route = self.creating(
                        self.route,
                        self.request_route,
                        self.list_tau_costs,
                        self.list_metrics_cmt_by_element,
                    )
                self.route.set_request_route(self.request_route)
                self.solution.get_list_routes().append(self.route)
            return self.solution

        elif self.type_problem == ProblemType.HFVRP or self.type_problem == 1:
            while self.list_candidate_routes and self.list_capacities:
                list_metrics_cmt_by_customer = self._calculate_cost_cmt_by_element(
                    id_depot, customers_to_visit, self.list_candidate_routes
                )

                route = Route()
                self.is_open = True

                index = self.random.randint(0, len(self.list_candidate_routes) - 1)
                route = self.list_candidate_routes.pop(index)

                root_customer = self._get_element_by_id(
                    route.get_list_id_customers()[0], self.list_root_elements
                )
                request_route = root_customer.get_request_customer()
                self.list_root_elements.remove(root_customer)
                route.set_id_depot(id_depot)

                list_tau_costs = self._calculate_tau(
                    list_metrics_cmt_by_customer, index
                )

                while list_tau_costs:
                    pos_best_tau = len(list_tau_costs) - 1
                    self.element_to_insert = self._get_element_by_id(
                        list_tau_costs[pos_best_tau].get_id_element(),
                        customers_to_visit,
                    )

                    route = self.creating(
                        route,
                        request_route,
                        list_tau_costs,
                        list_metrics_cmt_by_customer,
                    )

                route.set_request_route(request_route)
                solution.get_list_routes().append(route)

                self.list_capacities.pop(0)
                self.is_open = False
            return self.is_open, solution

        elif self.type_problem == ProblemType.TTRP or self.type_problem == 4:
            list_access_vc = []
            while self.list_candidate_routes:
                self.list_metrics_CMT_by_customer = []
                self.list_metrics_CMT_by_customer = (
                    self._calculate_cost_cmt_by_element(
                        self.id_depot,
                        self.customers_to_visit,
                        self.list_candidate_routes,
                    )
                )

                self.route = Route()

                self.index = self.random.randint(0, len(self.list_candidate_routes) - 1)
                self.route = self.list_candidate_routes.pop(self.index)

                # self.root_customer = Customer()
                self.root_element = self._get_element_by_id(
                    self.route.get_list_id_customers()[0], self.list_root_elements
                )
                self.request_route = self.root_element.get_request_customer()

                # self.root_customer = CustomerTTRP(id_customer=self.root_customer.get_id_customer(), request_customer=self.root_customer.get_request_customer(),
                #                              location_customer=self.root_customer.get_location_customer(), type_customer=self.type_customer)
                self.list_root_elements.remove(self.root_element)
                self.route.set_id_depot(self.id_depot)

                if self.type_customer == CustomerType.TC:
                    self.capacity_total = self.capacity_vehicle
                else:
                    self.capacity_total = self.capacity_vehicle + self.capacity_trailer

                self.list_tau_costs = []
                self.list_tau_costs = self._calculate_tau(
                    self.list_metrics_CMT_by_customer, self.index
                )

                while self.list_tau_costs:
                    self.element_to_insert = Customer()
                    self.pos_best_tau = len(self.list_tau_costs) - 1
                    self.element_to_insert = self._get_element_by_id(
                        self.list_tau_costs[self.pos_best_tau].get_id_element(),
                        self.customers_to_visit,
                    )

                    self.route = self.creating()

                self.route.set_request_route(self.request_route)

                if self.type_customer == CustomerType.TC.value:
                    self.route = RouteTTRP(
                        list_id_customers=self.route.get_list_id_customers(),
                        request_route=self.route.get_request_route(),
                        cost_route=self.route.get_cost_route(),
                        id_depot=self.route.get_id_depot(),
                        list_access_vc=list_access_vc,
                        type_route=RouteType.PTR.value,
                    )
                else:
                    if self.is_TC:
                        self.route = RouteTTRP(
                            list_id_customers=self.route.get_list_id_customers(),
                            request_route=self.route.get_request_route(),
                            cost_route=self.route.get_cost_route(),
                            id_depot=self.route.get_id_depot(),
                            list_access_vc=list_access_vc,
                            type_route=RouteType.CVR.value,
                        )
                    else:
                        self.route = RouteTTRP(
                            list_id_customers=self.route.get_list_id_customers(),
                            request_route=self.route.get_request_route(),
                            cost_route=self.route.get_cost_route(),
                            id_depot=self.route.get_id_depot(),
                            list_access_vc=list_access_vc,
                            type_route=RouteType.PVR.value,
                        )

                self.solution.get_list_routes().append(self.route)
            return self.solution

    def execute(self):
        if self.type_problem == ProblemType.CVRP or self.type_problem in [0, 3]:
            while self.customers_to_visit:
                self.list_candidate_routes = self._do_first_phase(
                    self.customers_to_visit,
                    self.id_depot,
                    self.pos_depot,
                    self.capacity_vehicle,
                    self.count_vehicles,
                )
                self.list_root_elements = self._update_elements_to_visit(
                    self.list_candidate_routes, self.customers_to_visit
                )
                self.solution = self.processing(
                    self.customers_to_visit,
                    self.count_vehicles,
                    self.request_route,
                    self.route,
                    self.id_depot,
                    self.solution,
                )
                # break

        elif self.type_problem == ProblemType.SBRP or self.type_problem == 5:
            while self.list_bus_stops:
                self.list_candidate_routes = self._do_first_phase(
                    self.list_bus_stops,
                    self.id_depot,
                    self.pos_depot,
                    self.capacity_vehicle,
                    self.count_vehicles,
                )
                self.list_root_elements = self._update_elements_to_visit(
                    self.list_candidate_routes, self.list_bus_stops
                )
                self.solution = self.processing(
                    self.list_bus_stops,
                    self.count_vehicles,
                    self.request_route,
                    self.route,
                    self.id_depot,
                    self.solution,
                )

        elif self.type_problem == ProblemType.HFVRP or self.type_problem == 1:
            self.capacity_vehicle = self.list_capacities[0]
            self.is_open = False

            while self.customers_to_visit and self.list_capacities:
                self.list_candidate_routes = self._do_first_phase(
                    self.customers_to_visit,
                    self.id_depot,
                    self.pos_depot,
                    self.capacity_vehicle,
                    self.count_vehicles,
                )
                self.list_root_elements = self._update_elements_to_visit(
                    self.list_candidate_routes, self.customers_to_visit
                )
                self.is_open, self.solution = self.processing(
                    self.customers_to_visit,
                    self.count_vehicles,
                    self.request_route,
                    self.route,
                    self.id_depot,
                    self.solution,
                )

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
                        route.get_list_id_customers().append(
                            self.customers_to_visit[0].get_id_customer()
                        )
                        self.customers_to_visit.pop(0)

                    self.solution.get_list_routes().append(route)

                if self.is_open:
                    route.set_request_route(self.request_route)
                    route.set_id_depot(self.id_depot)
                    self.solution.get_list_routes().append(route)

        elif self.type_problem == ProblemType.MDVRP or self.type_problem == 2:
            for j in range(
                self.pos_depot, len(Problem.get_problem().get_list_depots())
            ):
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

                while self.customers_to_visit:
                    self.list_candidate_routes = self._do_first_phase(
                        self.customers_to_visit,
                        self.id_depot,
                        j,
                        self.capacity_vehicle,
                        self.count_vehicles,
                    )
                    self.list_root_elements = self._update_elements_to_visit(
                        self.list_candidate_routes, self.customers_to_visit
                    )
                    self.solution = self.processing(
                        self.customers_to_visit,
                        self.count_vehicles,
                        self.request_route,
                        self.route,
                        self.id_depot,
                        self.solution,
                    )

        elif self.type_problem == ProblemType.TTRP or self.type_problem == 4:
            while self.customers_to_visit:
                self.is_TC = False
                self.capacity_trailer = (
                    Problem.get_problem()
                    .get_list_depots()[self.pos_depot]
                    .get_list_fleets()[0]
                    .get_capacity_trailer()
                )
                self.capacity_total = 0.0

                self.type_customer = CustomerType.TC  # ARREGLAR !!!

                self.list_candidate_routes = self._do_first_phase(
                    self.customers_to_visit,
                    self.id_depot,
                    self.pos_depot,
                    self.capacity_vehicle,
                    self.count_vehicles,
                )
                self.list_root_elements = self._update_elements_to_visit(
                    self.list_candidate_routes, self.customers_to_visit
                )

                self.solution = self.processing(
                    self.customers_to_visit,
                    self.count_vehicles,
                    self.request_route,
                    self.route,
                    self.id_depot,
                    self.solution,
                )

        return self.solution

    def get_solution_inicial(self):

        self.execute()

        return self.solution

    # Método que realiza la primera fase del algoritmo CMT
    def _do_first_phase(
        self, elements_to_visit, id_depot, pos_depot, capacity_vehicle, count_vehicles
    ):
        list_routes = []
        list_elements = list(elements_to_visit)
        list_candidate_elements = None
        route = Route()
        request_route = 0.0

        three_opt = Operator_3opt()

        type_problem = Problem.get_problem().get_type_problem()

        if type_problem == ProblemType.SBRP:
            root_bus_stop = self._get_first_element(list_elements, self.first_element_type, id_depot)
            request_route = root_bus_stop.get_capacity_bus_stop()
            route.get_list_bus_stops().append(root_bus_stop)
            route.set_id_depot(id_depot)
            list_elements.remove(root_bus_stop)
        else:
            root_customer = self._get_first_element(
                list_elements, self.first_element_type, id_depot
            )
            request_route = root_customer.get_request_customer()
            route.get_list_id_customers().append(root_customer.get_id_customer())
            route.set_id_depot(id_depot)
            list_elements.remove(root_customer)

        if type_problem in [ProblemType.CVRP, ProblemType.SBRP, ProblemType.MDVRP]:
            if not list_elements:
                list_routes.append(route)
            else:
                while list_elements:
                    list_candidate_elements = []

                    if type_problem == ProblemType.SBRP:
                        for bus_stop in list(list_elements):
                            metric_cmt = Metric()
                            if capacity_vehicle >= (request_route + bus_stop.get_capacity_bus_stop()):
                                metric_cmt.set_id_element(bus_stop.get_id_bus_stop())
                                metric_cmt.set_insertion_cost(self._calculate_cost_of_cmt(id_depot, root_bus_stop.get_id_bus_stop(), bus_stop.get_id_bus_stop()))
                                list_candidate_elements.append(metric_cmt)
                    else:
                        for customer in list(list_elements):
                            metric_cmt = Metric()
                            if capacity_vehicle >= (
                                request_route + customer.get_request_customer()
                            ):
                                metric_cmt.set_id_element(customer.get_id_customer())
                                metric_cmt.set_insertion_cost(
                                    self._calculate_cost_of_cmt(
                                        id_depot,
                                        root_customer.get_id_customer(),
                                        customer.get_id_customer(),
                                    )
                                )
                                list_candidate_elements.append(metric_cmt)

                    self._ascendent_ordenate_list_without_order(
                        list_candidate_elements
                    )

                    while list_candidate_elements:
                        if type_problem == ProblemType.SBRP:
                            bus_stop_to_insert = self._get_element_by_id(list_candidate_elements[0].get_id_element(), list_elements)
                            if capacity_vehicle >= (request_route + bus_stop.get_capacity_bus_stop()):
                                request_route += bus_stop_to_insert.get_capacity_bus_stop()
                                route.get_list_bus_stops().append(bus_stop_to_insert)

                                list_candidate_elements.pop(0)
                                list_elements.remove(bus_stop_to_insert)
                            else:
                                list_candidate_elements.pop(0)
                        else:
                            customer_to_insert = self._get_element_by_id(
                                list_candidate_elements[0].get_id_element(), list_elements
                            )

                            if capacity_vehicle >= (
                                request_route + customer_to_insert.get_request_customer()
                            ):
                                request_route += customer_to_insert.get_request_customer()
                                route.get_list_id_customers().append(
                                    customer_to_insert.get_id_customer()
                                )

                                # if len(route.get_list_id_customers()) >= 6:
                                #   three_opt.to_optimize(route)

                                list_candidate_elements.pop(0)
                                list_elements.remove(customer_to_insert)
                            else:
                                list_candidate_elements.pop(0)

                    list_routes.append(route)

                    if list_elements:
                        route = Route()
                        request_route = 0.0

                        if type_problem == ProblemType.SBRP:
                            root_bus_stop = self._get_first_element(list_elements, self.first_element_type, id_depot)
                            request_route = root_bus_stop.get_capacity_bus_stop()
                            route.get_list_bus_stops().append(root_bus_stop)
                            route.set_id_depot(id_depot)
                            list_elements.remove(root_bus_stop)
                        else:
                            root_customer = self._get_first_element(
                                list_elements, self.first_element_type, id_depot
                            )
                            request_route = root_customer.get_request_customer()
                            route.get_list_id_customers().append(
                                root_customer.get_id_customer()
                            )
                            route.set_id_depot(id_depot)
                            list_elements.remove(root_customer)

                        if not list_elements:
                            list_routes.append(route)

        elif type_problem == ProblemType.HFVRP:
            if not list_elements:
                list_routes.append(route)
            else:
                list_capacities = list(Problem.get_problem().get_list_capacities())
                capacity_vehicle = list_capacities[0]

                while list_elements and list_capacities:
                    list_candidate_elements = []

                    for customer in list(list_elements):
                        metric_cmt = Metric()
                        if capacity_vehicle >= (
                            request_route + customer.get_request_customer()
                        ):
                            metric_cmt.set_id_element(customer.get_id_customer())
                            metric_cmt.set_insertion_cost(
                                self._calculate_cost_of_cmt(
                                    id_depot,
                                    root_customer.get_id_customer(),
                                    customer.get_id_customer(),
                                )
                            )
                            list_candidate_elements.append(metric_cmt)

                    self._ascendent_ordenate_list_without_order(
                        list_candidate_elements
                    )

                    while list_candidate_elements:
                        customer_to_insert = self._get_element_by_id(
                            list_candidate_elements[0].get_id_element(), list_elements
                        )

                        if capacity_vehicle >= (
                            request_route + customer_to_insert.get_request_customer()
                        ):
                            request_route += customer_to_insert.get_request_customer()
                            route.get_list_id_customers().append(
                                customer_to_insert.get_id_customer()
                            )
                            route.set_id_depot(id_depot)

                            # if len(route.get_list_id_customers()) >= 6:
                            #   three_opt.to_optimize(route)

                            list_candidate_elements.pop(0)
                            list_elements.remove(customer_to_insert)
                        else:
                            list_candidate_elements.pop(0)

                    list_routes.append(route)
                    list_capacities.pop(0)

                    if list_elements:
                        route = Route()
                        request_route = 0.0

                        root_customer = self._get_first_element(
                            list_elements, self.first_element_type, id_depot
                        )
                        request_route = root_customer.get_request_customer()
                        route.get_list_id_customers().append(
                            root_customer.get_id_customer()
                        )
                        route.set_id_depot(
                            Problem.get_problem()
                            .get_list_depots()[pos_depot]
                            .get_id_depot()
                        )
                        list_elements.remove(root_customer)

                        if not list_capacities:
                            continue
                        else:
                            capacity_vehicle = list_capacities[0]

                        if not list_elements:
                            list_routes.append(route)

        elif type_problem == ProblemType.TTRP:
            capacity_total = 0.0
            capacity_trailer = (
                Problem.get_problem()
                .get_list_depots()[pos_depot]
                .get_list_fleets()[0]
                .get_capacity_trailer()
            )

            if not list_elements:
                list_routes.append(route)
            else:
                while list_elements:
                    list_candidate_elements = []
                    type_customer = root_customer.get_type_customer()

                    if type_customer == CustomerType.TC:
                        capacity_total = capacity_vehicle
                    else:
                        capacity_total = capacity_vehicle + capacity_trailer

                    for customer in list(list_elements):
                        metric_cmt = Metric()
                        if capacity_total >= (
                            request_route + customer.get_request_customer()
                        ):
                            metric_cmt.set_id_element(customer.get_id_customer())
                            metric_cmt.set_insertion_cost(
                                self._calculate_cost_of_cmt(
                                    id_depot,
                                    root_customer.get_id_customer(),
                                    customer.get_id_customer(),
                                )
                            )
                            list_candidate_elements.append(metric_cmt)

                    self._ascendent_ordenate_list_without_order(
                        list_candidate_elements
                    )

                    while list_candidate_elements:
                        customer_to_insert = self._get_element_by_id(
                            list_candidate_elements[0].get_id_element(), list_elements
                        )

                        if capacity_total >= (
                            request_route + customer_to_insert.get_request_customer()
                        ):
                            request_route += customer_to_insert.get_request_customer()
                            route.get_list_id_customers().append(
                                customer_to_insert.get_id_customer()
                            )
                            route.set_id_depot(
                                Problem.get_problem()
                                .get_list_depots()[pos_depot]
                                .get_id_depot()
                            )

                            # if len(route.get_list_id_customers()) >= 6:
                            #   three_opt.to_optimize(route)

                            list_candidate_elements.pop(0)
                            list_elements.remove(customer_to_insert)
                        else:
                            list_candidate_elements.pop(0)

                    list_routes.append(route)

                    if list_elements:
                        route = Route()
                        request_route = 0.0

                        root_customer = self._get_first_element(
                            list_elements, self.first_element_type, id_depot
                        )
                        request_route = root_customer.get_request_customer()
                        route.get_list_id_customers().append(
                            root_customer.get_id_customer()
                        )
                        route.set_id_depot(
                            Problem.get_problem()
                            .get_list_depots()[pos_depot]
                            .get_id_depot()
                        )
                        list_elements.remove(root_customer)

                        if not list_elements:
                            list_routes.append(route)

        self._empty_routes(list_routes)
        return list_routes

    # Método que calcula el costo de insertar un cliente en la ruta
    def _calculate_cost_of_cmt(self, id_depot, current_element, next_element):
        cost_depot_to_next = Problem.get_problem().get_cost_matrix()[
            Problem.get_problem().get_pos_element(id_depot),
            Problem.get_problem().get_pos_element(next_element),
        ]

        '''if Problem.get_problem().get_type_problem() == ProblemType.SBRP:
            actual = current_element.get_id_bus_stop()
            cost_next_to_current = Problem.get_problem().get_cost_matrix()[
                Problem.get_problem().get_pos_element(next_element),
                Problem.get_problem().get_pos_element(actual),
            ]
        else:'''
        cost_next_to_current = Problem.get_problem().get_cost_matrix()[
                Problem.get_problem().get_pos_element(next_element),
                Problem.get_problem().get_pos_element(current_element),
            ]

        return cost_depot_to_next + (self.parameter_l * cost_next_to_current)

    # Método que vacia la lista de rutas dejando solo el primer cliente en cada una
    def _empty_routes(self, list_routes):
        for i in range(len(list_routes)):
            j = 1

            if Problem.get_problem().get_type_problem() == ProblemType.SBRP:
                while j < len(list_routes[i].get_list_bus_stops()):
                    list_routes[i].get_list_bus_stops().pop(j)
            else:
                while j < len(list_routes[i].get_list_id_customers()):
                    list_routes[i].get_list_id_customers().pop(j)

    # Método que devuelve en una lista los clientes a eliminar que ya pertenecen a una ruta
    def _update_elements_to_visit(self, list_routes, elements_to_visit):
        """
        Actualiza la lista de clientes a visitar, eliminando aquellos que ya están en las rutas dadas.

        :param list_routes: Lista de rutas, donde cada ruta contiene una lista de IDs de clientes.
        :param elements_to_visit: Lista de clientes a visitar.
        :return: Lista de clientes raíz que se han eliminado de la lista de clientes a visitar.
        """
        list_root_elements = []

        for route in list_routes:
            if Problem.get_problem().get_type_problem() == ProblemType.SBRP:
                root_bus_stop = route.get_list_bus_stops()[0]
                for bus_stop in elements_to_visit:
                    if bus_stop.get_id_bus_stop() == root_bus_stop.get_id_bus_stop():
                        list_root_elements.append(bus_stop)
                        elements_to_visit.remove(bus_stop)
                        break  # Salir del bucle una vez que se ha encontrado y eliminado el cliente
            else:
                root_customer_id = route.get_list_id_customers()[0]
                for customer in elements_to_visit:
                    if customer.get_id_customer() == root_customer_id:
                        list_root_elements.append(customer)
                        elements_to_visit.remove(customer)
                        break  # Salir del bucle una vez que se ha encontrado y eliminado el cliente

        return list_root_elements

    # Método que retorna la lista ordenada con los costos CMT en cada ruta para cada cliente
    def _calculate_cost_cmt_by_element(self, id_depot, list_elements, list_routes):
        list_metrics_cmt_by_element = []

        for i in range(len(list_elements)):
            list_metric_cmt = []

            for j in range(len(list_routes)):
                metric_cmt = Metric()

                if Problem.get_problem().get_type_problem() == ProblemType.SBRP:
                    metric_cmt.set_id_element(list_elements[i].get_id_bus_stop())
                    metric_cmt.set_insertion_cost(self._calculate_cost_of_cmt(id_depot,
                                                                              list_routes[j].get_list_bus_stops()[0],
                                                                              list_elements[i].get_id_bus_stop()))
                else:
                    metric_cmt.set_id_element(list_elements[i].get_id_customer())
                    metric_cmt.set_insertion_cost(
                        self._calculate_cost_of_cmt(
                            id_depot,
                            list_routes[j].get_list_id_customers()[0],
                            list_elements[i].get_id_customer(),
                        )
                    )
                metric_cmt.set_index(j)
                list_metric_cmt.append(metric_cmt)

            if len(list_routes) > 1:
                self._ascendent_ordenate_list_without_order(list_metric_cmt)

            list_metrics_cmt_by_element.append(list_metric_cmt)

        return list_metrics_cmt_by_element

    # Método que devuelve listado de clientes con el TAU calculado y ordenado
    def _calculate_tau(self, list_metrics_cmt_by_element, pos_route):
        list_tau_costs = []
        first_cost = 0.0
        second_cost = 0.0

        for i in range(len(list_metrics_cmt_by_element)):
            j = 0

            if list_metrics_cmt_by_element[i][0].get_index() == pos_route:
                metric_cmt = Metric()
                metric_cmt.set_id_element(
                    list_metrics_cmt_by_element[i][j].get_id_element()
                )

                first_cost = list_metrics_cmt_by_element[i][j].get_insertion_cost()

                if len(list_metrics_cmt_by_element[i]) > 1:
                    second_cost = list_metrics_cmt_by_element[i][
                        j + 1
                    ].get_insertion_cost()
                    tau_cost = second_cost - first_cost
                else:
                    tau_cost = first_cost

                metric_cmt.set_insertion_cost(tau_cost)

                list_tau_costs.append(metric_cmt)

        if len(list_tau_costs) > 1:
            self._ascendent_ordenate_list_without_order(list_tau_costs)

        return list_tau_costs

    # Método que elimina un cliente de la lista ordenada de los costos
    def _delete_element(self, id_element, list_metrics_cmt_by_customer):
        deleted = False
        i = 0

        while i < len(list_metrics_cmt_by_customer) and not deleted:
            if list_metrics_cmt_by_customer[i][0].get_id_element() == id_element:
                list_metrics_cmt_by_customer.pop(i)
                deleted = True
            else:
                i += 1
