import sys
import os
import numpy as np
import pandas as pd
from tools.LoadFile import LoadFile
from factory.interfaces.HeuristicType import HeuristicType
from data.ProblemType import ProblemType
from generator.controller.StrategyHeuristic import StrategyHeuristic

def main(self):
    try:
        file_output = open("/D:/Escuela/BHCVRP/ResultadosCVRP/Instancia_CVRP_p14/Resultado_MoleJameson20.txt", "w")
        sys.stdout = file_output

        path_files = "modified-cvrp//CVRP_p14"
        # total_instances = 5
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
        load_file.load_customers(id_customers, axis_x_customers, axis_y_customers, request_customers)
        load_file.load_depots(id_depots, axis_x_depots, axis_y_depots)

        load_file.fill_list_distances(id_customers, axis_x_customers, axis_y_customers, id_depots, axis_x_depots, axis_y_depots, list_distances)

        heuristic_type = HeuristicType.MoleJameson

        if StrategyHeuristic.get_strategy_heuristic().load_CVRP(id_customers, request_customers, id_depots, count_vehicles[0], capacity_vehicles[0], list_distances, axis_x_customers, axis_y_customers, axis_x_depots, axis_y_depots, ProblemType.CVRP):
            StrategyHeuristic.get_strategy_heuristic().execute_heuristic(20, heuristic_type)
            result = StrategyHeuristic.get_strategy_heuristic().get_best_solution()
            cost = StrategyHeuristic.get_strategy_heuristic().get_total_cost_solution()
            request_by_route = len(StrategyHeuristic.get_strategy_heuristic().get_request_by_route())
            time = StrategyHeuristic.get_strategy_heuristic().get_time_execute()

            print(" ")
            print("------------------------------------------")
            # print("INSTANCIA: P" + (i + 1))
            print("HEURÍSTICA DE CONSTRUCCIÓN: " + heuristic_type)
            print("COSTO TOTAL: " + cost)
            print("TOTAL DE RUTAS: " + request_by_route)
            # print("TIEMPO DE EJECUCIÓN: " + time)
            print(" ")
            for j in range(request_by_route):
                print("R" + str(j + 1) + result.get_list_routes()[j].get_list_id_customers())
            print("------------------------------------------")

        file_output.close()
        sys.stdout = sys.__stdout__  # Restore standard output
    except IOError as e:
        print(e)

if __name__ == "__main__":
    main()