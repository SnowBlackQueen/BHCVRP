from generator.heuristic.Heuristic import Heuristic
from data.Problem import Problem
from data.ProblemType import ProblemType
from generator.solution.RouteType import RouteType
from generator.solution.Solution import Solution
import numpy as np
from generator.postoptimization.Operator_3opt import Operator_3opt
from generator.heuristic.Save import Save
from random import Random


class SaveSequential(Save):

    def __init__(self):
        super().__init__()

    def initialize_specifics(self):
        super().initialize_specifics()
        self.random = Random()
        self.index = -1

        self.ext_inic = -1
        self.ext_end = -1
        self.no_extreme = -1
        self.exist_save = False

    def creating(self, route=None, request_route=None, list_tau=None, list_metrics=None):
        if self.type_problem in [0, 2,
                                 3] or self.type_problem == ProblemType.CVRP or self.type_problem == ProblemType.MDVRP:
            row_matrix = Problem.get_problem().get_pos_element(self.ext_inic)
            submatrix = self.save_matrix[row_matrix, :self.cant_customers]
            self.max_save_inic = (row_matrix, np.argmax(submatrix))
            if self.ext_inic != self.ext_end:
                row_matrix = Problem.get_problem().get_pos_element(self.ext_end)
                submatrix = self.save_matrix[row_matrix, :self.cant_customers]
                self.max_save_end = (row_matrix, np.argmax(submatrix))
            else:
                self.max_save_end = self.max_save_inic

            # Comparar los valores y asignar el máximo
            if self.save_matrix[self.max_save_inic[0], self.max_save_inic[1]] > self.save_matrix[
                self.max_save_end[0], self.max_save_end[1]]:
                self.max_save = self.max_save_inic
            else:
                self.max_save = self.max_save_end
                self.position_save = True

            if self.current_route.get_request_route() == self.capacity_vehicle:
                self.save_matrix[Problem.get_problem().get_pos_element(self.ext_inic), :] = -np.inf
                self.save_matrix[:, Problem.get_problem().get_pos_element(self.ext_inic)] = -np.inf

                self.save_matrix[Problem.get_problem().get_pos_element(self.ext_end), :] = -np.inf
                self.save_matrix[:, Problem.get_problem().get_pos_element(self.ext_end)] = -np.inf

                self.exist_save = False
                return

            self.save_value = self.save_matrix[self.max_save[0], self.max_save[1]]

        elif self.type_problem == 1 or self.type_problem == ProblemType.HFVRP:

            row_matrix = Problem.get_problem().get_pos_element(self.ext_inic)
            submatrix = self.save_matrix[row_matrix, :self.cant_customers]
            self.max_save_inic = (row_matrix, np.argmax(submatrix))

            if self.ext_inic != self.ext_end:
                row_matrix = Problem.get_problem().get_pos_element(self.ext_end)
                submatrix = self.save_matrix[row_matrix, :self.cant_customers]
                self.max_save_end = (row_matrix, np.argmax(submatrix))
            else:
                self.max_save_end = self.max_save_inic

            # Comparar los valores y asignar el máximo
            if self.save_matrix[self.max_save_inic[0], self.max_save_inic[1]] > self.save_matrix[
                self.max_save_end[0], self.max_save_end[1]]:
                self.max_save = self.max_save_inic
            else:
                self.max_save = self.max_save_end
                self.position_save = True

            if self.current_route.get_request_route() == self.list_capacities[0]:  # capacity_vehicle
                # Llenar con infinito negativo para ext_inic
                self.save_matrix[Problem.get_problem().get_pos_element(self.ext_inic), :] = -np.inf
                self.save_matrix[:, Problem.get_problem().get_pos_element(self.ext_inic)] = -np.inf

                # Llenar con infinito negativo para ext_end
                self.save_matrix[Problem.get_problem().get_pos_element(self.ext_end), :] = -np.inf
                self.save_matrix[:, Problem.get_problem().get_pos_element(self.ext_end)] = -np.inf

                self.exist_save = False
                return

            self.save_value = self.save_matrix[self.max_save[0], self.max_save[1]]

        elif self.type_problem == 4 or self.type_problem == ProblemType.TTRP:
            row_matrix = Problem.get_problem().get_pos_element(self.ext_inic)
            submatrix = self.save_matrix[row_matrix, :self.cant_customers]
            self.max_save_inic = (row_matrix, np.argmax(submatrix))

            if self.ext_inic != self.ext_end:
                row_matrix = Problem.get_problem().get_pos_element(self.ext_end)
                submatrix = self.save_matrix[row_matrix, :self.cant_customers]
                self.max_save_end = (row_matrix, np.argmax(submatrix))
            else:
                self.max_save_end = self.max_save_inic

            if self.save_matrix[self.max_save_inic[0], self.max_save_inic[1]] > self.save_matrix[self.max_save_end[0], self.max_save_end[1]]:
                self.max_save = self.max_save_inic
            else:
                self.max_save = self.max_save_end
                self.position_save = True

            type_route = self.current_route._type_route

            if ((type_route == 0 and self.current_route.get_request_route() == self.capacity_vehicle)
                    or ((type_route == 1 or type_route == 2) and
                    self.current_route.get_request_route() == (self.capacity_vehicle + self.capacity_trailer))):
                # Llenar con infinito negativo para ext_inic
                self.save_matrix[Problem.get_problem().get_pos_element(self.ext_inic), :] = -np.inf
                self.save_matrix[:, Problem.get_problem().get_pos_element(self.ext_inic)] = -np.inf

                # Llenar con infinito negativo para ext_end
                self.save_matrix[Problem.get_problem().get_pos_element(self.ext_end), :] = -np.inf
                self.save_matrix[:, Problem.get_problem().get_pos_element(self.ext_end)] = -np.inf

                self.exist_save = False
                return

            self.save_value = self.save_matrix[self.max_save[0], self.max_save[1]]

    def processing(self, customers_to_visit=None, count_vehicles=None, request_route=None, route=None, id_depot=None,
                   solution=None):
        if self.type_problem in [0, 1, 2,
                                 3] or self.type_problem == ProblemType.CVRP or self.type_problem == ProblemType.MDVRP or self.type_problem == ProblemType.HFVRP:
            if self.save_value == -np.inf:
                self.exist_save = False
                return
            else:
                pos_route = self.get_position_route(self.list_routes,
                                                    self.customers_to_visit[self.max_save[1]].get_id_customer())
                save_route = self.list_routes[pos_route]

                is_factible = None

                if self.type_problem == ProblemType.CVRP or self.type_problem == ProblemType.MDVRP:
                    is_factible = self.checking_merge(self.current_route, save_route, self.capacity_vehicle, 0.0,
                                                      self.position_save)
                elif self.type_problem == ProblemType.HFVRP:
                    is_factible = self.checking_merge(self.current_route, save_route, self.list_capacities[0], 0.0,
                                                      self.position_save)

                if is_factible != -1:
                    if self.position_save:
                        self.current_route.get_list_id_customers().extend(save_route.get_list_id_customers())
                        self.ext_end = self.customers_to_visit[self.max_save[1]].get_id_customer()
                    else:
                        self.current_route.list_id_customers = save_route.get_list_id_customers() + self.current_route.get_list_id_customers()
                        self.ext_inic = self.customers_to_visit[self.max_save[1]].get_id_customer()

                    self.current_route.set_id_depot(id_depot)
                    self.current_route.set_request_route(
                        (self.current_route.get_request_route() + save_route.get_request_route()))
                    self.list_routes.remove(save_route)

                    if len(self.current_route.get_list_id_customers()) > 2:
                        no_extreme = self.max_save[0]
                        # Llenar con infinito negativo para no_extreme
                        self.save_matrix[no_extreme, :] = -np.inf
                        self.save_matrix[:, no_extreme] = -np.inf

                        # Llenar con infinito negativo para ext_inic y ext_end
                        self.save_matrix[
                            Problem.get_problem().get_pos_element(self.ext_inic), Problem.get_problem().get_pos_element(
                                self.ext_end)] = -np.inf
                        self.save_matrix[
                            Problem.get_problem().get_pos_element(self.ext_end), Problem.get_problem().get_pos_element(
                                self.ext_inic)] = -np.inf

                # Asignar infinito negativo a max_save
                self.save_matrix[self.max_save[0], self.max_save[1]] = -np.inf
                self.save_matrix[self.max_save[1], self.max_save[0]] = -np.inf


        elif self.type_problem == 4 or self.type_problem == ProblemType.TTRP:
            if self.save_value == -np.inf:
                self.exist_save = False
                return
            else:
                self.pos_route = self.get_position_route(self.list_routes,
                                                    self.customers_to_visit[self.max_save[1]].get_id_customer())
                self.save_route = self.list_routes[self.pos_route]

                self.is_factible = self.checking_merge(self.current_route, self.save_route, self.capacity_vehicle,
                                                  self.capacity_trailer, self.position_save)

                if self.is_factible != -1:
                    #type_route = None

                    if self.position_save:
                        self.current_route.get_list_id_customers().extend(self.save_route.get_list_id_customers())
                        self.ext_end = self.customers_to_visit[self.max_save[1]].get_id_customer()

                        if self.current_route._type_route == self.save_route._type_route:
                            self.type_route = self.current_route._type_route
                        else:
                            if not self.current_route._type_route == RouteType.PTR:
                                self.type_route = RouteType.CVR
                            else:
                                self.type_route = self.current_route._type_route
                    else:
                        self.current_route.get_list_id_customers().insert(0, self.save_route.get_list_id_customers())
                        self.ext_inic = self.customers_to_visit[self.max_save[1]].get_id_customer()

                        if self.save_route._type_route == self.current_route._type_route:
                            self.type_route = self.save_route._type_route
                        else:
                            if self.save_route._type_route.value > 0:
                                self.type_route = RouteType.CVR
                            else:
                                self.type_route = self.save_route._type_route

                        self.current_route.set_type_route(self.type_route.value)
                        self.current_route.set_id_depot(self.id_depot)
                        self.current_route.set_request_route(self.current_route.get_request_route() + self.save_route.get_request_route())
                        self.list_routes.remove(self.save_route)

                        if len(self.current_route.get_list_id_customers()) > 2:
                            self.no_extreme = self.max_save
                            self.save_matrix[self.no_extreme, :] = -np.inf
                            self.save_matrix[:, self.no_extreme] = -np.inf

                            self.save_matrix[
                                Problem.get_problem().get_pos_element(self.ext_inic), Problem.get_problem().get_pos_element(
                                    self.ext_end)] = -np.inf
                            self.save_matrix[
                                Problem.get_problem().get_pos_element(self.ext_end), Problem.get_problem().get_pos_element(
                                    self.ext_inic)] = -np.inf

                    # Asignar infinito negativo a max_save
                    self.save_matrix[self.max_save[0], self.max_save[1]] = -np.inf
                    self.save_matrix[self.max_save[1], self.max_save[0]] = -np.inf

                #if len(self.current_route.get_list_id_customers()) >= 6:
                 #   self.three_opt.to_optimize(self.current_route)

                self.solution.get_list_routes().append(self.current_route)

    def execute(self):
        if self.type_problem in [0, 3] or self.type_problem == ProblemType.CVRP:
            while self.list_routes:
                self.index = self.random.randint(0, len(self.list_routes) - 1)
                self.current_route = self.list_routes.pop(self.index)
                self.exist_save = True

                self.ext_inic = self.current_route.get_list_id_customers()[0]
                self.ext_end = self.current_route.get_list_id_customers()[-1]

                while self.exist_save:
                    self.max_save_inic = None
                    self.max_save_end = None
                    self.max_save = None
                    self.position_save = False

                    self.creating()
                    if not self.exist_save:
                        continue
                    self.processing()

                if len(self.current_route.get_list_id_customers()) >= 6:
                    self.three_opt.to_optimize(self.current_route)

                self.solution.get_list_routes().append(self.current_route)

        elif self.type_problem == 1 or self.type_problem == ProblemType.HFVRP:
            self.list_capacities = list(Problem.get_problem().get_list_capacities())

            while (len(self.list_routes) > 0 and len(self.list_capacities) > 0):
                self.index = self.random.randint(0, len(self.list_routes) - 1)
                self.current_route = self.list_routes.pop(self.index)
                self.exist_save = True

                self.ext_inic = self.current_route.get_list_id_customers()[0]
                self.ext_end = self.current_route.get_list_id_customers()[-1]

                while self.exist_save:
                    self.max_save_inic = None
                    self.max_save_end = None
                    self.max_save = None
                    self.position_save = False

                    self.creating()

                    self.processing()

                if len(self.current_route.get_list_id_customers()) >= 6:
                    self.three_opt.to_optimize(self.current_route)

                self.solution.get_list_routes().append(self.current_route)
                self.list_capacities.pop(0)

        elif self.type_problem == 2 or self.type_problem == ProblemType.MDVRP:
            for j in range(self.pos_depot, len(Problem.get_problem().get_list_depots())):
                if j != self.pos_depot:
                    self.id_depot = Problem.get_problem().get_list_depots()[j].get_id_depot()
                    self.customers_to_visit = Problem.get_problem().get_customers_assigned_by_id_depot(self.id_depot, Problem.get_problem().get_list_customers(), Problem.get_problem().get_list_depots())

                    self.capacity_vehicle = Problem.get_problem().get_list_depots()[j].get_list_fleets()[0].get_capacity_vehicle()

                    if self.customers_to_visit:
                        self.list_routes = self.create_initial_routes(self.customers_to_visit)
                        self.cant_customers = len(self.customers_to_visit)
                        self.save_matrix = np.zeros(self.cant_customers, self.cant_customers)
                        self.save_matrix = self.fill_save_matrix(self.id_depot, self.customers_to_visit)

                while self.list_routes:
                    self.index = self.random.randint(0, len(self.list_routes) - 1)
                    self.current_route = self.list_routes.pop(self.index)
                    self.exist_save = True

                    self.ext_inic = self.current_route.get_list_id_customers()[0]
                    self.ext_end = self.current_route.get_list_id_customers()[
                        len(self.current_route.get_list_id_customers()) - 1]

                    while self.exist_save:
                        self.max_save_inic = None
                        self.max_save_end = None
                        self.max_save = None
                        self.position_save = False

                        self.creating()

                        self.processing()

        elif self.type_problem == 4 or self.type_problem == ProblemType.TTRP:
            self.capacity_trailer = Problem.get_problem().get_list_depots()[self.pos_depot].get_list_fleets()[0].get_capacity_trailer()

            while self.list_routes:
                self.index = self.random.randint(0, len(self.list_routes) - 1)
                self.current_route = self.list_routes.pop(self.index)

                self.exist_save = True

                self.ext_inic = self.current_route.get_list_id_customers()[0]
                self.ext_end = self.current_route.get_list_id_customers()[len(self.current_route.get_list_id_customers()) - 1]


                while self.exist_save:
                    self.max_save_inic = None
                    self.max_save_end = None
                    self.max_save = None
                    self.position_save = False

                    self.creating()

                    self.processing()

        return self.solution

    # Método encargado de generar la solución
    def get_solution_inicial(self):

        self.execute()

        return self.solution

    # Método que verifica si se pueden unir dos rutas
    def checking_merge(self, current_route, save_route, capacity_truck, capacity_trailer, pos_save):
        join = 0
        request_total = current_route.get_request_route() + save_route.get_request_route()

        if Problem.get_problem().get_type_problem() == ProblemType.TTRP:
            type_route_ini = None

            if pos_save:  # fin
                type_route_ini = current_route._type_route
            else:
                type_route_ini = save_route._type_route

            if type_route_ini == RouteType.PTR:
                if request_total > capacity_truck:
                    join = -1
            else:
                if type_route_ini == RouteType.PVR or type_route_ini == RouteType.CVR:
                    if request_total > (capacity_truck + capacity_trailer):
                        join = -1
        else:
            if request_total > capacity_truck:
                join = -1

        return join
