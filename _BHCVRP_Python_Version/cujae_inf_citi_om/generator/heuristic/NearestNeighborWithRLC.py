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

        if Problem.getProblem().getTypeProblem() == ProblemType.CVRP or Problem.getProblem().getTypeProblem() == ProblemType.HFVRP or Problem.getProblem().getTypeProblem() == ProblemType.OVRP or Problem.getProblem().getTypeProblem() == ProblemType.TTRP:
            pos_depot = 0
            id_depot = Problem.getProblem().getListDepots().get(pos_depot).getIdDepot()
            customers_to_visit = list(Problem.getProblem().getListCustomers())
        else:
            i = 0
            found = False

            while i < len(Problem.getProblem().getListDepots()) and not found:
                if not Problem.getProblem().getListDepots().get(i).getListAssignedCustomers():
                    pos_depot = i
                    id_depot = Problem.getProblem().getListDepots().get(pos_depot).getIdDepot()
                    customers_to_visit = list(Problem.getProblem().getCustomersAssignedByIDDepot(id_depot))

                    found = True
                else:
                    i += 1

        capacity_vehicle = Problem.getProblem().getListDepots().get(pos_depot).getListFleets().get(0).getCapacityVehicle()
        count_vehicles = Problem.getProblem().getListDepots().get(pos_depot).getListFleets().get(0).getCountVehicles()

        customer = Customer()
        route = Route()
        request_route = 0.0

        customer = self.get_NN_customer(customers_to_visit, id_depot)
        request_route = customer.getRequestCustomer()
        route.getListIdCustomers().append(customer.getIdCustomer())
        customers_to_visit.remove(customer)

        if Problem.getProblem().getTypeProblem().ordinal() == 0 or Problem.getProblem().getTypeProblem().ordinal() == 3:
            while customers_to_visit and count_vehicles > 0:
                customer = self.get_NN_customer(customers_to_visit, customer.getIdCustomer())

                if capacity_vehicle >= request_route + customer.getRequestCustomer():
                    request_route += customer.getRequestCustomer()
                    route.getListIdCustomers().append(customer.getIdCustomer())
                    customers_to_visit.remove(customer)
                else:
                    route.setRequestRoute(request_route)
                    route.setIdDepot(id_depot)
                    solution.getListRoutes().append(route)

                    route = None
                    count_vehicles -= 1

                    if count_vehicles > 0:
                        route = Route()

                        request_route = customer.getRequestCustomer()
                        route.getListIdCustomers().append(customer.getIdCustomer())
                        customers_to_visit.remove(customer)

            if route:
                route.setRequestRoute(request_route)
                route.setIdDepot(id_depot)
                solution.getListRoutes().append(route)

            if customers_to_visit:
                route = Route()
                request_route = 0.0

                while customers_to_visit:
                    j = 0
                    found = False
                    request_route = solution.getListRoutes().get(j).getRequestRoute()

                    while j < len(solution.getListRoutes()) and not found:
                        if capacity_vehicle >= request_route + customer.getRequestCustomer():
                            solution.getListRoutes().get(j).setRequestRoute(request_route + customer.getRequestCustomer())
                            solution.getListRoutes().get(j).getListIdCustomers().append(customer.getIdCustomer())
                            customers_to_visit.remove(customer)

                            found = True
                        else:
                            j += 1
                            if j != len(solution.getListRoutes()):
                                request_route = solution.getListRoutes().get(j).getRequestRoute()

                    if not found:
                        route.getListIdCustomers().append(customer.getIdCustomer())
                        route.setRequestRoute(route.getRequestRoute() + customer.getRequestCustomer())
                        customers_to_visit.remove(customer)

                    if customers_to_visit:
                        customer = self.get_NN_customer(customers_to_visit, customer.getIdCustomer())

                if route.getListIdCustomers():
                    route.setIdDepot(id_depot)
                    solution.getListRoutes().append(route)

        elif Problem.getProblem().getTypeProblem().ordinal() == 1:
            list_capacities = list(Problem.getProblem().getListCapacities())
            capacity_vehicle = list_capacities[0]
            is_open = True

            while customers_to_visit and list_capacities:
                customer = self.get_NN_customer(customers_to_visit, customer.getIdCustomer())

                if capacity_vehicle >= request_route + customer.getRequestCustomer():
                    request_route += customer.getRequestCustomer()
                    route.getListIdCustomers().append(customer.getIdCustomer())
                    customers_to_visit.remove(customer)
                else:
                    route.setRequestRoute(request_route)
                    route.setIdDepot(id_depot)
                    solution.getListRoutes().append(route)

                    is_open = False
                    list_capacities.pop(0)

                    if list_capacities:
                        route = Route()

                        request_route = customer.getRequestCustomer()
                        route.getListIdCustomers().append(customer.getIdCustomer())
                        customers_to_visit.remove(customer)

                        is_open = True
                        capacity_vehicle = list_capacities[0]

            if is_open:
                route.setRequestRoute(request_route)
                route.setIdDepot(id_depot)
                solution.getListRoutes().append(route)

            if customers_to_visit:
                route = Route()
                request_route = 0.0

                list_capacities = list(Problem.getProblem().getListCapacities())
                iterator_cap_vehicle = iter(list_capacities)

                while customers_to_visit:
                    j = 0
                    found = False
                    request_route = solution.getListRoutes().get(j).getRequestRoute()

                    while iterator_cap_vehicle and not found:
                        if next(iterator_cap_vehicle) >= request_route + customer.getRequestCustomer():
                            solution.getListRoutes().get(j).setRequestRoute(request_route + customer.getRequestCustomer())
                            solution.getListRoutes().get(j).getListIdCustomers().append(customer.getIdCustomer())
                            customers_to_visit.remove(customer)

                            found = True
                        else:
                            j += 1
                            if j != len(solution.getListRoutes()):
                                request_route = solution.getListRoutes().get(j).getRequestRoute()

                    if not found:
                        route.getListIdCustomers().append(customer.getIdCustomer())
                        route.setRequestRoute(route.getRequestRoute() + customer.getRequestCustomer())
                        customers_to_visit.remove(customer)

                    if customers_to_visit:
                        customer = self.get_NN_customer(customers_to_visit, customer.getIdCustomer())

                if route.getListIdCustomers():
                    route.setIdDepot(id_depot)
                    solution.getListRoutes().append(route)

        elif Problem.getProblem().getTypeProblem().ordinal() == 2:
            for j in range(pos_depot, len(Problem.getProblem().getListDepots())):
                if j != pos_depot:
                    id_depot = Problem.getProblem().getListDepots().get(j).getIdDepot()
                    customers_to_visit = list(Problem.getProblem().getCustomersAssignedByIDDepot(id_depot))

                    capacity_vehicle = Problem.getProblem().getListDepots().get(j).getListFleets().get(0).getCapacityVehicle()
                    count_vehicles = Problem.getProblem().getListDepots().get(j).getListFleets().get(0).getCountVehicles()

                    if customers_to_visit:
                        route = Route()

                        customer = self.get_NN_customer(customers_to_visit, id_depot)
                        request_route = customer.getRequestCustomer()
                        route.getListIdCustomers().append(customer.getIdCustomer())
                        customers_to_visit.remove(customer)
                    else:
                        continue

                while customers_to_visit and count_vehicles > 0:
                    customer = self.get_NN_customer(customers_to_visit, customer.getIdCustomer())

                    if capacity_vehicle >= request_route + customer.getRequestCustomer():
                        route.getListIdCustomers().append(customer.getIdCustomer())
                        request_route += customer.getRequestCustomer()
                        customers_to_visit.remove(customer)
                    else:
                        route.setRequestRoute(request_route)
                        route.setIdDepot(id_depot)
                        solution.getListRoutes().append(route)

                        route = None
                        count_vehicles -= 1

                        if count_vehicles > 0:
                            route = Route()

                            request_route = customer.getRequestCustomer()
                            route.getListIdCustomers().append(customer.getIdCustomer())
                            customers_to_visit.remove(customer)

                if route:
                    route.setRequestRoute(request_route)
                    route.setIdDepot(id_depot)
                    solution.getListRoutes().append(route)

                if customers_to_visit:
                    route = Route()
                    request_route = 0.0

                    while customers_to_visit:
                        k = 0
                        found = False
                        request_route = solution.getListRoutes().get(k).getRequestRoute()

                        while k < len(solution.getListRoutes()) and not found:
                            if capacity_vehicle >= request_route + customer.getRequestCustomer():
                                solution.getListRoutes().get(k).setRequestRoute(request_route + customer.getRequestCustomer())
                                solution.getListRoutes().get(k).getListIdCustomers().append(customer.getIdCustomer())
                                customers_to_visit.remove(customer)

                                found = True
                            else:
                                k += 1
                                if k != len(solution.getListRoutes()):
                                    request_route = solution.getListRoutes().get(k).getRequestRoute()

                        if not found:
                            route.getListIdCustomers().append(customer.getIdCustomer())
                            route.setRequestRoute(route.getRequestRoute() + customer.getRequestCustomer())
                            customers_to_visit.remove(customer)

                        if customers_to_visit:
                            customer = self.get_NN_customer(customers_to_visit, customer.getIdCustomer())

                    if route.getListIdCustomers():
                        route.setIdDepot(id_depot)
                        solution.getListRoutes().append(route)

        elif Problem.getProblem().getTypeProblem().ordinal() == 4:
            is_tc = False
            capacity_trailer = Problem.getProblem().getListDepots().get(pos_depot).getListFleets().get(0).getCapacityTrailer()

            type_customer = customer.getTypeCustomer()

            list_access_vc = []

            while customers_to_visit:
                customer = self.get_NN_customer(customers_to_visit, customer.getIdCustomer())

                if type_customer == CustomerType.TC:
                    if capacity_vehicle >= request_route + customer.getRequestCustomer():
                        request_route += customer.getRequestCustomer()
                        route.getListIdCustomers().append(customer.getIdCustomer())
                        customers_to_visit.remove(customer)
                    else:
                        route.setRequestRoute(request_route)
                        route.setIdDepot(id_depot)
                        solution.getListRoutes().append(route)

                        route = Route()

                        request_route = customer.getRequestCustomer()
                        type_customer = customer.getTypeCustomer()
                        route.getListIdCustomers().append(customer.getIdCustomer())
                        customers_to_visit.remove(customer)
                else:
                    if customer.getTypeCustomer() == CustomerType.TC:
                        is_tc = True

                    if capacity_vehicle + capacity_trailer >= request_route + customer.getRequestCustomer():
                        request_route += customer.getRequestCustomer()
                        route.getListIdCustomers().append(customer.getIdCustomer())
                        customers_to_visit.remove(customer)
                    else:
                        route.setRequestRoute(request_route)

                        if is_tc:
                            route = RouteTTRP(route.getListIdCustomers(), route.getRequestRoute(), route.getCostRoute(), route.getIdDepot(), list_access_vc, RouteType.CVR)
                        else:
                            route = RouteTTRP(route.getListIdCustomers(), route.getRequestRoute(), route.getCostRoute(), route.getIdDepot(), list_access_vc, RouteType.PVR)

                        route.setIdDepot(id_depot)
                        solution.getListRoutes().append(route)
                        is_tc = False

                        route = Route()

                        request_route = customer.getRequestCustomer()
                        type_customer = customer.getTypeCustomer()
                        route.getListIdCustomers().append(customer.getIdCustomer())
                        customers_to_visit.remove(customer)

            route.setRequestRoute(request_route)

            if type_customer == CustomerType.TC:
                route = RouteTTRP(route.getListIdCustomers(), route.getRequestRoute(), route.getCostRoute(), route.getIdDepot(), list_access_vc, RouteType.PTR)
            else:
                if is_tc:
                    route = RouteTTRP(route.getListIdCustomers(), route.getRequestRoute(), route.getCostRoute(), route.getIdDepot(), list_access_vc, RouteType.CVR)
                else:
                    route = RouteTTRP(route.getListIdCustomers(), route.getRequestRoute(), route.getCostRoute(), route.getIdDepot(), list_access_vc, RouteType.PVR)

            route.setIdDepot(id_depot)
            solution.getListRoutes().append(route)

        return solution

    def get_NN_customer(self, listCustomers, reference):
        customer = Customer()
        RLC = -1

        if len(listCustomers) == 1:
            customer = listCustomers[0]
        else:
            list_nn = self.get_list_NN(listCustomers, reference)
            list_rlc = []

            RLC = min(NearestNeighborWithRLC.size_rlc, len(listCustomers))

            for i in range(RLC):
                list_rlc.append(list_nn[i])

            random = Random()
            index = random.randint(0, RLC - 1)
            customer = list_rlc.pop(index)

        return customer

    def get_list_NN(self, listCustomers, reference):
        list_distances = []
        list_nn = []
        ref_distance = 0.0

        for i in range(len(listCustomers)):
            ref_distance = Problem.getProblem().getCostMatrix().item(Problem.getProblem().getPosElement(reference), Problem.getProblem().getPosElement(listCustomers[i].getIdCustomer()))
            list_distances.append(ref_distance)
            list_nn.append(listCustomers[i])

        self.ascendent_ordenate(list_distances, list_nn)

        return list_nn


