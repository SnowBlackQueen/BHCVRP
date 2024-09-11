import random
from decimal import Decimal, ROUND_UP
from tools.OrderType import OrderType

class Tools:
    @staticmethod
    def round_double(number, decimal_place):
        bd = Decimal(str(number))
        rounded = bd.quantize(Decimal(f'0.{"0"*decimal_place}'), rounding=ROUND_UP)
        return rounded.to_float()

    @staticmethod
    def ordinate_method(list_capacities, type_order: OrderType):
        flag = False

        if type_order == 0 or type_order == 1 or type_order == OrderType.Ascending or type_order == OrderType.Descending:
            for i in range(len(list_capacities) - 1):
                min_val = list_capacities[i]
                pos = i

                for j in range(i + 1, len(list_capacities)):
                    if type_order == 0:
                        if list_capacities[j] <= min_val:
                            min_val = list_capacities[j]
                            pos = j
                            flag = True
                    else:
                        if list_capacities[j] >= min_val:
                            min_val = list_capacities[j]
                            pos = j
                            flag = True

                    if flag:
                        list_capacities[pos], list_capacities[i] = list_capacities[i], min_val
                        flag = False
        elif type_order == 2 or type_order == OrderType.Random:
            list_capacity_order = []
            while list_capacities:
                index = random.randint(0, len(list_capacities) - 1)
                list_capacity_order.append(list_capacities.pop(index))
            list_capacities.extend(list_capacity_order)

