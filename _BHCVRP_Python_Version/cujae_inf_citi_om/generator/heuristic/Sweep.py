from heuristic.Heuristic import Heuristic
from data.Customer import Customer
from solution.Solution import Solution
from data.Problem import Problem
from data.ProblemType import ProblemType
from data.DepotMDVRP import DepotMDVRP
from solution.Route import Route
from random import Random
from data.CustomerType import CustomerType
from solution.RouteType import RouteType

class Sweep(Heuristic):
    
    def __init__(self):
        super().__init__()

    def get_solution_inicial(self):
        solution = Solution()
        customers_to_visit = None
        id_depot = -1
        pos_depot = -1

        if Problem.get_problem().get_type_problem() == ProblemType.CVRP or Problem.get_problem().get_type_problem() == ProblemType.HFVRP or Problem.get_problem().get_type_problem() == ProblemType.OVRP or Problem.get_problem().get_type_problem() == ProblemType.TTRP:
            pos_depot = 0
            id_depot = Problem.get_problem().get_list_depots()[pos_depot].get_id_depot()
            customers_to_visit = list(Problem.get_problem().get_list_customers())
        else:
            i = 0
            found = False

            while i < len(Problem.get_problem().get_list_depots()) and not found:
                if not isinstance(Problem.get_problem().get_list_depots()[i], DepotMDVRP) or not Problem.get_problem().get_list_depots()[i].get_list_assigned_customers():
                    pos_depot = i
                    id_depot = Problem.get_problem().get_list_depots()[pos_depot].get_id_depot()
                    customers_to_visit = list(Problem.get_problem().get_customers_assigned_by_id_depot(id_depot))

                    found = True
                else:
                    i += 1

        capacity_vehicle = Problem.get_problem().get_list_depots()[pos_depot].get_list_fleets()[0].get_capacity_vehicle()
        count_vehicles = Problem.get_problem().get_list_depots()[pos_depot].get_list_fleets()[0].get_count_vehicles()

        random = Random()
        index = -1

        customer = Customer()
        route = Route()
        request_route = 0.0

        self.bubble_method(customers_to_visit)

        index = random.randint(0, len(customers_to_visit) - 1)
        customer = customers_to_visit[index]
        request_route = customer.get_request_customer()
        route.get_list_id_customers().append(customer.get_id_customer())
        customers_to_visit.remove(customer)
        
        type_problem = Problem.get_problem().get_type_problem()
        
        if type_problem in [0, 3]:
            while customers_to_visit and count_vehicles > 0:
                if index == len(customers_to_visit):
                    index = 0
                    
                customer = customers_to_visit[index]

                if capacity_vehicle >= (request_route + customer.get_request_customer()):
                    request_route += customer.get_request_customer()
                    route.get_list_id_customers().append(customer.get_id_customer())
                    customers_to_visit.remove(customer)
                else:
                    route.set_request_route(request_route)
                    route.set_id_depot(id_depot)
                    solution.get_list_routes().append(route)
                    
                    route = None
                    count_vehicles -= 1

                    if count_vehicles > 0:
                        route = Route()
                        
                        request_route = customer.get_request_customer()
                        route.get_list_id_customers().append(customer.get_id_customer())
                        customers_to_visit.remove(customer)

            if route is not None:
                route.set_request_route(request_route)
                route.set_id_depot(id_depot)
                solution.get_list_routes().append(route)

            if customers_to_visit:
                route = Route()
                request_route = 0.0
                
                while customers_to_visit:
                    j = 0
                    found = False
                    
                    request_route = solution.get_list_routes()[j].get_request_route()

                    while j < len(solution.get_list_routes()) and not found:
                        if capacity_vehicle >= (request_route + customer.get_request_customer()):
                            solution.get_list_routes()[j].set_request_route(request_route + customer.get_request_customer())
                            solution.get_list_routes()[j].get_list_id_customers().append(customer.get_id_customer())
                            customers_to_visit.remove(customer)
                            
                            found = True
                        else:
                            j += 1
                            request_route = solution.get_list_routes()[j].get_request_route()
                    
                    if not found:
                        route.get_list_id_customers().append(customer.get_id_customer())
                        route.set_request_route(route.get_request_route() + customer.get_request_customer())
                        customers_to_visit.remove(customer)
                    
                    if customers_to_visit:
                        if index == len(customers_to_visit):
                            index = 0
                        
                        customer = customers_to_visit[index]

            if route.get_list_id_customers():
                route.set_id_depot(id_depot)
                solution.get_list_routes().append(route)
                
        elif type_problem == 1:
            list_capacities = list(Problem.get_problem().get_list_capacities())
            capacity_vehicle = list_capacities[0]
            is_open = True

            while customers_to_visit and list_capacities:
                if index == len(customers_to_visit):
                    index = 0
                
                customer = customers_to_visit[index]
                
                if capacity_vehicle >= (request_route + customer.get_request_customer()):
                    request_route += customer.get_request_customer()
                    route.get_list_id_customers().append(customer.get_id_customer())
                    customers_to_visit.remove(customer)
                else:
                    route.set_request_route(request_route)
                    route.set_id_depot(id_depot)
                    solution.get_list_routes().append(route)
                    
                    is_open = False
                    list_capacities.pop(0)
                    
                    if list_capacities:
                        route = Route()
                        
                        request_route = customer.get_request_customer()
                        route.get_list_id_customers().append(customer.get_id_customer())
                        customers_to_visit.remove(customer)
                        
                        is_open = True
                        capacity_vehicle = list_capacities[0]
                
                if is_open:
                    route.set_request_route(request_route)
                    route.set_id_depot(id_depot)
                    solution.get_list_routes().append(route)
                
                if customers_to_visit:
                    route = Route()
                    request_route = 0.0
                    
                    list_capacities = list(Problem.get_problem().get_list_capacities())
                    iterator_cap_vehicle = iter(list_capacities)
                    
                    while customers_to_visit:
                        j = 0
                        found = False
                        request_route = solution.get_list_routes()[j].get_request_route()
                        
                        while True:
                            try:
                                if next(iterator_cap_vehicle) >= (request_route + customer.get_request_customer()):
                                    solution.get_list_routes()[j].set_request_customer()(request_route + customer.get_request_customer())
                                    solution.get_list_routes()[j].get_list_id_customers().append(customer.get_id_customer())
                                    customers_to_visit.remove(customer)
                                    
                                    found = True
                                    break
                                else:
                                    j += 1
                                    request_route = solution.get_list_routes()[j].get_request_route()
                            except StopIteration:
                                break
                        
                        if not found:
                            route.get_list_id_customers().append(customer.get_id_customer())
                            route.set_request_route()(route.get_request_route() + customer.get_request_customer())
                            customers_to_visit.remove(customer)
                        
                        if customers_to_visit:
                            if index == len(customers_to_visit):
                                index = 0
                            
                            customer = customers_to_visit[index]
                            
        elif type_problem == 2:
            for j in range(pos_depot, len(Problem.get_problem().get_list_depots())):
                if j != pos_depot:
                    id_depot = Problem.get_problem().get_list_depots().get(j).getid_depot()
                    customers_to_visit = list(Problem.get_problem().get_customers_assigned_by_id_depot(id_depot))
                    
                    capacity_vehicle = Problem.get_problem().get_list_depots().get(j).get_list_fleets().get(0).get_capacity_vehicle()
                    count_vehicles = Problem.get_problem().get_list_depots().get(j).get_list_fleets().get(0).get_count_vehicles()
                    
                    self.bubble_method(customers_to_visit)
                    
                    route = Route()
                    
                    index = random.randint(0, len(customers_to_visit) - 1)
                    customer = customers_to_visit[index]
                    request_route = customer.get_request_customer()
                    route.get_list_id_customers().append(customer.get_id_customer())
                    customers_to_visit.remove(customer)
                    
                while customers_to_visit and count_vehicles > 0:
                    if index == len(customers_to_visit):
                        index = 0
                    
                    customer = customers_to_visit[index]
                    
                    if capacity_vehicle >= (request_route + customer.get_request_customer()):
                        request_route += customer.get_request_customer()
                        route.get_list_id_customers().append(customer.get_id_customer())
                        customers_to_visit.remove(customer)
                    else:
                        route.set_request_route(request_route)
                        route.set_id_depot(id_depot)
                        solution.get_list_routes().append(route)
                        
                        route = None
                        count_vehicles -= 1
                        
                        if count_vehicles > 0:
                            route = Route()
                            
                            request_route = customer.get_request_customer()
                            route.get_list_id_customers().append(customer.get_id_customer())
                            customers_to_visit.remove(customer)
                
                if route is not None:
                    route.set_request_route(request_route)
                    route.set_id_depot(id_depot)
                    solution.get_list_routes().append(route)
                
                if customers_to_visit:
                    route = Route()
                    request_route = 0.0
                    
                    while customers_to_visit:
                        k = 0
                        found = False
                        
                        request_route = solution.get_list_routes()[k].get_request_route()
                        
                        while k < len(solution.get_list_routes()) and not found:
                            if (request_route + customer.get_request_customer()) <= capacity_vehicle:
                                solution.get_list_routes()[k].set_request_route(request_route + customer.get_request_customer())
                                solution.get_list_routes()[k].get_list_id_customers().append(customer.get_id_customer())
                                customers_to_visit.remove(customer)
                                
                                found = True
                            else:
                                k += 1
                                request_route = solution.get_list_routes()[k].get_request_route()
                        
                        if not found:
                            route.get_list_id_customers().append(customer.get_id_customer())
                            route.set_request_route(route.get_request_route() + customer.get_request_customer())
                            customers_to_visit.remove(customer)
                        
                        if customers_to_visit:
                            if index == len(customers_to_visit):
                                index = 0
                            
                            customer = customers_to_visit[index]
                    
                    if route.get_list_id_customers():
                        route.set_id_depot(id_depot)
                        solution.get_list_routes().append(route)
                        
        elif type_problem == 4:
            is_TC = False
            capacity_trailer = Problem.get_problem().get_list_depots().get(pos_depot).get_list_fleets().get(0).get_capacity_trailer()

            type_customer = customer.get_type_customer()

            while customers_to_visit:
                if index == len(customers_to_visit):
                    index = 0

                customer = customers_to_visit.get(index)

                if type_customer == CustomerType.TC:
                    if capacity_vehicle >= (request_route + customer.get_request_customer()):
                        request_route += customer.get_request_customer()
                        route.get_list_id_customers().add(customer.get_id_customer())
                        customers_to_visit.remove(customer)
                    else:
                        route.set_request_route(request_route)
                        route.set_type_route(RouteType.PTR)
                        route.set_id_depot(id_depot)
                        solution.get_list_routes().add(route)

                        route = Route()

                        request_route = customer.get_request_customer()
                        type_customer = customer.get_type_customer()
                        route.get_list_id_customers().add(customer.get_id_customer())
                        customers_to_visit.remove(customer)
                else:
                    if customer.get_type_customer() == CustomerType.TC:
                        is_TC = True

                    if (capacity_vehicle + capacity_trailer) >= (request_route + customer.get_request_customer()):
                        request_route += customer.get_request_customer()
                        route.get_list_id_customers().add(customer.get_id_customer())
                        customers_to_visit.remove(customer)
                    else:
                        route.set_request_route(request_route)

                        if is_TC:
                            route.set_type_route(RouteType.CVR)
                        else:
                            route.set_type_route(RouteType.PVR)

                        route.set_id_depot(id_depot)
                        solution.get_list_routes().add(route)
                        is_TC = False

                        route = Route()
                        request_route = customer.get_request_customer()
                        type_customer = customer.get_type_customer()
                        route.get_list_id_customers().add(customer.get_id_customer())
                        customers_to_visit.remove(customer)

            route.set_request_route(request_route)

            if type_customer == CustomerType.TC:
                route.set_type_route(RouteType.PTR)
            else:
                if is_TC:
                    route.set_type_route(RouteType.CVR)
                else:
                    route.set_type_route(RouteType.PVR)

            route.set_id_depot(id_depot)
            solution.get_list_routes().add(route)
        
        return solution
    
    # Método de ordenamiento Burbujas utilizando las coordenadas polares
    def bubble_method(self, list_customers):
        value_theta_one = 0.0
        value_rho_one = 0.0
        value_theta_two = 0.0
        value_rho_two = 0.0

        for i in range(len(list_customers) - 1):
            value_theta_one = list_customers[i].get_location_customer().get_polar_theta()

            for j in range(i + 1, len(list_customers)):
                customer = Customer()

                value_theta_two = list_customers[j].get_location_customer().get_polar_theta()

                if value_theta_one > value_theta_two:
                    customer = list_customers[i]
                    list_customers[i] = list_customers[j]
                    list_customers[j] = customer

                    value_theta_one = value_theta_two
                else:
                    if value_theta_one == value_theta_two:
                        value_rho_one = list_customers[i].get_location_customer().get_polar_rho()
                        value_rho_two = list_customers[j].get_location_customer().get_polar_rho()

                        if value_rho_one > value_rho_two:
                            customer = list_customers[i]
                            list_customers[i] = list_customers[j]
                            list_customers[j] = customer

                            value_theta_one = value_theta_two
        return list_customers