/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Main.java to edit this template
 */
package test;

import cujae.inf.citi.om.data.CustomerType;
import cujae.inf.citi.om.data.ProblemType;
import cujae.inf.citi.om.factory.interfaces.DistanceType;
import cujae.inf.citi.om.factory.interfaces.HeuristicType;
import cujae.inf.citi.om.generator.controller.StrategyHeuristic;
import cujae.inf.citi.om.generator.solution.Solution;
import java.io.IOException;
import java.lang.reflect.InvocationTargetException;
import java.util.ArrayList;

/**
 *
 * @author kmych
 */
public class TTRP {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) throws IOException, IllegalArgumentException, SecurityException, ClassNotFoundException, InstantiationException, IllegalAccessException, InvocationTargetException, NoSuchMethodException 
    {
        String pathFiles = "instances-ttrp//TTRP_1.txt";
            //int totalInstances = 5;
            LoadFile loadFile = new LoadFile();

            //for(int i = 1; i < totalInstances; i++)
            //{
                loadFile.loadFile(pathFiles); //i + 1

                ArrayList<Integer> idCustomers = new ArrayList<Integer>();
                ArrayList<Double> axisXCustomers = new ArrayList<Double>();
                ArrayList<Double> axisYCustomers = new ArrayList<Double>();
                ArrayList<Double> requestCustomers = new ArrayList<Double>();
                ArrayList<Integer> typeCustomers = new ArrayList<Integer>();

                ArrayList<Integer> idDepots = new ArrayList<Integer>();
                ArrayList<Double> axisXDepots = new ArrayList<Double>();
                ArrayList<Double> axisYDepots = new ArrayList<Double>();
                ArrayList<Integer> countVehicles = new ArrayList<Integer>();
                ArrayList<Double> capacityVehicles = new ArrayList<Double>();
                ArrayList<Integer> countTrailers = new ArrayList<Integer>();
                ArrayList<Double> capacityTrailers = new ArrayList<Double>();

                ArrayList<ArrayList<Double>> listDistances = new ArrayList<ArrayList<Double>>();

                loadFile.loadCountVehiclesForDepotTTRP(countVehicles);
                loadFile.loadCapacityVehiclesTTRP(capacityVehicles);
                loadFile.loadCountTrailersForDepotTTRP(countTrailers);
                loadFile.loadCapacityTrailersTTRP(capacityTrailers);
                loadFile.loadCustomersTTRP(idCustomers, axisXCustomers, axisYCustomers, requestCustomers, typeCustomers);
                loadFile.loadDepotsTTRP(idDepots, axisXDepots, axisYDepots);

                loadFile.fillListDistances(idCustomers, axisXCustomers, axisYCustomers, idDepots, axisXDepots, axisYDepots, listDistances);

                ArrayList<ArrayList<Integer>> idAssignedCustomers = new ArrayList<ArrayList<Integer>>();
                idAssignedCustomers.add(idCustomers);

                HeuristicType heuristicType = HeuristicType.SaveParallel;
                
                if(heuristicType == HeuristicType.Sweep){
                    if(StrategyHeuristic.getStrategyHeuristic().loadProblem(idCustomers, requestCustomers, axisXCustomers, axisYCustomers,
                            typeCustomers, idDepots, axisXDepots, axisYDepots, idAssignedCustomers, countVehicles, capacityVehicles, 
                            countTrailers, capacityTrailers, ProblemType.TTRP, DistanceType.Euclidean))
                    {
                                StrategyHeuristic.getStrategyHeuristic().executeHeuristic(20, heuristicType);
                                Solution result = StrategyHeuristic.getStrategyHeuristic().getBestSolution();
                                double cost = StrategyHeuristic.getStrategyHeuristic().getTotalCostSolution();
                                int requestByRoute = StrategyHeuristic.getStrategyHeuristic().getRequestByRoute().size();
                                long time = StrategyHeuristic.getStrategyHeuristic().getTimeExecute();

                                System.out.println(" ");
                                System.out.println("------------------------------------------");
                                //System.out.println("INSTANCIA: P" + (i + 1));
                                System.out.println("HEURÍSTICA DE CONSTRUCCIÓN: " + heuristicType);
                                System.out.println("COSTO TOTAL: " + cost);
                                System.out.println("TOTAL DE RUTAS: " + requestByRoute);
                                //System.out.println("TIEMPO DE EJECUCIÓN: " + time);
                                System.out.println(" ");
                                for(int j = 0; j < requestByRoute; j++)
                                    System.out.println("R" + (j+1) + result.getListRoutes().get(j).getListIdCustomers());
                                System.out.println("------------------------------------------");
                    }
                    
                }
                else{
                    if(StrategyHeuristic.getStrategyHeuristic().loadProblem(idCustomers, requestCustomers, typeCustomers, idDepots, idAssignedCustomers, countVehicles, capacityVehicles, countTrailers, capacityTrailers, listDistances, ProblemType.TTRP))
                        {
                                StrategyHeuristic.getStrategyHeuristic().executeHeuristic(20, heuristicType);
                                Solution result = StrategyHeuristic.getStrategyHeuristic().getBestSolution();
                                double cost = StrategyHeuristic.getStrategyHeuristic().getTotalCostSolution();
                                int requestByRoute = StrategyHeuristic.getStrategyHeuristic().getRequestByRoute().size();
                                long time = StrategyHeuristic.getStrategyHeuristic().getTimeExecute();

                                System.out.println(" ");
                                System.out.println("------------------------------------------");
                                //System.out.println("INSTANCIA: P" + (i + 1));
                                System.out.println("HEURÍSTICA DE CONSTRUCCIÓN: " + heuristicType);
                                System.out.println("COSTO TOTAL: " + cost);
                                System.out.println("TOTAL DE RUTAS: " + requestByRoute);
                                //System.out.println("TIEMPO DE EJECUCIÓN: " + time);
                                System.out.println(" ");
                                for(int j = 0; j < requestByRoute; j++)
                                    System.out.println("R" + (j+1) + result.getListRoutes().get(j).getListIdCustomers());
                                System.out.println("------------------------------------------");
                        }
                }
                
    }
    
}
