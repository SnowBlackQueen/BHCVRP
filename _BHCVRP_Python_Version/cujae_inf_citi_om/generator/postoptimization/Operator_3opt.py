import random
from generator.postoptimization.StepOptimization import StepOptimization
from generator.solution.Route import Route

class Operator_3opt(StepOptimization):

    def to_optimize(self, route: Route):
        list_opt = route.get_list_id_customers().copy()
        list_aux = route.get_list_id_customers().copy()
        list_key = []

        best_cost = route.get_cost_single_route()
        current_cost = 0.0

        key_first = random.randint(0, len(route.get_list_id_customers()) - 1)
        key_second = random.randint(0, len(route.get_list_id_customers()) - 1)
        key_third = random.randint(0, len(route.get_list_id_customers()) - 1)

        if len(route.get_list_id_customers()) > 5:
            while (key_first == key_second or key_first == key_third or key_second == key_third or
                   abs(key_first - key_second) <= 1 or abs(key_first - key_third) <= 1 or abs(key_second - key_third) <= 1 or
                   (key_first == len(route.get_list_id_customers()) - 1 and (key_second == 0 or key_third == 0)) or
                   (key_second == len(route.get_list_id_customers()) - 1 and (key_first == 0 or key_third == 0)) or
                   (key_third == len(route.get_list_id_customers()) - 1 and (key_second == 0 or key_first == 0))):
                key_first = random.randint(0, len(route.get_list_id_customers()) - 1)
                key_second = random.randint(0, len(route.get_list_id_customers()) - 1)
                key_third = random.randint(0, len(route.get_list_id_customers()) - 1)

        if min(key_first, key_second) == key_first and min(key_first, key_third) == key_first:
            list_key.append(key_first)
            list_key.append(min(key_second, key_third))
            list_key.append(max(key_second, key_third))

        if min(key_second, key_first) == key_second and min(key_second, key_third) == key_second:
            list_key.append(key_second)
            list_key.append(min(key_first, key_third))
            list_key.append(max(key_first, key_third))

        if min(key_third, key_first) == key_third and min(key_third, key_second) == key_third:
            list_key.append(key_third)
            list_key.append(min(key_first, key_second))
            list_key.append(max(key_first, key_second))

        moves = 0
        #duplicate = False

        while moves < 7 :
            list_candidates = list_aux.copy()
            id_vistos = []

            if moves == 0:
                self.invert(list_candidates, list_key[1], list_key[2])
                route.set_list_id_customers(list_candidates)
                list_key.append(list_key.pop(0))

            elif moves == 1:
                self.invert(list_candidates, list_key[1], list_key[2])
                list_key.append(list_key.pop(0))
                route.set_list_id_customers(list_candidates)

            elif moves == 2:
                self.invert(list_candidates, list_key[1], list_key[2])
                list_key.append(list_key.pop(0))
                route.set_list_id_customers(list_candidates)

            elif moves == 3:
                self.invert(list_candidates, list_key[0], list_key[1])
                self.invert(list_candidates, list_key[1], list_key[2])
                route.set_list_id_customers(list_candidates)

            elif moves == 4:
                cad_one = list_candidates[list_key[0] + 1:list_key[1] + 1]
                cad_two = list_candidates[list_key[1] + 1:list_key[2] + 1]
                pos_insert_one = list_key[0] + 1
                pos_insert_two = list_key[0] + len(cad_two) + 1
                list_candidates = self.swap(list_candidates, cad_one, cad_two, pos_insert_one, pos_insert_two)
                route.set_list_id_customers(list_candidates)

            elif moves == 5:
                cad_one = list_candidates[list_key[0] + 1:list_key[1] + 1]
                cad_two = list_candidates[list_key[1] + 1:list_key[2] + 1]
                pos_insert_one = list_key[0] + 1
                pos_insert_two = list_key[0] + len(cad_two) + 1
                self.invert(list_candidates, list_key[0], list_key[1])
                cad_one = list_candidates[list_key[0] + 1:list_key[1] + 1]
                list_candidates = self.swap(list_candidates, cad_one, cad_two, pos_insert_one, pos_insert_two)
                route.set_list_id_customers(list_candidates)

            elif moves == 6:
                cad_one = list_candidates[list_key[0] + 1:list_key[1] + 1]
                cad_two = list_candidates[list_key[1] + 1:list_key[2] + 1]
                pos_insert_one = list_key[0] + 1
                pos_insert_two = list_key[0] + len(cad_two) + 1
                self.invert(list_candidates, list_key[1], list_key[2])
                cad_two = list_candidates[list_key[1] + 1:list_key[2] + 1]
                list_candidates = self.swap(list_candidates, cad_one, cad_two, pos_insert_one, pos_insert_two)
                route.set_list_id_customers(list_candidates)


            #for id_cliente in list_candidates:
             #   if id_cliente in id_vistos:
              #      duplicate = True
               # id_vistos.append(id_cliente)


            current_cost = route.get_cost_single_route()

            if best_cost > current_cost:
                best_cost = current_cost
                list_opt = list_candidates.copy()

            moves += 1

        route.set_list_id_customers(list_opt)
        route.set_cost_route(best_cost)

    def swap(self, list_candidates, cad_one, cad_two, pos_insert_one, pos_insert_two):
        list_temp = []

        i = 0
        while i < len(list_candidates):
            if i == pos_insert_one:
                for j in range(len(cad_two)):
                    list_temp.append(cad_two[j])
                    i += 1

            if i == pos_insert_two:
                for j in range(len(cad_one)):
                    list_temp.append(cad_one[j])
                    i += 1

                i -= 1

            else:
                list_temp.append(list_candidates[i])
            i += 1

        return list_temp

    def invert(self, list_candidates, start, end):
        while start < end:
            list_candidates[start], list_candidates[end] = list_candidates[end], list_candidates[start]
            start += 1
            end -= 1


