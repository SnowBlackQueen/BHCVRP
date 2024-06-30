from heuristic.Heuristic import Heuristic
from data.Problem import Problem
from data.ProblemType import ProblemType
from heuristic.Metric import Metric
from data.CustomerType import CustomerType
from solution.Solution import Solution
from solution.Route import Route
from solution.RouteType import RouteType
from solution.RouteTTRP import RouteTTRP
from data.Customer import Customer
from data.CustomerType import CustomerType
from data.CustomerTTRP import CustomerTTRP

class KilbyAlgorithm(Heuristic):
    
    def __init__(self):
        super().__init__()

    def get_solution_inicial(self):
        solution = Solution()
        customers_to_visit = None

        pos_depot = -1
        list_candidate_routes = []
        list_kilby_costs = None

        if Problem.get_problem().get_type_problem() == ProblemType.CVRP or Problem.get_problem().get_type_problem() == ProblemType.HFVRP or Problem.get_problem().get_type_problem() == ProblemType.OVRP or Problem.get_problem().get_type_problem() == ProblemType.TTRP:
            customers_to_visit = list(Problem.get_problem().get_list_customers())
            pos_depot = 0
        else: 
            i = 0
            found = False
            
            while i < len(Problem.get_problem().get_list_depots()) and not found:
                if not Problem.get_problem().get_list_depots()[i].get_list_assigned_customers():
                    customers_to_visit = list(Problem.get_problem().get_customers_assigned_by_id_depot(Problem.get_problem().get_list_depots()[i].get_id_depot()))
                    found = True
                    pos_depot = i
                else:
                    i += 1
        
        count_vehicles = 0
        count_trailers = 0
        capacity_vehicle = Problem.get_problem().get_list_depots()[pos_depot].get_list_fleets()[0].get_capacity_vehicle()
        
        if Problem.get_problem().get_type_problem() == ProblemType.CVRP:
            count_trailers = Problem.get_problem().get_list_depots()[pos_depot].get_list_fleets()[0].get_count_trailers()
        
        if Problem.get_problem().get_type_problem() == ProblemType.HFVRP:
            count_vehicles = len(Problem.get_problem().fill_list_capacities())
        else:
            count_vehicles = Problem.get_problem().get_list_depots()[pos_depot].get_list_fleets()[0].get_count_vehicles()
        
        #Operator_2opt stepOptimizacion1 = new Operator_2opt();
        #Operator_Relocate stepOptimizacion2 = new Operator_Relocate();
        #Operator_Exchange stepOptimizacion3 = new Operator_Exchange();

        customer = None
        metric_kilby = None
        request = 0.0
        pos_route = -1
        is_route_full = True
        routes_with_customers = 0

        for i in range(count_vehicles):
            route = Route()
            list_candidate_routes.append(route)
            
        type_problem = Problem.get_problem().get_type_problem()
        list_route_opt = []
        
        if type_problem in [0, 3]:
            if customers_to_visit:
                list_kilby_costs = []
                list_kilby_costs = self.select_best_cost(count_vehicles, count_trailers, Problem.get_problem().get_list_depots().get(pos_depot).get_id_depot(), customers_to_visit)

                while list_kilby_costs:
                    i = 0
                    while i < len(list_candidate_routes) and list_kilby_costs:
                        customer = Customer()
                        customer = self._get_customer_by_id(list_kilby_costs[0].get_id_element(), customers_to_visit)
                        request = customer.get_request_customer()

                        list_candidate_routes[i].get_list_id_customers().append(customer.get_id_customer())
                        list_candidate_routes[i].set_request_route(request)
                        list_candidate_routes[i].set_id_depot(Problem.get_problem().get_list_depots().get(pos_depot).get_id_depot())
                        list_kilby_costs.pop(0)
                        customers_to_visit.remove(customer)
                        routes_with_customers += 1

                        i += 1

                j = routes_with_customers

                while routes_with_customers < len(list_candidate_routes):
                    list_candidate_routes.remove(j)

                while list_candidate_routes and customers_to_visit:
                    metric_kilby = Metric()
                    metric_kilby = self.get_best_customer(Problem.get_problem().get_list_depots().get(pos_depot).get_id_depot(), customers_to_visit, list_candidate_routes, capacity_vehicle, count_trailers)

                    if metric_kilby is None:
                        posRoute = self.close_route(list_candidate_routes)
                        is_route_full = False
                    else:
                        customer_insert = Customer()
                        customer_insert = self._get_customer_by_id(metric_kilby.get_id_element(), customers_to_visit)

                        posRoute = metric_kilby.get_index()
                        request = list_candidate_routes[metric_kilby.get_index()].get_request_route() + customer_insert.get_request_customer()

                        list_candidate_routes[posRoute].get_list_id_customers().append(customer_insert.get_id_customer())
                        list_candidate_routes[posRoute].set_request_route(request)
                        list_candidate_routes[posRoute].set_id_depot(Problem.get_problem().get_list_depots().get(pos_depot).get_id_depot())
                        customers_to_visit.remove(customer_insert)

                        is_route_full = self.request_perfect(customers_to_visit, capacity_vehicle, request)

                    if not is_route_full:
                        # if listCandidateRoutes[posRoute].getListIdCustomers().size() >= 4:
                        #     stepOptimizacion1.stepOptimizacion(listCandidateRoutes[posRoute], variant)
                        #
                        # if listCandidateRoutes[posRoute].getListIdCustomers().size() >= 2:
                        #     stepOptimizacion2.stepOptimizacion(listCandidateRoutes[posRoute], variant)
                        #     stepOptimizacion3.stepOptimizacion(listCandidateRoutes[posRoute], variant)
                        #
                        # listRouteOpt.append(listCandidateRoutes[posRoute])
                        # routesCandidates.remove(posRoute)
                        pass

                while list_candidate_routes:
                    posRoute = 0

                    # if listCandidateRoutes[posRoute].getListIdCustomers().size() >= 4:
                    #     stepOptimizacion1.stepOptimizacion(listCandidateRoutes[posRoute], variant)
                    #
                    # if listCandidateRoutes[posRoute].getListIdCustomers().size() >= 2:
                    #     stepOptimizacion2.stepOptimizacion(listCandidateRoutes[posRoute], variant)
                    #     stepOptimizacion3.stepOptimizacion(listCandidateRoutes[posRoute], variant)
                    #
                    # listRouteOpt.append(listCandidateRoutes[posRoute])
                    # listCandidateRoutes.remove(posRoute)

            solution.set_list_routes(list_route_opt)

        elif type_problem == 1:
            pass

        elif type_problem == 2:
            pass

        elif type_problem == 4:
            pass

        return solution
    
    # Método que devuelve una lista de los n mejores para las n rutas
    def select_best_cost(self, count_vehicles, count_trailers, id_depot, list_customer):
        list_kilby_costs = []
        metric_kilby = None
        cost_kilby = 0.0

        count_routes_pvr = count_trailers
        count_routes_ptr = count_vehicles - count_trailers
        type_customer = None

        for i in range(len(list_customer)):
            metric_kilby = Metric()

            type_customer = list_customer[i].get_type_customer()
            cost_kilby = self.calculate_cost_of_kilby(id_depot, id_depot, list_customer[i].get_id_customer())

            if len(list_kilby_costs) < count_vehicles:
                if ((type_customer == CustomerType.VC and count_routes_pvr != 0) or 
                    (type_customer == CustomerType.TC and count_routes_ptr != 0)):
                    metric_kilby.set_id_element(list_customer[i].get_id_customer())
                    metric_kilby.set_insertion_cost(cost_kilby)

                    list_kilby_costs.append(metric_kilby)

                    if type_customer == CustomerType.VC:
                        count_routes_pvr -= 1
                    else:
                        count_routes_ptr -= 1
            else:
                pos_max_cost = self.find_max_cost(list_kilby_costs, list_customer, type_customer)

                if cost_kilby < list_kilby_costs[pos_max_cost].get_insertion_cost():
                    metric_kilby.set_id_element(list_customer[i].get_id_customer())
                    metric_kilby.set_insertion_cost(cost_kilby)

                    list_kilby_costs.pop(pos_max_cost)
                    list_kilby_costs.append(metric_kilby)

        return list_kilby_costs
    
    # Método que calcula el costo de insertar un cliente en la ruta 
    def calculate_cost_of_kilby(self, id_depot, current_element, next_element):
        cost_actual_to_next = Problem.get_problem().get_cost_matrix()[Problem.get_problem().get_pos_element(current_element), Problem.get_problem().get_pos_element(next_element)]
        cost_next_to_depot = Problem.get_problem().get_cost_matrix()[Problem.get_problem().get_pos_element(next_element), Problem.get_problem().get_pos_element(id_depot)]
        cost_actual_to_depot = Problem.get_problem().get_cost_matrix()[Problem.get_problem().get_pos_element(current_element), Problem.get_problem().get_pos_element(id_depot)]

        return (cost_actual_to_next + cost_next_to_depot - cost_actual_to_depot)


    # Método que devuelve la posición del mayor costo de la lista
    def find_max_cost(self, list_kilby_costs, list_customers, type_customer):
        pos_max_cost = -1
        max_cost = 0.0
        current_cost = 0.0
        current_type_customer = None

        case = Problem.get_problem().get_type_problem()

        if case in [0, 1, 2, 3]:
            pos_max_cost = 0
            max_cost = list_kilby_costs[pos_max_cost].get_insertion_cost()

            for i in range(1, len(list_kilby_costs)):
                current_cost = list_kilby_costs[i].get_insertion_cost()

                if max_cost < current_cost:
                    max_cost = current_cost
                    pos_max_cost = i

        elif case == 4:
            pos_max_cost = self.find_first_customer_equals_access(type_customer, list_kilby_costs, list_customers)
            max_cost = list_kilby_costs[pos_max_cost].get_insertion_cost()

            for i in range(pos_max_cost + 1, len(list_kilby_costs)):
                current_cost = list_kilby_costs[i].get_insertion_cost()
                current_type_customer = self.get_customer_by_id(list_kilby_costs[i].get_id_element(), list_customers).get_type_customer()

                if max_cost < current_cost and current_type_customer == type_customer:
                    max_cost = current_cost
                    pos_max_cost = i

        return pos_max_cost


    # Método que devuelve la pocisi�n del primer cliente con un acceso dado
    def find_first_customer_equals_access(self, type_customer, list_kilby_costs, list_customers):
        i = 0
        found = False
        new_type_customer = None
        pos = -1

        while i < len(list_kilby_costs) and not found:
            new_type_customer = self.get_customer_by_id(list_kilby_costs[i].get_id_element(), list_customers).get_type_customer()

            if new_type_customer == type_customer:
                pos = i
                found = True

            i += 1

        return pos
    
    # Método que devuelve el mejor cliente
    def get_best_customer(self, id_depot, list_customer, list_routes, capacity_truck, capacity_trailer):
        best_metric_kilby = None

        best_cost = 0.0
        best_id_customer = -1
        best_route = -1
        current_cost = 0.0
        request_route = 0.0
        request_analice = 0.0
        total_capacity = 0.0
        found = False
        i = 0

        while i < len(list_customer) and not found:
            if Problem.get_problem().get_type_problem() == ProblemType.CVRP or Problem.get_problem().get_type_problem() == ProblemType.HFVRP or Problem.get_problem().get_type_problem() == ProblemType.OVRP or Problem.get_problem().get_type_problem() == ProblemType.MDVRP or (Problem.get_problem().get_type_problem() == ProblemType.TTRP and isinstance(list_routes[0], RouteTTRP) and list_routes[0].get_type_route() == RouteType.PTR):
                total_capacity = capacity_truck
            else:
                total_capacity = capacity_truck + capacity_trailer

            j = 0
            while j < len(list_routes) and not found:
                if list_routes[j].get_request_route() + list_customer[i].get_request_customer() <= total_capacity:
                    best_id_customer = list_customer[i].get_id_customer()
                    best_cost = self.calculate_cost_of_kilby(id_depot, list_routes[0].get_list_id_customers()[0], list_customer[0].get_id_customer())
                    best_route = j
                    found = True
                else:
                    j += 1

            i += 1

        for k in range(len(list_customer)):
            for l in range(len(list_routes)):  # this loop started at 1, had to change it
                if Problem.get_problem().get_type_problem() == ProblemType.CVRP or Problem.get_problem().get_type_problem() == ProblemType.HFVRP or Problem.get_problem().get_type_problem() == ProblemType.OVRP or Problem.get_problem().get_type_problem() == ProblemType.MDVRP or (Problem.get_problem().get_type_problem() == ProblemType.TTRP and isinstance(list_routes[l], RouteTTRP) and list_routes[l].get_type_route() == RouteType.PTR):
                    total_capacity = capacity_truck
                else:
                    total_capacity = capacity_truck + capacity_trailer

                request_route = list_routes[l].get_request_route()
                current_cost = self.calculate_cost_of_kilby(id_depot, list_routes[l].get_list_id_customers()[0], list_customer[k].get_id_customer())
                request_analice = request_route + list_customer[k].get_request_customer()

                if current_cost < best_cost and request_analice <= total_capacity:
                    best_cost = current_cost
                    best_id_customer = list_customer[k].get_id_customer()
                    best_route = l

        if found:
            best_metric_kilby = Metric()
            best_metric_kilby.set_id_element(best_id_customer)
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
    def request_perfect(self, customers_to_visit, capacity_total, request_route):
        pass_val = False
        ideal_request = capacity_total - request_route
        
        if ideal_request != 0:
            i = 0
            
            while i < len(customers_to_visit) and not pass_val:
                if customers_to_visit[i].get_request_customer() <= ideal_request:
                    pass_val = True
                else:
                    i += 1
                    
        return pass_val