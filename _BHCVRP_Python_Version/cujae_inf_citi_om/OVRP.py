import os
from i_o.input.LoadFile import LoadFile
from factory.interfaces.HeuristicType import HeuristicType
from data.ProblemType import ProblemType
from controller.StrategyHeuristic import StrategyHeuristic
from i_o.output.ExportResult import ExportResult
from tools.DistanceType import DistanceType


def main():
    try:
        path_files = "instances\\cvrp\\CVRP_1"
        path_file_result = "results\\ovrp\\resultSP1"

        # Obtener la extensión del archivo
        file_extension = os.path.splitext(path_files)[1].lower()

        load_file = LoadFile()
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
        distance_type = DistanceType.Euclidean
        heuristic_type = HeuristicType.SaveParallel

        # Validar si el archivo es .txt o .json
        if file_extension == ".json":
            # Cargar archivo .json usando el método creado anteriormente
            problem_instance = load_file.load_cvrp_from_json(path_files)
            if problem_instance:
                id_customers = problem_instance.get_problem().get_list_id_customers()
                for i in range(len(id_customers)):
                    customer = problem_instance.get_problem().get_list_customers()[i]
                    axis_x_customers.append(customer.get_location_customer().get_axis_x())
                    axis_y_customers.append(customer.get_location_customer().get_axis_y())
                    request_customers.append(customer.get_request_customer())

                depot = problem_instance.get_problem().get_list_depots()[0]
                id_depots.append(depot.get_id_depot())
                axis_x_depots.append(depot.get_location_depot().get_axis_x())
                axis_y_depots.append(depot.get_location_depot().get_axis_y())
                count_vehicles = problem_instance.get_problem().get_list_count_vehicles(list_depots=problem_instance.get_problem().get_list_depots())
                capacity_vehicles = problem_instance.get_problem().get_list_capacity_vehicles(list_depots=problem_instance.get_problem().get_list_depots())

        else:
            load_file.load_file(path_files)  # i + 1

            load_file.load_count_vehicles_for_depot(count_vehicles)
            load_file.is_load_capacity_vehicles(capacity_vehicles)
            load_file.is_load_customers(
                id_customers, axis_x_customers, axis_y_customers, request_customers
            )
            load_file.is_load_depots(id_depots, axis_x_depots, axis_y_depots)

        load_file.fill_list_distances(
            id_customers,
            axis_x_customers,
            axis_y_customers,
            id_depots,
            axis_x_depots,
            axis_y_depots,
            list_distances,
            distance_type
        )

        if StrategyHeuristic.get_strategy_heuristic().load_cvrp(
                id_customers,
                request_customers,
                id_depots,
                count_vehicles[0],
                capacity_vehicles[0],
                list_distances,
                axis_x_customers,
                axis_y_customers,
                axis_x_depots,
                axis_y_depots,
                ProblemType.OVRP,
        ):
            StrategyHeuristic.get_strategy_heuristic().execute_heuristic(
                20, heuristic_type
            )
            result = StrategyHeuristic.get_strategy_heuristic().get_best_solution()
            cost = StrategyHeuristic.get_strategy_heuristic().get_total_cost_solution()
            request_by_route = len(
                StrategyHeuristic.get_strategy_heuristic().get_request_by_route()
            )
            time = StrategyHeuristic.get_strategy_heuristic().get_time_execute()

            # Para formato TXT
            # Construir la cadena de texto con el formato de los prints
            output_text = (
                " \n"
                "------------------------------------------\n"
                f"DISTANCIA: {distance_type.name}\n"
                f"HEURÍSTICA DE CONSTRUCCIÓN: {heuristic_type.name}\n"
                f"COSTO TOTAL: {cost}\n"
                f"TOTAL DE RUTAS: {request_by_route}\n"
                f"TIEMPO DE EJECUCIÓN: {time}\n"
                " \n"
            )

            # Agregar las rutas al texto
            for j in range(request_by_route):
                output_text += (
                    f"R{j + 1}{result.get_list_routes()[j].get_list_id_customers()}\n"
                )

            output_text += "------------------------------------------\n"

            # Exportar resultados en diferentes formatos
            full_path = f"{path_file_result}.txt"
            ExportResult.to_txt(output_text, full_path)

            # Para formato JSON y XML
            # Recopilar resultados en un diccionario
            results = {
                "distance_type": distance_type.name,
                "heuristic_type": heuristic_type.name,
                "total_cost": cost,
                "total_routes": request_by_route,
                "execution_time": time,
                "routes": [
                    {
                        "route_id": j + 1,
                        "customers": result.get_list_routes()[j].get_list_id_customers()
                    }
                    for j in range(request_by_route)
                ]
            }

            full_path = f"{path_file_result}.json"
            ExportResult.to_json(results, full_path)
            full_path = f"{path_file_result}.xml"
            ExportResult.to_xml(results, full_path)

            # Para formato CSV
            # Crear una lista de listas para el CSV
            csv_data = [
                ["Tipo de distancia", distance_type.name],
                ["Tipo de heurística", heuristic_type.name],
                ["Costo total", cost],
                ["Tiempo de ejecución", time],
                ["Ruta", "Clientes"]  # Encabezado de las rutas
            ]

            # Agregar las rutas
            for j in range(request_by_route):
                csv_data.append([f"R{j + 1}", result.get_list_routes()[j].get_list_id_customers()])

            # Exportar a CSV
            full_path = f"{path_file_result}.csv"
            ExportResult.to_csv(csv_data, full_path)

    except IOError as e:
        print(e)


if __name__ == "__main__":
    main()
