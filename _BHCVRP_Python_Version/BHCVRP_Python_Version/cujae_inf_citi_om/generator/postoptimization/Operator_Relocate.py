from typing import List
from postoptimization.StepOptimization import StepOptimization
from solution.Route import Route

class Operator_Relocate(StepOptimization):
    def to_optimize(self, route: Route):
        list_opt = route.get_list_id_customers().copy()
        best_cost = route.get_cost_single_route()
        current_cost = 0.0

        for i in range(len(list_opt)):
            for j in range(i + 1, len(list_opt)):
                # Intentamos mover el cliente en la posición i a todas las demás posiciones
                new_route = list_opt[:]
                new_route[i], new_route[j] = new_route[j], new_route[i]

                new_cost = self.calculate_total_distance(new_route)
                if new_cost < best_cost:
                    best_cost = new_cost
                    list_opt = new_route

        route.set_list_id_customers(list_opt)
        route.set_cost_route(best_cost)