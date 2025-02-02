from tools.LoadFile import LoadFile
from factory.interfaces.HeuristicType import HeuristicType
from data.ProblemType import ProblemType
from generator.controller.StrategyHeuristic import StrategyHeuristic
from data.Problem import Problem


def main():
    try:
        file_output = open(
            "D:\\Escuela\\BHCVRP_Python_Version\\Resultados\\Resultado_BSS_Random1.txt",
            "w",
        )
        # sys.stdout = file_output

        path_file_original_instance = "D:\\Escuela\\BHCVRP_Python_Version\\Resultados\\instance-4_B-80_P-800_D-1_MW-10_MBC-15_MVC-25_BSS.json"
        path_file_solution_BSS = "D:\\Escuela\\BHCVRP_Python_Version\\Resultados\\BSS_solution-11_B-74_P-800_S-METAHEURISTIC_A-MH_GENETIC_BSS.json"

        # total_instances = 5
        load_file = LoadFile()

        # for i in range(1, total_instances):
        depots = load_file.load_depots_from_json(path_file_original_instance)  # i + 1
        id_depots = []
        axis_x_depots = []
        axis_y_depots = []

        for i in range(len(depots)):
            id = depots[i]._id_depot
            id_depots.append(id)

            location = depots[i]._location_depot
            axis_x = location.get_axis_x()
            axis_y = location.get_axis_y()

            axis_x_depots.append(axis_x)
            axis_y_depots.append(axis_y)


        list_distances = []

        bus_stops = load_file.load_bus_stops_from_json(path_file_solution_BSS)
        id_bus_stops = []
        axis_x_bus_stops = []
        axis_y_bus_stops = []

        for i in range(len(bus_stops)):
            id = bus_stops[i]._id_bus_stop
            id_bus_stops.append(id)

            location = bus_stops[i]._location_bus_stop
            axis_x = location.get_axis_x()
            axis_y = location.get_axis_y()

            axis_x_bus_stops.append(axis_x)
            axis_y_bus_stops.append(axis_y)



        load_file.fill_list_distances(
            id_bus_stops, axis_x_bus_stops, axis_y_bus_stops,
            id_depots, axis_x_depots, axis_y_depots,
            list_distances)

        heuristic_type = HeuristicType.CMT
        problem = Problem.get_problem()
        problem.set_type_problem(type_problem=ProblemType.SBRP)
        Problem.get_problem().set_cost_matrix(StrategyHeuristic.get_strategy_heuristic().fill_cost_matrix(list_distances))

        StrategyHeuristic.get_strategy_heuristic().execute_heuristic(20, heuristic_type)
        result = StrategyHeuristic.get_strategy_heuristic().get_best_solution()
        cost = StrategyHeuristic.get_strategy_heuristic().get_total_cost_solution()
        request_by_route = len(StrategyHeuristic.get_strategy_heuristic().get_request_by_route())
        time = StrategyHeuristic.get_strategy_heuristic().get_time_execute()

        print(" ")
        print("------------------------------------------")
        # print("INSTANCIA: P" + (i + 1))
        print("HEURÍSTICA DE CONSTRUCCIÓN: " + heuristic_type.name)
        print("COSTO TOTAL: " + str(cost))
        print("TOTAL DE RUTAS: " + str(request_by_route))
        print("TIEMPO DE EJECUCIÓN: " + str(time))
        print(" ")
        if heuristic_type == HeuristicType.SaveSequential or heuristic_type == HeuristicType.SaveParallel or heuristic_type == HeuristicType.MatchingBasedSavingAlgorithm or heuristic_type == HeuristicType.KilbyAlgorithm:
            for j in range(request_by_route):
                bus_stops_by_route = result.get_list_routes()[j].get_list_bus_stops()
                for k in range(len(bus_stops_by_route)):
                    print(
                        "R"
                        + str(j + 1)
                        + str(bus_stops_by_route[k].get_id_bus_stop())
                    )
                # print(" ", len(result.get_list_routes()[j].get_list_id_customers()))
        else:
            for j in range(request_by_route):
                print(
                    "R"
                    + str(j + 1)
                    + str(result.get_list_routes()[j].get_list_bus_stops())
                )
                # print(" ", len(result.get_list_routes()[j].get_list_id_customers()))
        print("------------------------------------------")

        file_output.close()
        # sys.stdout = sys.__stdout__  # Restore standard output
    except IOError as e:
        print(e)


if __name__ == "__main__":
    main()