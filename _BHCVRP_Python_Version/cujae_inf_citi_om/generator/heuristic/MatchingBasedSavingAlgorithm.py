from generator.heuristic.Save import Save
from data.Problem import Problem
from data.Customer import Customer
from data.Depot import Depot
from generator.solution.Route import Route
from generator.solution.Solution import Solution
from typing import List, Tuple, Dict
from data.ProblemType import ProblemType
import numpy as np
from generator.solution.RouteType import RouteType


class MatchingBasedSavingAlgorithm (Save):
    def __init__(self):
        super().__init__()

    def initialize_specifics(self):
        super().initialize_specifics()

        self.depots = Problem.get_problem().get_list_depots()
        self.depot = self.depots[0]

        if self.type_problem == 2 or self.type_problem == ProblemType.MDVRP:
            self.customers = Problem.get_problem().get_customers_assigned_by_id_depot(self.id_depot, Problem.get_problem().get_list_customers(), self.depots)

        else:
            self.customers = Problem.get_problem().get_list_customers()
        
        # Define cost matrix (distances between depot and customers, and customers themselves)
        #self.cost_matrix = Problem.get_problem().get_cost_matrix()

        #self.routes = []
    
    def get_solution_inicial(self):
        if self.type_problem == 0 or self.type_problem == ProblemType.CVRP:  
            self.list_routes = self.match_based_savings_algorithm(self.customers, self.depots)

            # for r in self.list_routes:
            #    if len(r.get_list_id_customers()) >= 6:
            #        self.three_opt.to_optimize(r)

            self.solution.get_list_routes().extend(self.list_routes)

        elif self.type_problem == 1 or self.type_problem == ProblemType.HFVRP:
            self.list_capacities = list(Problem.get_problem().get_list_capacities())

            while (len(self.list_routes) > 0 and len(self.list_capacities) > 0):
                self.list_routes = self.match_based_savings_algorithm(self.customers, self.depots)

                self.list_capacities.pop(0)

            self.solution.get_list_routes().extend(self.list_routes)

        elif self.type_problem == 2 or self.type_problem == ProblemType.MDVRP: #REVISAR
            self.repeat = False
            self.depot_finish = False
            for j in range(self.pos_depot, len(Problem.get_problem().get_list_depots())):
                if j != self.pos_depot:
                    self.id_depot = Problem.get_problem().get_list_depots()[j].get_id_depot()
                    self.customers = Problem.get_problem().get_customers_assigned_by_id_depot(self.id_depot, Problem.get_problem().get_list_customers(), Problem.get_problem().get_list_depots())

                    self.capacity_vehicle = Problem.get_problem().get_list_depots()[j].get_list_fleets()[0].get_capacity_vehicle()

                    if self.customers:
                        self.list_routes = self.create_initial_routes(self.customers)
                        self.cant_customers = len(self.customers)
                        self.save_matrix = np.full((self.cant_customers, self.cant_customers), 0)
                        self.save_matrix = self.fill_save_matrix(self.id_depot, self.customers)

                while self.list_routes and not self.repeat and not self.depot_finish and self.customers:
                    self.list_routes = self.match_based_savings_algorithm(self.customers, self.depots)
                    self.cant_customers = len(self.customers)

                    if j == (len(self.depots)-1):
                        self.depot_finish = True

                self.solution.get_list_routes().extend(self.list_routes)


        elif self.type_problem == 4 or self.type_problem == ProblemType.TTRP:
            self.capacity_trailer = Problem.get_problem().get_list_depots()[self.pos_depot].get_list_fleets()[0].get_capacity_trailer()

            while self.list_routes:
                self.list_routes = self.match_based_savings_algorithm(self.customers, self.depots)

            self.solution.get_list_routes().extend(self.list_routes)

        return self.solution
    
    def calculate_savings_matrix(self, customers: List[Customer]) -> List[Tuple[Tuple[int, int], float]]:
        """Calculate savings for each pair of customers based on cost matrix and depot location."""
        savings_list = []
        #if self.type_problem == 0 or self.type_problem == 1 or self.type_problem == 4 or self.type_problem == ProblemType.CVRP or self.type_problem == ProblemType.HFVRP or self.type_problem == ProblemType.TTRP:
            #for k in range (len(self.depots)):
        for i in range(len(customers)):
            for j in range(i + 1, len(customers)):
                c_i, c_j = customers[i], customers[j]

                if self.type_problem == 2 or self.type_problem == ProblemType.MDVRP:
                    ci = Problem.get_problem().get_pos_element_by_id_depot(self.id_depot, c_i.get_id_customer(), self.depots)
                    cj = Problem.get_problem().get_pos_element_by_id_depot(self.id_depot, c_j.get_id_customer(), self.depots)
                else:
                    ci = Problem.get_problem().get_pos_element(c_i.get_id_customer())
                    cj = Problem.get_problem().get_pos_element(c_j.get_id_customer())

                if self.type_problem == 0 or self.type_problem == 1 or self.type_problem == 4 or self.type_problem == ProblemType.CVRP or self.type_problem == ProblemType.HFVRP or self.type_problem == ProblemType.TTRP:
                    self.pos_depot = (Problem.get_problem().get_pos_element(self.depots[0]._id_depot)) - self.cant_customers
                else:
                    self.pos_depot = (Problem.get_problem().get_pos_element(self.cant_customers))
                depot_to_i = self.save_matrix[self.pos_depot][ci]
                depot_to_j = self.save_matrix[self.pos_depot][cj]
                i_to_j = self.save_matrix[ci][cj]

                savings = depot_to_i + depot_to_j - i_to_j
                savings_list.append(((c_i._id_customer, c_j._id_customer), savings))

        #else:
         #   pass

        # Sort savings in descending order
        savings_list.sort(key=lambda x: x[1], reverse=True)
        return savings_list

    def match_based_savings_algorithm(self, customers: List[Customer], depots: List[Depot]) -> List[Route]:
        if self.type_problem == 0 or self.type_problem == 1 or self.type_problem == 2 or self.type_problem == ProblemType.CVRP or self.type_problem == ProblemType.HFVRP or self.type_problem == ProblemType.MDVRP:    
            """Solve CVRP using matching-based savings algorithm."""
            if self.type_problem == 1 or self.type_problem == ProblemType.HFVRP:
                fleet_capacity = self.list_capacities[0]
            else:
                fleet_capacity = depots[0]._list_fleets[0]._capacity_vehicle
            
            # Step 1: Calculate savings matrix
            savings_list = self.calculate_savings_matrix(customers)
            
            # Step 2: Merge routes based on savings
            for (c1_id, c2_id), saving in savings_list:
                route1 = None
                route2 = None
                
                for route in self.list_routes:
                    if c1_id in route.list_id_customers:
                        route1 = route
                    if c2_id in route.list_id_customers:
                        route2 = route
                
                if route1 is None or route2 is None or route1 == route2:
                    continue  # Skip if they're already merged
                
                combined_demand = route1.request_route + route2.request_route
                if combined_demand <= fleet_capacity:
                    # Merge the routes
                    merged_route = Route(list_id_customers=route1.list_id_customers + route2.list_id_customers,
                                        request_route=combined_demand,
                                        cost_route=route1.cost_route + route2.cost_route - saving,
                                        id_depot=depots[0]._id_depot, list_access_vc=None, maximum_distance=None)
                    #merged_route.get_cost_single_route()
                    
                    # Remove old routes and add the new merged route
                    self.list_routes.remove(route1)
                    self.list_routes.remove(route2)

                    if len(merged_route.get_list_id_customers()) >= 6:
                        self.three_opt.to_optimize(merged_route)

                    self.list_routes.append(merged_route)

                    if self.type_problem == 1 or self.type_problem == ProblemType.HFVRP:
                        self.route = merged_route
                        self.update_customers_to_visit(merged_route, self.customers_to_visit)

            if self.type_problem == 2 or self.type_problem == ProblemType.MDVRP:
                for c in self.customers:
                    for r in range (len(self.list_routes)):
                        for i in range (len(self.list_routes[r].get_list_id_customers())):
                            if c.get_id_customer() == self.list_routes[r].get_list_id_customers()[i]:
                                self.customers.pop(0)
                routes_copy = self.list_routes.copy()
                if len(routes_copy) == len(self.list_routes) and self.depot_finish:
                    self.repeat = True
            #for r in self.list_routes:
            #    if len(r.get_list_id_customers()) >= 6:
            #        self.three_opt.to_optimize(r)

        elif self.type_problem == 4 or self.type_problem == ProblemType.TTRP:  #REVISAR
            type_route = self.current_route._type_route

            if ((type_route == 0 or type_route == RouteType.PTR and self.current_route.get_request_route() == self.capacity_vehicle)
                    or ((type_route == 1 or type_route == RouteType.PVR or type_route == 2 or type_route == RouteType.CVR) and
                    self.current_route.get_request_route() == (self.capacity_vehicle + self.capacity_trailer))):
                # Llenar con infinito negativo para ext_inic
                self.save_matrix[Problem.get_problem().get_pos_element(self.ext_inic), :] = -np.inf
                self.save_matrix[:, Problem.get_problem().get_pos_element(self.ext_inic)] = -np.inf

                # Llenar con infinito negativo para ext_end
                self.save_matrix[Problem.get_problem().get_pos_element(self.ext_end), :] = -np.inf
                self.save_matrix[:, Problem.get_problem().get_pos_element(self.ext_end)] = -np.inf

                self.exist_save = False
                print("existSave = False")
                return

        return self.list_routes
        

    # Método que actualiza la lista de CustomersToVisit
    def update_customers_to_visit(self, close_route, customers_to_visit):
        for i in range(len(close_route.get_list_id_customers())):
            j = 0
            found = False
            
            while j < len(customers_to_visit) and not found:
                if customers_to_visit[j].get_id_customer() == close_route.get_list_id_customers()[i]:
                    customers_to_visit.pop(j)
                    found = True
                else:
                    j += 1