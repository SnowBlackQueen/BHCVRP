from generator.heuristic import Heuristic
from data.ProblemType import ProblemType
from data.Problem import Problem
from data.Customer import Customer
from generator.solution.Route import Route
from data.CustomerType import CustomerType
from generator.solution.RouteTTRP import RouteTTRP
from generator.solution.RouteType import RouteType
from random import Random
from generator.solution.Solution import Solution
from exceptions.RLC_Exception import RLC_Exception

class NearestNeighborWithRLC(Heuristic):
    size_rlc = 3

    def __init__(self):
        super().__init__()

    def get_solution_inicial(self):
        if NearestNeighborWithRLC.size_rlc == 0:
            NearestNeighborWithRLC.size_rlc = 1
        elif NearestNeighborWithRLC.size_rlc > (Problem.get_problem().get_list_customers / 2):
            raise RLC_Exception("La lista de candidatos restringidos debe ser menor que la mitad del total de clientes")    

        solution = Solution()
        customers_to_visit = None
        id_depot = -1
        pos_depot = -1

        if Problem.get_problem().get_type_problem() == ProblemType.CVRP or Problem.get_problem().get_type_problem() == ProblemType.HFVRP or Problem.get_problem().get_type_problem() == ProblemType.OVRP or Problem.get_problem().get_type_problem() == ProblemType.TTRP:
            pos_depot = 0
            id_depot = Problem.get_problem().get_list_depots().get(pos_depot).get_id_depot()
            customers_to_visit = list(Problem.get_problem().get_list_customers())
        else:
            i = 0
            found = False

            while i < len(Problem.get_problem().get_list_depots()) and not found:
                if Problem.get_problem().get_list_depots().get(i).get_list_assigned_customers():
                    pos_depot = i
                    id_depot = Problem.get_problem().get_list_depots().get(pos_depot).get_id_depot()
                    customers_to_visit = list(Problem.get_problem().get_customers_assigned_by_id_depot(id_depot))

                    found = True
                else:
                    i += 1

        capacity_vehicle = Problem.get_problem().get_list_depots().get(pos_depot).get_list_fleets().get(0).get_capacity_vehicle()
        count_vehicles = Problem.get_problem().get_list_depots().get(pos_depot).get_list_fleets().get(0).get_count_vehicles()

        customer = Customer()
        route = Route()
        request_route = 0.0

        customer = self._get_NN_customer(customers_to_visit, id_depot)
        request_route = customer.get_request_customer()
        route.get_list_id_customers().append(customer.get_id_customer())
        customers_to_visit.remove(customer)

        if Problem.get_problem().get_type_problem() == 0 or Problem.get_problem().get_type_problem() == 3:
            while customers_to_visit and count_vehicles > 0:
                customer = self._get_NN_customer(customers_to_visit, customer.get_id_customer())

                if capacity_vehicle >= request_route + customer.get_request_customer():
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

            if route:
                route.set_request_route(request_route)
                route.set_id_depot(id_depot)
                solution.get_list_routes().append(route)

            if customers_to_visit:
                route = Route()
                request_route = 0.0

                while customers_to_visit:
                    j = 0
                    found = False
                    request_route = solution.get_list_routes().get(j).get_request_route()

                    while j < len(solution.get_list_routes()) and not found:
                        if capacity_vehicle >= request_route + customer.get_request_customer():
                            solution.get_list_routes().get(j).set_request_route(request_route + customer.get_request_customer())
                            solution.get_list_routes().get(j).get_list_id_customers().append(customer.get_id_customer())
                            customers_to_visit.remove(customer)

                            found = True
                        else:
                            j += 1
                            if j != len(solution.get_list_routes()):
                                request_route = solution.get_list_routes().get(j).get_request_route()

                    if not found:
                        route.get_list_id_customers().append(customer.get_id_customer())
                        route.set_request_route(route.get_request_route() + customer.get_request_customer())
                        customers_to_visit.remove(customer)

                    if customers_to_visit:
                        customer = self._get_NN_customer(customers_to_visit, customer.get_id_customer())

                if route.get_list_id_customers():
                    route.set_id_depot(id_depot)
                    solution.get_list_routes().append(route)

        elif Problem.get_problem().get_type_problem() == 1:
            list_capacities = list(Problem.get_problem().get_list_capacities())
            capacity_vehicle = list_capacities[0]
            is_open = True

            while customers_to_visit and list_capacities:
                customer = self._get_NN_customer(customers_to_visit, customer.get_id_customer())

                if capacity_vehicle >= request_route + customer.get_request_customer():
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
                    request_route = solution.get_list_routes().get(j).get_request_route()

                    while iterator_cap_vehicle and not found:
                        if next(iterator_cap_vehicle) >= request_route + customer.get_request_customer():
                            solution.get_list_routes().get(j).set_request_route(request_route + customer.get_request_customer())
                            solution.get_list_routes().get(j).get_list_id_customers().append(customer.get_id_customer())
                            customers_to_visit.remove(customer)

                            found = True
                        else:
                            j += 1
                            if j != len(solution.get_list_routes()):
                                request_route = solution.get_list_routes().get(j).get_request_route()

                    if not found:
                        route.get_list_id_customers().append(customer.get_id_customer())
                        route.set_request_route(route.get_request_route() + customer.get_request_customer())
                        customers_to_visit.remove(customer)

                    if customers_to_visit:
                        customer = self._get_NN_customer(customers_to_visit, customer.get_id_customer())

                if route.get_list_id_customers():
                    route.set_id_depot(id_depot)
                    solution.get_list_routes().append(route)

        elif Problem.get_problem().get_type_problem() == 2:
            for j in range(pos_depot, len(Problem.get_problem().get_list_depots())):
                if j != pos_depot:
                    id_depot = Problem.get_problem().get_list_depots().get(j).get_id_depot()
                    customers_to_visit = list(Problem.get_problem().get_customers_assigned_by_id_depot(id_depot))

                    capacity_vehicle = Problem.get_problem().get_list_depots().get(j).get_list_fleets().get(0).get_capacity_vehicle()
                    count_vehicles = Problem.get_problem().get_list_depots().get(j).get_list_fleets().get(0).get_count_vehicles()

                    if customers_to_visit:
                        route = Route()

                        customer = self._get_NN_customer(customers_to_visit, id_depot)
                        request_route = customer.get_request_customer()
                        route.get_list_id_customers().append(customer.get_id_customer())
                        customers_to_visit.remove(customer)
                    else:
                        continue

                while customers_to_visit and count_vehicles > 0:
                    customer = self._get_NN_customer(customers_to_visit, customer.get_id_customer())

                    if capacity_vehicle >= request_route + customer.get_request_customer():
                        route.get_list_id_customers().append(customer.get_id_customer())
                        request_route += customer.get_request_customer()
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

                if route:
                    route.set_request_route(request_route)
                    route.set_id_depot(id_depot)
                    solution.get_list_routes().append(route)

                if customers_to_visit:
                    route = Route()
                    request_route = 0.0

                    while customers_to_visit:
                        k = 0
                        found = False
                        request_route = solution.get_list_routes().get(k).get_request_route()

                        while k < len(solution.get_list_routes()) and not found:
                            if capacity_vehicle >= request_route + customer.get_request_customer():
                                solution.get_list_routes().get(k).set_request_route(request_route + customer.get_request_customer())
                                solution.get_list_routes().get(k).get_list_id_customers().append(customer.get_id_customer())
                                customers_to_visit.remove(customer)

                                found = True
                            else:
                                k += 1
                                if k != len(solution.get_list_routes()):
                                    request_route = solution.get_list_routes().get(k).get_request_route()

                        if not found:
                            route.get_list_id_customers().append(customer.get_id_customer())
                            route.set_request_route(route.get_request_route() + customer.get_request_customer())
                            customers_to_visit.remove(customer)

                        if customers_to_visit:
                            customer = self._get_NN_customer(customers_to_visit, customer.get_id_customer())

                    if route.get_list_id_customers():
                        route.set_id_depot(id_depot)
                        solution.get_list_routes().append(route)

        elif Problem.get_problem().get_type_problem() == 4:
            is_tc = False
            capacity_trailer = Problem.get_problem().get_list_depots().get(pos_depot).get_list_fleets().get(0).get_capcity_trailer()

            type_customer = customer.get_type_customer()

            list_access_vc = []

            while customers_to_visit:
                customer = self._get_NN_customer(customers_to_visit, customer.get_id_customer())

                if type_customer == CustomerType.TC:
                    if capacity_vehicle >= request_route + customer.get_request_customer():
                        request_route += customer.get_request_customer()
                        route.get_list_id_customers().append(customer.get_id_customer())
                        customers_to_visit.remove(customer)
                    else:
                        route.set_request_route(request_route)
                        route.set_id_depot(id_depot)
                        solution.get_list_routes().append(route)

                        route = Route()

                        request_route = customer.get_request_customer()
                        type_customer = customer.get_type_customer()
                        route.get_list_id_customers().append(customer.get_id_customer())
                        customers_to_visit.remove(customer)
                else:
                    if customer.get_type_customer() == CustomerType.TC:
                        is_tc = True

                    if capacity_vehicle + capacity_trailer >= request_route + customer.get_request_customer():
                        request_route += customer.get_request_customer()
                        route.get_list_id_customers().append(customer.get_id_customer())
                        customers_to_visit.remove(customer)
                    else:
                        route.set_request_route(request_route)

                        if is_tc:
                            route = RouteTTRP(route.get_list_id_customers(), route.get_request_route(), route.get_cost_route(), route.get_id_depot(), list_access_vc, RouteType.CVR)
                        else:
                            route = RouteTTRP(route.get_list_id_customers(), route.get_request_route(), route.get_cost_route(), route.get_id_depot(), list_access_vc, RouteType.PVR)

                        route.set_id_depot(id_depot)
                        solution.get_list_routes().append(route)
                        is_tc = False

                        route = Route()

                        request_route = customer.get_request_customer()
                        type_customer = customer.get_type_customer()
                        route.get_list_id_customers().append(customer.get_id_customer())
                        customers_to_visit.remove(customer)

            route.set_request_route(request_route)

            if type_customer == CustomerType.TC:
                route = RouteTTRP(route.get_list_id_customers(), route.get_request_route(), route.get_cost_route(), route.get_id_depot(), list_access_vc, RouteType.PTR)
            else:
                if is_tc:
                    route = RouteTTRP(route.get_list_id_customers(), route.get_request_route(), route.get_cost_route(), route.get_id_depot(), list_access_vc, RouteType.CVR)
                else:
                    route = RouteTTRP(route.get_list_id_customers(), route.get_request_route(), route.get_cost_route(), route.get_id_depot(), list_access_vc, RouteType.PVR)

            route.set_id_depot(id_depot)
            solution.get_list_routes().append(route)

        return solution

    # Método que devuelve el cliente más cercano al cliente referencia
    def _get_NN_customer(self, list_customers, reference):
        customer = Customer()
        RLC = -1

        if len(list_customers) == 1:
            customer = list_customers[0]
        else:
            list_nn = self._get_list_NN(list_customers, reference)
            list_rlc = []

            RLC = min(NearestNeighborWithRLC.size_rlc, len(list_customers))

            for i in range(RLC):
                list_rlc.append(list_nn[i])

            random = Random()
            index = random.randint(0, RLC - 1)
            customer = list_rlc.pop(index)

        return customer

    # Método que devuelve la lista de vecinos más cercanos
    def _get_list_NN(self, list_customers, reference):
        list_distances = []
        list_nn = []
        ref_distance = 0.0

        for i in range(len(list_customers)):
            ref_distance = Problem.get_problem().getCostMatrix().item(Problem.get_problem().getPosElement(reference), Problem.get_problem().getPosElement(list_customers[i].get_id_customer()))
            list_distances.append(ref_distance)
            list_nn.append(list_customers[i])

        self._ascendent_ordenate(list_distances, list_nn)

        return list_nn


