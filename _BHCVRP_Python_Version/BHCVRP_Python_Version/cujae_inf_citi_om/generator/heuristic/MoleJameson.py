from generator.heuristic.Heuristic import Heuristic
from data.Problem import Problem
from data.ProblemType import ProblemType
from generator.heuristic.Metric import Metric
from data.CustomerType import CustomerType
from generator.heuristic.FirstCustomerType import FirstCustomerType
from generator.solution.Solution import Solution
from data.DepotMDVRP import DepotMDVRP
from data.Customer import Customer
from generator.solution.Route import Route
from generator.postoptimization.Operator_3opt import Operator_3opt
from generator.solution.RouteTTRP import RouteTTRP
from generator.solution.RouteType import RouteType
from data.FleetTTRP import FleetTTRP

class MoleJameson(Heuristic):
    
    parameter_c1 = 1
    parameter_c2 = 1
    first_customer_type = FirstCustomerType.FurthestCustomer

    def __init__(self):
        super().__init__()

    def initialize_specifics(self):

        self.customer = self._get_first_customer(self.customers_to_visit, self.first_customer_type, self.id_depot)

        if not self.initialized:
            if self.parameter_c1 <= 0:
                self.parameter_c1 = 1

            if self.parameter_c2 <= 0:
                self.parameter_c2 = 1

            self.three_opt = Operator_3opt()
            self.list_best_positions = None
            self.metric_MJ = None
            self.count_no_feasible = 0
            self.request_route = self.customer.get_request_customer()
            self.route.get_list_id_customers().append(self.id_depot)
            self.route.get_list_id_customers().append(self.customer.get_id_customer())
            self.route.get_list_id_customers().append(self.id_depot)
            self.route.set_id_depot(self.id_depot)
            self.customers_to_visit.remove(self.customer)
    
    def creating(self, route=None, request_route=None, list_tau=None, list_metrics=None):
        if self.type_problem in [0, 3] or self.type_problem == ProblemType.CVRP:
            for i in range(len(self.customers_to_visit)):
                if self.capacity_vehicle >= (self.request_route + self.customers_to_visit[i].get_request_customer()):
                    self.list_best_positions.append(self.get_position_with_best_cost(self.route, self.customers_to_visit[i].get_id_customer()))
                else:
                    self.count_no_feasible += 1
                    
            if self.count_no_feasible == len(self.customers_to_visit):
                self.route.get_list_id_customers().pop(0)
                self.route.get_list_id_customers().pop((len(self.route.get_list_id_customers()) - 1))
                self.route.set_request_route(self.request_route)
                self.solution.get_list_routes().append(self.route)

                # route = None
                self.count_vehicles -= 1

                if self.count_vehicles > 0:
                    self.route = Route()

                    self.customer = self._get_first_customer(self.customers_to_visit, self.first_customer_type, self.id_depot)
                    self.request_route = self.customer.get_request_customer()
                    self.route.get_list_id_customers().append(self.id_depot)
                    self.route.get_list_id_customers().append(self.customer.get_id_customer())
                    self.route.get_list_id_customers().append(self.id_depot)
                    self.route.set_id_depot(self.id_depot)
                    self.customers_to_visit.remove(self.customer)
            else:
                self.metric_MJ = self.get_MJ_customer(self.list_best_positions, self.id_depot)
                self.request_route += Problem.get_problem().get_request_by_id_customer(self.metric_MJ.get_id_element())
                self.route.get_list_id_customers().insert(self.metric_MJ.get_index(), self.metric_MJ.get_id_element())
                self.customers_to_visit.remove(Problem.get_problem().get_customer_by_id_customer(self.metric_MJ.get_id_element()))

                if len(self.route.get_list_id_customers()) >= 6:
                    self.route.get_list_id_customers().pop(0)
                    self.route.get_list_id_customers().pop(len(self.route.get_list_id_customers()) - 1)

                    if len(self.route.get_list_id_customers()) >= 6:
                        self.three_opt.to_optimize(self.route)

                    self.route.get_list_id_customers().insert(0, self.id_depot)
                    self.route.get_list_id_customers().append(self.id_depot)
                    
        elif self.type_problem == 1 or self.type_problem == ProblemType.HFVRP:
            for i in range(len(self.customers_to_visit)):
                if self.capacity_vehicle >= self.request_route + self.customers_to_visit[i].get_request_customer():
                    self.list_best_positions.append(self.get_position_with_best_cost(self.route, self.customers_to_visit[i].get_id_customer()))
                else:
                    self.count_no_feasible += 1

            if self.count_no_feasible == len(self.customers_to_visit):
                self.route.get_list_id_customers().pop(0)
                self.route.get_list_id_customers().pop(-1)
                self.route.set_request_route(self.request_route)
                self.solution.get_list_routes().append(self.route)

                # self.route = None
                self.list_capacities.pop(0)

                if self.list_capacities:

                    self.route = Route()

                    customer = self._get_first_customer(self.customers_to_visit, self.first_customer_type, self.id_depot)
                    self.request_route = customer.get_request_customer()
                    self.route.get_list_id_customers().extend([self.id_depot, customer.get_id_customer(), self.id_depot])
                    self.route.set_id_depot(self.id_depot)
                    self.customers_to_visit.remove(customer)

                    self.capacity_vehicle = self.list_capacities[0]
            else:
                metric_MJ = self.get_MJ_customer(self.list_best_positions, self.id_depot)
                self.request_route += Problem.get_problem().get_request_by_id_customer(metric_MJ.get_id_element())
                self.route.get_list_id_customers().insert(metric_MJ.get_index(), metric_MJ.get_id_element())
                self.customers_to_visit.remove(Problem.get_problem().get_customer_by_id_customer(metric_MJ.get_id_element()))

                if len(self.route.get_list_id_customers()) >= 6:
                    self.route.get_list_id_customers().pop(0)
                    self.route.get_list_id_customers().pop(-1)

                    if len(self.route.get_list_id_customers()) >= 6:
                        self.three_opt.to_optimize(self.route)

                    self.route.get_list_id_customers().insert(0, self.id_depot)
                    self.route.get_list_id_customers().append(self.id_depot)
                    
        elif self.type_problem == 2 or self.type_problem == ProblemType.MDVRP:
            for k in range(len(self.customers_to_visit)):
                if capacity_vehicle >= (requestRoute + self.customers_to_visit.get(k).get_request_customer()):
                    self.list_best_positions.append(self.get_position_with_best_cost(route, self.customers_to_visit.get(k).get_id_customer()))
                else:
                    self.count_no_feasible += 1
                    
            if self.count_no_feasible == len(self.customers_to_visit):
                route.get_list_id_customers().remove(0)
                route.get_list_id_customers().remove((len(route.get_list_id_customers()) - 1))
                route.set_request_route(requestRoute)
                self.solution.get_list_routes().append(route)
                        
                route = None
                self.count_vehicles -= 1
                        
                if self.count_vehicles > 0:
                    route = Route()
                            
                    customer = self._get_first_customer(self.customers_to_visit, self.first_customer_type, self.id_depot)
                    requestRoute = customer.get_request_customer()
                    route.get_list_id_customers().append(self.id_depot)
                    route.get_list_id_customers().append(customer.get_id_customer())
                    route.get_list_id_customers().append(self.id_depot)
                    route.set_id_depot(self.id_depot)
                    self.customers_to_visit.remove(customer)
            else:
                metric_MJ = self.get_MJ_customer(self.list_best_positions, self.id_depot)
                requestRoute += Problem.get_problem().get_request_by_id_customer(metric_MJ.get_id_element())
                route.get_list_id_customers().insert(metric_MJ.get_index(), metric_MJ.get_id_element())
                self.customers_to_visit.remove(Problem.get_problem().get_customer_by_id_customer(metric_MJ.get_id_element()))
                
                if len(route.get_list_id_customers()) >= 6:
                    route.get_list_id_customers().remove(0)
                    route.get_list_id_customers().remove((len(route.get_list_id_customers()) - 1))
                            
                    if len(route.get_list_id_customers()) >= 6:
                        self.three_opt.to_optimize(route)
                            
                    route.get_list_id_customers().insert(0, self.id_depot)
                    route.get_list_id_customers().append(self.id_depot)
                    
        elif self.type_problem == 4 or self.type_problem == ProblemType.TTRP:
            if self.count_no_feasible == len(self.customers_to_visit):
                route.get_list_id_customers().remove(0)
                route.get_list_id_customers().remove((len(route.get_list_id_customers()) - 1))
                route.set_request_route(request_route)
                    
                if Problem.get_problem().get_type_by_id_customer(route.get_list_id_customers().get(0)).equals(CustomerType.TC):
                    route = RouteTTRP(route.get_list_id_customers(), route.get_request_route(), route.get_cost_route(), route.get_id_depot(), self.list_access_VC, RouteType.PTR)
                else:
                    if self.exist_TC(route):
                        route = RouteTTRP(route.get_list_id_customers(), route.get_request_route(), route.get_cost_route(), route.get_id_depot(), self.list_access_VC, RouteType.CVR)
                    else:
                        route = RouteTTRP(route.get_list_id_customers(), route.get_request_route(), route.get_cost_route(), route.get_id_depot(), self.list_access_VC, RouteType.PVR)
                    
                if len(route.get_list_id_customers()) >= 6:
                    self.three_opt.to_optimize(route)
                    
                self.solution.get_list_routes().append(route)
                    
                if self.customers_to_visit:
                    route = Route()
                    customer = self.get_first_customer(self.customers_to_visit, self.first_customer_type, self.id_depot)
                    request_route = customer.get_request_customer()
                    route.get_list_id_customers().append(self.id_depot)
                    route.get_list_id_customers().append(self.id_depot)
                    route.get_list_id_customers().append(1, customer.get_id_customer())
                    route.set_id_depot(self.id_depot)
                    self.customers_to_visit.remove(customer)
                
            else:
                metric_MJ = self.get_MJ_customer(self.list_best_positions, self.id_depot)
                    
                request_route += Problem.get_problem().get_request_by_id_customer(metric_MJ.get_id_element())
                route.get_list_id_customers().append(metric_MJ.get_index(), metric_MJ.get_id_element())
                self.customers_to_visit.remove(Problem.get_problem().get_customer_by_id_customer(metric_MJ.get_id_element()))
                
        return route
    
    def processing(self, customers_to_visit=None, count_vehicles=None, request_route=None, route=None, id_depot=None, solution=None):
        if self.type_problem in [0, 3] or self.type_problem == ProblemType.CVRP:
            if self.route is not None:
                self.route.get_list_id_customers().pop(0)
                self.route.get_list_id_customers().pop((len(self.route.get_list_id_customers()) - 1))
                self.route.set_request_route(self.request_route)
                self.solution.get_list_routes().append(self.route)

            if self.customers_to_visit:
                self.route = Route()
                self.metric_MJ = Metric()

                self.customer = self._get_first_customer(self.customers_to_visit, self.first_customer_type, self.id_depot)
                self.request_route = self.customer.get_request_customer()
                self.route.get_list_id_customers().append(self.id_depot)
                self.route.get_list_id_customers().append(self.customer.get_id_customer())
                self.route.get_list_id_customers().append(self.id_depot)
                self.route.set_id_depot(self.id_depot)
                self.customers_to_visit.remove(self.customer)

                while self.customers_to_visit:
                    self.list_best_positions = []

                    for i in range(len(self.customers_to_visit)):
                        self.list_best_positions.append(self.get_position_with_best_cost(self.route, self.customers_to_visit[i].get_id_customer()))

                    self.metric_MJ = self.get_MJ_customer(self.list_best_positions, self.id_depot)
                    self.request_route += Problem.get_problem().get_request_by_id_customer(self.metric_MJ.get_id_element())
                    self.route.get_list_id_customers().append(self.metric_MJ.get_index(), self.metric_MJ.get_id_element())
                    self.customers_to_visit.remove(Problem.get_problem().get_customer_by_id_customer(self.metric_MJ.get_id_element()))

                    if len(self.route.get_list_id_customers()) >= 6:
                        self.route.get_list_id_customers().remove(0)
                        self.route.get_list_id_customers().remove((len(self.route.get_list_id_customers()) - 1))

                        if len(self.route.get_list_id_customers()) >= 6:
                            self.three_opt.to_optimize(self.route)

                        self.route.get_list_id_customers().insert(0, self.id_depot)
                        self.route.get_list_id_customers().append(self.id_depot)

                self.route.get_list_id_customers().remove(0)
                self.route.get_list_id_customers().remove((len(self.route.get_list_id_customers()) - 1))
                self.route.set_request_route(self.request_route)
                self.solution.get_list_routes().append(self.route)
                
        elif self.type_problem == 1 or self.type_problem == ProblemType.HFVRP:
            if self.route:
                self.route.get_list_id_customers().pop(0)
                self.route.get_list_id_customers().pop(-1)
                self.route.set_request_route(self.request_route)
                self.solution.get_list_routes().append(self.route)

            if self.customers_to_visit:
                self.route = Route()
                metric_MJ = Metric()

                customer = self._get_first_customer(self.customers_to_visit, self.first_customer_type, self.id_depot)
                self.request_route = customer.get_request_customer()
                self.route.get_list_id_customers().extend([self.id_depot, customer.get_id_customer(), self.id_depot])
                self.route.set_id_depot(self.id_depot)
                self.customers_to_visit.remove(customer)

                while self.customers_to_visit:
                    list_best_positions = []

                    for i in range(len(self.customers_to_visit)):
                        list_best_positions.append(self.get_position_with_best_cost(self.route, self.customers_to_visit[i].get_id_customer()))
                        
                    metric_MJ = self.get_MJ_customer(list_best_positions, id_depot)
                    self.request_route += Problem.get_problem().get_request_by_id_customer(metric_MJ.get_id_element())
                    self.route.get_list_id_customers().insert(metric_MJ.get_index(), metric_MJ.get_id_element())
                    self.customers_to_visit.remove(Problem.get_problem().get_customer_by_id_customer(metric_MJ.get_id_element()))

                    if len(self.route.get_list_id_customers()) >= 6:
                        self.route.get_list_id_customers().pop(0)
                        self.route.get_list_id_customers().pop((len(self.route.get_list_id_customers()) - 1))

                        if len(self.route.get_list_id_customers()) >= 6:
                            self.three_opt.to_optimize(self.route)

                        self.route.get_list_id_customers().insert(0, id_depot)
                        self.route.get_list_id_customers().append(id_depot)

                self.route.get_list_id_customers().pop(0)
                self.route.get_list_id_customers().pop(len(self.route.get_list_id_customers()) - 1)
                self.route.set_request_route(self.request_route)

                self.solution.get_list_routes().append(self.route)
                    
        elif self.type_problem == 2 or self.type_problem == ProblemType.MDVRP:
            if route is not None:
                route.get_list_id_customers().remove(0)
                route.get_list_id_customers().remove((len(route.get_list_id_customers()) - 1))
                route.set_request_route(requestRoute)
                self.solution.get_list_routes().append(route)
                
            if customers_to_visit:
                route = Route()
                metric_MJ = Metric()
                    
                customer = self._get_first_customer(customers_to_visit, self.first_customer_type, id_depot)
                requestRoute = customer.get_request_customer()
                route.get_list_id_customers().append(id_depot)
                route.get_list_id_customers().append(customer.get_id_customer())
                route.get_list_id_customers().append(id_depot)
                route.set_id_depot(id_depot)
                customers_to_visit.remove(customer)
                    
                while customers_to_visit:
                    list_best_positions = []
                        
                    for l in range(len(customers_to_visit)):
                        list_best_positions.append(self.get_position_with_best_cost(route, customers_to_visit.get(l).get_id_customer()))
                        
                    metric_MJ = self.get_MJ_customer(list_best_positions, id_depot)
                    request_route += Problem.get_problem().get_request_by_id_customer(metric_MJ.get_id_element())
                    route.get_list_id_customers().insert(metric_MJ.get_index(), metric_MJ.get_id_element())
                    customers_to_visit.remove(Problem.get_problem().get_customer_by_id_customer(metric_MJ.get_id_element()))

                    if len(route.get_list_id_customers()) >= 6:
                        route.get_list_id_customers().pop(0)
                        route.get_list_id_customers().pop(-1)

                        if len(route.get_list_id_customers()) >= 6:
                            self.three_opt.to_optimize(route)

                        route.get_list_id_customers().insert(0, id_depot)
                        route.get_list_id_customers().append(id_depot)

                    route.get_list_id_customers().pop(0)
                    route.get_list_id_customers().pop(-1)
                    route.set_request_route(request_route)
                    self.solution.get_list_routes().append(route)
                    
        elif self.type_problem == 4 or self.type_problem == ProblemType.TTRP:
            if request_route > 0.0:  # cambiar condicion
                route.get_list_id_customers().remove(0)
                route.get_list_id_customers().remove((len(route.get_list_id_customers()) - 1))
                route.set_request_route(request_route)

                if Problem.get_problem().get_type_by_id_customer(route.get_list_id_customers()[0]) == CustomerType.TC:
                    route = RouteTTRP(route.get_list_id_customers(), route.get_request_route(), route.get_cost_route(),
                                    route.get_id_depot(), self.list_access_VC, RouteType.PTR)
                    # ((RouteTTRP)route).setTypeRoute(RouteType.PTR)
                else:
                    if self.exist_tc(route):
                        route = RouteTTRP(route.get_list_id_customers(), route.get_request_route(), route.get_cost_route(),
                                        route.get_id_depot(), self.list_access_VC, RouteType.CVR)
                        # ((RouteTTRP)route).setTypeRoute(RouteType.CVR)
                    else:
                        route = RouteTTRP(route.get_list_id_customers(), route.get_request_route(), route.get_cost_route(),
                                        route.get_id_depot(), self.list_access_VC, RouteType.PVR)
                        # ((RouteTTRP)route).setTypeRoute(RouteType.PVR)

                # 3opt
                if len(route.list_id_customers) >= 6:
                    self.three_opt.to_optimize(route)

                self.solution.get_list_routes().append(route)

        return self.solution
    
    def execute(self):
        if self.type_problem in [0, 3] or self.type_problem == ProblemType.CVRP:
            while self.customers_to_visit and (self.count_vehicles > 0):
                self.count_no_feasible = 0
                self.list_best_positions = []
                self.creating()
            self.processing()
            
        elif self.type_problem == 1 or self.type_problem == ProblemType.HFVRP:
            self.list_capacities = list(Problem.get_problem().get_list_capacities())
            self.capacity_vehicle = self.list_capacities[0]

            while self.customers_to_visit and self.list_capacities:
                self.count_no_feasible = 0
                self.list_best_positions = []
                self.creating()

            self.processing()
            
        elif self.type_problem == 2 or self.type_problem == ProblemType.MDVRP:
            for j in range(self.pos_depot, len(Problem.get_problem().get_list_depots())):
                if j != self.pos_depot:
                    id_depot = Problem.get_problem().get_list_depots().get(j).get_id_depot()
                    customers_to_visit = Problem.get_problem().get_customers_assigned_by_id_depot(id_depot)
                    
                    self.capacity_vehicle = Problem.get_problem().get_list_depots().get(j).get_list_fleets().get(0).get_capacity_vehicle()
                    count_vehicles = Problem.get_problem().get_list_depots().get(j).get_list_fleets().get(0).get_count_vehicles()
                    
                    if customers_to_visit:
                        route = Route()
                        
                        customer = self.get_first_customer(customers_to_visit, self.first_customer_type, id_depot)
                        self.request_route = customer.get_request_customer()
                        route.get_list_id_customers().append(id_depot)
                        route.get_list_id_customers().append(customer.get_id_customer())
                        route.get_list_id_customers().append(id_depot)
                        route.set_id_depot(id_depot)
                        customers_to_visit.remove(customer)
                
                while customers_to_visit and count_vehicles > 0:
                    self.count_no_feasible = 0
                    self.list_best_positions = []
                    self.creating()
                self.processing()
                
        elif self.type_problem == 4 or self.type_problem == ProblemType.TTRP:
            # boolean isTC = False
            capacity_trailer = Problem.get_problem().get_list_depots()[self.pos_depot].get_list_fleets()[0].get_capacity_trailer()
            
            type_customer = None
            self.list_access_VC = []

            while customers_to_visit:
                list_best_positions = []
                type_customer = Problem.get_problem().get_type_by_id_customer(route.get_list_id_customers().get(1))

                case = type_customer.ordinal()
                if case == 0:
                    count_no_feasible = 0
                    
                    for i in range(len(customers_to_visit)):
                        if (self.capacity_vehicle + capacity_trailer) >= (self.request_route + customers_to_visit.get(i).get_request_customer()):
                            list_best_positions.append(self.get_position_with_best_cost(route, customers_to_visit.get(i).get_id_customer()))
                        else:
                            count_no_feasible += 1
                    
                elif case == 1:
                    count_no_feasible = 0
                    
                    for i in range(len(customers_to_visit)):
                        if self.capacity_vehicle >= (self.request_route + customers_to_visit.get(i).get_request_customer()):
                            list_best_positions.append(self.get_position_with_best_cost(route, customers_to_visit.get(i).get_id_customer()))
                        else:
                            count_no_feasible += 1
                            
                self.creating()
                
            self.processing()
        
        return self.solution

    
    def get_solution_inicial(self):
        
        self.execute()
        
        return self.solution
    
    # Método que devuelve la métrica del cliente con el mejor C1
    def get_position_with_best_cost(self, route, id_customer):
        best_position = 1
        best_cost = 0.0
        current_cost = 0.0
        size_route = len(route.get_list_id_customers())

        if Problem.get_problem().get_type_problem() == ProblemType.OVRP:
            size_route -= 1

        for i in range(1, size_route):
            current_cost = self.calculate_c1(route.get_list_id_customers()[i - 1], route.get_list_id_customers()[i], id_customer)

            if i == 1:
                best_cost = current_cost
            else:
                if current_cost < best_cost:
                    best_cost = current_cost
                    best_position = i

        best_c1 = Metric()
        best_c1.set_insertion_cost(best_cost)
        best_c1.set_index(best_position)
        best_c1.set_id_element(id_customer)

        return best_c1

    # Método que calcula la métrica c1
    def calculate_c1(self, previous_element, next_element, current_element):
        cost_first = Problem.get_problem().get_cost_matrix()[Problem.get_problem().get_pos_element(previous_element), Problem.get_problem().get_pos_element(current_element)]
        cost_second = Problem.get_problem().get_cost_matrix()[Problem.get_problem().get_pos_element(current_element), Problem.get_problem().get_pos_element(next_element)]
        cost_third = Problem.get_problem().get_cost_matrix()[Problem.get_problem().get_pos_element(previous_element), Problem.get_problem().get_pos_element(next_element)]

        return ((cost_first + cost_second) - (self.parameter_c1 * cost_third))

    # Método que calcula la métrica c2
    def calculate_c2(self, cost_to_depot, cost_c1):
        return ((self.parameter_c2 * cost_to_depot) - cost_c1)

    # Método que devuelve el cliente con el mejor C2
    def get_MJ_customer(self, list_best_positions, id_depot):
        current_value = 0.0
        max_value = 0.0
        position_MJ = 0

        for i in range(len(list_best_positions)):
            best_customer = list_best_positions[i].get_id_element()
            cost_to_depot = Problem.get_problem().get_cost_matrix()[Problem.get_problem().get_pos_element(id_depot), Problem.get_problem().get_pos_element(best_customer)]

            current_value = self.calculate_c2(cost_to_depot, list_best_positions[i].get_insertion_cost())

            if i == 0:
                max_value = current_value
            else:
                if current_value > max_value:
                    max_value = current_value
                    position_MJ = i

        return list_best_positions.pop(position_MJ)

    # Método que dice si existen clientes de tipo TC en la ruta construida
    def exist_TC(self, route):
        exist = False
        i = 0

        while i < len(route.get_list_id_customers()) and not exist:
            if Problem.get_problem().get_type_by_id_customer(route.get_list_id_customers()[i]) == CustomerType.TC:
                exist = True
            else:
                i += 1

        return exist