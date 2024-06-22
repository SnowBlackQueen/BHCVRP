from heuristic.Heuristic import Heuristic
from data.Problem import Problem
from heuristic.Metric import Metric
from data.Customer import Customer
from solution.Route import Route
from postoptimization.Operator_3opt import Operator_3opt
from data.CustomerType import CustomerType
from solution.Solution import Solution
from data.ProblemType import ProblemType
from data.DepotMDVRP import DepotMDVRP
from random import Random
from solution.RouteTTRP import RouteTTRP
from solution.RouteType import RouteType
from data.CustomerTTRP import CustomerTTRP
from heuristic.FirstCustomerType import FirstCustomerType


class CMT(Heuristic):
    
    parameter_l = 1
    first_customer_type = FirstCustomerType.RandomCustomer

    def __init__(self):
        super().__init__()
    
    def get_solution_inicial(self):
        if parameter_l <= 0:
            parameter_l = 1

        solution = Solution()
        customers_to_visit = None
        list_candidate_routes = []
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

        three_opt = Operator_3opt()

        random = Random()
        index = -1

        list_root_customers = []
        list_metrics_cmt_by_customer = None
        list_tau_costs = None
        route = None
        root_customer = None
        customer_to_insert = None
        request_route = 0.0
        pos_best_tau = -1
        
        type_problem = Problem.get_problem().get_type_problem()
        
        if type_problem in [0, 3]:
            while customers_to_visit:
                list_candidate_routes = self._do_first_phase(customers_to_visit, id_depot, pos_depot, capacity_vehicle, count_vehicles)
                list_root_customers = self._update_customers_to_visit(list_candidate_routes, customers_to_visit)
            
                while list_candidate_routes:
                    list_metrics_CMT_by_customer = []
                    list_metrics_CMT_by_customer = self._calculate_cost_cmt_by_customer(id_depot, customers_to_visit, list_candidate_routes)
            
                    route = Route()
            
                    index = random.randint(len(list_candidate_routes))
                    route = list_candidate_routes.pop(index)
                                
                    root_customer = Customer()
                    root_customer = self._get_customer_by_id(route.get_list_id_customers()[0], list_root_customers)
                    request_route = root_customer.get_request_customer()
                    list_root_customers.remove(root_customer)
                    route.set_id_depot(id_depot)
            
                    list_tau_costs = []
                    list_tau_costs = self._calculate_tau(list_metrics_CMT_by_customer, index)
            
                    while list_tau_costs:
                        customer_to_insert = Customer()
                        pos_best_tau = len(list_tau_costs) - 1
                        customer_to_insert = self._get_customer_by_id(list_tau_costs[pos_best_tau].get_id_element(), customers_to_visit)
            
                        if capacity_vehicle >= (request_route + customer_to_insert.get_request_customer()):
                            request_route += customer_to_insert.get_request_customer()
                            route.get_list_id_customers().append(customer_to_insert.get_id_customer())
                                        
                            if len(route.get_list_id_customers()) >= 6:
                                three_opt.to_optimize(route)
                                        
                            list_tau_costs.pop(pos_best_tau)
                            self._delete_element(customer_to_insert.get_id_customer(), list_metrics_CMT_by_customer)
                            customers_to_visit.remove(customer_to_insert)
                        else:
                            list_tau_costs.pop(pos_best_tau)
            
                    route.set_Request_route(request_route)
                    solution.get_list_routes().append(route)
                    
            # actualizar countvehicles
            
        elif type_problem == 1: 
            list_capacities = Problem.get_problem().get_list_capacities()
            capacity_vehicle = list_capacities[0]
            is_open = False

            while customers_to_visit and list_capacities:
                list_candidate_routes = self._do_first_phase(customers_to_visit, id_depot, pos_depot, capacity_vehicle, count_vehicles)
                list_root_customers = self._update_customers_to_visit(list_candidate_routes, customers_to_visit)

                while list_candidate_routes and list_capacities:
                    list_metrics_cmt_by_customer = self._calculate_cost_cmt_by_customer(id_depot, customers_to_visit, list_candidate_routes)

                    route = Route()
                    is_open = True

                    index = random.randint(0, len(list_candidate_routes) - 1)
                    route = list_candidate_routes.pop(index)

                    root_customer = self._get_customer_by_id(route.get_list_id_customers()[0], list_root_customers)
                    request_route = root_customer.get_request_customer()
                    list_root_customers.remove(root_customer)
                    route.set_id_depot(id_depot)

                    list_tau_costs = self._calculate_tau(list_metrics_cmt_by_customer, index)

                    while list_tau_costs:
                        pos_best_tau = len(list_tau_costs) - 1
                        customer_to_insert = self._get_customer_by_id(list_tau_costs[pos_best_tau].getIdElement(), customers_to_visit)

                        if capacity_vehicle >= (request_route + customer_to_insert.get_request_customer()):
                            request_route += customer_to_insert.get_request_customer()
                            route.get_list_id_customers().append(customer_to_insert.get_id_customer())

                            if len(route.getListIdCustomers()) >= 6:
                                three_opt.to_optimize(route)

                            list_tau_costs.pop(pos_best_tau)
                            self._delete_element(customer_to_insert.get_id_customer(), list_metrics_cmt_by_customer)
                            customers_to_visit.remove(customer_to_insert)
                        else:
                            list_tau_costs.pop(pos_best_tau)

                    route.set_request_route(request_route)
                    solution.get_list_routes().append(route)

                    list_capacities.pop(0)
                    is_open = False

                if is_open and customers_to_visit:
                    route.set_request_route(request_route)
                    route.set_id_depot(id_depot)
                    solution.get_list_routes().append(route)

                if customers_to_visit:
                    route = Route()
                    new_request = 0.0
                    route.set_id_depot(id_depot)

                    while customers_to_visit:
                        new_request += customers_to_visit[0].get_request_customer()
                        route.set_request_route(new_request)
                        route.get_list_id_customers().append(customers_to_visit[0].get_id_customer())
                        customers_to_visit.pop(0)

                    solution.get_list_routes().append(route)

                if is_open:
                    route.set_request_route(request_route)
                    route.set_id_depot(id_depot)
                    solution.get_list_routes().append(route)
                    
        elif type_problem == 2:
            for j in range(pos_depot, len(Problem.get_problem().get_list_depots())):
                if j != pos_depot:
                    id_depot = Problem.get_problem().get_list_depots().get(j).get_id_depot()
                    customers_to_visit = list(Problem.get_problem().get_customers_assigned_by_id_depot(id_depot))
                    
                    capacity_vehicle = Problem.get_problem().get_list_depots().get(j).get_list_fleets().get(0).get_capacity_vehicle()
                    count_vehicles = Problem.get_problem().get_list_depots().get(j).get_list_fleets().get(0).get_count_vehicles()
                
                while customers_to_visit:
                    list_candidate_routes = self._do_first_phase(customers_to_visit, id_depot, j, capacity_vehicle, count_vehicles)
                    list_root_customers = self._update_customers_to_visit(list_candidate_routes, customers_to_visit)
                    
                    while list_candidate_routes:
                        list_metrics_CMT_by_customer = self._calculate_cost_cmt_by_customer(id_depot, customers_to_visit, list_candidate_routes)
                        route = Route()
                        
                        index = random.randint(0, len(list_candidate_routes) - 1)
                        route = list_candidate_routes.pop(index)
                        
                        root_customer = Customer()
                        root_customer = self._get_customer_by_id(int(route.get_list_id_customers()[0]), list_root_customers)
                        request_route = root_customer.get_request_customer()
                        list_root_customers.remove(root_customer)
                        route.set_id_depot(id_depot)
                        
                        list_tau_costs = self._calculate_tau(list_metrics_CMT_by_customer, index)
                        
                        while list_tau_costs:
                            customer_to_insert = Customer()
                            pos_best_tau = len(list_tau_costs) - 1
                            customer_to_insert = self._get_customer_by_id(list_tau_costs[pos_best_tau].get_id_element(), customers_to_visit)
                            
                            if capacity_vehicle >= (request_route + customer_to_insert.get_request_customer()):
                                request_route += customer_to_insert.get_request_customer()
                                route.get_list_id_customers().append(customer_to_insert.get_id_customer())
                                
                                if len(route.get_list_id_customers()) >= 6:
                                    three_opt.to_optimize(route)
                                
                                list_tau_costs.pop(pos_best_tau)
                                self._delete_element(customer_to_insert.get_id_customer(), list_metrics_CMT_by_customer)
                                customers_to_visit.remove(customer_to_insert)
                            else:
                                list_tau_costs.pop(pos_best_tau)
                        
                        route.set_request_route(request_route)
                        solution.get_list_routes().append(route)
                        
        elif type_problem == 4:
            list_access_VC = []

            while customers_to_visit:
                is_TC = False
                capacity_trailer = Problem.get_problem().get_list_depots().get(pos_depot).get_list_fleets().get(0).get_capacity_trailer()
                capacity_total = 0.0
                
                type_customer = CustomerType.TC  # ARREGLAR !!!
                
                list_candidate_routes = self._do_first_phase(customers_to_visit, id_depot, pos_depot, capacity_vehicle, count_vehicles)
                list_root_customers = self._update_customers_to_visit(list_candidate_routes, customers_to_visit)
                
                while list_candidate_routes:
                    list_metrics_CMT_by_customer = []
                    list_metrics_CMT_by_customer = self._calculate_cost_cmt_by_customer(id_depot, customers_to_visit, list_candidate_routes)
                    
                    route = Route()
                    
                    index = random.randint(len(list_candidate_routes))
                    route = list_candidate_routes.remove(index)
                    
                    root_customer = Customer()
                    root_customer = self._get_customer_by_id(route.get_list_id_customers().get(0), list_root_customers)
                    request_route = root_customer.get_request_customer()
                    
                    root_customer = CustomerTTRP(root_customer.get_id_customer(), root_customer.get_request_customer(), root_customer.get_location_customer(), type_customer)
                    list_root_customers.remove(root_customer)
                    route.set_id_depot(id_depot)
                    
                    if type_customer == CustomerType.TC:
                        capacity_total = capacity_vehicle
                    else:
                        capacity_total = capacity_vehicle + capacity_trailer
                    
                    list_tau_costs = []
                    list_tau_costs = self._calculate_tau(list_metrics_CMT_by_customer, index)
                    
                    while list_tau_costs:
                        customer_to_insert = Customer()
                        pos_best_tau = len(list_tau_costs) - 1
                        customer_to_insert = self._get_customer_by_id(list_tau_costs.get(pos_best_tau).get_id_element(), customers_to_visit)
                        
                        if capacity_total >= (request_route + customer_to_insert.get_request_customer()):
                            request_route += customer_to_insert.get_request_customer()
                            route.get_list_id_customers().add(customer_to_insert.get_id_customer())
                            
                            if len(route.get_list_id_customers()) >= 6:
                                three_opt.to_optimize(route)
                            
                            list_tau_costs.remove(pos_best_tau)
                            self._delete_element(customer_to_insert.get_id_customer(), list_metrics_CMT_by_customer)
                            customers_to_visit.remove(customer_to_insert)
                            
                            if type_customer == CustomerType.VC and customer_to_insert.get_type_customer() == CustomerType.TC:
                                is_TC = True
                        else:
                            list_tau_costs.remove(pos_best_tau)
                    
                    route.set_request_route(request_route)
                    
                    if type_customer == CustomerType.TC:
                        route = RouteTTRP(route.get_list_id_customers(), route.get_request_route(), route.get_cost_route(), route.get_id_depot(), list_access_VC, RouteType.PTR)
                    else:
                        if is_TC:
                            route = RouteTTRP(route.get_list_id_customers(), route.get_request_route(), route.get_cost_route(), route.get_id_depot(), list_access_VC, RouteType.CVR)
                        else:
                            route = RouteTTRP(route.get_list_id_customers(), route.get_request_route(), route.get_cost_route(), route.get_id_depot(), list_access_VC, RouteType.PVR)
                    
                    solution.get_list_routes().add(route)
    
        return solution
    
    
    # Método que realiza la primera fase del algoritmo CMT
    def _do_first_phase(self, customers_to_visit, id_depot, pos_depot, capacity_vehicle, count_vehicles):
        list_routes = []
        list_customers = list(customers_to_visit)
        list_candidate_customers = None
        root_customer = Customer()
        customer_to_insert = None
        route = Route()
        request_route = 0.0

        ThreeOpt = Operator_3opt()

        root_customer = self._get_first_customer(customers_to_visit, self.first_customer_type, id_depot)
        request_route = root_customer.get_request_customer()
        route.list_id_customers.append(root_customer.get_id_customer())
        route.set_id_depot(id_depot)
        list_customers.remove(root_customer)

        type_problem = Problem.get_problem().get_type_problem()

        if type_problem in [0, 2, 3]:
            if not list_customers:
                list_routes.append(route)
            else:
                while list_customers:
                    list_candidate_customers = []

                    for i in range(len(list_customers)):
                        metric_cmt = Metric()

                        if capacity_vehicle >= (request_route + list_customers[i].get_request_customer()):
                            metric_cmt.set_id_element(list_customers[i].get_id_customer())
                            metric_cmt.set_insertion_cost(self._calculate_cost_of_cmt(id_depot, root_customer.get_id_customer(), list_customers[i].get_id_customer()))
                            list_candidate_customers.append(metric_cmt)

                    self._ascendent_ordenate(list_candidate_customers)

                    while list_candidate_customers:
                        customer_to_insert = Customer()
                        customer_to_insert = self._get_customer_by_id(list_candidate_customers[0].get_id_element(), list_customers)

                        if capacity_vehicle >= (request_route + customer_to_insert.get_request_customer()):
                            request_route += customer_to_insert.get_request_customer()
                            route.list_id_customers.append(customer_to_insert.get_id_customer())

                            if len(route.list_id_customers) >= 6:
                                ThreeOpt.to_optimize(route)

                            list_candidate_customers.pop(0)
                            list_customers.remove(customer_to_insert)
                        else:
                            list_candidate_customers.pop(0)

                    list_routes.append(route)

                    if len(list_customers) > 0:
                        route = Route()
                        request_route = 0.0

                        root_customer = self._get_first_customer(customers_to_visit, self.first_customer_type, id_depot)
                        request_route = root_customer.get_request_customer()
                        route.list_id_customers.append(root_customer.get_id_customer())
                        route.set_id_depot(id_depot)
                        list_customers.remove(root_customer)

                        if not list_customers:
                            list_routes.append(route)
                            
        elif type_problem == 1:
            if list_customers.isEmpty():
                list_routes.add(route)
            else:
                listCapacities = list(Problem.getProblem().getListCapacities())
                capacityVehicle = listCapacities[0]
                
                while (not list_customers.isEmpty()) and (not listCapacities.isEmpty()):
                    list_candidate_customers = []
                    
                    for i in range(len(list_customers)):
                        metricCMT = Metric()
                        
                        if capacityVehicle >= (requestRoute + list_customers[i].getRequestCustomer()):
                            metricCMT.setIdElement(list_customers[i].getIdCustomer())
                            metricCMT.setInsertionCost(self._calculate_cost_of_cmt(id_depot, rootCustomer.getIdCustomer(), list_customers[i].getIdCustomer()))
                            list_candidate_customers.append(metricCMT)
                    
                    self._ascendent_ordenate(list_candidate_customers)

                    while not list_candidate_customers.isEmpty():
                        customerToInsert = Customer()
                        customerToInsert = self._get_customer_by_id(list_candidate_customers[0].getIdElement(), list_customers)
                        
                        if capacityVehicle >= (requestRoute + customerToInsert.getRequestCustomer()):
                            requestRoute += customerToInsert.getRequestCustomer()
                            route.getListIdCustomers().append(customerToInsert.getIdCustomer())
                            route.setIdDepot(id_depot)
                            
                            if len(route.getListIdCustomers()) >= 6:
                                ThreeOpt.toOptimize(route)
                            
                            list_candidate_customers.remove(0)
                            list_customers.remove(customerToInsert)
                        else:
                            list_candidate_customers.remove(0)
                    
                    list_routes.add(route)
                    listCapacities.remove(0)
                    
                    if len(list_customers) > 0:
                        requestRoute = 0.0
                        route = Route()

                        rootCustomer = self._get_first_customer(customers_to_visit, self.first_customer_type, id_depot)  
                        requestRoute = rootCustomer.getRequestCustomer()
                        route.getListIdCustomers().append(rootCustomer.getIdCustomer())
                        route.setIdDepot(Problem.getProblem().getListDepots()[pos_depot].getIdDepot())
                        list_customers.remove(rootCustomer)

                        capacityVehicle = listCapacities[0]
                        
                        if list_customers.isEmpty():
                            list_routes.add(route)
                            
        elif type_problem == 4:
            capacity_total = 0.0
            capacity_trailer = Problem.getProblem().getListDepots().get(pos_depot).getListFleets().get(0).getCapacityTrailer()

            type_customer = None

            if list_customers.isEmpty():
                list_routes.add(route)
            else:
                while not list_customers.isEmpty():
                    list_candidate_customers = []
                    type_customer = rootCustomer.getTypeCustomer()

                    if type_customer.equals(CustomerType.TC):
                        capacity_total = capacityVehicle
                    else:
                        capacity_total = capacityVehicle + capacity_trailer

                    for i in range(len(list_customers)):
                        metric_CMT = Metric()

                        if capacity_total >= (requestRoute + list_customers.get(i).getRequestCustomer()):
                            metric_CMT.setIdElement(list_customers.get(i).getIdCustomer())
                            metric_CMT.setInsertionCost(self._calculate_cost_of_cmt(id_depot, rootCustomer.getIdCustomer(), list_customers.get(i).getIdCustomer()))
                            list_candidate_customers.append(metric_CMT)

                    self._ascendent_ordenate(list_candidate_customers)

                    while not list_candidate_customers.isEmpty():
                        customerToInsert = Customer()
                        customerToInsert = self._get_customer_by_id(list_candidate_customers.get(0).getIdElement(), list_customers)

                        if capacity_total >= (requestRoute + customerToInsert.getRequestCustomer()):
                            requestRoute += customerToInsert.getRequestCustomer()
                            route.getListIdCustomers().add(customerToInsert.getIdCustomer())
                            route.setIdDepot(Problem.getProblem().getListDepots().get(pos_depot).getIdDepot())

                            if len(route.getListIdCustomers()) >= 6:
                                ThreeOpt.toOptimize(route)

                            list_candidate_customers.remove(0)
                            list_customers.remove(customerToInsert)
                        else:
                            list_candidate_customers.remove(0)

                    list_routes.add(route)

                    if len(list_customers) > 0:
                        route = Route()
                        requestRoute = 0.0

                        rootCustomer = self._get_first_customer(customers_to_visit, self.first_customer_type, id_depot)
                        requestRoute = rootCustomer.getRequestCustomer()
                        route.getListIdCustomers().add(rootCustomer.getIdCustomer())
                        route.setIdDepot(Problem.getProblem().getListDepots().get(pos_depot).getIdDepot())
                        list_customers.remove(rootCustomer)

                        if list_customers.isEmpty():
                            list_routes.add(route)

        self._empty_routes(list_routes)

        return list_routes
    
    # Método que calcula el costo de insertar un cliente en la ruta
    def _calculate_cost_of_cmt(self, id_depot, current_element, next_element):
        cost_depot_to_next = Problem.get_problem().get_cost_matrix().get_item(Problem.get_problem().get_pos_element(id_depot), Problem.get_problem().get_pos_element(next_element))
        cost_next_to_current = Problem.get_problem().get_cost_matrix().get_item(Problem.get_problem().get_pos_element(next_element), Problem.get_problem().get_pos_element(current_element))
        
        return (cost_depot_to_next + (self.parameterL * cost_next_to_current))

    # Método que vacia la lista de rutas dejando solo el primer cliente en cada una
    def _empty_routes(self, list_routes):
        for i in range(len(list_routes)):
            j = 1
            
            while j < len(list_routes[i].get_list_id_customers()):
                list_routes[i].get_list_id_customers().remove(j)

    # Método que devuelve en una lista los clientes a eliminar que ya pertenecen a una ruta
    def _update_customers_to_visit(self, list_routes, customers_to_visit):    
        list_root_customers = []
        
        for i in range(len(list_routes)):
            j = 0
            found = False

            while j < len(customers_to_visit) and not found:
                if customers_to_visit[j].get_id_customer() == list_routes[i].get_list_id_customers()[0]:
                    list_root_customers.append(customers_to_visit.pop(j))
                    found = True
                else:
                    j += 1
                    
        return list_root_customers

    # Método que retorna la lista ordenada con los costos CMT en cada ruta para cada cliente
    def _calculate_cost_cmt_by_customer(self, id_depot, list_customers, list_routes):
        list_metrics_cmt_by_customer = []
        
        for i in range(len(list_customers)):
            list_metric_cmt = []
            
            for j in range(len(list_routes)):
                metric_cmt = Metric()
                metric_cmt.set_id_element(list_customers[i].get_id_customer())
                metric_cmt.set_insertion_cost(self._calculate_cost_of_cmt(id_depot, list_routes[j].get_list_id_customers()[0], list_customers[i].get_id_customer()))
                metric_cmt.set_index(j)
                list_metric_cmt.append(metric_cmt)
            
            if len(list_routes) > 1:
                self._ascendent_ordenate(list_metric_cmt)
            
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
            self._ascendent_ordenate(list_tau_costs)

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