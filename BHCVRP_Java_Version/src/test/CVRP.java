/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Main.java to edit this template
 */
package test;

import cujae.inf.citi.om.factory.interfaces.HeuristicType;
import cujae.inf.citi.om.generator.controller.StrategyHeuristic;
import cujae.inf.citi.om.generator.solution.Solution;
import java.io.IOException;
import java.lang.reflect.InvocationTargetException;
import java.util.ArrayList;
import cujae.inf.citi.om.data.ProblemType;
import java.io.FileOutputStream;
import java.io.PrintStream;

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
        try {
            FileOutputStream fileOutputStream = new FileOutputStream("/D:/Escuela/BHCVRP/ResultadosCVRP/Instancia_CVRP_4/Resultado_SaveSequential21.txt");
            PrintStream printStream = new PrintStream(fileOutputStream);

            System.setOut(printStream);
        
            String pathFiles = "modified-cvrp//CVRP_4";
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
                loadFile.loadCapacityVehicles(capacityVehicles);
                loadFile.loadCustomers(idCustomers, axisXCustomers, axisYCustomers, requestCustomers);
                loadFile.loadDepots(idDepots, axisXDepots, axisYDepots);

                loadFile.fillListDistances(idCustomers, axisXCustomers, axisYCustomers, idDepots, axisXDepots, axisYDepots, listDistances);


                HeuristicType heuristicType = HeuristicType.SaveSequential;

                if(StrategyHeuristic.getStrategyHeuristic().loadCVRP(idCustomers, requestCustomers, idDepots, countVehicles.get(0), capacityVehicles.get(0), listDistances, axisXCustomers, axisYCustomers, axisXDepots, axisYDepots, ProblemType.CVRP))
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
            printStream.close();
            fileOutputStream.close();

            System.setOut(System.out); // Restaurar la salida estándar
            } catch (IOException e) {
                e.printStackTrace();
            }
            //}
    }
    
    public static ArrayList<ArrayList<Double>> fillListDistances(ArrayList<Integer> idCustomers, ArrayList<Double> axisXCustomers, ArrayList<Double> axisYCustomers, ArrayList<Integer> idDepots, ArrayList<Double> axisXDepots, ArrayList<Double> axisYDepots) throws IllegalArgumentException, SecurityException, ClassNotFoundException, InstantiationException, IllegalAccessException, InvocationTargetException, NoSuchMethodException{
    	ArrayList<ArrayList<Double>> listDistances = new ArrayList<ArrayList<Double>>();

    	//int size = idCustomers.size() + idDepots.size(); 

    	for(int i = 0; i < idCustomers.size(); i++)
    	{	    	
    		ArrayList<Double> distancesFromCustomers = new ArrayList<Double>();
    		
    		for(int j = 0; j < idCustomers.size(); j++)
    			distancesFromCustomers.add(calculateDistance(axisXCustomers.get(j), axisYCustomers.get(j), axisXCustomers.get(i), axisYCustomers.get(i)));

    		for(int k = 0; k < idDepots.size(); k++)
     			distancesFromCustomers.add(calculateDistance(axisXDepots.get(k), axisYDepots.get(k), axisXCustomers.get(i), axisYCustomers.get(i)));

    		listDistances.add(distancesFromCustomers);//hasta aqui voy a tener la lista de distancias llena de cada cliente y deposito a los clientes
    		
    	}

    	for(int i = 0; i < idDepots.size(); i++)
    	{
    		ArrayList<Double> distancesFromCustomers = new ArrayList<Double>();
    		
    		for(int j = 0; j < idCustomers.size(); j++)
    			distancesFromCustomers.add(calculateDistance(axisXCustomers.get(j), axisYCustomers.get(j), axisXDepots.get(i), axisYDepots.get(i)));

    		for(int k = 0; k < idDepots.size(); k++)
    			distancesFromCustomers.add(calculateDistance(axisXDepots.get(k), axisYDepots.get(k), axisXDepots.get(i), axisYDepots.get(i)));

    		listDistances.add(distancesFromCustomers);//ya aqui la voy a tener llena completa
    	}
    	return listDistances;
    }

	public static Double calculateDistance(double axisXStart, double axisYStart, double axisXEnd, double axisYEnd) {
		double distance = 0.0;
		double axisX = 0.0;
		double axisY = 0.0;
		
		axisX = Math.pow((axisXStart - axisXEnd), 2);
		axisY = Math.pow((axisYStart - axisYEnd), 2);
		distance = Math.sqrt((axisX + axisY));
		
		return distance;
	}
        
        public static int getPosElement(int idElement, ArrayList<Integer> listCustomers, ArrayList<Integer> listDepots){
		int i = 0;
		boolean found = false;
		int posElement = -1;
		
		while ((i < listDepots.size()) && (!found)) 
		{
			if (listDepots.get(i) == idElement) 
			{
				posElement = i + listCustomers.size();
				found = true;
			} 
			else
				i++;
		}

		i = 0;
		while ((i < listCustomers.size()) && (!found)) 
		{
			if (listCustomers.get(i) == idElement) 
			{
				posElement = i;
				found = true;
			} 
			else
				i++;
		}
		
		return posElement;
	}
        
}
