from data.Customer import Customer
from data.CustomerType import CustomerType
from data.Problem import Problem
from data.ProblemType import ProblemType
from generator.solution.Solution import Solution
from typing import List
from generator.heuristic.Metric import Metric
from generator.heuristic.FirstCustomerType import FirstCustomerType
import random
from random import Random
from abc import ABC, abstractmethod
from data.DepotMDVRP import DepotMDVRP
from generator.solution.Route import Route
from generator.solution.RouteType import RouteType
from generator.postoptimization.Operator_3opt import Operator_3opt

# Clase abstracta que modela una heurística de construcción

class Heuristic(ABC):
    
    # Template Method
    def template_method(self) -> Solution:
        self.comun_initialize()
        self.initialize_specifics()
        return self.get_solution_inicial()
    
    @abstractmethod # Método para inicializar parámetros específicos de algunas heurísticas
    def initialize_specifics(self):
        pass 
    
    # Método que inicializa todo los parámetros en común de las HC
    def comun_initialize(self):
        self.solution = Solution()
        self.customers_to_visit = None
        self.id_depot = -1
        self.pos_depot = -1

        if Problem.get_problem().get_type_problem() == ProblemType.CVRP or Problem.get_problem().get_type_problem() == ProblemType.HFVRP or Problem.get_problem().get_type_problem() == ProblemType.OVRP or Problem.get_problem().get_type_problem() == ProblemType.TTRP:
            self.pos_depot = 0
            self.id_depot = Problem.get_problem().get_list_depots()[self.pos_depot].get_id_depot()
            self.customers_to_visit = list(Problem.get_problem().get_list_customers())
        else:
            self.i = 0
            self.found = False

            while i < len(Problem.get_problem().get_list_depots()) and not self.found:
                if not isinstance(Problem.get_problem().get_list_depots()[i], DepotMDVRP) or not Problem.get_problem().get_list_depots()[i].get_list_assigned_customers():
                    self.pos_depot = i
                    self.id_depot = Problem.get_problem().get_list_depots()[self.pos_depot].get_id_depot()
                    self.customers_to_visit = list(Problem.get_problem().get_customers_assigned_by_id_depot(self.id_depot))

                    self.found = True
                else:
                    i += 1

        self.capacity_vehicle = Problem.get_problem().get_list_depots()[self.pos_depot].get_list_fleets()[0].get_capacity_vehicle()
        self.count_vehicles = Problem.get_problem().get_list_depots()[self.pos_depot].get_list_fleets()[0].get_count_vehicles()

        self.customer = Customer()
        self.route = Route()
        self.request_route = 0.0
        
        self.type_problem = Problem.get_problem().get_type_problem()

    @abstractmethod # Método para ejecutar la variante específica del problema para cierta heurística
    def get_solution_inicial(self) -> Solution:
        pass
    
    def execute(self):
        if self.type_problem == ProblemType.CVRP or self.type_problem in [0, 3]:
            while self.customers_to_visit:
                new_route = self.processing(self.customers_to_visit, self.count_vehicles, self.request_route, self.route, self.id_depot, self.solution)
                if new_route.get_list_id_customers():
                    new_route.set_id_depot(self.id_depot)
                    self.solution.get_list_routes().append(new_route)
                    break
        elif self.type_problem == ProblemType.HFVRP or self.type_problem== 1:
            if self.customers_to_visit:
                    route = Route()
                    new_request_route = 0.0
                    
                    list_capacities = list(Problem.get_problem().get_list_capacities())
                    iterator_cap_vehicle = iter(list_capacities)
                    
                    while self.customers_to_visit:
                        j = 0
                        found = False
                        new_request_route = self.processing(self.customers_to_visit, self.count_vehicles, self.request_route, self.route, self.id_depot, self.solution)
                        
                        while True:
                            try:
                                if next(iterator_cap_vehicle) >= (new_request_route + self.customer.get_request_customer()):
                                    self.solution.get_list_routes()[j].set_request_customer()(new_request_route + self.customer.get_request_customer())
                                    self.solution.get_list_routes()[j].get_list_id_customers().append(self.customer.get_id_customer())
                                    self.customers_to_visit.remove(self.customer)
                                    
                                    found = True
                                    break
                                else:
                                    j += 1
                                    new_request_route = self.solution.get_list_routes()[j].get_request_route()
                            except StopIteration:
                                break
                        
                        if not found:
                            route.get_list_id_customers().append(self.customer.get_id_customer())
                            route.set_request_route()(route.get_request_route() + self.customer.get_request_customer())
                            self.customers_to_visit.remove(self.customer)
                        
                        if self.customers_to_visit:
                            self.initialize_specifics()
                        break  
                
        elif self.type_problem == ProblemType.MDVRP or self.type_problem == 2:
            for j in range(self.pos_depot, len(Problem.get_problem().get_list_depots())):
                if j != self.pos_depot:
                    self.initialize_specifics()
                    routes = self.creating(self)
                    for route in routes:
                        route.set_id_depot(self.id_depot)
                        self.solution.get_list_routes().append(route)
                        
        elif self.type_problem == ProblemType.TTRP or self.type_problem == 4:
            is_TC = False
            self.capacity_trailer = Problem.get_problem().get_list_depots().get(self.pos_depot).get_list_fleets().get(0).get_capacity_trailer()

            self.type_customer = self.customer.get_type_customer()
            
            new_route = self.processing(self.customers_to_visit, self.count_vehicles, self.request_route, self.route, self.id_depot, self.solution)
            
            new_route.set_request_route(self.request_route)

            if self.type_customer == CustomerType.TC:
                route.set_type_route(RouteType.PTR)
            else:
                if is_TC:
                    route.set_type_route(RouteType.CVR)
                else:
                    route.set_type_route(RouteType.PVR)

            route.set_id_depot(self.id_depot)
            self.solution.get_list_routes().add(route)
            
        return self.solution
        
    # Redefinir
    def creating(self):
        if self.type_problem == ProblemType.CVRP or self.type_problem == 0:
            if self.request_route + self.customer.get_request_customer() <= self.capacity_vehicle:
                self.request_route += self.customer.get_request_customer()
                # self.route.get_list_id_customers().append(self.customer.get_id_customer())
                # self.customers_to_visit.remove(self.customer)
            else:
                self.route.set_request_route(self.request_route)
                self.route.set_id_depot(self.id_depot)
                self.solution.get_list_routes().append(self.route)
                return True, None
            return False, self.route
            
        if self.type_problem == ProblemType.HFVRP or self.type_problem == 1:
            while self.customers_to_visit:
                self.initialize_specifics()  
                
                if self.capacity_vehicle >= (request_route + self.customer.get_request_customer()):
                    request_route += self.customer.get_request_customer()
                    route.get_list_id_customers().append(self.customer.get_id_customer())
                    self.customers_to_visit.remove(self.customer)  # Remueve el primer cliente procesado
                else:
                    route.set_request_route(request_route)
                    route.set_id_depot(self.id_depot)
                    self.solution.get_list_routes().append(route)
                    
                    return False, None, self.customers_to_visit  # Indicando que se necesita un nuevo vehículo/ruta
                    
            return True, route, self.customers_to_visit  # Indicando que el vehículo aún tiene capacidad
        
        if self.type_problem == ProblemType.MDVRP  or self.type_problem == 2:
            routes = self.solution.get_list_routes()
            
            while self.customers_to_visit and self.count_vehicles > 0:
                self.initialize_specifics()
                
                if self.capacity_vehicle >= (request_route + self.customer.get_request_customer()):
                    request_route += self.customer.get_request_customer()
                    route.get_list_id_customers().append(self.customer.get_id_customer())
                    self.customers_to_visit.remove(self.customer)
                else:
                    route.set_request_route(request_route)
                    routes.append(route)
                    
                    if self.count_vehicles > 0:
                        route = Route()
                        request_route = self.customer.get_request_customer()
                        route.get_list_id_customers().append(self.customer.get_id_customer())
                        self.customers_to_visit.remove(self.customer)
                        self.count_vehicles -= 1
                        
            if route.get_list_id_customers():
                routes.append(route)
            
            return routes
        
        if self.type_problem == ProblemType.TTRP or self.type_problem == 4:
            if request_route + self.customer.get_request_customer() <= self.capacity_vehicle:
                request_route += self.customer.get_request_customer()
                route.get_list_id_customers().append(self.customer.get_id_customer())
                self.customers_to_visit.remove(self.customer)
            else:
                route.set_request_route(request_route)
                route.set_type_route(RouteType.PTR)
                route.set_id_depot(self.id_depot)
                self.solution.get_list_routes().append(route)
                
                route = Route()

                request_route = self.customer.get_request_customer()
                self.type_customer = self.customer.get_type_customer()
                route.get_list_id_customers().add(self.customer.get_id_customer())
                self.customers_to_visit.remove(self.customer)
                
                return True, None
            return False, route
                

    # Redefinir
    def processing(self, customers_to_visit, count_vehicles, request_route, route, id_depot, solution):
        if self.type_problem == ProblemType.CVRP or self.type_problem == 0:
            cv = int(count_vehicles)
            while customers_to_visit and cv > 0:
                self.initialize_specifics()  # Para que customer sea tratado según la variante
                found, new_route = self.creating()
                if found:
                    route = new_route
                cv -= 1
        
        if self.type_problem == ProblemType.HFVRP or self.type_problem == 1:
            list_capacities = Problem.get_problem().get_list_capacities()
            capacity_vehicle = list_capacities[0]
            is_open = True
            route = None
            
            while customers_to_visit and list_capacities:
                if not route:
                    route = Route()
                
                success, route, customers_to_visit = self.creating(route, request_route, self.customer, capacity_vehicle, id_depot, solution, customers_to_visit)
                
                if not success:
                    # Manejo cuando se agota la capacidad del vehículo actual
                    if list_capacities:
                        route = Route()
                        
                        request_route = self.customer.get_request_customer()
                        route.get_list_id_customers().append(self.customer.get_id_customer())
                        customers_to_visit.remove(self.customer)
                        
                        capacity_vehicle = list_capacities.pop(0)
                        is_open = True
                    else:
                        is_open = False
                    
                if is_open:
                    route.set_request_route(request_route)
                    route.set_id_depot(id_depot)
                    self.solution.get_list_routes().append(route)
                    
        if self.type_problem == ProblemType.TTRP or self.type_problem == 4:
            while self.customers_to_visit:
                self.initialize_specifics()
                if self.type_customer == CustomerType.TC:
                    found, new_route = self.creating(route, request_route, self.customer, capacity_vehicle, id_depot, solution, customers_to_visit)
                if not found:
                    if self.customer.get_type_customer() == CustomerType.TC:
                        is_TC = True

                    if (self.capacity_vehicle + self.capacity_trailer) >= (request_route + self.customer.get_request_customer()):
                        request_route += self.customer.get_request_customer()
                        route.get_list_id_customers().add(self.customer.get_id_customer())
                        self.customers_to_visit.remove(self.customer)
                    else:
                        route.set_request_route(request_route)

                        if is_TC:
                            route.set_type_route(RouteType.CVR)
                        else:
                            route.set_type_route(RouteType.PVR)

                        route.set_id_depot(self.id_depot)
                        self.solution.get_list_routes().add(route)
                        is_TC = False

                        route = Route()
                        request_route = self.customer.get_request_customer()
                        type_customer = self.customer.get_type_customer()
                        route.get_list_id_customers().add(self.customer.get_id_customer())
                        self.customers_to_visit.remove(self.customer)
            
        return route 
    
    def _get_customer_by_id(self, idCustomer, listCustomers):
        i = 0
        found = False
        customer = None

        while i < len(listCustomers) and not found:
            if listCustomers[i].get_id_customer() == idCustomer:
                customer = listCustomers[i]
                found = True
            else:
                i += 1

        return customer

    def _ascendent_ordenate(self, listWithOutOrder: List[Metric]):
        for i in range(len(listWithOutOrder)):
            minorInsertionCost = listWithOutOrder[i].getInsertionCost()
            minorMetric = listWithOutOrder[i]
            referencePos = i

            currentMetric = None
            currentPos = -1

            for j in range(i + 1, len(listWithOutOrder)):
                if listWithOutOrder[j].getInsertionCost() < minorInsertionCost:
                    minorInsertionCost = listWithOutOrder[j].getInsertionCost()
                    currentMetric = listWithOutOrder[j]
                    currentPos = j

            if currentPos != -1:
                listWithOutOrder[referencePos] = currentMetric
                listWithOutOrder[currentPos] = minorMetric
                
    def _ascendent_ordenate(self, list_distances, list_nn: List[Customer]):
        for i in range(len(list_distances)):
            minor_distance = list_distances[i]
            customer_nn = list_nn[i]
            reference_pos = i

            current_distance = 0.0
            current_customer = None
            current_pos = -1

            for j in range(i + 1, len(list_distances)):
                if minor_distance > list_distances[j]:
                    current_distance = list_distances[j]
                    current_customer = list_nn[j]
                    current_pos = j

            if current_pos != -1:
                list_distances[reference_pos] = current_distance
                list_distances[current_pos] = minor_distance

                list_nn[reference_pos] = current_customer
                list_nn[current_pos] = customer_nn
                
    def _select_first_customer_in_mdvrp(self, customers_to_visit, first_customer_type, pos_matrix_depot):
        selected_customer = None
        currentIndex = -1
        currentCost = 0.0

        selected_customer = customers_to_visit[0]
        bestIndex = Problem.get_problem().get_pos_element(selected_customer.get_id_customer())
        bestCost = Problem.get_problem().get_cost_matrix().item(pos_matrix_depot, bestIndex)

        for i in range(1, len(customers_to_visit)):
            currentIndex = Problem.get_problem().get_pos_element(customers_to_visit[i].get_id_customer())
            currentCost = Problem.get_problem().get_cost_matrix().item(pos_matrix_depot, currentIndex)

            if first_customer_type == FirstCustomerType.FurthestCustomer:
                if currentCost > bestCost:
                    bestCost = currentCost
                    bestIndex = currentIndex
                    selected_customer = customers_to_visit[i]
            else:
                if first_customer_type == FirstCustomerType.NearestCustomer:
                    if currentCost < bestCost:
                        bestCost = currentCost
                        bestIndex = currentIndex
                        selected_customer = customers_to_visit[i]

        return selected_customer
    
    def _get_first_customer(self, customers_to_visit, first_customer_type, id_depot):
        firstCustomer = None
        index = -1
        posMatrixDepot = -1
        rc = None

        if first_customer_type == FirstCustomerType.OtherType:  # Replace with the actual condition
            index = random.randint(0, len(customers_to_visit) - 1)
            firstCustomer = customers_to_visit[index]
        else:
            pos_matrix_depot = Problem.get_problem().get_pos_element(id_depot)

            if Problem.get_problem().get_type_problem() == ProblemType.MDVRP:
                firstCustomer = self.select_first_customer_in_mdvrp(customers_to_visit, first_customer_type, pos_matrix_depot)
            else:
                if first_customer_type == FirstCustomerType.NearestCustomer:
                    rc = Problem.get_problem().get_cost_matrix().index_lower_value(posMatrixDepot, 0, posMatrixDepot, len(customers_to_visit) - 1)
                elif first_customer_type == FirstCustomerType.FurthestCustomer:
                    rc = Problem.get_problem().get_cost_matrix().index_bigger_value(posMatrixDepot, 0, posMatrixDepot, len(customers_to_visit) - 1)

                index = rc.get_col()
                firstCustomer = customers_to_visit[index]

        return firstCustomer
    
    
    
    
    
    
    """# Cómo usar el patrón Template 
    def execute(self):
        self.step1()
        self.step2()
        self.step3()
        self.common_step()

    @abstractmethod
    def step1(self):
        pass

    @abstractmethod
    def step2(self):
        pass

    @abstractmethod
    def step3(self):
        pass

    def common_step(self):
        print("Executing common step")

    class HeuristicA(Heuristic):
        def step1(self):
            print("HeuristicA Step 1")

        def step2(self):
            print("HeuristicA Step 2")

        def step3(self):
            print("HeuristicA Step 3")

    class HeuristicB(Heuristic):
        def step1(self):
            print("HeuristicB Step 1")

        def step2(self):
            print("HeuristicB Step 2")

        def step3(self):
            print("HeuristicB Step 3")

    # Example usage
    heuristic_a = HeuristicA()
    heuristic_a.execute()

    heuristic_b = HeuristicB()
    heuristic_b.execute() 
    
    # Aquí empieza el código original"""