/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Main.java to edit this template
 */
package test;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import cujae.inf.citi.om.controller.StrategyHeuristic;
import cujae.inf.citi.om.data.ProblemType;
import cujae.inf.citi.om.factory.interfaces.HeuristicType;
import cujae.inf.citi.om.i_o.input.LoadFile;
import cujae.inf.citi.om.i_o.output.ExportResult;
import cujae.inf.citi.om.solution.Route;
import cujae.inf.ic.om.factory.DistanceType;
import java.lang.reflect.InvocationTargetException;
import java.util.HashMap;
import java.util.Map;

/**
 *
 * @author kmych
 */

public class VRPTW {

    public static void main(String[] args) throws IllegalArgumentException, SecurityException, ClassNotFoundException, InstantiationException, IllegalAccessException, InvocationTargetException, NoSuchMethodException, Exception {
        try {
            // Ruta del archivo de entrada
            String pathFiles = "D:\\Escuela\\BHCVRP_Python_Version\\Resultados\\VRPTW\\C1_2_1.txt";

            // Cargar el archivo
            LoadFile loadFile = new LoadFile();
            loadFile.loadFile(pathFiles);

            // Listas para almacenar datos
            ArrayList<Integer> idCustomers = new ArrayList<>();
            ArrayList<Double> axisXCustomers = new ArrayList<>();
            ArrayList<Double> axisYCustomers = new ArrayList<>();
            ArrayList<Double> requestCustomers = new ArrayList<>();

            ArrayList<Integer> idDepots = new ArrayList<>();
            ArrayList<Double> axisXDepots = new ArrayList<>();
            ArrayList<Double> axisYDepots = new ArrayList<>();
            ArrayList<ArrayList<Integer>> countVehicles = new ArrayList<ArrayList<Integer>>();
            ArrayList<ArrayList<Double>> capacityVehicles = new ArrayList<ArrayList<Double>>();

            ArrayList<ArrayList<Double>> listDistances = new ArrayList<>();
            ArrayList<Double> initialNodes = new ArrayList<>();
            ArrayList<Double> endNodes = new ArrayList<>();
            ArrayList<Double> serviceTimes = new ArrayList<>();

            // Cargar datos desde el archivo
            loadFile.loadCountVehiclesForDepot(countVehicles);
            loadFile.loadCapacityVehicles(capacityVehicles);
            loadFile.loadCustomers(idCustomers, axisXCustomers, axisYCustomers, requestCustomers);
            loadFile.loadDepots(idDepots, axisXDepots, axisYDepots);

            DistanceType distanceType = DistanceType.Euclidean;
            loadFile.fillListDistances(
                idCustomers, axisXCustomers, axisYCustomers,
                idDepots, axisXDepots, axisYDepots, listDistances, distanceType
            );

            loadFile.isLoadTimeWindows(initialNodes, endNodes, serviceTimes);

            // Tipo de heurística a utilizar
            HeuristicType heuristicType = HeuristicType.SaveParallel;

            // Ejecutar la heurística
            if (StrategyHeuristic.getStrategyHeuristic().loadVRPTW(
                idCustomers, requestCustomers, idDepots,
                countVehicles.get(0), capacityVehicles.get(0),
                listDistances, axisXCustomers, axisYCustomers,
                axisXDepots, axisYDepots, initialNodes, endNodes,
                serviceTimes, ProblemType.VRPTW
            )) {
                StrategyHeuristic.getStrategyHeuristic().executeHeuristic(1, heuristicType);

                // Obtener resultados
                double cost = StrategyHeuristic.getStrategyHeuristic().getTotalCostSolution();
                int requestByRoute = StrategyHeuristic.getStrategyHeuristic().getRequestByRoute().size();
                double time = StrategyHeuristic.getStrategyHeuristic().getTimeExecute();
                List<Route> routes = StrategyHeuristic.getStrategyHeuristic().getBestSolution().getListRoutes();

                /*// Imprimir resultados
                System.out.println(" ");
                System.out.println("------------------------------------------");
                System.out.println("HEURÍSTICA DE CONSTRUCCIÓN: " + heuristicType.name());
                System.out.println("COSTO TOTAL: " + cost);
                System.out.println("TOTAL DE RUTAS: " + requestByRoute);
                System.out.println("TIEMPO DE EJECUCIÓN: " + time);
                System.out.println(" ");

                for (int j = 0; j < requestByRoute; j++) {
                    System.out.println("R" + (j + 1) + routes.get(j).getListIdCustomers());
                }

                System.out.println("------------------------------------------");*/

                // Exportar resultados en diferentes formatos

                // 1. Exportar a TXT
                StringBuilder outputText = new StringBuilder();
                outputText.append(" \n")
                          .append("------------------------------------------\n")
                          .append("HEURÍSTICA DE CONSTRUCCIÓN: ").append(heuristicType.name()).append("\n")
                          .append("COSTO TOTAL: ").append(cost).append("\n")
                          .append("TOTAL DE RUTAS: ").append(requestByRoute).append("\n")
                          .append("TIEMPO DE EJECUCIÓN: ").append(time).append("\n")
                          .append(" \n");

                for (int j = 0; j < requestByRoute; j++) {
                    outputText.append("R").append(j + 1).append(routes.get(j).getListIdCustomers()).append("\n");
                }

                outputText.append("------------------------------------------\n");

                ExportResult.toTxt(outputText.toString(), "D:\\Escuela\\BHCVRP_Python_Version\\Resultados\\resultado.txt");

                // 2. Exportar a JSON y XML
                Map<String, Object> results = new HashMap<>();
                results.put("heuristic_type", heuristicType.name());
                results.put("total_cost", cost);
                results.put("total_routes", requestByRoute);
                results.put("execution_time", time);

                List<Map<String, Object>> routeList = new ArrayList<>();
                for (int j = 0; j < requestByRoute; j++) {
                    Map<String, Object> routeMap = new HashMap<>();
                    routeMap.put("route_id", j + 1);
                    routeMap.put("customers", routes.get(j).getListIdCustomers());
                    routeList.add(routeMap);
                }
                results.put("routes", routeList);

                ExportResult.toJson(results, "D:\\Escuela\\BHCVRP_Python_Version\\Resultados\\resultado.json");
                ExportResult.toXml(results, "D:\\Escuela\\BHCVRP_Python_Version\\Resultados\\resultado.xml");

                // 3. Exportar a CSV
                List<List<String>> csvData = new ArrayList<>();
                csvData.add(List.of("Tipo de heurística", heuristicType.name()));
                csvData.add(List.of("Costo total", String.valueOf(cost)));
                csvData.add(List.of("Tiempo de ejecución", String.valueOf(time)));
                csvData.add(List.of("Ruta", "Clientes"));

                for (int j = 0; j < requestByRoute; j++) {
                    csvData.add(List.of("R" + (j + 1), routes.get(j).getListIdCustomers().toString()));
                }

                ExportResult.toCsv(csvData, "D:\\Escuela\\BHCVRP_Python_Version\\Resultados\\resultado.csv");
            }

        } catch (IOException e) {
            e.printStackTrace();
        }
    }

}
