from heuristic.Save import Save
from solution.Route import Route
from solution.RouteTTRP import RouteTTRP
from solution.RouteType import RouteType
from solution.Solution import Solution
from data.Problem import Problem
from data.ProblemType import ProblemType
from data.Customer import Customer
from data.DepotMDVRP import DepotMDVRP
from postoptimization.Operator_3opt import Operator_3opt
import numpy as np



class SaveParallel(Save):
    def __init__(self):
        super().__init__()

    def initialize_specifics(self):
        self.list_capacities = list(Problem.get_problem().fill_list_capacities(self.pos_depot))  
        
        self.inspect_routes(self.list_routes, self.list_capacities, self.solution, self.customers_to_visit)  
        
        self.total_capacity = self.capacity_vehicle

        self.iterations = (self.cant_customers * (self.cant_customers - 1)) / 2
        self.counter = 0
        self.row_customer = 0
        self.col_customer = 0
        self.pos_row = 0
        self.pos_col = 0

        self.row_col = np.unravel_index(np.argmax(self.save_matrix), self.save_matrix.shape)
        self.route_row = Route()
        self.route_col = Route()
    
    def get_solution_inicial(self):
        
        if self.type_problem == 0:
            while counter < iterations and len(list_routes) > 1 and not np.all(save_matrix == np.NINF):
                save_value = save_matrix[row_col, row_col]

                if save_value > 0 or (save_value <= 0 and len(list_routes) > count_vehicles):
                    row_customer = customers_to_visit[row_col].get_id_customer()
                    col_customer = customers_to_visit[row_col].get_id_customer()
                    counter += 1

                    save_matrix[row_col, row_col] = np.NINF
                    save_matrix[row_col, row_col] = np.NINF

                    pos_row = self.get_position_route(list_routes, row_customer)
                    pos_col = self.get_position_route(list_routes, col_customer)

                    #if posRow == posCol:
                    #    continue

                    route_row = list_routes[pos_row]
                    route_col = list_routes[pos_col]

                    route = Route()
                    join = False

                    if self.checking_join(route_row, route_col, row_customer, col_customer, total_capacity):
                        route.get_list_id_customers().extend(route_row.get_list_id_customers())
                        route.get_list_id_customers().extend(route_col.get_list_id_customers())
                        join = True
                    else:
                        if self.checking_join(route_col, route_row, col_customer, row_customer, total_capacity):
                            route.get_list_id_customers().extend(route_row.get_list_id_customers())
                            route.get_list_id_customers().extend(route_col.get_list_id_customers())
                            join = True

                    if join:
                        route.set_request_route(route_row.get_request_route() + route_col.get_request_route())
                        route.set_id_depot(id_depot)

                        list_routes.remove(route_row)
                        list_routes.remove(route_col)
                        list_routes.append(route)
                else:
                    if save_value <= 0 and len(list_routes) <= count_vehicles:
                        save_matrix.fill(np.NINF)

            for j in range(len(list_routes)):
                if len(list_routes[j].get_list_id_customers()) >= 6:
                    three_opt.to_optimize(list_routes[j])

            solution.get_list_routes().extend(list_routes)

        elif type_problem == 1:
            is_first = True
            is_open = False

            while list_routes and list_capacities:
                if (counter == iterations) and (not is_open): #es q recorri ya la matriz completa
                    close_route = self.route_to_close(list_routes)
                    close_route.set_id_depot(id_depot)

                    if len(close_route.get_list_id_customers()) >= 6:
                        three_opt.to_optimize(close_route)

                    solution.get_list_routes().add(close_route)
                    list_capacities.remove(0)

                    is_open = True
                    self.update_customers_to_visit(close_route, customers_to_visit)

                    if len(list_routes) == 1:

                        list_routes.get(0).set_id_depot(id_depot)

                        if len(list_routes.get(0).get_list_id_customers()) >= 6:
                            three_opt.to_optimize(list_routes.get(0))
                        
                        solution.get_list_routes().add(list_routes.get(0))
                        list_routes.remove(0)         
                

                is_open = False

                if not is_first:
                    cant_customers = len(customers_to_visit)
                    save_matrix = np.zeros(cant_customers, cant_customers)
                    save_matrix = self.fill_save_matrix(id_depot, customers_to_visit)

                    iterations = (cant_customers * (cant_customers - 1)) / 2
                    counter = 0

                is_first = False
                
                while counter < iterations and len(list_routes) > 1 and not np.all(save_matrix == np.NINF) and list_capacities and (not is_open):
                    save_value = save_matrix[row_col, row_col]
                    
                    if (save_value > 0) or ((save_value <= 0) and (len(list_routes) > count_vehicles)):
                        row_customer = customers_to_visit[row_col].get_id_customer()
                        col_customer = customers_to_visit[row_col].get_id_customer()
                        counter += 1

                        save_matrix[row_col, row_col] = np.NINF
                        save_matrix[row_col, row_col] = np.NINF

                        pos_row = self.get_position_route(list_routes, row_customer)
                        pos_col = self.get_position_route(list_routes, col_customer)

                        if pos_row == pos_col:
                            continue

                        route_row = list_routes[pos_row]
                        route_col = list_routes[pos_col]

                        route = Route()
                        join = False

                        if self.checking_join(route_row, route_col, row_customer, col_customer, list_capacities[0]):
                            route.get_list_id_customers().extend(route_row.get_list_id_customers())
                            route.get_list_id_customers().extend(route_col.get_list_id_customers())
                            join = True
                        else:
                            if self.checking_join(route_col, route_row, col_customer, row_customer, list_capacities[0]):
                                route.get_list_id_customers().extend(route_col.get_list_id_customers())
                                route.get_list_id_customers().extend(route_row.get_list_id_customers())
                                join = True

                        if join:
                            route.set_request_route(route_row.get_request_route() + route_col.get_request_route())

                            list_routes.remove(route_row)
                            list_routes.remove(route_col)

                            if route.get_request_route() == list_capacities[0]:
                                route.set_id_depot(id_depot)

                                if len(route.get_list_id_customers()) >= 6:
                                    three_opt.to_optimize(route)
                                
                                solution.get_list_routes().append(route)
                                list_capacities.pop(0)

                                is_open = True
                                self.update_customers_to_visit(route, customers_to_visit)

                            else:
                                list_routes.append(route)

                    if counter == iterations or not np.all(save_matrix == np.NINF):
                        close_route = self.route_to_close(list_routes)

                        close_route.set_id_depot(id_depot)

                        if len(close_route.get_list_id_customers()) >= 6:
                            three_opt.to_optimize(close_route)
                        
                        solution.get_list_routes().append(close_route)
                        list_capacities.pop(0)

                        is_open = True
                        self.update_customers_to_visit(close_route, customers_to_visit)

                    if len(list_routes) == 1:
                        list_routes[0].setIdDepot(id_depot)

                        if len(list_routes[0].get_list_id_customers()) >= 6:
                            three_opt.to_optimize(list_routes[0])
                        
                        solution.get_list_routes().append(list_routes[0])
                        list_routes.pop(0)

                        is_open = True

                if len(list_routes) > 0:
                    route = Route()
                    new_request = 0.0

                    route.set_id_depot(id_depot)

                    while list_routes:
                        new_request += list_routes[0].get_request_route()
                        route.set_request_route(new_request)
                        route.get_list_id_customers().extend(list_routes[0].get_list_id_customers())
                        list_routes.pop(0)

                    if len(route.get_list_id_customers()) >= 6:
                        three_opt.to_optimize(route)
                    
                    solution.get_list_routes().append(route)
                    
        elif type_problem == 2:
            for j in range(pos_depot, len(Problem.get_problem().get_list_depots())):
                if j != pos_depot:
                    id_depot = Problem.get_problem().get_list_depots().get(j).get_id_depot()
                    customers_to_visit = list(Problem.get_problem().get_customers_assigned_by_id_depot(id_depot))
                    
                    capacity_vehicle = Problem.get_problem().get_list_depots().get(j).get_list_fleets().get(0).get_capacity_vehicle()
                    count_vehicles = Problem.get_problem().get_list_depots().get(j).get_list_fleets().get(0).get_count_vehicles()
                    
                    list_capacities = list(Problem.getProblem().getListCapacities())  # fill o listparametro con el depot
                    
                    if customers_to_visit:
                        list_routes = self.create_initial_routes(customers_to_visit)
                        self.inspect_routes(list_routes, list_capacities, solution, customers_to_visit)
                        
                        cant_customers = len(customers_to_visit)
                        save_matrix = np.zeros(cant_customers, cant_customers)
                        save_matrix = self.fill_save_matrix(Problem.get_problem().get_list_depots().get(j).get_id_depot(), customers_to_visit)
                        
                        total_capacity = capacity_vehicle
                        iterations = (cant_customers * (cant_customers - 1)) / 2
                        counter = 0
                
                while counter < iterations and len(list_routes) > 1 and not np.all(save_matrix == np.NINF):
                    save_value = save_matrix[row_col, row_col]
                    
                    if save_value > 0 or (save_value <= 0 and len(list_routes) > count_vehicles):
                        row_customer = customers_to_visit[row_col].get_id_customer()
                        col_customer = customers_to_visit[row_col].get_id_customer()
                        counter += 1
                        
                        save_matrix[row_col, row_col] = np.NINF
                        save_matrix[row_col, row_col] = np.NINF
                        
                        pos_row = self.get_position_route(list_routes, row_customer)
                        pos_col = self.get_position_route(list_routes, col_customer)
                        
                        if pos_row == pos_col:
                            continue
                        
                        route_row = list_routes[pos_row]
                        route_col = list_routes[pos_col]
                        
                        route = Route()
                        join = False
                        
                        if self.checking_join(route_row, route_col, row_customer, col_customer, total_capacity):
                            route.get_list_id_customers().extend(route_row.get_list_id_customers())
                            route.get_list_id_customers().extend(route_col.get_list_id_customers())
                            join = True
                        
                        else:
                            if self.checking_join(route_col, route_row, col_customer, row_customer, total_capacity):
                                route.get_list_id_customers().extend(route_col.get_list_id_customers())
                                route.get_list_id_customers().extend(route_row.get_list_id_customers())
                                join = True
                        
                        if join:
                            route.set_request_route(route_row.get_request_route() + route_col.get_request_route())
                            route.set_id_depot(id_depot)
                            
                            list_routes.remove(route_row)
                            list_routes.remove(route_col)
                            list_routes.append(route)
                        
                    else:
                        if save_value <= 0 and len(list_routes) <= count_vehicles:
                            save_matrix.fill(np.NINF)
                
                solution.get_list_routes().extend(list_routes)
                
        elif type_problem == 4:
            capacity_trailer = Problem.get_problem().get_list_depots()[pos_depot].get_list_fleets()[0].get_capacity_trailer()

            while counter < iterations and len(list_routes) > 1 and not np.all(save_matrix == np.NINF):
                save_value = save_matrix[row_col, row_col]
                
                if save_value > 0 or (save_value <= 0 and len(list_routes) > count_vehicles):
                    row_customer = customers_to_visit[row_col].get_id_customer() 
                    col_customer = customers_to_visit[row_col].get_id_customer()
                    counter += 1
                    
                    save_matrix[row_col, row_col] = np.NINF 
                    save_matrix[row_col, row_col] = np.NINF
                    
                    pos_row = self.get_position_route(list_routes, row_customer)
                    pos_col = self.get_position_route(list_routes, col_customer)
                    
                    if pos_row == pos_col:
                        continue
                    
                    route_row = list_routes[pos_row]
                    route_col = list_routes[pos_col]
                    
                    route = Route()
                    join = False
                    type_route = None
                    
                    total_capacity = capacity_vehicle
                    
                    if self.compatible_routes(route_row, route_col) or self.compatible_routes(route_col, route_row):
                        if route_row.get_type_route() != 0:
                            total_capacity += capacity_trailer
                    
                        if self.checking_join(route_row, route_col, row_customer, col_customer, total_capacity):
                            route.get_list_id_customers().extend(route_row.get_list_id_customers())
                            route.get_list_id_customers().extend(route_col.get_list_id_customers())
                            join = True
                    
                            if route_row.get_type_route() == route_col.get_type_route():
                                type_route = route_row.get_type_route()
                            else:
                                if not route_row.get_type_route() == RouteType.PTR:
                                    type_route = RouteType.CVR
                                else:
                                    type_route = RouteType.PTR
                        else:
                            total_capacity = capacity_vehicle
                            
                            if not route_col.get_type_route() == RouteType.PTR:
                                total_capacity += capacity_trailer
                    
                            if self.checking_join(route_col, route_row, col_customer, row_customer, total_capacity):
                                route.get_list_id_customers().extend(route_col.get_list_id_customers())
                                route.get_list_id_customers().extend(route_row.get_list_id_customers())
                                join = True
                    
                                if route_col.get_type_route() == route_row.get_type_route():
                                    type_route = route_col.get_type_route()
                                else:
                                    if not route_col.get_type_route() == RouteType.PTR:
                                        type_route = RouteType.CVR
                                    else:
                                        type_route = RouteType.PTR
                    
                    if join:
                        route.set_request_route(route_row.get_request_route() + route_col.get_request_route())
                        #route.setTypeRoute(type_route)
                        route.set_id_depot(id_depot)
                        list_access_VC = []
                        route = RouteTTRP(route.get_list_id_customers(), route.get_request_route(), route.get_cost_route(),
                                        route.get_id_depot(), list_access_VC, type_route)
                        
                        list_routes.remove(route_row)
                        list_routes.remove(route_col)
                        list_routes.append(route)
                        
                        self.reduce_options(route, save_matrix)
                
            for j in range(len(list_routes)):
                if len(list_routes[j].get_list_id_customers()) >= 6:
                    three_opt.to_optimize(list_routes[j])

            solution.get_list_routes().extend(list_routes)
            
        return solution
    
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
        for i in range(len(close_route.list_id_customers)):
            j = 0
            found = False
            
            while j < len(customers_to_visit) and not found:
                if customers_to_visit[j].id_customer == close_route.list_id_customers[i]:
                    customers_to_visit.pop(j)
                    found = True
                else:
                    j += 1

    # Método que devuelve la ruta con la demanda más cercana a la capacidad
    def route_to_close(self, list_routes):
        route = Route()
        
        max_capacity = list_routes[0].request_route
        pos_max = 0
        
        for i in range(1, len(list_routes)):
            if list_routes[i].request_route > max_capacity:
                max_capacity = list_routes[i].request_route
                pos_max = i
        
        route = list_routes[pos_max]
        list_routes.pop(pos_max)
        
        return route

    # Método que indica si dos rutas pueden unirse
    def checking_join(self, route_ini, route_end, id_customer_ini, id_customer_end, total_capacity):
        join = False
        size_route = len(route_ini.list_id_customers)
        
        if (route_ini.request_route + route_end.request_route) <= total_capacity:
            if (route_ini.list_id_customers[size_route - 1] == id_customer_ini) and (route_end.list_id_customers[0] == id_customer_end):
                join = True
        
        return join

    # Método que indica si dos rutas son compatibles
    def compatible_routes(self, route_ini, route_end):
        is_compatible = True
        
        if isinstance(route_ini, RouteTTRP) and route_ini.type_route == RouteType.PTR and not isinstance(route_end, RouteTTRP):
            is_compatible = False
        
        return is_compatible