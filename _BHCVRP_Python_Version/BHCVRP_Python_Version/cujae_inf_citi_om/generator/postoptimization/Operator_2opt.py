from typing import List
import numpy as np
from postoptimization.StepOptimization import StepOptimization
from solution.Route import Route

class Operator_2opt(StepOptimization):
    def to_optimize(self, route: Route):
        list_opt = route.get_list_id_customers().copy()
        best_cost = route.get_cost_single_route()
        current_cost = 0.0

        for i in range(1, len(list_opt) - 1):
            for j in range(i + 1, len(list_opt)):
                if i < j:  
                    new_route = list_opt[:]
                    new_route[i:j] = reversed(new_route[i:j])
                    
                    new_cost = self.calculate_total_distance(new_route)
                    if new_cost < best_cost:
                        best_cost = new_cost
                        list_opt = new_route

        route.set_list_id_customers(list_opt)
        route.set_cost_route(best_cost)