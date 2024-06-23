from heuristic.Heuristic import Heuristic
from data.Problem import Problem
from data.ProblemType import ProblemType
from solution.RouteType import RouteType
from solution.Solution import Solution
import numpy as np
from postoptimization.Operator_3opt import Operator_3opt
from random import Random


class SaveSequential(Heuristic):
    
    def __init__(self):
        super().__init__()

    # Método encargado de generar la solución
    def get_solution_inicial(self):
        if parameter_shape <= 0:
            parameter_shape = 1

        solution = Solution()
        customers_to_visit = None
        id_depot = -1
        pos_depot = -1

        if Problem.get_problem().getTypeProblem() == ProblemType.CVRP or Problem.get_problem().getTypeProblem() == ProblemType.HFVRP or Problem.get_problem().getTypeProblem() == ProblemType.OVRP or Problem.get_problem().getTypeProblem() == ProblemType.TTRP:
            customers_to_visit = list(Problem.get_problem().get_list_customers())
            pos_depot = 0
            id_depot = Problem.get_problem().get_listDepots()[pos_depot].get_id_depot()
        else:
            i = 0
            found = False

            while i < len(Problem.get_problem().get_list_depots()) and not found:
                customers_to_visit = Problem.get_problem().get_customers_assigned_by_id_depot(Problem.get_problem().get_list_depots()[i].get_id_depot())

                if customers_to_visit:
                    found = True
                    pos_depot = i
                    id_depot = Problem.get_problem().get_list_depots()[pos_depot].get_id_depot()
                else:
                    i += 1

        capacity_vehicle = Problem.get_problem().get_list_depots()[pos_depot].get_list_fleets()[0].get_capacity_vehicle()
        # countVehicles = Problem.get_problem().get_list_depots()[pos_depot].get_list_fleets()[0].getCountVehicles()

        three_opt = Operator_3opt()

        list_routes = []
        list_routes = self.create_initial_routes(customers_to_visit)
        # inspect ?

        cant_customers = len(customers_to_visit)

        save_matrix = np.zeros(cant_customers, cant_customers)

        save_matrix = self.fill_save_matrix(id_depot, customers_to_visit)

        random = Random()
        index = -1

        ext_inic = -1
        ext_end = -1
        no_extreme = -1
        exist_save = False
        
        type_problem = Problem.get_problem().get_type_problem()
        
        if type_problem in [0, 3]:
            while list_routes:
                index = random.randint(0, len(list_routes) - 1)
                current_route = list_routes.pop(index)
                exist_save = True

                ext_inic = current_route.get_get_list_id_customers()[0]
                ext_end = current_route.get_get_list_id_customers()[-1]

                while exist_save:
                    max_save_inic = None
                    max_save_end = None
                    max_save = None
                    position_save = False

                    max_save_inic = np.unravel_index(np.argmax(save_matrix), save_matrix.shape)
                    
                    if ext_inic != ext_end:
                        max_pos_end = np.unravel_index(np.argmax(save_matrix), save_matrix.shape)
                    else:
                        max_pos_end = max_save_inic

                    # Obtener los valores correspondientes a las posiciones máximas
                    max_value_inic = save_matrix[max_save_inic]
                    max_value_end = save_matrix[max_pos_end]

                    # Comparar los valores y asignar el máximo
                    if max_value_inic > max_value_end:
                        max_save = max_save_inic
                    else:
                        max_save = max_pos_end
                        position_save = True

                    if current_route.get_request_route() == capacity_vehicle:
                        # Llenar con infinito negativo para ext_inic
                        save_matrix[Problem.get_problem().get_pos_element(ext_inic), :] = np.NINF
                        save_matrix[:, Problem.get_problem().get_pos_element(ext_inic)] = np.NINF

                        # Llenar con infinito negativo para ext_end
                        save_matrix[Problem.get_problem().get_pos_element(ext_end), :] = np.NINF
                        save_matrix[:, Problem.get_problem().get_pos_element(ext_end)] = np.NINF

                        exist_save = False
                        continue

                    save_value = save_matrix[max_save, max_save]

                    if save_value == np.NINF:
                        exist_save = False
                        continue
                    else:
                        pos_route = self.get_position_route(list_routes, customers_to_visit.get(max_save).get_id_customer())
                        save_route = list_routes[pos_route]

                        is_factible = self.checking_merge(current_route, save_route, capacity_vehicle, 0.0, position_save)

                        if is_factible != -1:
                            if position_save:
                                current_route.get_get_list_id_customers().extend(save_route.get_get_list_id_customers())
                                ext_end = customers_to_visit.get(max_save).get_id_customer()
                            else:
                                current_route.get_get_list_id_customers().insert(0, save_route.get_get_list_id_customers())
                                ext_inic = customers_to_visit.get(max_save).get_id_customer()

                            current_route.set_id_depot(id_depot)
                            current_route.set_request_route((current_route.get_request_route() + save_route.get_request_route()))
                            list_routes.remove(save_route)

                            if len(current_route.get_get_list_id_customers()) > 2:
                                no_extreme = max_save
                                # Llenar con infinito negativo para no_extreme
                                save_matrix[no_extreme, :] = np.NINF
                                save_matrix[:, no_extreme] = np.NINF
                                
                                # Llenar con infinito negativo para ext_inic y ext_end
                                save_matrix[Problem.get_problem().get_pos_element(ext_inic), Problem.get_problem().get_pos_element(ext_end)] = np.NINF
                                save_matrix[Problem.get_problem().get_pos_element(ext_end), Problem.get_problem().get_pos_element(ext_inic)] = np.NINF
                                
                            # Asignar infinito negativo a max_save
                            save_matrix[max_save, max_save] = np.NINF
                            save_matrix[max_save, max_save] = np.NINF
                            
                    if len(current_route.get_get_list_id_customers()) >= 6:
                        three_opt.to_optimize(current_route)
                    
                    solution.get_list_routes().append(current_route)
                    
        elif type_problem == 1:
            list_capacities = list(Problem.get_problem().get_list_capacities())

            while (len(list_routes) > 0 and len(list_capacities) > 0):
                index = random.randint(0, len(list_routes) - 1)
                current_route = list_routes.pop(index)
                exist_save = True

                ext_inic = current_route.get_get_list_id_customers()[0]
                ext_end = current_route.get_get_list_id_customers()[-1]

                while exist_save:
                    max_save_inic = None
                    max_save_end = None
                    max_save = None
                    position_save = False

                    max_save_inic = np.unravel_index(np.argmax(save_matrix), save_matrix.shape)
                    
                    if ext_inic != ext_end:
                        max_save_inic = np.unravel_index(np.argmax(save_matrix), save_matrix.shape)
                    else:
                        max_save_end = max_save_inic

                    # Obtener los valores correspondientes a las posiciones máximas
                    max_value_inic = save_matrix[max_save_inic]
                    max_value_end = save_matrix[max_pos_end]

                    # Comparar los valores y asignar el máximo
                    if max_value_inic > max_value_end:
                        max_save = max_save_inic
                    else:
                        max_save = max_save_end
                        position_save = True

                    if current_route.get_request_route() == list_capacities[0]:  # capacity_vehicle
                        # Llenar con infinito negativo para ext_inic
                        save_matrix[Problem.get_problem().get_pos_element(ext_inic), :] = np.NINF
                        save_matrix[:, Problem.get_problem().get_pos_element(ext_inic)] = np.NINF

                        # Llenar con infinito negativo para ext_end
                        save_matrix[Problem.get_problem().get_pos_element(ext_end), :] = np.NINF
                        save_matrix[:, Problem.get_problem().get_pos_element(ext_end)] = np.NINF
                        
                        exist_save = False
                        continue

                    save_value = save_matrix[max_save, max_save]

                    if save_value == np.NINF:
                        exist_save = False
                        continue
                    else:
                        pos_route = self.get_position_route(list_routes, customers_to_visit[max_save].get_id_customer())
                        save_route = list_routes[pos_route]

                        is_factible = self.checking_merge(current_route, save_route, list_capacities[0], 0.0, position_save)

                        if is_factible != -1:
                            if position_save:
                                current_route.get_get_list_id_customers().extend(save_route.get_get_list_id_customers())
                                ext_end = customers_to_visit[max_save.get_col()].get_id_customer()
                            else:
                                current_route.get_get_list_id_customers().extend(0, save_route.get_get_list_id_customers())
                                ext_inic = customers_to_visit[max_save].get_id_customer()

                            current_route.set_id_depot(id_depot)
                            current_route.set_request_route(current_route.get_request_route() + save_route.get_request_route())
                            list_routes.remove(save_route)

                            if len(current_route.get_get_list_id_customers()) > 2:
                                no_extreme = max_save
                                save_matrix[no_extreme, :] = np.NINF
                                save_matrix[:, no_extreme] = np.NINF

                                save_matrix[Problem.get_problem().get_pos_element(ext_inic), Problem.get_problem().get_pos_element(ext_end)] = np.NINF
                                save_matrix[Problem.get_problem().get_pos_element(ext_end), Problem.get_problem().get_pos_element(ext_inic)] = np.NINF
                                
                            # Asignar infinito negativo a max_save
                            save_matrix[max_save, max_save] = np.NINF
                            save_matrix[max_save, max_save] = np.NINF
                            
                    if len(current_route.get_get_list_id_customers()) >= 6:
                        three_opt.to_optimize(current_route)

                    solution.get_list_routes().append(current_route)
                    list_capacities.pop(0)  
                    
        elif type_problem == 2:
            for j in range(pos_depot, len(Problem.get_problem().get_list_depots())):
                if j != pos_depot:
                    id_depot = Problem.get_problem().get_list_depots().get(j).get_id_depot()
                    customers_to_visit = Problem.get_problem().get_customers_assigned_by_id_depot(id_depot)

                    capacity_vehicle = Problem.get_problem().get_list_depots().get(j).get_list_fleets().get(0).get_capacity_vehicle()

                    if customers_to_visit:
                        list_routes = self.create_initial_routes(customers_to_visit)
                        cant_customers = len(customers_to_visit)
                        save_matrix = np.zeros(cant_customers, cant_customers)
                        save_matrix = self.fill_save_matrix(id_depot, customers_to_visit)

                while list_routes:
                    index = random.randint(0, len(list_routes) - 1)
                    current_route = list_routes.pop(index)
                    exist_save = True

                    ext_inic = current_route.get_get_list_id_customers()[0]
                    ext_end = current_route.get_get_list_id_customers()[len(current_route.get_get_list_id_customers()) - 1]

                    while exist_save:
                        max_save_inic = None
                        max_save_end = None
                        max_save = None
                        position_save = False

                        max_save_inic = np.unravel_index(np.argmax(save_matrix), save_matrix.shape)
                    
                        if ext_inic != ext_end:
                            max_save_inic = np.unravel_index(np.argmax(save_matrix), save_matrix.shape)
                        else:
                            max_save_end = max_save_inic

                        # Obtener los valores correspondientes a las posiciones máximas
                        max_value_inic = save_matrix[max_save_inic]
                        max_value_end = save_matrix[max_pos_end]

                        # Comparar los valores y asignar el máximo
                        if max_value_inic > max_value_end:
                            max_save = max_save_inic
                        else:
                            max_save = max_save_end
                            position_save = True

                        if current_route.get_request_route() == capacity_vehicle:
                            # Llenar con infinito negativo para ext_inic
                            save_matrix[Problem.get_problem().get_pos_element(ext_inic), :] = np.NINF
                            save_matrix[:, Problem.get_problem().get_pos_element(ext_inic)] = np.NINF

                            # Llenar con infinito negativo para ext_end
                            save_matrix[Problem.get_problem().get_pos_element(ext_end), :] = np.NINF
                            save_matrix[:, Problem.get_problem().get_pos_element(ext_end)] = np.NINF
                            
                            exist_save = False
                            continue

                        save_value = save_matrix[max_save, max_save]

                        if save_value == np.NINF:
                            exist_save = False
                            continue
                        else:
                            pos_route = self.get_position_route(list_routes, customers_to_visit.get(max_save).get_id_customer())
                            save_route = list_routes[pos_route]

                            is_factible = self.checking_merge(current_route, save_route, capacity_vehicle, 0.0, position_save)
                            
                            if is_factible != -1:
                                if position_save:
                                    current_route.get_get_list_id_customers().extend(save_route.get_get_list_id_customers())
                                    ext_end = customers_to_visit.get(max_save).get_id_customer()
                                else:
                                    current_route.get_get_list_id_customers().insert(0, save_route.get_get_list_id_customers())
                                    ext_inic = customers_to_visit.get(max_save).get_id_customer()

                                current_route.set_id_depot(id_depot)
                                current_route.set_request_route((current_route.get_request_route() + save_route.get_request_route()))
                                list_routes.remove(save_route)

                                if len(current_route.get_get_list_id_customers()) > 2:
                                    no_extreme = max_save
                                    save_matrix[no_extreme, :] = np.NINF
                                    save_matrix[:, no_extreme] = np.NINF

                                    save_matrix[Problem.get_problem().get_pos_element(ext_inic), Problem.get_problem().get_pos_element(ext_end)] = np.NINF
                                    save_matrix[Problem.get_problem().get_pos_element(ext_end), Problem.get_problem().get_pos_element(ext_inic)] = np.NINF
                                    
                                # Asignar infinito negativo a max_save
                                save_matrix[max_save, max_save] = np.NINF
                                save_matrix[max_save, max_save] = np.NINF

                            if len(current_route.get_get_list_id_customers()) >= 6:
                                three_opt.to_optimize(current_route)

                            solution.get_list_routes().append(current_route)
                            
        elif type_problem == 4:
            capacity_trailer = Problem.get_problem().get_list_depots().get(pos_depot).get_list_fleets().get(0).get_capacity_trailer()

            while list_routes:
                index = random.randint(len(list_routes))
                current_route = list_routes.remove(index)

                exist_save = True

                ext_inic = current_route.get_get_list_id_customers().get(0)
                ext_end = current_route.get_get_list_id_customers().get(len(current_route.get_get_list_id_customers()) - 1)

                while exist_save:
                    max_save_inic = None
                    max_save_end = None
                    max_save = None
                    position_save = False

                    max_save_inic = np.unravel_index(np.argmax(save_matrix), save_matrix.shape)
                    
                    if ext_inic != ext_end:
                        max_save_inic = np.unravel_index(np.argmax(save_matrix), save_matrix.shape)
                    else:
                        max_save_end = max_save_inic

                    # Obtener los valores correspondientes a las posiciones máximas
                    max_value_inic = save_matrix[max_save_inic]
                    max_value_end = save_matrix[max_pos_end]

                    # Comparar los valores y asignar el máximo
                    if max_value_inic > max_value_end:
                        max_save = max_save_inic
                    else:
                        max_save = max_save_end
                        position_save = True

                    if ((current_route).get_type_route() == 0 and (current_route).getRequestRoute() == capacity_vehicle) or (((current_route).get_type_route() == 1 or (current_route).get_type_route() == 2) and (current_route).getRequestRoute() == (capacity_vehicle + capacity_trailer)):
                        # Llenar con infinito negativo para ext_inic
                            save_matrix[Problem.get_problem().get_pos_element(ext_inic), :] = np.NINF
                            save_matrix[:, Problem.get_problem().get_pos_element(ext_inic)] = np.NINF

                            # Llenar con infinito negativo para ext_end
                            save_matrix[Problem.get_problem().get_pos_element(ext_end), :] = np.NINF
                            save_matrix[:, Problem.get_problem().get_pos_element(ext_end)] = np.NINF
                            
                            exist_save = False
                            continue

                    save_value = save_matrix[max_save, max_save]

                    if save_value == np.Infinity:
                        exist_save = False
                        continue
                    else:
                        pos_route = self.get_position_route(list_routes, customers_to_visit.get(max_save).get_id_customer())
                        save_route = list_routes.get(pos_route)

                        is_factible = self.checking_merge(current_route, save_route, capacity_vehicle, capacity_trailer, position_save)

                        if is_factible != -1:
                            type_route = None

                            if position_save:
                                current_route.get_get_list_id_customers().addAll(save_route.get_get_list_id_customers())
                                ext_end = customers_to_visit.get(max_save).get_id_customer()

                                if (current_route).get_type_route().equals((save_route).get_type_route()):
                                    type_route = (current_route).get_type_route()
                                else:
                                    if not (current_route).get_type_route().equals(RouteType.PTR):
                                        type_route = RouteType.CVR
                                    else:
                                        type_route = (current_route).get_type_route()
                            else:
                                current_route.get_list_id_customers().extend(save_route.get_list_id_customers())
                                ext_inic = customers_to_visit.get(max_save).get_id_customer()

                                if save_route.get_type_route() == current_route.get_type_route():
                                    type_route = save_route.get_type_route()
                                else:
                                    if save_route.get_type_route() > 0:
                                        type_route = RouteType.CVR
                                    else:
                                        type_route = save_route.get_type_route()

                                current_route.set_type_route(type_route)
                                current_route.set_id_depot(id_depot)
                                current_route.set_request_route((current_route.get_request_route() + save_route.get_request_route()))
                                list_routes.remove(save_route)

                                if len(current_route.get_list_id_customers()) > 2:
                                    noExtreme = max_save.row
                                    save_matrix[no_extreme, :] = np.NINF
                                    save_matrix[:, no_extreme] = np.NINF

                                    save_matrix[Problem.get_problem().get_pos_element(ext_inic), Problem.get_problem().get_pos_element(ext_end)] = np.NINF
                                    save_matrix[Problem.get_problem().get_pos_element(ext_end), Problem.get_problem().get_pos_element(ext_inic)] = np.NINF
                                    
                            # Asignar infinito negativo a max_save
                            save_matrix[max_save, max_save] = np.NINF
                            save_matrix[max_save, max_save] = np.NINF

                        # if len(currentRoute.list_id_customer) >= 6:
                        #     stepOptimization.stepOptimization(currentRoute)

                        solution.get_list_routes().append(current_route)
            
        return solution
    
    # Método que verifica si se pueden unir dos rutas
    def checking_merge(current_route, save_route, capacity_truck, capacity_trailer, pos_save):
        join = 0
        request_total = current_route.get_request_route() + save_route.get_request_route()
        
        if Problem.get_problem().get_type_problem() == ProblemType.TTRP:
            type_route_ini = None
            
            if pos_save: # fin
                type_route_ini = current_route.get_type_route()
            else:
                type_route_ini = save_route.get_type_route()
            
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