import sys
import os
import io
from i_o.input.LoadFile import LoadFile
from factory.interfaces.HeuristicType import HeuristicType
from data.ProblemType import ProblemType
from controller.StrategyHeuristic import StrategyHeuristic
from controller.StrategyHeuristic import AssignmentTypePython
from i_o.output.ExportResult import ExportResult


def main():
    try:
        """file_output = open(
            "D:\\Escuela\\BHCVRP_Python_Version\\Resultados\\MDVRP\\Instancia_p14\\Resultado_Matching1.txt",
            "w",
        )"""
        # sys.stdout = file_output

        path_files = "D:\\Escuela\\BHCVRP_Python_Version\\Resultados\\MDVRP\\p1"
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
        )

        heuristic_type = HeuristicType.KilbyAlgorithm

        if StrategyHeuristic.get_strategy_heuristic().load_problem_with_assign(
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
            ProblemType.MDVRP,
            AssignmentTypePython.BestNearest,
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

            """print(" ")
            print("------------------------------------------")
            # print("INSTANCIA: P" + (i + 1))
            print("HEURÍSTICA DE CONSTRUCCIÓN: " + heuristic_type.name)
            print("COSTO TOTAL: " + str(cost))
            print("TOTAL DE RUTAS: " + str(request_by_route))
            print("TIEMPO DE EJECUCIÓN: " + str(time))
            print(" ")
            for j in range(request_by_route):
                print(
                    "R"
                    + str(j + 1)
                    + str(result.get_list_routes()[j].get_list_id_customers())
                )
                # print(" ", len(result.get_list_routes()[j].get_list_id_customers()))
            print("------------------------------------------")

        file_output.close()
        sys.stdout = sys.__stdout__  # Restore standard output"""

            # Para formato TXT
            # Construir la cadena de texto con el formato de los prints
            output_text = (
                " \n"
                "------------------------------------------\n"
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
            ExportResult.to_txt(output_text, "D:\\Escuela\\BHCVRP_Python_Version\\Resultados\\resultado.txt")

            # Para formato JSON y XML
            # Recopilar resultados en un diccionario
            results = {
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

            ExportResult.to_json(results, "D:\\Escuela\\BHCVRP_Python_Version\\Resultados\\resultado.json")
            ExportResult.to_xml(results, "D:\\Escuela\\BHCVRP_Python_Version\\Resultados\\resultado.xml")

            # Para formato CSV
            # Crear una lista de listas para el CSV
            csv_data = [
                ["Tipo de heurística", heuristic_type.name],
                ["Costo total", cost],
                ["Tiempo de ejecución", time],
                ["Ruta", "Clientes"]  # Encabezado de las rutas
            ]

            # Agregar las rutas
            for j in range(request_by_route):
                csv_data.append([f"R{j + 1}", result.get_list_routes()[j].get_list_id_customers()])

            # Exportar a CSV
            ExportResult.to_csv(
                csv_data,
                "D:\\Escuela\\BHCVRP_Python_Version\\Resultados\\resultado.csv"
            )

    except IOError as e:
        print(e)


if __name__ == "__main__":
    main()
