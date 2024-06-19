from factory.methods.FactoryHeuristic import FactoryHeuristic
from factory.methods.FactoryDistance import FactoryDistance
from data.Customer import Customer
from data.CustomerTTRP import CustomerTTRP
from data.Location import Location
from data.DepotMDVRP import DepotMDVRP
from data.Fleet import Fleet
from data.FleetTTRP import FleetTTRP
from data.Problem import Problem
from typing import List
from generator.solution.RouteType import RouteType
from generator.solution.RouteTTRP import RouteTTRP
from tools.Tools import Tools
from data.Depot import Depot

class StrategyHeuristic:
    strategy_heuristic = None

    def __init__(self):
        self.best_solution = None
        self.list_solutions = []
        self.time_execute = 0
        self.calculate_time = True

    @staticmethod # Método que implementa el Patrón Singleton.
    def get_strategy_heuristic():
        if StrategyHeuristic.strategy_heuristic is None:
            StrategyHeuristic.strategy_heuristic = StrategyHeuristic()
        return StrategyHeuristic.strategy_heuristic

    def get_best_solution(self):
        return self.best_solution

    def set_best_solution(self, best_solution):
        self.best_solution = best_solution

    def get_list_solutions(self):
        return self.list_solutions

    def set_list_solutions(self, list_solutions):
        self.list_solutions = list_solutions

    def get_time_execute(self):
        return self.time_execute

    # Método encargado de crear una heurística de construcción
    def new_heuristic(self, heuristic_type):
        ifactory_heuristic = FactoryHeuristic()
        heuristic = ifactory_heuristic.create_heuristic(heuristic_type)
        return heuristic

    # Método encargado de crear una distancia
    def new_distance(self, type_distance):
        ifactory_distance = FactoryDistance()
        distance = ifactory_distance.create_distance(type_distance)
        return distance

    # Método encargado de cargar los datos de los clientes con coordenadas
    def load_customer(self, id_customers, request_customers, axis_X_customers=None, axis_Y_customers=None) -> List[Customer]:
        list_customers = []
        for i in range(len(id_customers)):
            customer = Customer()
            customer._id_customer = id_customers[i]
            customer._request_customer = request_customers[i]
            if axis_X_customers and axis_Y_customers:
                location = Location()
                location._axis_X = axis_X_customers[i]
                location._axis_Y = axis_Y_customers[i]
                customer._location_customer = location
            list_customers.append(customer)
        return list_customers

    # Método encargado de cargar los datos de los clientes TTRP con coordenadas
    def load_customer_TTRP(self, id_customers, request_customers, axis_X_customers=None, axis_Y_customers=None, type_customers=None) -> List[Customer]:
        list_customers = self.load_customer(id_customers, request_customers, axis_X_customers, axis_Y_customers)
        for i in range(len(list_customers)):
            c = list_customers[i]
            customerTTRP = CustomerTTRP(c.id_customer, c.request_customer, c.location_customer, type_customers[i])
            list_customers[i] = customerTTRP
        return list_customers

    # Método encargado de cargar los datos de los depósitos y las flotas con coordenadas y asignación predeterminada
    def load_depot(self, id_depots, axis_X_depots=None, axis_Y_depots=None, id_assigned_customers=None, count_vehicles=None, capacity_vehicles=None) -> List[Depot]:
        list_depots = []
        for i in range(len(id_depots)):
            depot = DepotMDVRP()
            depot.id_depot = id_depots[i]
            if axis_X_depots and axis_Y_depots:
                location = Location()
                location._axis_X = axis_X_depots[i]
                location._axis_Y = axis_Y_depots[i]
                depot.location_depot = location
            if id_assigned_customers:
                depot._list_assigned_customers = id_assigned_customers[i]
            listFleets = []
            for j in range(len(count_vehicles)):
                fleet = Fleet()
                fleet._count_vehicles = count_vehicles[j]
                fleet._capacity_vehicle = capacity_vehicles[j]
                listFleets.append(fleet)
            depot.list_fleets = listFleets
            list_depots.append(depot)
        return list_depots

    # Método encargado de cargar los datos de los depósitos y las flotas TTRP con coordenadas
    def load_depot_TTRP(self, id_depots, axis_X_depots=None, axis_Y_depots=None, count_vehicles=None, capacity_vehicles=None, count_trailers=None, capacity_trailers=None) -> List[Depot]:
        list_depots = self.load_depot(id_depots, axis_X_depots, axis_Y_depots, None, count_vehicles, capacity_vehicles)
        for i in range(len(list_depots)):
            f = list_depots[i].list_fleets[0]
            fleetTTRP = FleetTTRP(f.count_vehicles, f.capacity_vehicle, count_trailers[i], capacity_trailers[i])
            list_depots[i].list_fleets[0] = fleetTTRP
        return list_depots

    # Método encargado de cargar los datos del problema usando listas de distancias y las coordenadas
    def load_problem(self, id_customers, request_customers, id_depots, count_vehicles, capacity_vehicles, list_distances, axis_X_customers=None, axis_Y_customers=None, axis_X_depots=None, axis_Y_depots=None, type_problem=None, type_assignment=None) -> bool:
        loaded = False
        Problem.get_problem().type_problem = type_problem
        if id_customers and request_customers and id_depots and count_vehicles and capacity_vehicles and list_distances and axis_X_customers and axis_Y_customers and axis_X_depots and axis_Y_depots:
            list_customers = self.load_customer(id_customers, request_customers, axis_X_customers, axis_Y_customers)
            list_depots = self.load_depot(id_depots, axis_X_depots, axis_Y_depots, None, count_vehicles, capacity_vehicles)
            Problem.get_problem().list_customers = list_customers
            Problem.get_problem().list_depots = list_depots
            if Problem.get_problem().total_capacity >= Problem.get_problem().total_request:
                loaded = True
                Problem.get_problem().costMatrix = self.fill_cost_matrix(list_distances)
                listCountV = [count_vehicles] * len(id_depots)
                listCapV = [capacity_vehicles] * len(id_depots)
                # Este Controller es de BHAVRP
            """ if Controller.getController().load_problem(id_customers, request_customers, axis_X_customers, axis_Y_customers, id_depots, axis_X_depots, axis_Y_depots, listCountV, listCapV, list_distances):
                    Controller.getController().executeAssignment(type_assignment)
                    self.adapt(Controller.getController().solution.clusters)"""
        return loaded

    # Método encargado de llenar la matriz de costo usando listas de distancias
    def fill_cost_matrix(self, list_distances):
        cost_matrix = []
        for i in range(len(list_distances)):
            row = []
            for j in range(len(list_distances[i])):
                row.append(list_distances[i][j])
            cost_matrix.append(row)
        return cost_matrix

    # Esta función es para adaptar la respuesta que da BHAVRP.
    """ def adapt(self, listClusters):
        depots = []
        for i in range(len(listClusters)):
            found = False
            for j in range(len(Problem.getProblem().listDepots)):
                if listClusters[i].idCluster == Problem.getProblem().listDepots[j].idDepot:
                    found = True
                    listIdCustomers = []
                    for k in range(len(listClusters[i].itemsOfCluster)):
                        listIdCustomers.append(listClusters[i].itemsOfCluster[k])
                    # ((DepotMDVRP)Problem.getProblem().listDepots[j]).listAssignedCustomers = listIdCustomers
            depots.append(depot)"""
            
    # Método encargado de ejecutar una heurística de construcción
    def execute_heuristic(self, count_execution, heuristic_type):
        if self.calculate_time:
            time_execute = self.time.time()

        heuristic = self.new_heuristic(heuristic_type)

        for i in range(1, count_execution + 1):
            current_solution = heuristic.get_solution_inicial()
            current_solution.calculate_cost()
            self.list_solutions.append(current_solution)

            if i == 1:
                best_solution = current_solution
            else:
                if round(current_solution.get_cost_solution(), 2) < round(best_solution.get_cost_solution(), 2):
                    best_solution = current_solution

        if self.calculate_time:
            time_execute = abs(self.time.time() - time_execute)

    # Método que devuelve el listado de los clientes de la mejor solución obtenida
    def get_orden_visit(self):
        code = []

        for i in range(len(self.best_solution.get_list_routes())):
            for j in range(len(self.best_solution.get_list_routes()[i].get_list_id_customers())):
                code.append(self.best_solution.get_list_routes()[i].get_list_id_customers()[j])

        return code

    # Método que devuelve todas las soluciones obtenidas con la heurística
    def get_all_solutions(self):
        all_solutions = []

        for i in range(len(self.list_solutions)):
            code = []
            for j in range(len(self.list_solutions[i].get_list_routes())):
                for k in range(len(self.list_solutions[i].get_list_routes()[j].get_list_id_customers())):
                    code.append(self.list_solutions[i].get_list_routes()[j].get_list_id_customers()[k])
            all_solutions.append(code)

        return all_solutions

    # Método que devuelve el costo total de la mejor solución
    def get_total_cost_solution(self):
        return round(self.best_solution.get_cost_solution(), 2)

    # Método que devuelve la cantidad de rutas de una solución
    def count_routes(self):
        return len(self.best_solution.get_list_routes())

    # Método que devuelve la demanda para cada una de las rutas de la mejor solución
    def get_request_by_route(self) -> List[float]:
        list_requests = []
        for route in self.best_solution.get_list_routes():
            list_requests.append(route.get_request_route())
        return list_requests

    # Método que devuelve el tipo de cada una de las rutas de la mejor solución
    def get_type_route_by_route(self) -> List[RouteType]:
        list_types = []
        """for route in self.best_solution.getListRoutes():
            listTypes.append(((RouteTTRP)route).getTypeRoute())"""
        return list_types

    # Método que devuelve la cantidad de rutas para un depósito dado en la mejor solución
    def count_routes_for_depot(self, id_depot: int) -> int:
        count_routes = 0
        for route in self.best_solution.get_list_routes():
            if route.get_id_depot() == id_depot:
                count_routes += 1
        return count_routes

    # Método que devuelve la demanda cubierta para un depósito dado en la mejor solución
    def request_for_depot(self, id_depot: int) -> float:
        request_depot = -1.0
        for route in self.best_solution.get_list_routes():
            if route.get_id_depot() == id_depot:
                request_depot += route.get_request_route()
        return request_depot

    # Método que devuelve las rutas para un depósito dado en la mejor solución
    def routes_for_depot(self, id_depot: int) -> List[List[int]]:
        list_routes_depot = []
        for route in self.best_solution.get_list_routes():
            if route.get_id_depot() == id_depot:
                list_routes_depot.append(route.get_list_id_customers())
        return list_routes_depot

    # Método que devuelve el costo total para un depósito dado en la mejor solución
    def cost_for_depot(self, id_depot: int) -> float:
        cost_depot = -1.0
        for route in self.best_solution.get_list_routes():
            if route.get_id_depot() == id_depot:
                cost_depot += route.get_cost_route()
        return Tools.round_double(cost_depot, 2)

    # Método que restaura los parámetros globales de la clase StrategyHeuristic
    def clean_strategy(self):
        self.best_solution = None
        self.list_solutions.clear()
        self.time_execute = 0.0

    @staticmethod # Método que destruye la instancia de la controladora
    def destroy_strategy(self):
        self.strategy_heuristic = None






