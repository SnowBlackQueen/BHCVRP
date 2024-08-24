from data.CustomerType import CustomerType
from data.Problem import Problem
from generator.solution.Route import Route
from generator.solution.RouteType import RouteType
from typing import List, Tuple
from exceptions.CostException import CostException

class RouteTTRP(Route):
    def __init__(self, type_route=None, list_id_customers=None, request_route=None, cost_route=None, id_depot=None, list_access_vc=None, maximum_distance=None):
        super().__init__(list_id_customers, request_route, cost_route, id_depot, list_access_vc, maximum_distance)
        self._type_route = type_route
        self.list_access_vc = list_access_vc if list_access_vc else []
        
    def __init__(self, type_route=None, list_id_customers=None, request_route=None, cost_route=None, id_depot=None, list_access_vc=None, maximum_distance=None):
        if list_id_customers is not None and request_route is not None and cost_route is not None and id_depot is not None and list_access_vc is not None and type_route is not None:
            super().__init__(list_id_customers, request_route, cost_route, id_depot, list_access_vc, maximum_distance)
            self._type_route = type_route
            self.list_access_vc = list_access_vc 
            self.list_id_customers = list_id_customers 
            self.request_route = request_route
            self.cost_route = 0.0
            self.id_depot = id_depot
            self.list_access_vc = []
            self.maximum_distance = maximum_distance
        else:
            self.list_id_customers = []
            self.request_route = 0.0
            self.cost_route = 0.0
            self.id_depot = -1
            self.maximum_distance = 0.0
            self.list_access_vc = []
            self._type_route = 0

    @property
    def get_type_route(self):
        return self._type_route

    def set_type_route(self, value):
        if value == 0:
            self._type_route = RouteType.PTR
        elif value == 1:
            self._type_route = RouteType.PVR
        elif value == 2:
            self._type_route = RouteType.CVR
        else:
            raise ValueError("Invalid route type")

    @property
    def get_list_access_vc(self):
        return self._list_access_vc

    def set_list_access_vc(self, value):
        self._list_access_vc = value
        
    def get_cost_route_with_sub_tour(self, list_id_customers: List[int]) -> float:
        cost_route = 0.0
        request_sub_route = 0.0
        customer_ini = 0
        customer_next = None
        type_customer_ini = None
        type_customer_next = None
        id_last_vc = -1
        vc_in_sub = False

        pos_customer_ini = -1
        pos_customer_next = -1
        pos_customer_last_vc = 0

        capacity_vehicle = Problem.get_problem().get_list_depots()[0].get_list_fleets()[0].get_capacity_vehicle()

        customer_ini = list_id_customers[0]
        pos_customer_ini = Problem.get_problem().get_pos_element(customer_ini)
        type_customer_ini = Problem.get_problem().get_type_by_id_customer(customer_ini)
        list_access_vc = [0]

        # cost_route += Problem.getProblem().getCostMatrix().getItem(Problem.getProblem().getPosElement(0), pos_customer_ini)

        for i in range(1, len(list_id_customers)):
            customer_next = list_id_customers[i]
            pos_customer_next = Problem.get_problem().get_pos_element(customer_next)
            type_customer_next = Problem.get_problem().get_type_by_id_customer(customer_next)

            if type_customer_ini == CustomerType.VC and type_customer_next == CustomerType.VC and not vc_in_sub:
               # cost_route += Problem.getProblem().getCostMatrix().getItem(pos_customer_ini, pos_customer_next)
                list_access_vc.append(0)
            else:
                if type_customer_ini == CustomerType.VC and type_customer_next == CustomerType.TC and not vc_in_sub:
                    id_last_vc = customer_ini
                    pos_customer_last_vc = pos_customer_ini
                    # cost_route += Problem.getProblem().getCostMatrix().getItem(pos_customer_ini, pos_customer_next)
                    request_sub_route += Problem.get_problem().get_request_by_id_customer(customer_next)
                else:
                    if (type_customer_ini == CustomerType.TC and type_customer_next == CustomerType.TC) or (type_customer_ini == CustomerType.VC and type_customer_next == CustomerType.TC and vc_in_sub):
                        request_sub_route += Problem.get_problem().get_request_by_id_customer(customer_next)
                        if request_sub_route <= capacity_vehicle:
                            # Pendiente
                            cost_route += Problem.getProblem().getCostMatrix().getItem(pos_customer_ini, pos_customer_next)
                        else:
                            request_sub_route = Problem.get_problem().get_request_by_id_customer(customer_next)
                            # cost_route += Problem.getProblem().getCostMatrix().getItem(pos_customer_ini, pos_customer_last_vc)
                            # cost_route += Problem.getProblem().getCostMatrix().getItem(pos_customer_last_vc, pos_customer_next)
                            vc_in_sub = False
                    else:
                        if (type_customer_ini == CustomerType.TC and type_customer_next == CustomerType.VC) or (type_customer_ini == CustomerType.VC and type_customer_next == CustomerType.VC and vc_in_sub):
                            request_sub_route += Problem.get_problem().get_request_by_id_customer(customer_next)
                            if request_sub_route <= capacity_vehicle:
                                # cost_route += Problem.getProblem().getCostMatrix().getItem(pos_customer_ini, pos_customer_next)
                                vc_in_sub = True
                                list_access_vc.append(1)
                            else:
                                request_sub_route = 0.0
                                # cost_route += Problem.getProblem().getCostMatrix().getItem(pos_customer_ini, pos_customer_last_vc)
                                # cost_route += Problem.getProblem().getCostMatrix().getItem(pos_customer_last_vc, pos_customer_next)
                                id_last_vc = -1
                                vc_in_sub = False
                                list_access_vc.append(0)

            customer_ini = customer_next
            pos_customer_ini = pos_customer_next
            type_customer_ini = type_customer_next
            
            if id_last_vc != -1:
                # costRoute += Problem.getProblem().getCostMatrix().getItem(posCustomerIni, posCustomerLastVC)
                customer_ini = id_last_vc
                pos_customer_ini = pos_customer_last_vc
                id_last_vc = -1

            # costRoute += Problem.getProblem().getCostMatrix().getItem(posCustomerIni, Problem.getProblem().getPosElement(idDepot))
            # set_cost_route(cost_route)


        if cost_route > 0:
            return cost_route
        else:
            raise CostException("El costo de la ruta debe ser mayor que cero")

