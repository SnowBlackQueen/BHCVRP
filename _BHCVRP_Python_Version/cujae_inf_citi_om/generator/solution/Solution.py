from cujae_inf_citi_om.data import Problem, ProblemType
from generator.solution import RouteType

class Solution:
    def __init__(self, list_routes=None):
        self._list_routes = list_routes if list_routes else []

    def get_list_routes(self):
        return self._list_routes

    def set_list_routes(self, list_routes):
        self._list_routes = list_routes

    def calculate_cost(self):
        total_cost = 0.0

        for route in self._list_routes:
            if not Problem.get_problem().get_type_problem() == ProblemType.TTRP or (Problem.get_problem().get_type_problem() == ProblemType.TTRP and (isinstance(route, RouteType.PTR) or isinstance(route, RouteType.PVR))):
                total_cost += route.get_cost_single_route()
            else:
                total_cost = route.get_cost_route_with_sub_tour()

        return total_cost

    def get_cost_solution(self):
        cost_solution = 0.0

        for route in self._list_routes:
            cost_solution += route.get_cost_route()

        return cost_solution