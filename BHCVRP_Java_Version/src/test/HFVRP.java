/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Main.java to edit this template
 */
package test;

import cujae.inf.citi.om.data.ProblemType;
import cujae.inf.citi.om.factory.interfaces.HeuristicType;
import cujae.inf.citi.om.generator.controller.StrategyHeuristic;
import cujae.inf.citi.om.generator.solution.Solution;
import cujae.inf.citi.om.tools.OrderType;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.PrintStream;
import java.lang.reflect.InvocationTargetException;
import java.util.ArrayList;

/**
 *
 * @author kmych
 */
public class HFVRP {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) throws IOException, IllegalArgumentException, SecurityException, ClassNotFoundException, InstantiationException, IllegalAccessException, InvocationTargetException, NoSuchMethodException 
    {
        try {
            FileOutputStream fileOutputStream = new FileOutputStream("/D:/Escuela/BHCVRP/ResultadosHFVRP/Instancia_HFVRP_p14/Resultado_NN20.txt");
            PrintStream printStream = new PrintStream(fileOutputStream);

            System.setOut(printStream);

            String pathFiles = "modified-hfvrp//HFVRP_p14";
                //int totalInstances = 5;
                LoadFile loadFile = new LoadFile();

                //for(int i = 1; i < totalInstances; i++)
                //{
                    loadFile.loadFile(pathFiles); //i + 1

                    ArrayList<Integer> idCustomers = new ArrayList<Integer>();
                    ArrayList<Double> axisXCustomers = new ArrayList<Double>();
                    ArrayList<Double> axisYCustomers = new ArrayList<Double>();
                    ArrayList<Double> requestCustomers = new ArrayList<Double>();

                    ArrayList<Integer> idDepots = new ArrayList<Integer>();
                    ArrayList<Double> axisXDepots = new ArrayList<Double>();
                    ArrayList<Double> axisYDepots = new ArrayList<Double>();
                    ArrayList<ArrayList<Integer>> countVehicles = new ArrayList<ArrayList<Integer>>();
                    ArrayList<ArrayList<Double>> capacityVehicles = new ArrayList<ArrayList<Double>>();

                    ArrayList<ArrayList<Double>> listDistances = new ArrayList<ArrayList<Double>>();

                    loadFile.loadCountVehiclesForDepot(countVehicles);
                    loadFile.loadCapacityVehiclesForHFVRP(capacityVehicles);
                    loadFile.loadCustomers(idCustomers, axisXCustomers, axisYCustomers, requestCustomers);
                    loadFile.loadDepots(idDepots, axisXDepots, axisYDepots);

                    loadFile.fillListDistances(idCustomers, axisXCustomers, axisYCustomers, idDepots, axisXDepots, axisYDepots, listDistances);

                    ProblemType typeProblem = ProblemType.HFVRP;
                    OrderType orderType = OrderType.Descending;
                    HeuristicType heuristicType = HeuristicType.NearestNeighborWithRLC;

                    if(StrategyHeuristic.getStrategyHeuristic().loadHFVRP(idCustomers, requestCustomers, idDepots, 
                            countVehicles.get(0), capacityVehicles.get(0), listDistances, 
                            axisXCustomers, axisYCustomers, axisXDepots, axisYDepots, typeProblem, orderType))
                    {
                                    StrategyHeuristic.getStrategyHeuristic().executeHeuristic(100, heuristicType);
                                    Solution result = StrategyHeuristic.getStrategyHeuristic().getBestSolution();
                                    double cost = StrategyHeuristic.getStrategyHeuristic().getTotalCostSolution();
                                    int requestByRoute = StrategyHeuristic.getStrategyHeuristic().getRequestByRoute().size();
                                    long time = StrategyHeuristic.getStrategyHeuristic().getTimeExecute();

                                    System.out.println(" ");
                                    System.out.println("------------------------------------------");
                                    //System.out.println("INSTANCIA: P" + (i + 1));
                                    System.out.println("CANTIDAD DE EJECUCIONES: " + 100);
                                    System.out.println("HEURÍSTICA DE CONSTRUCCIÓN: " + heuristicType);
                                    System.out.println("COSTO TOTAL: " + cost);
                                    System.out.println("TOTAL DE RUTAS: " + requestByRoute);
                                    System.out.println("TIEMPO DE EJECUCIÓN: " + time + " milisegundos");
                                    //System.out.println("TIEMPO DE EJECUCIÓN: " + time);
                                    System.out.println(" ");
                                    for(int j = 0; j < requestByRoute; j++)
                                        System.out.println("R" + (j+1) + result.getListRoutes().get(j).getListIdCustomers());
                                    System.out.println("------------------------------------------");
                            }
            printStream.close();
            fileOutputStream.close();

            System.setOut(System.out); // Restaurar la salida estándar
            } catch (IOException e) {
                e.printStackTrace();
            }
            //}
    }
    
}
