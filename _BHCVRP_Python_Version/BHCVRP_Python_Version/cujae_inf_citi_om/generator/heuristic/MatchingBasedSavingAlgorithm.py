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

class MatchingBasedSavingAlgorithm(Save):
    def __init__(self):
        super().__init__()

    def initialize_specifics(self):
        super().initialize_specifics()
        self.matching_pairs = []
        self.list_capacities = list(Problem.get_problem().fill_list_capacities(self.pos_depot))  
        
        # self.inspect_routes(self.list_routes, self.list_capacities, self.solution, self.customers_to_visit)  
        
        self.total_capacity = self.capacity_vehicle

        self.iterations = (self.cant_customers * (self.cant_customers - 1)) / 2
        self.counter = 0
        self.previous_total_cost = float('inf')
        self.min_improvement = 1  # Ejemplo de umbral de mejora mínima
        self.row, self.col = np.unravel_index(np.argmax(self.save_matrix), self.save_matrix.shape)
        
    def get_solution_inicial(self) -> Solution:
        if self.type_problem == 0 or self.type_problem == ProblemType.CVRP:
            while self.convergence_criteria_with_max_iterations():
                self.select_matching_pairs()
                
                self.counter += 1

                self.combine_pairs()

                self.combine_routes()
                            
                self.update_save_matrix_after_combination()

            # Esto corresponde a optimize_routes
            for j in range(len(self.list_routes)):
                if len(self.list_routes[j].get_list_id_customers()) >= 6:
                    self.three_opt.to_optimize(self.list_routes[j])

            self.solution.get_list_routes().extend(self.list_routes)
    

    def select_matching_pairs(self):
        # Ordena los pares por ahorro y selecciona los candidatos para combinar
        # Ordenar la matriz de ahorros por ahorro descendente
        sorted_indices = np.argsort(self.save_matrix, axis=None)[::-1]

        for pair in zip(sorted_indices[:-1], sorted_indices[1:-1]):
            # Aquí seleccionamos los pares con mayor ahorro
            # Verificar si el par es factible de combinar bajo las restricciones del problema
            if self.is_feasible_pair(pair[0], pair[1]):
                # Suponiendo que is_feasible_pair es una función que verifica la factibilidad de combinar el par bajo las restricciones del problema
                # Actualizar la matriz de ahorros eliminando el par seleccionado para futuras iteraciones
                self.save_matrix[pair[0], pair[1]] = np.NINF
                self.save_matrix[pair[1], pair[0]] = np.NINF
                # Actualizar self.list_routes con el nuevo par de clientes combinados

    def combine_pairs(self):
        # Combina los pares seleccionados en rutas, actualizando la matriz de ahorros y las rutas
        # Suponiendo que ya hemos seleccionado pares de clientes para combinar en select_matching_pairs
        for pair in self.matching_pairs:
            # Encuentra las rutas actuales de los clientes en el par
            route_i = self.find_route_for_customer(pair[0])
            route_j = self.find_route_for_customer(pair[1])
            
            # Verifica si ambos clientes están en la misma ruta
            if route_i == route_j:
                continue  # No se puede combinar en la misma ruta, pasa al siguiente par
            
            # Verifica si la combinación es factible (capacidad del vehículo, restricciones de tiempo, etc.)
            if not self.is_feasible_combination(route_i, route_j):
                continue  # Si no es factible, pasa al siguiente par
            
            # Combina las rutas
            new_route = self.combine_routes(route_i, route_j)
            
            # Actualiza la lista de rutas
            self.list_routes.remove(route_i)
            self.list_routes.remove(route_j)
            self.list_routes.append(new_route)
            
            # Actualiza la matriz de ahorros para reflejar la combinación
            self.fill_save_matrix(pair[0], pair[1])
    
    def combine_routes(self, route_i, route_j):
        # Crea una nueva ruta combinando route_i y route_j
        # Esto es un ejemplo simplificado, necesitarás ajustarlo a tu implementación específica
        new_route = Route()
        new_route.list_id_customers = route_i.get_list_id_customers() + route_j.get_list_id_customers()  # Combina las listas de clientes
        new_route.set_id_depot(route_i.get_id_depot())  # Asume un solo depósito
        new_route.calculate_request_route()  # Calcula la demanda total de la nueva ruta
        return new_route

    def convergence_criteria_with_max_iterations(self):
        # Ejemplo basado en el número de iteraciones
        return self.counter >= self.iterations
        
    def convergence_criteria_best_cost(self):
        # Ejemplo basado en mejora en el costo total de las rutas
        current_total_cost = sum(self.route_cost(route) for route in self.list_routes)
        improvement = self.previous_total_cost - current_total_cost
        self.previous_total_cost = current_total_cost
        return improvement < self.min_improvement or self.counter >= self.iterations
        
    def is_feasible_combination(self, route_i, route_j):
        # Verifica si la combinación de route_i y route_j es factible
        # Ejemplo: verifica la capacidad del vehículo
        total_demand = route_i.get_request_route() + route_j.get_request_route()
        return total_demand <= self.capacity_vehicle
        
    def update_save_matrix_after_combination(self, customer_i, customer_j):
        # Actualiza la matriz de ahorros para reflejar que customer_i y customer_j ya no son elegibles para combinaciones
        # Puedes marcar sus filas y columnas con -np.inf o similar
        self.save_matrix[customer_i, :] = -np.inf
        self.save_matrix[:, customer_i] = -np.inf
        self.save_matrix[customer_j, :] = -np.inf
        self.save_matrix[:, customer_j] = -np.inf
        
    def find_route_for_customer(list_routes, id_customer):
        for route in list_routes:
            if id_customer in route.get_list_id_customers():
                return route
        return None
        
    '''def calculate_savings(self):               esta corresponde con fill_save_matrix()...
        # Calcula y llena la matriz de ahorros aquí
        count_customers = len(self.self.customers_to_visit)
        self.self.save_matrix = np.full((count_customers, count_customers), -np.inf)

        # Asumimos que self.customers_to_visit contiene los IDs de los clientes como índices
        self.id_depot = Problem.get_problem().get_list_depots()[0].get_self.id_depot()

        for i in range(count_customers):
            for j in range(i+1, count_customers):  # Evitamos el auto-loop para evitar repetir el mismo nodo
                save_i_j = Problem.get_problem().get_cost_matrix(self.id_depot, self.self.customers_to_visit[i].id_customer) + \
                        Problem.get_problem().get_cost_matrix(self.self.customers_to_visit[j].id_customer, self.id_depot) - \
                        (self.parameter_shape * Problem.get_problem().get_cost_matrix(self.self.customers_to_visit[i].id_customer, self.self.customers_to_visit[j].id_customer))
                self.self.save_matrix[i, j] = save_i_j
                self.self.save_matrix[j, i] = save_i_j  # Simetría por ser simétrico
        pass
        
        def optimize_routes(self):
        # Aplica el operador 3-opt a las rutas generadas
        for route in self.list_routes:
            if len(route.list_id_customers) >= 6:  # 3-opt requiere al menos 4 nodos para operar
                improved = True
                while improved:
                    improved = False
                    for i in range(len(route.list_id_customers) - 2):
                        for j in range(i + 2, len(route.list_id_customers)):
                            if j - i >= 2:  # Asegura que haya suficientes nodos entre i y j
                                new_route = route
                                self.three_opt.to_optimize(new_route)
                                if new_route.get_cost_route() < route.get_cost_route():
                                    route = new_route
                                    improved = True
                            self.solution.get_list_routes().append(route)
        pass'''