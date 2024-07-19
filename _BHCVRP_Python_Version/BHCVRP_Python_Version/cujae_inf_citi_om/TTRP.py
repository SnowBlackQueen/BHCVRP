import sys
import os
import sys
from tools.LoadFile import LoadFile
from data.ProblemType import ProblemType
from factory.interfaces.HeuristicType import HeuristicType
from generator.controller.StrategyHeuristic import StrategyHeuristic
from factory.interfaces.DistanceType import DistanceType

def main():
    try:
        file_output_stream = open("../Resultado_TTRP1.txt", "w")
        #sys.stdout = file_output

        path_files = "../TTRP_1.txt"
        load_file = LoadFile()

        load_file.load_file(path_files)

        id_customers = []
        axis_x_customers = []
        axis_y_customers = []
        request_customers = []
        type_customers = []

        id_depots = []
        axis_x_depots = []
        axis_y_depots = []
        count_vehicles = []
        capacity_vehicles = []
        count_trailers = []
        capacity_trailers = []

        list_distances = []

        load_file.load_count_vehicles_for_depot_ttrp(count_vehicles)
        load_file.load_capacity_vehicles_ttrp(capacity_vehicles)
        load_file.load_count_trailers_for_depot_ttrp(count_trailers)
        load_file.load_capacity_trailers_ttrp(capacity_trailers)
        load_file.is_load_customers_ttrp(id_customers, axis_x_customers, axis_y_customers, request_customers, type_customers)
        load_file.is_load_depots_ttrp(id_depots, axis_x_depots, axis_y_depots)

        load_file.fill_list_distances(id_customers, axis_x_customers, axis_y_customers, id_depots, axis_x_depots, axis_y_depots, list_distances)

        id_assigned_customers = []
        id_assigned_customers.extend(id_customers)

        heuristic_type = HeuristicType.MoleJameson
        count_execution = 100

        if heuristic_type == HeuristicType.Sweep:
            if StrategyHeuristic.get_strategy_heuristic().load_problem_(id_customers, request_customers, axis_x_customers, axis_y_customers,
                    type_customers, id_depots, axis_x_depots, axis_y_depots, id_assigned_customers, count_vehicles, capacity_vehicles, 
                    count_trailers, capacity_trailers, ProblemType.TTRP, DistanceType.Euclidean):
                
                StrategyHeuristic.get_strategy_heuristic().execute_heuristic(20, heuristic_type)
                result = StrategyHeuristic.get_strategy_heuristic().get_best_solution()
                cost = StrategyHeuristic.get_strategy_heuristic().get_total_cost_solution()
                request_by_route = StrategyHeuristic.get_strategy_heuristic().get_request_by_route().size()
                time = StrategyHeuristic.get_strategy_heuristic().get_time_execute()

                print(" ")
                print("------------------------------------------")
                print("HEURÍSTICA DE CONSTRUCCIÓN: " + heuristic_type)
                print("COSTO TOTAL: " + cost)
                print("TOTAL DE RUTAS: " + request_by_route)
                print(" ")

                for j in range(request_by_route):
                    print("R" + str(j+1) + result.get_list_routes()[j].get_list_id_customers())
                
                print("------------------------------------------")
                
        elif StrategyHeuristic.get_strategy_heuristic().load_problem(id_customers, request_customers, type_customers, id_depots, id_assigned_customers, count_vehicles, capacity_vehicles, count_trailers, capacity_trailers, list_distances, ProblemType.TTRP):
            StrategyHeuristic.get_strategy_heuristic().execute_heuristic(20, heuristic_type)
            result = StrategyHeuristic.get_strategy_heuristic().get_best_solution()
            cost = StrategyHeuristic.get_strategy_heuristic().get_total_cost_solution()
            request_by_route = len(StrategyHeuristic.get_strategy_heuristic().get_request_by_route())
            time = StrategyHeuristic.get_strategy_heuristic().get_time_execute()

            print(" ")
            print("------------------------------------------")
            print("HEURÍSTICA DE CONSTRUCCIÓN: " + heuristic_type.name)
            print("COSTO TOTAL: " + str(cost))
            print("TOTAL DE RUTAS: " + str(request_by_route))
            print(" ")

            for j in range(request_by_route):
                print("R" + str(j + 1) + str(result.get_list_routes()[j].get_list_id_customers()))
                #print("R" + str(j+1) + result.get_list_routes()[j].get_list_id_customers())
                
            print("------------------------------------------")

        file_output_stream.close()
        #sys.stdout = sys.__stdout__

    except IOError as e:
        print(e)

if __name__ == "__main__":
    main()