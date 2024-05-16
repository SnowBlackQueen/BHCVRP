/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Main.java to edit this template
 */
package test;

import cujae.inf.citi.om.data.ProblemType;
import cujae.inf.citi.om.factory.interfaces.AssignmentType;
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
public class CVRP {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) throws IOException, IllegalArgumentException, SecurityException, ClassNotFoundException, InstantiationException, IllegalAccessException, InvocationTargetException, NoSuchMethodException 
    {
        String pathFiles = "modified-cvrp//p";
        int totalInstances = 5;
        LoadFile loadFile = new LoadFile();
        
        //for(int i = 1; i < totalInstances; i++)
	//{
            loadFile.loadFile(pathFiles + (3)); //i + 1
			
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
            loadFile.loadCapacityVehicles(capacityVehicles);
            loadFile.loadCustomers(idCustomers, axisXCustomers, axisYCustomers, requestCustomers);
            loadFile.loadDepots(idDepots, axisXDepots, axisYDepots);

            loadFile.fillListDistances(idCustomers, axisXCustomers, axisYCustomers, idDepots, axisXDepots, axisYDepots, listDistances);

			
	    	
	    if(StrategyHeuristic.getStrategyHeuristic().loadProblem(idCustomers, requestCustomers, idDepots, countVehicles.get(0), capacityVehicles.get(0), listDistances, axisXCustomers, axisYCustomers, axisXDepots, axisYDepots, ProblemType.CVRP, AssignmentType.Sweep))
	    {
                StrategyHeuristic.getStrategyHeuristic().executeHeuristic(1, HeuristicType.SaveParallel);
                Solution result = StrategyHeuristic.getStrategyHeuristic().getBestSolution();
                double cost = StrategyHeuristic.getStrategyHeuristic().getTotalCostSolution();
                int requestByRoute = StrategyHeuristic.getStrategyHeuristic().getRequestByRoute().size();
	    		
	    	System.out.println("------------------------------------------");
	    	//System.out.println("INSTANCIA: P" + (i + 1));
	    	System.out.println("COSTO TOTAL " + cost);
	    	System.out.println("TOTAL DE RUTAS " + requestByRoute);
                for(int j = 0; j < requestByRoute; j++)
                    System.out.println(result.getListRoutes().get(j).getListIdCustomers());
                System.out.println("------------------------------------------");
	    }
			
	//}
    }
    
}
