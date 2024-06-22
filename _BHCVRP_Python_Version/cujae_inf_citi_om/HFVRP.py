import sys
import os
from tools.LoadFile import LoadFile
from generator.controller.StrategyHeuristic import StrategyHeuristic
from data.ProblemType import ProblemType
from tools.OrderType import OrderType
from factory.interfaces.HeuristicType import HeuristicType

def main(self):
    try:
        file_output = open("/D:/Escuela/BHCVRP/ResultadosHFVRP/Instancia_HFVRP_p14/Resultado_NN20.txt", "w")
        sys.stdout = file_output

        path_files = "modified-hfvrp//HFVRP_p14"
        
        load_file = LoadFile()

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

        type_problem = ProblemType.HFVRP
        order_type = OrderType.Descending
        heuristic_type = HeuristicType.NearestNeighborWithRLC

        if StrategyHeuristic.get_strategy_heuristic().load_HFVRP(id_customers, request_customers, id_depots, 
                count_vehicles[0], capacity_vehicles[0], list_distances, 
                axis_x_customers, axis_y_customers, axis_x_depots, axis_y_depots, type_problem, order_type):
            
            StrategyHeuristic.get_strategy_heuristic().execute_heuristic(20, heuristic_type)
            result = StrategyHeuristic.get_strategy_heuristic().get_best_solution()
            cost = StrategyHeuristic.get_strategy_heuristic().get_total_cost_solution()
            request_by_route = len(StrategyHeuristic.get_strategy_heuristic().get_request_by_route())
            time = StrategyHeuristic.get_strategy_heuristic().get_time_execute()
            
            print(" ")
            print("------------------------------------------")
            print("CANTIDAD DE EJECUCIONES: 100")
            print("HEURÍSTICA DE CONSTRUCCIÓN: " + str(heuristic_type))
            print("COSTO TOTAL: " + str(cost))
            print("TOTAL DE RUTAS: " + str(request_by_route))
            print("TIEMPO DE EJECUCIÓN: " + str(time) + " milisegundos")
            print(" ")

            for j in range(request_by_route):
                print("R" + str(j + 1) + str(result.get_list_routes()[j].get_list_id_customers()))

            print("------------------------------------------")

        file_output.close()
        sys.stdout = sys.__stdout__
        
    except IOError as e:
        print(e)

if __name__ == "__main__":
    main()