import sys
import os
import io
from tools.LoadFile import LoadFile
from factory.interfaces.HeuristicType import HeuristicType
from data.ProblemType import ProblemType
from generator.controller.StrategyHeuristic import StrategyHeuristic
from enum import Enum

def main():
    try:
        fileOutputStream = open("D:\\Escuela\\BHCVRP_Python_Version\\Resultados\\MDVRP\\Instancia_p1\\Resultado_R1.txt", "w")
        printStream = io.TextIOWrapper(fileOutputStream)

        sys.stdout = printStream

        path_files = "D:\\Escuela\\BHCVRP_Python_Version\\Resultados\\MDVRP\\p1"
        load_file = LoadFile()

        # for i in range(1, total_instances):
        load_file.load_file(path_files)  # i + 1

        id_customers = []
        axis_x_customers = []
        axis_y_customers = []
        request_customers = []

        id_depots = []
        axis_x_depots = []
        axis_y_depots = []
        count_vehicles = []
        capacity_vehicles = []

        list_distances = []

        load_file.load_count_vehicles_for_depot(count_vehicles)
        load_file.load_capacity_vehicles(capacity_vehicles)
        load_file.is_load_customers(id_customers, axis_x_customers, axis_y_customers, request_customers)
        load_file.is_load_depots(id_depots, axis_x_depots, axis_y_depots)

        load_file.fill_list_distances(id_customers, axis_x_customers, axis_y_customers, id_depots, axis_x_depots, axis_y_depots, list_distances)

        heuristic_type = HeuristicType.RandomMethod

        if StrategyHeuristic.get_strategy_heuristic().load_problem(id_customers, request_customers, id_depots, count_vehicles[0], capacity_vehicles[0], list_distances, axis_x_customers, axis_y_customers, axis_x_depots, axis_y_depots, ProblemType.MDVRP, AssignmentType.BestNearest):
            StrategyHeuristic.get_strategy_heuristic().execute_heuristic(20, heuristic_type)
            result = StrategyHeuristic.get_strategy_heuristic().get_best_solution()
            cost = StrategyHeuristic.get_strategy_heuristic().get_total_cost_solution()
            request_by_route = len(StrategyHeuristic.get_strategy_heuristic().get_request_by_route())
            time = StrategyHeuristic.get_strategy_heuristic().get_time_execute()

            print(" ")
            print("------------------------------------------")
            print("HEURÍSTICA DE CONSTRUCCIÓN: " + str(heuristic_type))
            print("COSTO TOTAL: " + str(cost))
            print("TOTAL DE RUTAS: " + str(request_by_route))
            print(" ")

            for j in range(request_by_route):
                print("R" + str(j+1) + result.get_list_routes()[j].get_list_id_customers())
            
            print("------------------------------------------")

        printStream.close()
        fileOutputStream.close()

        sys.stdout = sys.__stdout__  # Restore standard output
    except IOError as e:
        print(e)


if __name__ == "__main__":
    main()
    
class AssignmentType(Enum):
    BestCyclicAssignment = 0
    BestNearest = 1
    CoefficientPropagation = 2
    CyclicAssignment = 3
    K_Means = 4
    NearestByCustomer = 5
    NearestByDepot = 6
    PAM = 7
    Parallel = 8
    RandomByElement = 9
    RandomNearestByCustomer = 10
    RandomNearestByDepot = 11
    RandomSequentialCyclic = 12
    RandomSequentialNearestByDepot = 13
    SequentialCyclic = 14
    SequentialNearestByDepot = 15
    Simplified = 16
    Sweep = 17
    ThreeCriteriaClustering = 18
    UPGMC = 19