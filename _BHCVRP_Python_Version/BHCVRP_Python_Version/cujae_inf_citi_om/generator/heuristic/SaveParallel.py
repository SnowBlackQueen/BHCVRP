from generator.heuristic.Save import Save
from generator.solution.Route import Route
from generator.solution.RouteTTRP import RouteTTRP
from generator.solution.RouteType import RouteType
from generator.solution.Solution import Solution
from data.Problem import Problem
from data.ProblemType import ProblemType
from data.Customer import Customer
from data.DepotMDVRP import DepotMDVRP
from generator.postoptimization.Operator_3opt import Operator_3opt
import numpy as np



class SaveParallel(Save):
    def __init__(self):
        super().__init__()

    def initialize_specifics(self):
        super().initialize_specifics()
        self.list_capacities = list(Problem.get_problem().fill_list_capacities(self.pos_depot))  
        
        self.inspect_routes(self.list_routes, self.list_capacities, self.solution, self.customers_to_visit)  
        
        self.total_capacity = self.capacity_vehicle

        self.iterations = (self.cant_customers * (self.cant_customers - 1)) / 2
        self.counter = 0
        self.row_customer = 0
        self.col_customer = 0
        self.pos_row = 0
        self.pos_col = 0

        # Encuentra el índice del valor máximo en save_matrix y desenrolla este índice a coordenadas (fila, columna)
        self.row, self.col = np.unravel_index(np.argmax(self.save_matrix), self.save_matrix.shape)

        self.route_row = Route()
        self.route_col = Route()
    
    def creating(self, route=None, request_route=None, list_tau=None, list_metrics=None):
        if self.type_problem in [0,2,3] or self.type_problem == ProblemType.CVRP or self.type_problem == ProblemType.MDVRP:    
            if self.checking_join(self.route_row, self.route_col, self.row_customer, self.col_customer, self.total_capacity):
                self.route.get_list_id_customers().extend(self.route_row.get_list_id_customers())
                self.route.get_list_id_customers().extend(self.route_col.get_list_id_customers())
                self.join = True
            else:
                if self.checking_join(self.route_col, self.route_row, self.col_customer, self.row_customer, self.total_capacity):
                    self.route.get_list_id_customers().extend(self.route_col.get_list_id_customers())
                    self.route.get_list_id_customers().extend(self.route_row.get_list_id_customers())
                    self.join = True

            if self.join:
                self.route.set_request_route(self.route_row.get_request_route() + self.route_col.get_request_route())
                self.route.set_id_depot(self.id_depot)

                self.list_routes.remove(self.route_row)
                self.list_routes.remove(self.route_col)
                self.list_routes.append(self.route)
                
        elif self.type_problem == 1 or self.type_problem == ProblemType.HFVRP:
            if self.checking_join(self.route_row, self.route_col, self.row_customer, self.col_customer, self.list_capacities[0]):
                self.route.get_list_id_customers().append(self.route_row.get_list_id_customers())
                self.route.get_list_id_customers().append(self.route_col.get_list_id_customers())
                self.join = True
            else:
                if self.checking_join(self.route_col, self.route_row, self.col_customer, self.row_customer, self.list_capacities[0]):
                    self.route.get_list_id_customers().append(self.route_col.get_list_id_customers())
                self.route.get_list_id_customers().append(self.route_row.get_list_id_customers())
                self.join = True

                if self.join:
                    self.route.set_request_route(self.route_row.get_request_route() + self.route_col.get_request_route())

                    self.list_routes.remove(self.route_row)
                    self.list_routes.remove(self.route_col)

                    if self.route.get_request_route() == self.list_capacities[0]:
                        self.route.set_id_depot(self.id_depot)

                        if len(self.route.get_list_id_customers()) >= 6:
                            self.three_opt.to_optimize(self.route)
                                
                            self.solution.get_list_routes().append(self.route)
                            self.list_capacities.pop(0)

                            is_open = True
                            self.update_customers_to_visit(self.route, self.customers_to_visit)

                        else:
                            self.list_routes.append(self.route)
                            
        elif self.type_problem == 4 or self.type_problem == ProblemType.TTRP:
            if self.compatible_routes(self.route_row, self.route_col) or self.compatible_routes(self.route_col, self.route_row):
                if self.route_row.get_type_route() != 0:
                    self.total_capacity += self.capacity_trailer
                    
                if self.checking_join(self.route_row, self.route_col, self.row_customer, self.col_customer, self.total_capacity):
                    self.route.get_list_id_customers().extend(self.route_row.get_list_id_customers())
                    self.route.get_list_id_customers().extend(self.route_col.get_list_id_customers())
                    self.join = True
                    
                    if self.route_row.get_type_route() == self.route_col.get_type_route():
                        self.type_route = self.route_row.get_type_route()
                    else:
                        if not self.route_row.get_type_route() == RouteType.PTR:
                            self.type_route = RouteType.CVR
                        else:
                            self.type_route = RouteType.PTR
                else:
                    self.total_capacity = self.capacity_vehicle
                            
                    if not self.route_col.get_type_route() == RouteType.PTR:
                        self.total_capacity += self.capacity_trailer
                    
                    if self.checking_join(self.route_col, self.route_row, self.col_customer, self.row_customer, self.total_capacity):
                        self.route.get_list_id_customers().extend(self.route_col.get_list_id_customers())
                        self.route.get_list_id_customers().extend(self.route_row.get_list_id_customers())
                        self.join = True
                    
                        if self.route_col.get_type_route() == self.route_row.get_type_route():
                            self.type_route = self.route_col.get_type_route()
                        else:
                            if not self.route_col.get_type_route() == RouteType.PTR:
                                self.type_route = RouteType.CVR
                            else:
                                self.type_route = RouteType.PTR
                    
            if self.join:
                self.route.set_request_route(self.route_row.get_request_route() + self.route_col.get_request_route())
                #route.setTypeRoute(type_route)
                self.route.set_id_depot(self.id_depot)
                list_access_VC = []
                route = RouteTTRP(self.route.get_list_id_customers(), self.route.get_request_route(), self.route.get_cost_route(),
                                        route.get_id_depot(), list_access_VC, self.type_route)
                        
                self.list_routes.remove(self.route_row)
                self.list_routes.remove(self.route_col)
                self.list_routes.append(self.route)
                        
                self.reduce_options(self.route, self.save_matrix)
    
    def processing(self, customers_to_visit=None, count_vehicles=None, request_route=None, route=None, id_depot=None, solution=None):
        if self.type_problem in [0, 2, 3, 4] or self.type_problem == ProblemType.CVRP or self.type_problem == ProblemType.MDVRP or self.type_problem == ProblemType.TTRP:
            if self.save_value > 0 or (self.save_value <= 0 and len(self.list_routes) > self.count_vehicles):
                self.row_customer = self.customers_to_visit[self.row].get_id_customer()
                self.col_customer = self.customers_to_visit[self.col].get_id_customer()
                self.counter += 1

                self.save_matrix[self.row, self.col] = -np.inf
                self.save_matrix[self.col, self.row] = -np.inf

                self.pos_row = self.get_position_route(self.list_routes, self.row_customer)
                self.pos_col = self.get_position_route(self.list_routes, self.col_customer)

                if self.pos_row == self.pos_col:
                    return

                self.route_row = self.list_routes[self.pos_row]
                self.route_col = self.list_routes[self.pos_col]

                self.route = Route()
                self.join = False
            
                self.creating()
            else:
                if self.save_value <= 0 and len(self.list_routes) <= self.count_vehicles:
                    self.save_matrix.fill(-np.inf)

        elif self.type_problem == 1 or self.type_problem == ProblemType.HFVRP:
            if (self.save_value > 0) or ((self.save_value <= 0) and (len(self.list_routes) > self.count_vehicles)):
                self.row_customer = self.customers_to_visit[self.row].get_id_customer()
                self.col_customer = self.customers_to_visit[self.col].get_id_customer()
                self.counter += 1

                self.save_matrix[self.row, self.col] = -np.inf
                self.save_matrix[self.col, self.row] = -np.inf

                self.pos_row = self.get_position_route(self.list_routes, self.row_customer)
                self.pos_col = self.get_position_route(self.list_routes, self.col_customer)

                if self.pos_row == self.pos_col:
                    return

                self.route_row = self.list_routes[self.pos_row]
                self.route_col = self.list_routes[self.pos_col]

                self.route = Route()
                self.join = False

                self.creating()

            if self.counter == self.iterations or not np.all(self.save_matrix == -np.inf):
                self.close_route = self.route_to_close(self.list_routes)

                self.close_route.set_id_depot(self.id_depot)

                if len(self.close_route.get_list_id_customers()) >= 6:
                    self.three_opt.to_optimize(self.close_route)
                        
                self.solution.get_list_routes().append(self.close_route)
                self.list_capacities.pop(0)

                self.is_open = True
                self.update_customers_to_visit(self.close_route, self.customers_to_visit)

            if len(self.list_routes) == 1:
                self.list_routes[0].set_id_depot(self.id_depot)

                if len(self.list_routes[0].get_list_id_customers()) >= 6:
                    self.three_opt.to_optimize(self.list_routes[0])
                        
                self.solution.get_list_routes().append(self.list_routes[0])
                self.list_routes.pop(0)

                self.is_open = True
    
    def execute(self):
        if self.type_problem == 0 or self.type_problem == ProblemType.CVRP:
            cond1 = self.counter < self.iterations
            cond2 = len(self.list_routes) > 1
            cond3 = not np.all(self.save_matrix == -np.inf)

            while self.counter < self.iterations and len(self.list_routes) > 1 and not np.all(self.save_matrix == -np.inf):
                self.save_value = self.save_matrix[self.row, self.col]

                self.processing()
                self.row, self.col = np.unravel_index(np.argmax(self.save_matrix), self.save_matrix.shape)

            for j in range(len(self.list_routes)):
                if len(self.list_routes[j].get_list_id_customers()) >= 6:
                    self.three_opt.to_optimize(self.list_routes[j])

            self.solution.get_list_routes().extend(self.list_routes)
        
        if self.type_problem == 1 or self.type_problem == ProblemType.HFVRP:
            self.is_first = True
            self.is_open = False

            while self.list_routes and self.list_capacities:
                if (self.counter == self.iterations) and (not self.is_open): #es q recorri ya la matriz completa
                    self.close_route = self.route_to_close(self.list_routes)
                    self.close_route.set_id_depot(self.id_depot)

                    if len(self.close_route.get_list_id_customers()) >= 6:
                        self.three_opt.to_optimize(self.close_route)

                    self.solution.get_list_routes().append(self.close_route)
                    self.list_capacities.pop(0)

                    self.is_open = True
                    self.update_customers_to_visit(self.close_route, self.customers_to_visit)

                    if len(self.list_routes) == 1:

                        self.list_routes[0].set_id_depot(self.id_depot)

                        if len(self.list_routes[0].get_list_id_customers()) >= 6:
                            self.three_opt.to_optimize(self.list_routes[0])
                        
                        self.solution.get_list_routes().append(self.list_routes[0])
                        self.list_routes.pop(0)         
                

                self.is_open = False

                if not self.is_first:
                    self.cant_customers = len(self.customers_to_visit)
                    self.save_matrix = np.zeros(self.cant_customers, self.cant_customers)
                    self.save_matrix = self.fill_save_matrix(self.id_depot, self.customers_to_visit)

                    self.iterations = (self.cant_customers * (self.cant_customers - 1)) / 2
                    self.counter = 0

                self.is_first = False
                
                while self.counter < self.iterations and len(self.list_routes) > 1 and not np.all(self.save_matrix == -np.inf) and self.list_capacities and (not self.is_open):
                    self.save_value = self.save_matrix[self.row, self.col]
                    
                    self.processing()

                if len(self.list_routes) > 0:
                    self.route = Route()
                    self.request = 0.0

                    self.route.set_id_depot(self.id_depot)

                    while self.list_routes:
                        self.request += self.list_routes[0].get_request_route()
                        self.route.set_request_route(self.request)
                        self.route.get_list_id_customers().append(self.list_routes[0].get_list_id_customers())
                        self.list_routes.pop(0)

                    if len(self.route.get_list_id_customers()) >= 6:
                        self.three_opt.to_optimize(self.route)
                    
                    self.solution.get_list_routes().append(self.route)
        
        elif self.type_problem == 2 or self.type_problem == ProblemType.MDVRP:
            for j in range(self.pos_depot, len(Problem.get_problem().get_list_depots())):
                if j != self.pos_depot:
                    self.id_depot = Problem.get_problem().get_list_depots().get(j).get_id_depot()
                    self.customers_to_visit = list(Problem.get_problem().get_customers_assigned_by_id_depot(self.id_depot))
                    
                    self.capacity_vehicle = Problem.get_problem().get_list_depots().get(j).get_list_fleets()[0].get_capacity_vehicle()
                    self.count_vehicles = Problem.get_problem().get_list_depots().get(j).get_list_fleets()[0].get_count_vehicles()
                    
                    self.list_capacities = list(Problem.getProblem().getListCapacities())  # fill o listparametro con el depot
                    
                    if self.customers_to_visit:
                        self.list_routes = self.create_initial_routes(self.customers_to_visit)
                        self.inspect_routes(self.list_routes, self.list_capacities, self.solution, self.customers_to_visit)
                        
                        self.cant_customers = len(self.customers_to_visit)
                        self.save_matrix = np.zeros(self.cant_customers, self.cant_customers)
                        self.save_matrix = self.fill_save_matrix(Problem.get_problem().get_list_depots().get(j).get_id_depot(), self.customers_to_visit)
                        
                        self.total_capacity = self.capacity_vehicle
                        self.iterations = (self.cant_customers * (self.cant_customers - 1)) / 2
                        self.counter = 0
                
                while self.counter < self.iterations and len(self.list_routes) > 1 and not np.all(self.save_matrix == -np.inf):
                    self.save_value = self.save_matrix[self.row, self.col]
                    
                    self.processing
                
                self.solution.get_list_routes().extend(self.list_routes)
                
        elif self.type_problem == 4 or self.type_problem == ProblemType.TTRP:
            self.capacity_trailer = Problem.get_problem().get_list_depots()[self.pos_depot].get_list_fleets()[0].get_capacity_trailer()

            while self.counter < self.iterations and len(self.list_routes) > 1 and not np.all(self.save_matrix == -np.inf):
                self.save_value = self.save_matrix[self.row, self.col]
                
                self.processing()
                
            for j in range(len(self.list_routes)):
                if len(self.list_routes[j].get_list_id_customers()) >= 6:
                    self.three_opt.to_optimize(self.list_routes[j])

            self.solution.get_list_routes().extend(self.list_routes)
                
        return self.solution
    
    def get_solution_inicial(self):
        
        self.execute()
            
        return self.solution
    
    # Método que revisa si alguna ruta cumple con la capacidad, la cierra y actualiza CustomersToVisit
    def inspect_routes(self, list_routes, list_capacities, solution, customers_to_visit):
        for i in range(len(list_routes)):
            j = 0
            found = False

            while j < len(list_capacities) and not found: # se debe eliminar la capacidad de la lista
                if list_routes[i].get_request_route() == list_capacities[j]:
                    solution.get_list_routes().append(list_routes[i])
                    list_routes.pop(i)
                    list_capacities.pop(j)
                    self.update_customers_to_visit(list_routes[i], customers_to_visit)

                    found = True
                else:
                    j+=1
    
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

    # Método que devuelve la ruta con la demanda más cercana a la capacidad
    def route_to_close(self, list_routes):
        route = Route()
        
        max_capacity = list_routes[0].get_request_route()
        pos_max = 0
        
        for i in range(1, len(list_routes)):
            if list_routes[i].get_request_route() > max_capacity:
                max_capacity = list_routes[i].get_request_route()
                pos_max = i
        
        route = list_routes[pos_max]
        list_routes.pop(pos_max)
        
        return route

    # Método que indica si dos rutas pueden unirse
    def checking_join(self, route_ini, route_end, id_customer_ini, id_customer_end, total_capacity):
        join = False
        size_route = len(route_ini.get_list_id_customers())
        
        if (route_ini.get_request_route() + route_end.get_request_route()) <= total_capacity:
            if (route_ini.get_list_id_customers()[size_route - 1] == id_customer_ini) and (route_end.get_list_id_customers()[0] == id_customer_end):
                join = True
        
        return join

    # Método que indica si dos rutas son compatibles
    def compatible_routes(self, route_ini, route_end):
        is_compatible = True
        
        if isinstance(route_ini, RouteTTRP) and route_ini.type_route == RouteType.PTR and not isinstance(route_end, RouteTTRP):
            is_compatible = False
        
        return is_compatible