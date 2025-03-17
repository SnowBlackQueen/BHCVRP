from colorama import Fore
import os
from i_o.input.LoadFile import LoadFile
from factory.interfaces.HeuristicType import HeuristicType
from data.ProblemType import ProblemType
from controller.StrategyHeuristic import StrategyHeuristic
from i_o.output.ExportResult import ExportResult
from tools.DistanceType import DistanceType
from data.Problem import Problem
from tools.OrderType import OrderType
from controller.StrategyHeuristic import AssignmentTypePython

def main():
    RESET = Fore.RESET
    WHITE = Fore.LIGHTWHITE_EX

    while True:  # Bucle infinito hasta que el usuario decida salir
        print()
        print(WHITE + "Seleccione la variante VRP a solucionar: ")
        print("1. Problema de Planificación de Rutas de Vehículos con Capacidades (CVRP)")
        print("2. Problema de Planificación de Rutas de Vehículos con Flota Heterogénea (HFVRP)")
        print("3. Problema de Planificación de Rutas de Vehículos Abiertos (OVRP)")
        print("4. Problema de Planificación de Rutas de Vehículos con Múltiples Depósitos (MDVRP)")
        print("5. Problema de Planificación de Rutas de Camiones y Remolques (TTRP)")
        print("6. Problema de Planificación de Rutas de Vehículos con Ventanas de Tiempo (VRPTW)")
        print("7. Problema de Planificación de Rutas de Autobuses Escolares (SBRP)")
        print("0. Salir")

        while True:  # Bucle para la selección de la variante VRP
            opcion = input("Opción número: ")
            print()

            if opcion == '0':  # Condición de parada
                print("Saliendo del programa...")
                return  # Salir del programa
            elif opcion in ['1', '2', '3', '4', '5', '6', '7']:
                break  # Opción válida, salir del bucle
            else:
                print("Opción no válida. Intente de nuevo.")

        print("Seleccione la instancia del problema a utilizar: ")
        print("1. Instancia pequeña")
        print("2. Instancia mediana")
        print("3. Instancia grande")
        print("0. Salir")

        while True:  # Bucle para la selección de la instancia
            inst = input("Instancia número: ")
            print()

            if inst == '0':
                print("Saliendo del programa...")
                return  # Salir del programa
            elif inst in ['1', '2', '3']:
                break  # Opción válida, salir del bucle
            else:
                print("Opción no válida. Intente de nuevo.")

        print("Seleccione la heurística de construcción a utilizar: ")
        print("1. Heurística de construcción con mejor calidad en cuanto a costo en distancia")
        print("2. Heurística de construcción con peor calidad en cuanto a costo en distancia")
        print("3. Heurística de construcción con calidad promedio")
        print("0. Salir")

        while True:  # Bucle para la selección de la heurística
            hc = input("Heurística de construcción número: ")
            print()

            if hc == '0':
                print("Saliendo del programa...")
                return  # Salir del programa
            elif hc in ['1', '2', '3']:
                break  # Opción válida, salir del bucle
            else:
                print("Opción no válida. Intente de nuevo.")

        if opcion == '1':
            cvrp(inst, hc)
        elif opcion == '2':
            hfvrp(inst, hc)
        elif opcion == '3':
            ovrp(inst, hc)
        elif opcion == '4':
            mdvrp(inst, hc)
        elif opcion == '5':
            ttrp(inst, hc)
        elif opcion == '6':
            vrptw(inst, hc)
        elif opcion == '7':
            sbrp(inst, hc)




def cvrp(number_instance, hc):
    try:
        BLUE = Fore.BLUE
        RED = Fore.RED
        GREEN = Fore.GREEN
        RESET = Fore.RESET

        path_files = " "
        if number_instance == '1':
            path_files = "instances\\cvrp\\CVRP_1"
        elif number_instance == '2':
            path_files = "instances\\cvrp\\CVRP_p5"
        elif number_instance == '3':
            path_files = "instances\\cvrp\\C1_2_1.txt"

        heuristic_type = " "
        if hc == '1':
            heuristic_type = HeuristicType.SaveParallel
        elif hc == '2':
            heuristic_type = HeuristicType.Sweep
        elif hc == '3':
            if number_instance == '3':
                heuristic_type = HeuristicType.FisherJaikumar
            else:
                heuristic_type = HeuristicType.KilbyAlgorithm

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
                ProblemType.CVRP,
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

            if hc == '1':
                print(GREEN + " ")
                print(GREEN + "------------------------------------------")
                print(GREEN + "VARIANTE: " + ProblemType.CVRP.name)
                print(GREEN + "DISTANCIA: " + distance_type.name)
                print(GREEN + "HEURÍSTICA DE CONSTRUCCIÓN: " + heuristic_type.name)
                print(GREEN + "COSTO TOTAL: " + str(cost))
                print(GREEN + "TOTAL DE RUTAS: " + str(request_by_route))
                print(GREEN + "TIEMPO DE EJECUCIÓN: " + str(time))
                print(GREEN + " ")
                for j in range(request_by_route):
                    print(
                        GREEN + "R"
                        + str(j + 1)
                        + str(result.get_list_routes()[j].get_list_id_customers())
                    )
                    # print(" ", len(result.get_list_routes()[j].get_list_id_customers()))
                print(GREEN + "------------------------------------------")

            elif hc == '2':
                print(RED + " ")
                print(RED + "------------------------------------------")
                print(RED + "VARIANTE: " + ProblemType.CVRP.name)
                print(RED + "DISTANCIA: " + distance_type.name)
                print(RED + "HEURÍSTICA DE CONSTRUCCIÓN: " + heuristic_type.name)
                print(RED + "COSTO TOTAL: " + str(cost))
                print(RED + "TOTAL DE RUTAS: " + str(request_by_route))
                print(RED + "TIEMPO DE EJECUCIÓN: " + str(time))
                print(RED + " ")
                for j in range(request_by_route):
                    print(
                        RED + "R"
                        + str(j + 1)
                        + str(result.get_list_routes()[j].get_list_id_customers())
                    )
                    # print(" ", len(result.get_list_routes()[j].get_list_id_customers()))
                print(RED + "------------------------------------------")

            elif hc == '3':
                print(BLUE + " ")
                print(BLUE + "------------------------------------------")
                print(BLUE + "VARIANTE: " + ProblemType.CVRP.name)
                print(BLUE + "DISTANCIA: " + distance_type.name)
                print(BLUE + "HEURÍSTICA DE CONSTRUCCIÓN: " + heuristic_type.name)
                print(BLUE + "COSTO TOTAL: " + str(cost))
                print(BLUE + "TOTAL DE RUTAS: " + str(request_by_route))
                print(BLUE + "TIEMPO DE EJECUCIÓN: " + str(time))
                print(BLUE + " ")
                for j in range(request_by_route):
                    print(
                        BLUE + "R"
                        + str(j + 1)
                        + str(result.get_list_routes()[j].get_list_id_customers())
                        )
                        # print(" ", len(result.get_list_routes()[j].get_list_id_customers()))
                print(BLUE + "------------------------------------------")

    except IOError as e:
        print(e)

def hfvrp(number_instance, hc):
    try:
        BLUE = Fore.BLUE
        RED = Fore.RED
        GREEN = Fore.GREEN
        RESET = Fore.RESET

        path_files = " "
        if number_instance == '1':
            path_files = "instances\\hfvrp\\HFVRP_1"
        elif number_instance == '2':
            path_files = "instances\\hfvrp\\HFVRP_p5"
        elif number_instance == '3':
            path_files = "instances\\hfvrp\\HFVRP_C1_2_1.txt"

        heuristic_type = " "
        if hc == '1':
            if number_instance == '3':
                heuristic_type = HeuristicType.SaveSequential
            else:
                heuristic_type = HeuristicType.MoleJameson
        elif hc == '2':
            heuristic_type = HeuristicType.RandomMethod
        elif hc == '3':
            if number_instance == '3':
                heuristic_type = HeuristicType.SaveParallel
            else:
                heuristic_type = HeuristicType.KilbyAlgorithm

        # Obtener la extensión del archivo
        file_extension = os.path.splitext(path_files)[1].lower()

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
        problem = Problem.get_problem()
        distance_type = DistanceType.Euclidean
        type_problem = ProblemType.HFVRP
        order_type = OrderType.Descending

        # Validar si el archivo es .txt o .json
        if file_extension == ".json":
            # Cargar archivo .json usando el método creado anteriormente
            problem_instance = load_file.load_hfvrp_from_json(path_files)
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
                count_vehicles = problem_instance.get_problem().get_list_count_vehicles(
                    list_depots=problem_instance.get_problem().get_list_depots())
                capacity_vehicles = problem_instance.get_problem().get_list_capacity_vehicles(
                    list_depots=problem_instance.get_problem().get_list_depots())

        else:
            load_file.load_count_vehicles_for_depot(count_vehicles)
            load_file.load_capacity_vehicles_for_hfvrp(capacity_vehicles)
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

        if StrategyHeuristic.get_strategy_heuristic().load_hfvrp(
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
                type_problem,
                order_type,
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

            if hc == '1':
                print(GREEN + " ")
                print(GREEN + "------------------------------------------")
                print(GREEN + "VARIANTE: " + ProblemType.HFVRP.name)
                print(GREEN + "DISTANCIA: " + distance_type.name)
                print(GREEN + "HEURÍSTICA DE CONSTRUCCIÓN: " + heuristic_type.name)
                print(GREEN + "COSTO TOTAL: " + str(cost))
                print(GREEN + "TOTAL DE RUTAS: " + str(request_by_route))
                print(GREEN + "TIEMPO DE EJECUCIÓN: " + str(time))
                print(GREEN + " ")
                for j in range(request_by_route):
                    print(
                        GREEN + "R"
                        + str(j + 1)
                        + str(result.get_list_routes()[j].get_list_id_customers())
                    )
                    # print(" ", len(result.get_list_routes()[j].get_list_id_customers()))
                print(GREEN + "------------------------------------------")

            elif hc == '2':
                print(RED + " ")
                print(RED + "------------------------------------------")
                print(RED + "VARIANTE: " + ProblemType.HFVRP.name)
                print(RED + "DISTANCIA: " + distance_type.name)
                print(RED + "HEURÍSTICA DE CONSTRUCCIÓN: " + heuristic_type.name)
                print(RED + "COSTO TOTAL: " + str(cost))
                print(RED + "TOTAL DE RUTAS: " + str(request_by_route))
                print(RED + "TIEMPO DE EJECUCIÓN: " + str(time))
                print(RED + " ")
                for j in range(request_by_route):
                    print(
                        RED + "R"
                        + str(j + 1)
                        + str(result.get_list_routes()[j].get_list_id_customers())
                    )
                    # print(" ", len(result.get_list_routes()[j].get_list_id_customers()))
                print(RED + "------------------------------------------")

            elif hc == '3':
                print(BLUE + " ")
                print(BLUE + "------------------------------------------")
                print(BLUE + "VARIANTE: " + ProblemType.HFVRP.name)
                print(BLUE + "DISTANCIA: " + distance_type.name)
                print(BLUE + "HEURÍSTICA DE CONSTRUCCIÓN: " + heuristic_type.name)
                print(BLUE + "COSTO TOTAL: " + str(cost))
                print(BLUE + "TOTAL DE RUTAS: " + str(request_by_route))
                print(BLUE + "TIEMPO DE EJECUCIÓN: " + str(time))
                print(BLUE + " ")
                for j in range(request_by_route):
                    print(
                        BLUE + "R"
                        + str(j + 1)
                        + str(result.get_list_routes()[j].get_list_id_customers())
                        )
                        # print(" ", len(result.get_list_routes()[j].get_list_id_customers()))
                print(BLUE + "------------------------------------------")


    except IOError as e:
        print(e)

def ovrp(number_instance, hc):
    try:
        BLUE = Fore.BLUE
        RED = Fore.RED
        GREEN = Fore.GREEN
        RESET = Fore.RESET

        path_files = " "
        if number_instance == '1':
            path_files = "instances\\cvrp\\CVRP_1"
        elif number_instance == '2':
            path_files = "instances\\cvrp\\CVRP_p5"
        elif number_instance == '3':
            path_files = "instances\\cvrp\\C1_2_1.txt"

        heuristic_type = " "
        if hc == '1':
            heuristic_type = HeuristicType.SaveParallel
        elif hc == '2':
            heuristic_type = HeuristicType.Sweep
        elif hc == '3':
            heuristic_type = HeuristicType.FisherJaikumar

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
                count_vehicles = problem_instance.get_problem().get_list_count_vehicles(
                    list_depots=problem_instance.get_problem().get_list_depots())
                capacity_vehicles = problem_instance.get_problem().get_list_capacity_vehicles(
                    list_depots=problem_instance.get_problem().get_list_depots())

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

            if hc == '1':
                print(GREEN + " ")
                print(GREEN + "------------------------------------------")
                print(GREEN + "VARIANTE: " + ProblemType.OVRP.name)
                print(GREEN + "DISTANCIA: " + distance_type.name)
                print(GREEN + "HEURÍSTICA DE CONSTRUCCIÓN: " + heuristic_type.name)
                print(GREEN + "COSTO TOTAL: " + str(cost))
                print(GREEN + "TOTAL DE RUTAS: " + str(request_by_route))
                print(GREEN + "TIEMPO DE EJECUCIÓN: " + str(time))
                print(GREEN + " ")
                for j in range(request_by_route):
                    print(
                        GREEN + "R"
                        + str(j + 1)
                        + str(result.get_list_routes()[j].get_list_id_customers())
                    )
                    # print(" ", len(result.get_list_routes()[j].get_list_id_customers()))
                print(GREEN + "------------------------------------------")

            elif hc == '2':
                print(RED + " ")
                print(RED + "------------------------------------------")
                print(RED + "VARIANTE: " + ProblemType.OVRP.name)
                print(RED + "DISTANCIA: " + distance_type.name)
                print(RED + "HEURÍSTICA DE CONSTRUCCIÓN: " + heuristic_type.name)
                print(RED + "COSTO TOTAL: " + str(cost))
                print(RED + "TOTAL DE RUTAS: " + str(request_by_route))
                print(RED + "TIEMPO DE EJECUCIÓN: " + str(time))
                print(RED + " ")
                for j in range(request_by_route):
                    print(
                        RED + "R"
                        + str(j + 1)
                        + str(result.get_list_routes()[j].get_list_id_customers())
                    )
                    # print(" ", len(result.get_list_routes()[j].get_list_id_customers()))
                print(RED + "------------------------------------------")

            elif hc == '3':
                print(BLUE + " ")
                print(BLUE + "------------------------------------------")
                print(BLUE + "VARIANTE: " + ProblemType.OVRP.name)
                print(BLUE + "DISTANCIA: " + distance_type.name)
                print(BLUE + "HEURÍSTICA DE CONSTRUCCIÓN: " + heuristic_type.name)
                print(BLUE + "COSTO TOTAL: " + str(cost))
                print(BLUE + "TOTAL DE RUTAS: " + str(request_by_route))
                print(BLUE + "TIEMPO DE EJECUCIÓN: " + str(time))
                print(BLUE + " ")
                for j in range(request_by_route):
                    print(
                        BLUE + "R"
                        + str(j + 1)
                        + str(result.get_list_routes()[j].get_list_id_customers())
                        )
                        # print(" ", len(result.get_list_routes()[j].get_list_id_customers()))
                print(BLUE + "------------------------------------------")



    except IOError as e:
        print(e)

def mdvrp(number_instance, hc):
    try:
        BLUE = Fore.BLUE
        RED = Fore.RED
        GREEN = Fore.GREEN
        RESET = Fore.RESET

        path_files = " "
        if number_instance == '1':
            path_files = "instances\\mdvrp\\p1"
        elif number_instance == '2':
            path_files = "instances\\mdvrp\\p5"
        elif number_instance == '3':
            path_files = "instances\\mdvrp\\p16"

        heuristic_type = " "
        if hc == '1':
            heuristic_type = HeuristicType.MoleJameson
        elif hc == '2':
            heuristic_type = HeuristicType.Sweep
        elif hc == '3':
            heuristic_type = HeuristicType.SaveSequential

        # Obtener la extensión del archivo
        file_extension = os.path.splitext(path_files)[1].lower()

        load_file = LoadFile()

        load_file.load_file(path_files)

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

        # Validar si el archivo es .txt o .json
        if file_extension == ".json":
            # Cargar archivo .json usando el método creado anteriormente
            problem_instance = load_file.load_mdvrp_from_json(path_files)
            if problem_instance:
                id_customers = problem_instance.get_problem().get_list_id_customers()
                for i in range(len(id_customers)):
                    customer = problem_instance.get_problem().get_list_customers()[i]
                    axis_x_customers.append(customer.get_location_customer().get_axis_x())
                    axis_y_customers.append(customer.get_location_customer().get_axis_y())
                    request_customers.append(customer.get_request_customer())

                depots = problem_instance.get_problem().get_list_depots()
                for i in range(len(depots)):
                    id_depots.append(depots[i].get_id_depot())
                    axis_x_depots.append(depots[i].get_location_depot().get_axis_x())
                    axis_y_depots.append(depots[i].get_location_depot().get_axis_y())

                count_vehicles = problem_instance.get_problem().get_list_count_vehicles(
                    list_depots=problem_instance.get_problem().get_list_depots())
                capacity_vehicles = problem_instance.get_problem().get_list_capacity_vehicles(
                    list_depots=problem_instance.get_problem().get_list_depots())

        else:
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

            if hc == '1':
                print(GREEN + " ")
                print(GREEN + "------------------------------------------")
                print(GREEN + "VARIANTE: " + ProblemType.MDVRP.name)
                print(GREEN + "DISTANCIA: " + distance_type.name)
                print(GREEN + "HEURÍSTICA DE CONSTRUCCIÓN: " + heuristic_type.name)
                print(GREEN + "COSTO TOTAL: " + str(cost))
                print(GREEN + "TOTAL DE RUTAS: " + str(request_by_route))
                print(GREEN + "TIEMPO DE EJECUCIÓN: " + str(time))
                print(GREEN + " ")
                for j in range(request_by_route):
                    print(
                        GREEN + "R"
                        + str(j + 1)
                        + str(result.get_list_routes()[j].get_list_id_customers())
                    )
                    # print(" ", len(result.get_list_routes()[j].get_list_id_customers()))
                print(GREEN + "------------------------------------------")

            elif hc == '2':
                print(RED + " ")
                print(RED + "------------------------------------------")
                print(RED + "VARIANTE: " + ProblemType.MDVRP.name)
                print(RED + "DISTANCIA: " + distance_type.name)
                print(RED + "HEURÍSTICA DE CONSTRUCCIÓN: " + heuristic_type.name)
                print(RED + "COSTO TOTAL: " + str(cost))
                print(RED + "TOTAL DE RUTAS: " + str(request_by_route))
                print(RED + "TIEMPO DE EJECUCIÓN: " + str(time))
                print(RED + " ")
                for j in range(request_by_route):
                    print(
                        RED + "R"
                        + str(j + 1)
                        + str(result.get_list_routes()[j].get_list_id_customers())
                    )
                    # print(" ", len(result.get_list_routes()[j].get_list_id_customers()))
                print(RED + "------------------------------------------")

            elif hc == '3':
                print(BLUE + " ")
                print(BLUE + "------------------------------------------")
                print(BLUE + "VARIANTE: " + ProblemType.MDVRP.name)
                print(BLUE + "DISTANCIA: " + distance_type.name)
                print(BLUE + "HEURÍSTICA DE CONSTRUCCIÓN: " + heuristic_type.name)
                print(BLUE + "COSTO TOTAL: " + str(cost))
                print(BLUE + "TOTAL DE RUTAS: " + str(request_by_route))
                print(BLUE + "TIEMPO DE EJECUCIÓN: " + str(time))
                print(BLUE + " ")
                for j in range(request_by_route):
                    print(
                        BLUE + "R"
                        + str(j + 1)
                        + str(result.get_list_routes()[j].get_list_id_customers())
                        )
                        # print(" ", len(result.get_list_routes()[j].get_list_id_customers()))
                print(BLUE + "------------------------------------------")


    except IOError as e:
        print(e)

def ttrp(number_instance, hc):
    try:
        BLUE = Fore.BLUE
        RED = Fore.RED
        GREEN = Fore.GREEN
        RESET = Fore.RESET

        path_files = " "
        if number_instance == '1':
            path_files = "instances\\ttrp\\TTRP_1.txt"
        elif number_instance == '2':
            path_files = "instances\\ttrp\\TTRP_5.txt"
        elif number_instance == '3':
            path_files = "instances\\ttrp\\TTRP_15.txt"

        heuristic_type = " "
        if hc == '1':
            heuristic_type = HeuristicType.SaveParallel
        elif hc == '2':
            heuristic_type = HeuristicType.Sweep
        elif hc == '3':
            if number_instance == '3':
                heuristic_type = HeuristicType.SaveSequential
            else:
                heuristic_type = HeuristicType.KilbyAlgorithm

        # Obtener la extensión del archivo
        file_extension = os.path.splitext(path_files)[1].lower()

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
        distance_type = DistanceType.Euclidean


        # Validar si el archivo es .txt o .json
        if file_extension == ".json":
            # Cargar archivo .json usando el método creado anteriormente
            problem_instance = load_file.load_ttrp_from_json(path_files)
            if problem_instance:
                customers = problem_instance.get_problem().get_list_customers()
                for c in customers:
                    id_customers.append(c.get_id_customer())
                    axis_x_customers.append(c.get_location_customer().get_axis_x())
                    axis_y_customers.append(c.get_location_customer().get_axis_y())
                    request_customers.append(c.get_request_customer())
                    type_customers.append(c.get_type_customer())

                depot = problem_instance.get_problem().get_list_depots()[0]
                id_depots.append(depot.get_id_depot())
                axis_x_depots.append(depot.get_location_depot().get_axis_x())
                axis_y_depots.append(depot.get_location_depot().get_axis_y())

                count_trailers = depot.get_list_fleets()[0].get_count_trailers()
                capacity_trailers = depot.get_list_fleets()[0].get_capacity_trailer()
                count_vehicles = problem_instance.get_problem().get_list_count_vehicles(
                    list_depots=problem_instance.get_problem().get_list_depots())
                capacity_vehicles = problem_instance.get_problem().get_list_capacity_vehicles(
                    list_depots=problem_instance.get_problem().get_list_depots())

        else:
            load_file.load_count_vehicles_for_depot_ttrp(count_vehicles)
            load_file.load_capacity_vehicles_ttrp(capacity_vehicles)
            load_file.load_count_trailers_for_depot_ttrp(count_trailers)
            load_file.load_capacity_trailers_ttrp(capacity_trailers)
            load_file.is_load_customers_ttrp(
                id_customers,
                axis_x_customers,
                axis_y_customers,
                request_customers,
                type_customers,
            )
            load_file.is_load_depots_ttrp(id_depots, axis_x_depots, axis_y_depots)

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

        id_assigned_customers = []
        id_assigned_customers.extend(id_customers)

        # count_execution = 100

        if heuristic_type == HeuristicType.Sweep:
            if StrategyHeuristic.get_strategy_heuristic().load_problem_(
                id_customers,
                request_customers,
                axis_x_customers,
                axis_y_customers,
                type_customers,
                id_depots,
                axis_x_depots,
                axis_y_depots,
                id_assigned_customers,
                count_vehicles,
                capacity_vehicles,
                count_trailers,
                capacity_trailers,
                ProblemType.TTRP,
                distance_type,
            ):

                StrategyHeuristic.get_strategy_heuristic().execute_heuristic(
                    20, heuristic_type
                )
                result = StrategyHeuristic.get_strategy_heuristic().get_best_solution()
                cost = (
                    StrategyHeuristic.get_strategy_heuristic().get_total_cost_solution()
                )
                request_by_route = len(
                    StrategyHeuristic.get_strategy_heuristic().get_request_by_route()
                )
                time = StrategyHeuristic.get_strategy_heuristic().get_time_execute()

                if hc == '1':
                    print(GREEN + " ")
                    print(GREEN + "------------------------------------------")
                    print(GREEN + "VARIANTE: " + ProblemType.TTRP.name)
                    print(GREEN + "DISTANCIA: " + distance_type.name)
                    print(GREEN + "HEURÍSTICA DE CONSTRUCCIÓN: " + heuristic_type.name)
                    print(GREEN + "COSTO TOTAL: " + str(cost))
                    print(GREEN + "TOTAL DE RUTAS: " + str(request_by_route))
                    print(GREEN + "TIEMPO DE EJECUCIÓN: " + str(time))
                    print(GREEN + " ")
                    for j in range(request_by_route):
                        print(
                            GREEN + "R"
                            + str(j + 1)
                            + str(result.get_list_routes()[j].get_list_id_customers())
                        )
                        # print(" ", len(result.get_list_routes()[j].get_list_id_customers()))
                    print(GREEN + "------------------------------------------")

                elif hc == '2':
                    print(RED + " ")
                    print(RED + "------------------------------------------")
                    print(RED + "VARIANTE: " + ProblemType.TTRP.name)
                    print(RED + "DISTANCIA: " + distance_type.name)
                    print(RED + "HEURÍSTICA DE CONSTRUCCIÓN: " + heuristic_type.name)
                    print(RED + "COSTO TOTAL: " + str(cost))
                    print(RED + "TOTAL DE RUTAS: " + str(request_by_route))
                    print(RED + "TIEMPO DE EJECUCIÓN: " + str(time))
                    print(RED + " ")
                    for j in range(request_by_route):
                        print(
                            RED + "R"
                            + str(j + 1)
                            + str(result.get_list_routes()[j].get_list_id_customers())
                        )
                        # print(" ", len(result.get_list_routes()[j].get_list_id_customers()))
                    print(RED + "------------------------------------------")

                elif hc == '3':
                    print(BLUE + " ")
                    print(BLUE + "------------------------------------------")
                    print(BLUE + "VARIANTE: " + ProblemType.TTRP.name)
                    print(BLUE + "DISTANCIA: " + distance_type.name)
                    print(BLUE + "HEURÍSTICA DE CONSTRUCCIÓN: " + heuristic_type.name)
                    print(BLUE + "COSTO TOTAL: " + str(cost))
                    print(BLUE + "TOTAL DE RUTAS: " + str(request_by_route))
                    print(BLUE + "TIEMPO DE EJECUCIÓN: " + str(time))
                    print(BLUE + " ")
                    for j in range(request_by_route):
                        print(
                            BLUE + "R"
                            + str(j + 1)
                            + str(result.get_list_routes()[j].get_list_id_customers())
                        )
                        # print(" ", len(result.get_list_routes()[j].get_list_id_customers()))
                    print(BLUE + "------------------------------------------")



        else:
            if StrategyHeuristic.get_strategy_heuristic().load_problem(
                id_customers,
                request_customers,
                type_customers,
                id_depots,
                id_assigned_customers,
                count_vehicles,
                capacity_vehicles,
                count_trailers,
                capacity_trailers,
                list_distances,
                ProblemType.TTRP,
            ):
                StrategyHeuristic.get_strategy_heuristic().execute_heuristic(
                    20, heuristic_type)
                result = StrategyHeuristic.get_strategy_heuristic().get_best_solution()
                cost = (
                    StrategyHeuristic.get_strategy_heuristic().get_total_cost_solution()
                )
                request_by_route = len(
                    StrategyHeuristic.get_strategy_heuristic().get_request_by_route()
                )
                time = StrategyHeuristic.get_strategy_heuristic().get_time_execute()

                if hc == '1':
                    print(GREEN + " ")
                    print(GREEN + "------------------------------------------")
                    print(GREEN + "DISTANCIA: " + distance_type.name)
                    print(GREEN + "HEURÍSTICA DE CONSTRUCCIÓN: " + heuristic_type.name)
                    print(GREEN + "COSTO TOTAL: " + str(cost))
                    print(GREEN + "TOTAL DE RUTAS: " + str(request_by_route))
                    print(GREEN + "TIEMPO DE EJECUCIÓN: " + str(time))
                    print(GREEN + " ")
                    for j in range(request_by_route):
                        print(
                            GREEN + "R"
                            + str(j + 1)
                            + str(result.get_list_routes()[j].get_list_id_customers())
                        )
                        # print(" ", len(result.get_list_routes()[j].get_list_id_customers()))
                    print(GREEN + "------------------------------------------")

                elif hc == '2':
                    print(RED + " ")
                    print(RED + "------------------------------------------")
                    print(RED + "DISTANCIA: " + distance_type.name)
                    print(RED + "HEURÍSTICA DE CONSTRUCCIÓN: " + heuristic_type.name)
                    print(RED + "COSTO TOTAL: " + str(cost))
                    print(RED + "TOTAL DE RUTAS: " + str(request_by_route))
                    print(RED + "TIEMPO DE EJECUCIÓN: " + str(time))
                    print(RED + " ")
                    for j in range(request_by_route):
                        print(
                            RED + "R"
                            + str(j + 1)
                            + str(result.get_list_routes()[j].get_list_id_customers())
                        )
                        # print(" ", len(result.get_list_routes()[j].get_list_id_customers()))
                    print(RED + "------------------------------------------")

                elif hc == '3':
                    print(BLUE + " ")
                    print(BLUE + "------------------------------------------")
                    print(BLUE + "DISTANCIA: " + distance_type.name)
                    print(BLUE + "HEURÍSTICA DE CONSTRUCCIÓN: " + heuristic_type.name)
                    print(BLUE + "COSTO TOTAL: " + str(cost))
                    print(BLUE + "TOTAL DE RUTAS: " + str(request_by_route))
                    print(BLUE + "TIEMPO DE EJECUCIÓN: " + str(time))
                    print(BLUE + " ")
                    for j in range(request_by_route):
                        print(
                            BLUE + "R"
                            + str(j + 1)
                            + str(result.get_list_routes()[j].get_list_id_customers())
                        )
                        # print(" ", len(result.get_list_routes()[j].get_list_id_customers()))
                    print(BLUE + "------------------------------------------")



    except IOError as e:
        print(e)

def vrptw(number_instance, hc):
    try:
        BLUE = Fore.BLUE
        RED = Fore.RED
        GREEN = Fore.GREEN
        RESET = Fore.RESET

        path_files = " "
        if number_instance == '1':
            path_files = "instances\\vrptw\\C1_2_1.txt"
        elif number_instance == '2':
            path_files = "instances\\vrptw\\C1_4_1.txt"
        elif number_instance == '3':
            path_files = "instances\\vrptw\\C1_6_1.txt"

        heuristic_type = " "
        if hc == '1':
            heuristic_type = HeuristicType.SaveParallel
        elif hc == '2':
            heuristic_type = HeuristicType.RandomMethod
        elif hc == '3':
            heuristic_type = HeuristicType.FisherJaikumar

        # Obtener la extensión del archivo
        file_extension = os.path.splitext(path_files)[1].lower()

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
        initial_nodes = []
        end_nodes = []
        service_times = []

        distance_type = DistanceType.Euclidean

        # Validar si el archivo es .txt o .json
        if file_extension == ".json":  # TERMINAR INSTANCIA
            # Cargar archivo .json usando el método creado anteriormente
            problem_instance = load_file.load_vrptw_from_json(path_files)
            if problem_instance:
                id_customers = problem_instance.get_problem().get_list_id_customers()
                for i in range(len(id_customers)):
                    customer = problem_instance.get_problem().get_list_customers()[i]
                    axis_x_customers.append(customer.get_location_customer().get_axis_x())
                    axis_y_customers.append(customer.get_location_customer().get_axis_y())
                    request_customers.append(customer.get_request_customer())
                    initial_nodes.append(customer.get_time_window().get_initial_node())
                    end_nodes.append(customer.get_time_window().get_end_node())
                    service_times.append(customer.get_time_window().get_service_time())

                depot = problem_instance.get_problem().get_list_depots()[0]
                id_depots.append(depot.get_id_depot())
                axis_x_depots.append(depot.get_location_depot().get_axis_x())
                axis_y_depots.append(depot.get_location_depot().get_axis_y())
                count_vehicles = problem_instance.get_problem().get_list_count_vehicles(
                    list_depots=problem_instance.get_problem().get_list_depots())
                capacity_vehicles = problem_instance.get_problem().get_list_capacity_vehicles(
                    list_depots=problem_instance.get_problem().get_list_depots())

        else:
            load_file.load_count_vehicles_for_depot(count_vehicles)
            load_file.is_load_capacity_vehicles(capacity_vehicles)
            load_file.is_load_customers(
                id_customers, axis_x_customers, axis_y_customers, request_customers
            )
            load_file.is_load_depots(id_depots, axis_x_depots, axis_y_depots)

            load_file.is_load_time_windows(initial_nodes, end_nodes, service_times)

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

        if StrategyHeuristic.get_strategy_heuristic().load_vrptw(
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
                initial_nodes,
                end_nodes,
                service_times,
                ProblemType.VRPTW,
        ):
            if number_instance == '3':
                StrategyHeuristic.get_strategy_heuristic().execute_heuristic(
                    1, heuristic_type
                )
            elif number_instance == '2':
                StrategyHeuristic.get_strategy_heuristic().execute_heuristic(
                    5, heuristic_type
                )
            else:
                StrategyHeuristic.get_strategy_heuristic().execute_heuristic(
                    20, heuristic_type
                )

            result = StrategyHeuristic.get_strategy_heuristic().get_best_solution()
            cost = StrategyHeuristic.get_strategy_heuristic().get_total_cost_solution()
            request_by_route = len(
                StrategyHeuristic.get_strategy_heuristic().get_request_by_route()
            )
            time = StrategyHeuristic.get_strategy_heuristic().get_time_execute()

            if hc == '1':
                print(GREEN + " ")
                print(GREEN + "------------------------------------------")
                print(GREEN + "VARIANTE: " + ProblemType.VRPTW.name)
                print(GREEN + "DISTANCIA: " + distance_type.name)
                print(GREEN + "HEURÍSTICA DE CONSTRUCCIÓN: " + heuristic_type.name)
                print(GREEN + "COSTO TOTAL: " + str(cost))
                print(GREEN + "TOTAL DE RUTAS: " + str(request_by_route))
                print(GREEN + "TIEMPO DE EJECUCIÓN: " + str(time))
                print(GREEN + " ")
                for j in range(request_by_route):
                    print(
                        GREEN + "R"
                        + str(j + 1)
                        + str(result.get_list_routes()[j].get_list_id_customers())
                    )
                    # print(" ", len(result.get_list_routes()[j].get_list_id_customers()))
                print(GREEN + "------------------------------------------")

            elif hc == '2':
                print(RED + " ")
                print(RED + "------------------------------------------")
                print(RED + "VARIANTE: " + ProblemType.VRPTW.name)
                print(RED + "DISTANCIA: " + distance_type.name)
                print(RED + "HEURÍSTICA DE CONSTRUCCIÓN: " + heuristic_type.name)
                print(RED + "COSTO TOTAL: " + str(cost))
                print(RED + "TOTAL DE RUTAS: " + str(request_by_route))
                print(RED + "TIEMPO DE EJECUCIÓN: " + str(time))
                print(RED + " ")
                for j in range(request_by_route):
                    print(
                        RED + "R"
                        + str(j + 1)
                        + str(result.get_list_routes()[j].get_list_id_customers())
                    )
                    # print(" ", len(result.get_list_routes()[j].get_list_id_customers()))
                print(RED + "------------------------------------------")

            elif hc == '3':
                print(BLUE + " ")
                print(BLUE + "------------------------------------------")
                print(BLUE + "VARIANTE: " + ProblemType.VRPTW.name)
                print(BLUE + "DISTANCIA: " + distance_type.name)
                print(BLUE + "HEURÍSTICA DE CONSTRUCCIÓN: " + heuristic_type.name)
                print(BLUE + "COSTO TOTAL: " + str(cost))
                print(BLUE + "TOTAL DE RUTAS: " + str(request_by_route))
                print(BLUE + "TIEMPO DE EJECUCIÓN: " + str(time))
                print(BLUE + " ")
                for j in range(request_by_route):
                    print(
                        BLUE + "R"
                        + str(j + 1)
                        + str(result.get_list_routes()[j].get_list_id_customers())
                        )
                        # print(" ", len(result.get_list_routes()[j].get_list_id_customers()))
                print(BLUE + "------------------------------------------")

    except IOError as e:
        print(e)

def sbrp(number_instance, hc):
    try:
        BLUE = Fore.BLUE
        RED = Fore.RED
        GREEN = Fore.GREEN
        RESET = Fore.RESET

        path_file_original_instance = " "
        path_file_solution_BSS = " "
        if number_instance == '1':
            path_file_original_instance = "instances\\sbrp\\instance_1\\instance-1_B-10_P-100_D-1_MW-20_MBC-15_MVC-25_BSS.json"
            path_file_solution_BSS = "instances\\sbrp\\instance_1\\BSS_solution-110_B-10_P-100_S-metaheuristic_A-evolution_estrategic_BSS.json.json"

        elif number_instance == '2':
            path_file_original_instance = "instances\\sbrp\\instance_23\\instance-23_B-20_P-400_D-1_MW-5_MBC-15_MVC-50_BSS.json"
            path_file_solution_BSS = "instances\\sbrp\\instance_23\\BSS_solution-128_B-120_P-400_S-metaheuristic_A-local_search_BSS.json.json"

        elif number_instance == '3':
            path_file_original_instance = "instances\\sbrp\\instance_4\\instance-4_B-80_P-800_D-1_MW-10_MBC-15_MVC-25_BSS.json"
            path_file_solution_BSS = "instances\\sbrp\\instance_4\\BSS_solution-130_B-72_P-800_S-metaheuristic_A-evolution_estrategic_BSS.json.json"

        heuristic_type = " "
        if hc == '1':
            heuristic_type = HeuristicType.SaveParallel
        elif hc == '2':
            heuristic_type = HeuristicType.Sweep
        elif hc == '3':
            heuristic_type = HeuristicType.RandomMethod

        file_extension = os.path.splitext(path_file_original_instance)[1].lower()

        # total_instances = 5
        load_file = LoadFile()

        distance_type = DistanceType.Euclidean

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
        Problem.get_problem().set_cost_matrix(
            StrategyHeuristic.get_strategy_heuristic().fill_cost_matrix_with_list_distances(list_distances))

        StrategyHeuristic.get_strategy_heuristic().execute_heuristic(20, heuristic_type)
        result = StrategyHeuristic.get_strategy_heuristic().get_best_solution()
        cost = StrategyHeuristic.get_strategy_heuristic().get_total_cost_solution()
        request_by_route = len(StrategyHeuristic.get_strategy_heuristic().get_request_by_route())
        time = StrategyHeuristic.get_strategy_heuristic().get_time_execute()

        if hc == '1':
            """print(GREEN + " ")
            print(GREEN + "------------------------------------------")
            # print("INSTANCIA: P" + (i + 1))
            print(GREEN +  "VARIANTE: " + ProblemType.SBRP.name)
            print(GREEN +  "DISTANCIA: " + distance_type.name)
            print(GREEN +  "HEURÍSTICA DE CONSTRUCCIÓN: " + heuristic_type.name)
            print(GREEN +  "COSTO TOTAL: " + str(cost))
            print(GREEN +  "TOTAL DE RUTAS: " + str(request_by_route))
            print(GREEN +  "TIEMPO DE EJECUCIÓN: " + str(time))
            print(GREEN + " ")
            if heuristic_type == HeuristicType.SaveSequential or heuristic_type == HeuristicType.SaveParallel or heuristic_type == HeuristicType.MatchingBasedSavingAlgorithm or heuristic_type == HeuristicType.KilbyAlgorithm:
                for j in range(request_by_route):
                    bus_stops_by_route = result.get_list_routes()[j].get_list_bus_stops()
                    for k in range(len(bus_stops_by_route)):
                        print(
                            GREEN + "R"
                            + str(j + 1)
                            + str(bus_stops_by_route[k].get_id_bus_stop())
                        )
                    # print(" ", len(result.get_list_routes()[j].get_list_id_customers()))
            else:
                for j in range(request_by_route):
                    print(
                        GREEN + "R"
                        + str(j + 1)
                        + str(result.get_list_routes()[j].get_list_bus_stops())
                    )
                    # print(" ", len(result.get_list_routes()[j].get_list_id_customers()))
            print("------------------------------------------")"""
            output_text = (
                " \n"
                "------------------------------------------\n"
                f"VARIANTE: {ProblemType.SBRP.name}\n"
                f"DISTANCIA: {distance_type.name}\n"
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
            print(GREEN + output_text)

        elif hc == '2':
            print(RED + " ")
            print(RED + "------------------------------------------")
            # print("INSTANCIA: P" + (i + 1))
            print(RED + "VARIANTE: " + ProblemType.SBRP.name)
            print(RED + "DISTANCIA: " + distance_type.name)
            print(RED + "HEURÍSTICA DE CONSTRUCCIÓN: " + heuristic_type.name)
            print(RED + "COSTO TOTAL: " + str(cost))
            print(RED + "TOTAL DE RUTAS: " + str(request_by_route))
            print(RED + "TIEMPO DE EJECUCIÓN: " + str(time))
            print(RED + " ")
            if heuristic_type == HeuristicType.SaveSequential or heuristic_type == HeuristicType.SaveParallel or heuristic_type == HeuristicType.MatchingBasedSavingAlgorithm or heuristic_type == HeuristicType.KilbyAlgorithm:
                for j in range(request_by_route):
                    bus_stops_by_route = result.get_list_routes()[j].get_list_bus_stops()
                    for k in range(len(bus_stops_by_route)):
                        print(
                            RED + "R"
                            + str(j + 1)
                            + str(bus_stops_by_route[k].get_id_bus_stop())
                        )
                    # print(" ", len(result.get_list_routes()[j].get_list_id_customers()))
            else:
                for j in range(request_by_route):
                    print(
                        RED + "R"
                        + str(j + 1)
                        + str(result.get_list_routes()[j].get_list_bus_stops())
                    )
                    # print(" ", len(result.get_list_routes()[j].get_list_id_customers()))
            print("------------------------------------------")

        elif hc == '3':
            print(BLUE + " ")
            print(BLUE + "------------------------------------------")
            # print("INSTANCIA: P" + (i + 1))
            print(BLUE + "VARIANTE: " + ProblemType.SBRP.name)
            print(BLUE + "DISTANCIA: " + distance_type.name)
            print(BLUE + "HEURÍSTICA DE CONSTRUCCIÓN: " + heuristic_type.name)
            print(BLUE + "COSTO TOTAL: " + str(cost))
            print(BLUE + "TOTAL DE RUTAS: " + str(request_by_route))
            print(BLUE + "TIEMPO DE EJECUCIÓN: " + str(time))
            print(BLUE + " ")
            if heuristic_type == HeuristicType.SaveSequential or heuristic_type == HeuristicType.SaveParallel or heuristic_type == HeuristicType.MatchingBasedSavingAlgorithm or heuristic_type == HeuristicType.KilbyAlgorithm:
                for j in range(request_by_route):
                    bus_stops_by_route = result.get_list_routes()[j].get_list_bus_stops()
                    for k in range(len(bus_stops_by_route)):
                        print(
                            BLUE + "R"
                            + str(j + 1)
                            + str(bus_stops_by_route[k].get_id_bus_stop())
                        )
                    # print(" ", len(result.get_list_routes()[j].get_list_id_customers()))
            else:
                for j in range(request_by_route):
                    print(
                        BLUE + "R"
                        + str(j + 1)
                        + str(result.get_list_routes()[j].get_list_bus_stops())
                    )
                    # print(" ", len(result.get_list_routes()[j].get_list_id_customers()))
            print("------------------------------------------")
    except IOError as e:
        print(e)

if __name__ == "__main__":
    main()
