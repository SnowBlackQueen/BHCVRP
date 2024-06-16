from data.Customer import Customer
from data.Problem import Problem
from data.ProblemType import ProblemType
from generator.solution import Solution
from typing import List
from generator.heuristic.Metric import Metric
from generator.heuristic.FirstCustomerType import FirstCustomerType
import random

# Clase abstracta que modela una heurística de construcción

class Heuristic:
    def get_solution_inicial(self):
        # Método abstracto encargado de generar la solución
        pass

    def _get_customer_by_id(self, idCustomer, listCustomers):
        i = 0
        found = False
        customer = None

        while i < len(listCustomers) and not found:
            if listCustomers[i].get_id_customer() == idCustomer:
                customer = listCustomers[i]
                found = True
            else:
                i += 1

        return customer

    def _ascendent_ordenate(self, listWithOutOrder: List[Metric]):
        for i in range(len(listWithOutOrder)):
            minorInsertionCost = listWithOutOrder[i].getInsertionCost()
            minorMetric = listWithOutOrder[i]
            referencePos = i

            currentMetric = None
            currentPos = -1

            for j in range(i + 1, len(listWithOutOrder)):
                if listWithOutOrder[j].getInsertionCost() < minorInsertionCost:
                    minorInsertionCost = listWithOutOrder[j].getInsertionCost()
                    currentMetric = listWithOutOrder[j]
                    currentPos = j

            if currentPos != -1:
                listWithOutOrder[referencePos] = currentMetric
                listWithOutOrder[currentPos] = minorMetric
                
    def _ascendent_ordenate(self, list_distances, list_nn: List[Customer]):
        for i in range(len(list_distances)):
            minor_distance = list_distances[i]
            customer_nn = list_nn[i]
            reference_pos = i

            current_distance = 0.0
            current_customer = None
            current_pos = -1

            for j in range(i + 1, len(list_distances)):
                if minor_distance > list_distances[j]:
                    current_distance = list_distances[j]
                    current_customer = list_nn[j]
                    current_pos = j

            if current_pos != -1:
                list_distances[reference_pos] = current_distance
                list_distances[current_pos] = minor_distance

                list_nn[reference_pos] = current_customer
                list_nn[current_pos] = customer_nn
                
    def _select_first_customer_in_mdvrp(self, customers_to_visit, first_customer_type, pos_matrix_depot):
        selected_customer = None
        currentIndex = -1
        currentCost = 0.0

        selected_customer = customers_to_visit[0]
        bestIndex = Problem.get_problem().get_pos_element(selected_customer.get_id_customer())
        bestCost = Problem.get_problem().get_cost_matrix().get_item(pos_matrix_depot, bestIndex)

        for i in range(1, len(customers_to_visit)):
            currentIndex = Problem.get_problem().get_pos_element(customers_to_visit[i].get_id_customer())
            currentCost = Problem.get_problem().get_cost_matrix().get_item(pos_matrix_depot, currentIndex)

            if first_customer_type == FirstCustomerType.FurthestCustomer:
                if currentCost > bestCost:
                    bestCost = currentCost
                    bestIndex = currentIndex
                    selected_customer = customers_to_visit[i]
            else:
                if first_customer_type == FirstCustomerType.NearestCustomer:
                    if currentCost < bestCost:
                        bestCost = currentCost
                        bestIndex = currentIndex
                        selected_customer = customers_to_visit[i]

        return selected_customer
    
    def _get_first_customer(self, customers_to_visit, first_customer_type, id_depot):
        firstCustomer = None
        index = -1
        posMatrixDepot = -1
        rc = None

        if first_customer_type == FirstCustomerType.OtherType:  # Replace with the actual condition
            index = random.randint(0, len(customers_to_visit) - 1)
            firstCustomer = customers_to_visit[index]
        else:
            pos_matrix_depot = Problem.get_problem().get_pos_element(id_depot)

            if Problem.get_problem().get_type_problem() == ProblemType.MDVRP:
                firstCustomer = self.select_first_customer_in_mdvrp(customers_to_visit, first_customer_type, pos_matrix_depot)
            else:
                if first_customer_type == FirstCustomerType.NearestCustomer:
                    rc = Problem.get_problem().get_cost_matrix().index_lower_value(posMatrixDepot, 0, posMatrixDepot, len(customers_to_visit) - 1)
                elif first_customer_type == FirstCustomerType.FurthestCustomer:
                    rc = Problem.get_problem().get_cost_matrix().index_bigger_value(posMatrixDepot, 0, posMatrixDepot, len(customers_to_visit) - 1)

                index = rc.get_col()
                firstCustomer = customers_to_visit[index]

        return firstCustomer