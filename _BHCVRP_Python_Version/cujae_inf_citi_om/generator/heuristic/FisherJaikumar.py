from generator.heuristic.Heuristic import Heuristic
from data.ProblemType import ProblemType
from data.Problem import Problem
from solution.Solution import Solution
from solution.Route import Route
from data.CustomerType import CustomerType
from solution.RouteType import RouteType
from solution.RouteTTRP import RouteTTRP


class FisherJaikumar(Heuristic):

    def initialize_specifics(self):
        # Inicializar parámetros específicos de la heurística
        self.seed_points = []  # Puntos semilla (clientes con mayor demanda)
        self.vehicle_capacity = None  # Capacidad de los vehículos
        self.num_vehicles = None  # Número de vehículos
        self.assigned_elements = {}  # Diccionario para almacenar clientes asignados a cada vehículo

        self.num_vehicles = Problem.get_problem().get_list_depots()[0].get_list_fleets()[0].get_count_vehicles()

        if self.type_problem == ProblemType.HFVRP:
            self.vehicle_capacity = Problem.get_problem().get_list_capacities()
            self.assigned_elements = {i: [] for i in range(self.num_vehicles)}  # Diccionario para almacenar clientes asignados a cada vehículo
        else:
            self.vehicle_capacity = Problem.get_problem().get_list_depots()[0].get_list_fleets()[0].get_capacity_vehicle()  # Capacidad homogénea

        if self.type_problem == ProblemType.TTRP:
            self.trailer_capacity = None  # Capacidad de los remolques
            self.num_trailers = None  # Número de remolques

            # Obtener las capacidades de los camiones y remolques
            self.trailer_capacity = Problem.get_problem().get_list_depots()[0].get_list_fleets()[0].get_capacity_trailer()
            self.num_trailers = Problem.get_problem().get_list_depots()[0].get_list_fleets()[0].get_count_trailers()

            # Inicializar diccionario para almacenar clientes asignados a cada vehículo
            self.assigned_elements = {i: [] for i in range(self.num_vehicles + self.num_trailers)}

        self.depots = Problem.get_problem().get_list_depots()  # Lista de depósitos

        if self.type_problem == ProblemType.MDVRP:
            # Inicializar diccionario para almacenar clientes asignados a cada vehículo por depósito
            self.assigned_elements = {
                depot.get_id_depot(): {i: [] for i in range(depot.get_list_fleets()[0].get_count_vehicles())} for depot
                in self.depots}

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
        if self.type_problem == ProblemType.SBRP or self.type_problem == 5:
            elements = Problem.get_problem().get_list_buses_stop()
            sorted_elements = sorted(elements, key=lambda b: b.get_capacity_bus_stop(), reverse=True)
        else:
            # Seleccionar los clientes con mayor demanda como puntos semilla
            elements = Problem.get_problem().get_list_customers()
            # Ordenar clientes por demanda (de mayor a menor)
            sorted_elements = sorted(elements, key=lambda c: c.get_request_customer(), reverse=True)

        if self.type_problem == ProblemType.CVRP or self.type_problem == ProblemType.OVRP or self.type_problem == ProblemType.SBRP or self.type_problem == ProblemType.VRPTW or self.type_problem in [0, 3, 5, 6]:
            # Seleccionar los primeros `num_vehicles` clientes como puntos semilla
            return sorted_elements[:self.num_vehicles]

        elif self.type_problem == ProblemType.HFVRP or self.type_problem == 1:
            # Ordenar vehículos por capacidad (de mayor a menor)
            sorted_vehicles = sorted(range(self.num_vehicles), key=lambda i: self.vehicle_capacity[i], reverse=True)

            # Asignar los clientes con mayor demanda a los vehículos con mayor capacidad
            seed_points = []
            for i in range(min(self.num_vehicles, len(sorted_elements))):
                seed_points.append(sorted_elements[i])
                self.assigned_elements[sorted_vehicles[i]].append(sorted_elements[i])

            return seed_points

        elif self.type_problem == ProblemType.TTRP or self.type_problem == 4:
            # Seleccionar los primeros `num_vehicles` clientes TC como puntos semilla para camiones
            tc_customers = [c for c in sorted_elements if c.get_type_customer() == CustomerType.TC or c.get_type_customer() == 1]
            seed_points_tc = tc_customers[:self.num_vehicles]

            # Seleccionar los primeros `num_trailers` clientes VC como puntos semilla para remolques
            vc_customers = [c for c in sorted_elements if c.get_type_customer() == CustomerType.VC or c.get_type_customer() == 0]
            seed_points_vc = vc_customers[:self.num_trailers]

            # Combinar los puntos semilla para camiones y remolques
            seed_points = seed_points_tc + seed_points_vc

            # Asignar los puntos semilla a los vehículos correspondientes
            for i, customer in enumerate(seed_points):
                if i < self.num_vehicles:
                    self.assigned_elements[i].append(customer)  # Asignar a camiones
                else:
                    self.assigned_elements[i].append(customer)  # Asignar a remolques

            return seed_points

        elif self.type_problem == ProblemType.MDVRP:
            seed_points = []
            for depot in self.depots:
                # Obtener los clientes asignados a este depósito
                depot_customers = Problem.get_problem().get_customers_assigned_by_id_depot(
                    depot.get_id_depot(), elements, self.depots
                )
                # Seleccionar los primeros `num_vehicles` clientes como puntos semilla para este depósito
                depot_seed_points = sorted(depot_customers, key=lambda c: c.get_request_customer(), reverse=True)[:depot.get_list_fleets()[0].get_count_vehicles()]
                seed_points.extend(depot_seed_points)

                # Asignar los puntos semilla a los vehículos correspondientes
                for i, customer in enumerate(depot_seed_points):
                    self.assigned_elements[depot.get_id_depot()][i].append(customer)

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
        if self.type_problem == ProblemType.CVRP or self.type_problem == ProblemType.OVRP or self.type_problem == ProblemType.SBRP or self.type_problem == ProblemType.VRPTW or self.type_problem in [0, 3, 5, 6]:
            if self.type_problem == ProblemType.SBRP or self.type_problem == 5:
                elements = Problem.get_problem().get_list_buses_stop()
            else:
                # Asignar cada cliente al vehículo más cercano (en términos de costo)
                elements = Problem.get_problem().get_list_customers()
            cost_matrix = Problem.get_problem().get_cost_matrix()

            # Inicializar diccionario para almacenar clientes asignados a cada vehículo
            self.assigned_elements = {i: [] for i in range(self.num_vehicles)}

            for element in elements:
                if element in self.seed_points:
                    # Si el cliente es un punto semilla, asignarlo a su propio vehículo
                    vehicle_index = self.seed_points.index(element)
                    self.assigned_elements[vehicle_index].append(element)
                else:
                    # Asignar el cliente al vehículo más cercano (basado en el costo)
                    min_cost = float('inf')
                    best_vehicle = 0

                    for i, seed in enumerate(self.seed_points):
                        if self.type_problem == ProblemType.SBRP or self.type_problem == 5:
                            cost = cost_matrix.item(element.get_id_bus_stop(), seed.get_id_bus_stop())
                        else:
                            cost = cost_matrix.item(element.get_id_customer(), seed.get_id_customer())
                        if cost < min_cost:
                            min_cost = cost
                            best_vehicle = i

                    if self.type_problem == ProblemType.SBRP or self.type_problem == 5:
                        total_demand = sum(b.get_capacity_bus_stop() for b in self.assigned_elements[best_vehicle])
                        if total_demand + element.get_capacity_bus_stop() <= self.vehicle_capacity:
                            self.assigned_elements[best_vehicle].append(element)
                    else:
                        # Verificar que la capacidad del vehículo no se exceda
                        total_demand = sum(c.get_request_customer() for c in self.assigned_elements[best_vehicle])
                        if total_demand + element.get_request_customer() <= self.vehicle_capacity:
                            self.assigned_elements[best_vehicle].append(element)

        elif self.type_problem == ProblemType.HFVRP:
            # Asignar cada cliente al vehículo más cercano (en términos de costo) que tenga suficiente capacidad
            elements = Problem.get_problem().get_list_customers()
            cost_matrix = Problem.get_problem().get_cost_matrix()

            for element in elements:
                if element in self.seed_points:
                    continue  # Los puntos semilla ya están asignados

                min_cost = float('inf')
                best_vehicle = -1

                for i, seed in enumerate(self.seed_points):
                    cost = cost_matrix.item(element.get_id_customer(), seed.get_id_customer())
                    if cost < min_cost:
                        # Verificar que la capacidad del vehículo no se exceda
                        total_demand = sum(c.get_request_customer() for c in self.assigned_elements[i])
                        if total_demand + element.get_request_customer() <= self.vehicle_capacity[i]:
                            min_cost = cost
                            best_vehicle = i

                if best_vehicle != -1:
                    self.assigned_elements[best_vehicle].append(element)

        elif self.type_problem == ProblemType.TTRP:
            # Asignar cada cliente al vehículo más cercano (en términos de costo) que tenga suficiente capacidad
            elements = Problem.get_problem().get_list_customers()
            cost_matrix = Problem.get_problem().get_cost_matrix()

            for element in elements:
                if element in self.seed_points:
                    continue  # Los puntos semilla ya están asignados

                min_cost = float('inf')
                best_vehicle = -1

                for i, seed in enumerate(self.seed_points):
                    cost = cost_matrix.item(element.get_id_customer(), seed.get_id_customer())
                    if cost < min_cost:
                        # Verificar que la capacidad del vehículo no se exceda
                        if element.get_type_customer() == CustomerType.TC:
                            # Cliente TC solo puede ser asignado a camiones
                            if i < self.num_vehicles:
                                total_demand = sum(c.get_request_customer() for c in self.assigned_elements[i])
                                if total_demand + element.get_request_customer() <= self.vehicle_capacity:
                                    min_cost = cost
                                    best_vehicle = i
                        else:
                            # Cliente VC puede ser asignado a camiones con remolques
                            if i < self.num_vehicles + self.num_trailers:
                                total_demand = sum(c.get_request_customer() for c in self.assigned_elements[i])
                                if total_demand + element.get_request_customer() <= self.vehicle_capacity + self.trailer_capacity:
                                    min_cost = cost
                                    best_vehicle = i

                if best_vehicle != -1:
                    self.assigned_elements[best_vehicle].append(element)

        elif self.type_problem == ProblemType.MDVRP:
            # Asignar cada cliente al vehículo más cercano (en términos de costo) que tenga suficiente capacidad
            customers = Problem.get_problem().get_list_customers()
            cost_matrix = Problem.get_problem().get_cost_matrix()

            for depot in self.depots:
                depot_customers = Problem.get_problem().get_customers_assigned_by_id_depot(
                    depot.get_id_depot(), customers, self.depots
                )
                for customer in depot_customers:
                    if customer in self.seed_points:
                        continue  # Los puntos semilla ya están asignados

                    min_cost = float('inf')
                    best_vehicle = -1

                    for i, seed in enumerate(self.seed_points):
                        if seed.get_id_depot() == depot.get_id_depot():
                            cost = cost_matrix.item(customer.get_id_customer(), seed.get_id_customer())
                            if cost < min_cost:
                                # Verificar que la capacidad del vehículo no se exceda
                                total_demand = sum(
                                    c.get_request_customer() for c in self.assigned_elements[depot.get_id_depot()][i])
                                if total_demand + customer.get_request_customer() <= self.vehicle_capacity:
                                    min_cost = cost
                                    best_vehicle = i

                    if best_vehicle != -1:
                        self.assigned_elements[depot.get_id_depot()][best_vehicle].append(customer)


    def execute(self):
        if self.type_problem == ProblemType.CVRP or self.type_problem == ProblemType.OVRP or self.type_problem == ProblemType.HFVRP or self.type_problem == ProblemType.TTRP or self.type_problem == ProblemType.SBRP or self.type_problem == ProblemType.VRPTW or self.type_problem in [0, 1, 3, 4, 5, 6]:
            # Resolver el problema de enrutamiento para cada vehículo
            depot = Problem.get_problem().get_list_depots()[0]  # Único depósito
            cost_matrix = Problem.get_problem().get_cost_matrix()

            for vehicle_id, elements in self.assigned_elements.items():
                if not elements:
                    continue  # Si no hay clientes asignados, pasar al siguiente vehículo

                if self.type_problem == ProblemType.TTRP:
                    # Crear una ruta para el vehículo
                    route = RouteTTRP()
                    route.set_id_depot(depot.get_id_depot())

                    # Determinar el tipo de ruta (PVR, PTR o CVR)
                    if vehicle_id < self.num_vehicles:
                        route.set_type_route(RouteType.PVR.value)  # Ruta de camión
                    else:
                        route.set_type_route(RouteType.PTR.value)  # Ruta de camión con remolque

                else:
                    # Crear una ruta para el vehículo
                    route = Route()
                    route.set_id_depot(depot.get_id_depot())

                # Iniciar desde el depósito
                current_node = depot.get_id_depot()
                remaining_elements = elements.copy()

                if self.type_problem == ProblemType.VRPTW:
                    nearest_element = self._get_NN_element(remaining_elements, current_node)
                    route.get_list_id_customers().append(nearest_element.get_id_customer())
                    current_node = nearest_element.get_id_customer()

                while remaining_elements:
                    # Seleccionar el cliente más cercano usando RLC
                    nearest_element = self._get_NN_element(remaining_elements, current_node)

                    if self.type_problem == ProblemType.SBRP or self.type_problem == 5:
                        if self.capacity_vehicle >= (route.get_request_route() + nearest_element.get_capacity_bus_stop()):
                            route.get_list_bus_stops().append(nearest_element.get_id_bus_stop())
                            current_node = nearest_element.get_id_bus_stop()
                        else:
                            route = Route()
                            route.get_list_bus_stops().append(nearest_element.get_id_bus_stop())
                            current_node = nearest_element.get_id_bus_stop()
                    else:
                        if self.capacity_vehicle >= (route.get_request_route() + nearest_element.get_request_customer()):
                            tw_flag = True
                            if self.type_problem == ProblemType.VRPTW:
                                self.time_route = self.get_time_route(route.get_list_id_customers())
                                self.feasible_customers = self.get_feasible_customers(
                                    route.get_list_id_customers()[-1])
                                if nearest_element in self.feasible_customers:
                                    time_matrix = Problem.get_problem().get_time_matrix()
                                    current_time = time_matrix[
                                        route.get_list_id_customers()[
                                            -1], nearest_element.get_id_customer()]
                                    customer_ready_time = nearest_element.get_time_window().get_initial_node()
                                    customer_service_time = nearest_element.get_time_window().get_service_time()
                                    self.time_route = max(current_time, customer_ready_time) + customer_service_time
                                else:
                                    tw_flag = False
                                    nearest_element = self._get_NN_element(remaining_elements, current_node)
                            if tw_flag:
                                route.get_list_id_customers().append(nearest_element.get_id_customer())
                                current_node = nearest_element.get_id_customer()
                        else:
                            route = Route()
                            route.get_list_id_customers().append(nearest_element.get_id_customer())
                            current_node = nearest_element.get_id_customer()

                    remaining_elements.remove(nearest_element)

                # Añadir la ruta a la solución
                self.solution.get_list_routes().append(route)

        elif self.type_problem == ProblemType.MDVRP:
            # Resolver el problema de enrutamiento para cada vehículo en cada depósito
            cost_matrix = Problem.get_problem().get_cost_matrix()

            for depot in self.depots:
                for vehicle_id, customers in self.assigned_elements[depot.get_id_depot()].items():
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


