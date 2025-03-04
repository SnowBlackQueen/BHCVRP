from generator.heuristic.Heuristic import Heuristic
from data.ProblemType import ProblemType
from data.Problem import Problem
from solution.Solution import Solution
from solution.Route import Route


class FisherJaikumar(Heuristic):

    def initialize_specifics(self):
        # Inicializar parámetros específicos de la heurística
        self.seed_points = []  # Puntos semilla (clientes con mayor demanda)
        self.vehicle_capacity = None  # Capacidad de los vehículos
        self.num_vehicles = None  # Número de vehículos
        self.assigned_customers = {}  # Diccionario para almacenar clientes asignados a cada vehículo

        self.num_vehicles = Problem.get_problem().get_list_depots()[0].get_list_fleets()[0].get_count_vehicles()

        if self.type_problem == ProblemType.HFVRP:
            self.vehicle_capacity = Problem.get_problem().get_list_capacities()
            self.assigned_customers = {i: [] for i in range(self.num_vehicles)}  # Diccionario para almacenar clientes asignados a cada vehículo
        else:
            self.vehicle_capacity = Problem.get_problem().get_list_depots()[0].get_list_fleets()[0].get_capacity_vehicle()  # Capacidad homogénea

        self.seed_points = self.creating()  # Seleccionar puntos semilla



    def get_solution_inicial(self) -> Solution:
        # Fase de asignación
        self.processing()
        # Fase de enrutamiento
        self.execute()
        return self.solution

    def creating(
        self, route=None, request_route=None, list_tau=None, list_metrics=None
    ):
        # Seleccionar los clientes con mayor demanda como puntos semilla
        customers = Problem.get_problem().get_list_customers()
        # Ordenar clientes por demanda (de mayor a menor)
        sorted_customers = sorted(customers, key=lambda c: c.get_request_customer(), reverse=True)

        if self.type_problem == ProblemType.CVRP:
            # Seleccionar los primeros `num_vehicles` clientes como puntos semilla
            return sorted_customers[:self.num_vehicles]

        if self.type_problem == ProblemType.HFVRP:
            # Ordenar vehículos por capacidad (de mayor a menor)
            sorted_vehicles = sorted(range(self.num_vehicles), key=lambda i: self.vehicle_capacity[i], reverse=True)

            # Asignar los clientes con mayor demanda a los vehículos con mayor capacidad
            seed_points = []
            for i in range(min(self.num_vehicles, len(sorted_customers))):
                seed_points.append(sorted_customers[i])
                self.assigned_customers[sorted_vehicles[i]].append(sorted_customers[i])

            return seed_points

    def processing(
        self,
        customers_to_visit=None,
        count_vehicles=None,
        request_route=None,
        route=None,
        id_depot=None,
        solution=None,
    ):
        if self.type_problem == ProblemType.CVRP:
            # Asignar cada cliente al vehículo más cercano (en términos de costo)
            customers = Problem.get_problem().get_list_customers()
            cost_matrix = Problem.get_problem().get_cost_matrix()

            # Inicializar diccionario para almacenar clientes asignados a cada vehículo
            self.assigned_customers = {i: [] for i in range(self.num_vehicles)}

            for customer in customers:
                if customer in self.seed_points:
                    # Si el cliente es un punto semilla, asignarlo a su propio vehículo
                    vehicle_index = self.seed_points.index(customer)
                    self.assigned_customers[vehicle_index].append(customer)
                else:
                    # Asignar el cliente al vehículo más cercano (basado en el costo)
                    min_cost = float('inf')
                    best_vehicle = 0

                    for i, seed in enumerate(self.seed_points):
                        cost = cost_matrix.item(customer.get_id_customer(), seed.get_id_customer())
                        if cost < min_cost:
                            min_cost = cost
                            best_vehicle = i

                    # Verificar que la capacidad del vehículo no se exceda
                    total_demand = sum(c.get_request_customer() for c in self.assigned_customers[best_vehicle])
                    if total_demand + customer.get_request_customer() <= self.vehicle_capacity:
                        self.assigned_customers[best_vehicle].append(customer)

        if self.type_problem == ProblemType.HFVRP:
            # Asignar cada cliente al vehículo más cercano (en términos de costo) que tenga suficiente capacidad
            customers = Problem.get_problem().get_list_customers()
            cost_matrix = Problem.get_problem().get_cost_matrix()

            for customer in customers:
                if customer in self.seed_points:
                    continue  # Los puntos semilla ya están asignados

                min_cost = float('inf')
                best_vehicle = -1

                for i, seed in enumerate(self.seed_points):
                    cost = cost_matrix.item(customer.get_id_customer(), seed.get_id_customer())
                    if cost < min_cost:
                        # Verificar que la capacidad del vehículo no se exceda
                        total_demand = sum(c.get_request_customer() for c in self.assigned_customers[i])
                        if total_demand + customer.get_request_customer() <= self.vehicle_capacity[i]:
                            min_cost = cost
                            best_vehicle = i

                if best_vehicle != -1:
                    self.assigned_customers[best_vehicle].append(customer)


    def execute(self):
        if self.type_problem == ProblemType.CVRP or self.type_problem == ProblemType.HFVRP:
            # Resolver el problema de enrutamiento para cada vehículo
            depot = Problem.get_problem().get_list_depots()[0]  # Único depósito
            cost_matrix = Problem.get_problem().get_cost_matrix()

            for vehicle_id, customers in self.assigned_customers.items():
                if not customers:
                    continue  # Si no hay clientes asignados, pasar al siguiente vehículo

                # Crear una ruta para el vehículo
                route = Route()
                route.set_id_depot(depot.get_id_depot())

                # Iniciar desde el depósito
                current_node = depot.get_id_depot()
                remaining_customers = customers.copy()

                while remaining_customers:
                    # Seleccionar el cliente más cercano usando RLC
                    nearest_customer = self._get_NN_element(remaining_customers, current_node)
                    route.get_list_id_customers().append(nearest_customer.get_id_customer())
                    current_node = nearest_customer.get_id_customer()
                    remaining_customers.remove(nearest_customer)

                # Añadir la ruta a la solución
                self.solution.get_list_routes().append(route)

    def _get_NN_element(self, list_elements, reference):
        # Método copiado de NearestNeighborWithRLC
        RLC = 1

        if len(list_elements) == 1:
            element = list_elements[0]
        else:
            list_nn = self._get_list_NN(list_elements, reference)
            list_rlc = []

            list_rlc.append(list_nn[RLC])
            element = list_rlc.pop(0)

        return element

    def _get_list_NN(self, list_elements, reference):
        # Método copiado de NearestNeighborWithRLC
        list_distances = []
        list_nn = []
        ref_distance = 0.0

        for i in range(len(list_elements)):
            if Problem.get_problem().get_type_problem() == ProblemType.SBRP:
                ref_distance = (Problem.get_problem().get_cost_matrix().item(
                    Problem.get_problem().get_pos_element(reference),
                    Problem.get_problem().get_pos_element(list_elements[i].get_id_bus_stop())))
            else:
                ref_distance = (Problem.get_problem().get_cost_matrix().item(
                    Problem.get_problem().get_pos_element(reference),
                    Problem.get_problem().get_pos_element(list_elements[i].get_id_customer())))
            list_distances.append(ref_distance)
            list_nn.append(list_elements[i])

        self._ascendent_ordenate_list_distances(list_distances, list_nn)

        return list_nn


