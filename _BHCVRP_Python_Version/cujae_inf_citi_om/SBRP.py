from i_o.input.LoadFile import LoadFile
from factory.interfaces.HeuristicType import HeuristicType
from data.ProblemType import ProblemType
from controller.StrategyHeuristic import StrategyHeuristic
from data.Problem import Problem
from tools.DistanceType import DistanceType
from i_o.output.ExportResult import ExportResult
import os


def main():
    try:
        """file_output = open(
            "D:\\Escuela\\BHCVRP_Python_Version\\Resultados\\Resultado_BSS_Random1.txt",
            "w",
        )
        # sys.stdout = file_output"""

        path_file_original_instance = "instances\\sbrp\\instance_1\\instance-1_B-10_P-100_D-1_MW-20_MBC-15_MVC-25_BSS.json"
        path_file_solution_BSS = "instances\\sbrp\\instance_1\\BSS_solution-110_B-10_P-100_S-metaheuristic_A-evolution_estrategic_BSS.json.json"

        path_file_result = "results\\sbrp\\inst1_R1"
        file_extension = os.path.splitext(path_file_original_instance)[1].lower()

        # total_instances = 5
        load_file = LoadFile()

        distance_type = DistanceType.Euclidean
        heuristic_type = HeuristicType.RandomMethod

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
            list_distances, distance_type)

        problem = Problem.get_problem()
        problem.set_type_problem(type_problem=ProblemType.SBRP)
        Problem.get_problem().set_cost_matrix(StrategyHeuristic.get_strategy_heuristic().fill_cost_matrix_with_list_distances(list_distances))

        StrategyHeuristic.get_strategy_heuristic().execute_heuristic(20, heuristic_type)
        result = StrategyHeuristic.get_strategy_heuristic().get_best_solution()
        cost = StrategyHeuristic.get_strategy_heuristic().get_total_cost_solution()
        request_by_route = len(StrategyHeuristic.get_strategy_heuristic().get_request_by_route())
        time = StrategyHeuristic.get_strategy_heuristic().get_time_execute()

        """print(" ")
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

        file_output.close()"""

        # Construir la estructura de datos para exportar
        if heuristic_type == HeuristicType.SaveSequential or heuristic_type == HeuristicType.SaveParallel or heuristic_type == HeuristicType.MatchingBasedSavingAlgorithm or heuristic_type == HeuristicType.KilbyAlgorithm:
            data = {
                "heuristic_type": heuristic_type.name,
                "total_cost": cost,
                "execution_time": time,
                "routes": [
                    {
                        "route_id": j + 1,
                        "bus_stops": [
                            bus_stop.get_id_bus_stop()
                            for bus_stop in result.get_list_routes()[j].get_list_bus_stops()
                        ]
                    }
                    for j in range(request_by_route)
                ]
            }

            # Exportar a TXT
            output_text = (
                " \n"
                "------------------------------------------\n"
                f"HEURÍSTICA DE CONSTRUCCIÓN: {heuristic_type.name}\n"
                f"COSTO TOTAL: {cost}\n"
                f"TOTAL DE RUTAS: {request_by_route}\n"
                f"TIEMPO DE EJECUCIÓN: {time}\n"
                " \n"
            )
            for j in range(request_by_route):
                output_text += (
                    f"R{j + 1}{[bus_stop.get_id_bus_stop() for bus_stop in result.get_list_routes()[j].get_list_bus_stops()]}\n"
                )
            output_text += "------------------------------------------\n"

            # Exportar a CSV
            csv_data = [["Ruta", "Paradas"]] + [
                [f"R{j + 1}", ", ".join(map(str, [bus_stop.get_id_bus_stop() for bus_stop in
                                                  result.get_list_routes()[j].get_list_bus_stops()]))]
                for j in range(request_by_route)
            ]

        else:
            data = {
                "heuristic_type": heuristic_type.name,
                "total_cost": cost,
                "execution_time": time,
                "routes": [
                    {
                        "route_id": j + 1,
                        "bus_stops": [
                            bus_stop
                            for bus_stop in result.get_list_routes()[j].get_list_bus_stops()
                        ]
                    }
                    for j in range(request_by_route)
                ]
            }

            # Exportar a TXT
            output_text = (
                " \n"
                "------------------------------------------\n"
                f"HEURÍSTICA DE CONSTRUCCIÓN: {heuristic_type.name}\n"
                f"COSTO TOTAL: {cost}\n"
                f"TOTAL DE RUTAS: {request_by_route}\n"
                f"TIEMPO DE EJECUCIÓN: {time}\n"
                " \n"
            )
            for j in range(request_by_route):
                output_text += (
                    f"R{j + 1}{[bus_stop for bus_stop in result.get_list_routes()[j].get_list_bus_stops()]}\n"
                )
            output_text += "------------------------------------------\n"

            # Exportar a CSV
            csv_data = [["Ruta", "Paradas"]] + [
                [f"R{j + 1}", ", ".join(map(str, [bus_stop for bus_stop in
                                                  result.get_list_routes()[j].get_list_bus_stops()]))]
                for j in range(request_by_route)
            ]

        full_path = f"{path_file_result}.txt"
        ExportResult.to_txt(output_text, full_path)

        # Exportar a JSON
        full_path = f"{path_file_result}.json"
        ExportResult.to_json(data, full_path)

        full_path = f"{path_file_result}.csv"
        ExportResult.to_csv(csv_data, full_path)

        # Exportar a XML
        full_path = f"{path_file_result}.xml"
        ExportResult.to_xml(data, full_path)
        # sys.stdout = sys.__stdout__  # Restore standard output
    except IOError as e:
        print(e)


if __name__ == "__main__":
    main()