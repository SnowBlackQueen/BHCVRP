package test;
import java.io.*;
import java.lang.reflect.InvocationTargetException;
import java.util.ArrayList;

import cujae.inf.citi.om.data.CustomerType;
import cujae.inf.citi.om.data.Problem;
import cujae.inf.citi.om.data.ProblemType;
import cujae.inf.citi.om.factory.interfaces.AssignmentType;
import cujae.inf.citi.om.factory.interfaces.DistanceType;
import cujae.inf.citi.om.factory.interfaces.HeuristicType;
import cujae.inf.citi.om.generator.controller.StrategyHeuristic;
import cujae.inf.citi.om.generator.solution.Solution;
import cujae.inf.citi.om.heuristic.controller.Controller;
import cujae.inf.citi.om.heuristic.output.Cluster;
import cujae.inf.citi.om.tools.OrderType;
		
public class Main
{
    public static void main(String arg[]) throws IOException, IllegalArgumentException, SecurityException, ClassNotFoundException, InstantiationException, IllegalAccessException, InvocationTargetException, NoSuchMethodException
    {
    	String pathFiles = "C-mdvrp//p"; 
		int totalInstances = 2;
		LoadFile loadFile = new LoadFile();

		/*for(int i = 1; i < totalInstances; i++)
		{*/
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
			
/*			FleetAux fleet = loadFile.loadCountVehiclesFleet();
			int countCustomers = loadFile.loadCountCustomers();
	    	int countDepots = loadFile.loadCountDepots();
	    	ArrayList<Double> capacitiesVehicles = loadFile.loadCapacityVehicles();
	    	ArrayList<CustomerAux> customers = loadFile.loadCustomers();
	    	ArrayList<DepotAux> depots = loadFile.loadDepots();*/
	    	
	    	if(StrategyHeuristic.getStrategyHeuristic().loadProblem(idCustomers, requestCustomers, idDepots, countVehicles.get(0), capacityVehicles.get(0), listDistances, axisXCustomers, axisYCustomers, axisXDepots, axisYDepots, ProblemType.MDVRP, AssignmentType.Sweep))
	    	{
                        StrategyHeuristic.getStrategyHeuristic().executeHeuristic(1, HeuristicType.SaveParallel);
	    		Solution result = StrategyHeuristic.getStrategyHeuristic().getBestSolution();
	    		
	    		System.out.println("------------------------------------------");
	    		//System.out.println("INSTANCIA: P" + (i + 1));
	    		System.out.println("COSTO TOTAL " + StrategyHeuristic.getStrategyHeuristic().getTotalCostSolution());
	    		System.out.println("TOTAL DE RUTAS " + StrategyHeuristic.getStrategyHeuristic().getRequestByRoute().size());
	    		System.out.println("------------------------------------------");
	    	}
			
		//}

    	
    	
    	
    	
    	    	
    	
    	
    
    /*
    	System.out.println("***********************************************Datos del problema*************************************************");
    //	System.out.println("Cantidad de clientes: " + countCustomers);
    	ArrayList<CustomerAux> customers = loadFile.loadCustomers();
    	 	
    	
    	double demandaTotalClientes = 0.0;
    	for(int i = 0; i < customers.size(); i++)
    		demandaTotalClientes += customers.get(i).getRequestCustomer();
    		
    	System.out.println("Demanda total de los clientes: " + demandaTotalClientes);
    	
    	System.out.println("");
    	//System.out.println("Cantidad de dep�sitos: " + countDepots);
    	System.out.println("");
    	
    	ArrayList<DepotAux> depots = loadFile.loadDepots();
    	int cantV =  -1;   	
    	double capV = 0.0;
    	double capTotalDeposito = 0.0;
    	double capTotal = 0.0;
    	for(int m = 0; m < depots.size(); m ++)
    	{
    		System.out.println("Id dep�sito " + (m+1)+ ": " + depots.get(m).getIdDepot());
    		
    		cantV = depots.get(m).getListFleets().get(0).getCountVehicles();
    		System.out.println("Cantidad de veh�culos de la flota: "+ cantV);
    		capV = depots.get(m).getListFleets().get(0).getCapacityVehicle();
    		System.out.println("Capacidad de los veh�culos de la flota: "+ capV);
    		capTotalDeposito = cantV * capV;
    		System.out.println("Capacidad total del dep�sito: " + capTotalDeposito);
    		System.out.println("");
    		capTotal+= capTotalDeposito;
    		
    	}
    	System.out.println("Capacidad total de los dep�sitos: "+ capTotal);
    	System.out.println("");
    	    	
    	ArrayList<Integer> idCustomers = new ArrayList<Integer>();
    	ArrayList<Double> requestCustomers = new ArrayList<Double>();
    	ArrayList<Double> axisXs = new ArrayList<Double>();
    	ArrayList<Double> axisYs = new ArrayList<Double>();
    	
    /*	for(int i = 0; i < countCustomers; i++)
    	{
    		idCustomers.add(customers.get(i).getIdCustomer());
    		requestCustomers.add(customers.get(i).getRequestCustomer());
    		axisXs.add(customers.get(i).getAxisX());
    		axisYs.add(customers.get(i).getAxisY());
    	}
    	
    	ArrayList<Integer> idDepots = new ArrayList<Integer>();
    	ArrayList<Integer> countVehicles = new  ArrayList<Integer>();
    	ArrayList<Double> axisXsDepots = new ArrayList<Double>();
    	ArrayList<Double> axisYsDepots = new ArrayList<Double>();
    	
    	for(int i = 0; i < countDepots; i++)
    	{
    		idDepots.add(depots.get(i).getIdDepot());
    		countVehicles.add(f.getCountVehicles());
    		axisXsDepots.add(depots.get(i).getAxisX());
    		axisYsDepots.add(depots.get(i).getAxisY());
    		
    	*/
    	
    	//ArrayList<ArrayList<Double>> distances = fillListDistances(idCustomers, axisXs, axisYs, idDepots, axisXsDepots, axisYsDepots);    	
   /* 	ArrayList<Integer> aux = new ArrayList<Integer>();
    	ArrayList<Double> aux1 = new ArrayList<Double>();
    	
    	    
//    	StrategyHeuristic.getStrategyHeuristic().loadProblem(idCustomers, requestCustomers, idDepots, countVehicles, capacitiesVehicles, distances, axisXs, axisYs,  axisXsDepots, axisYsDepots, ProblemType.MDVRP, AssignmentType.Kmeans);
    /*	long start = System.currentTimeMillis();
    	StrategyHeuristic.getStrategyHeuristic().loadProblem(idCustomers, requestCustomers,axisXs, 
    			axisYs, aux, idDepots, axisXsDepots, axisYsDepots, countVehicles, 
    			capacitiesVehicles,  aux,  aux1, ProblemType.MDVRP, AssignmentType.PAM, null, DistanceType.Euclidean,  distances);
    	
    	long end = System.currentTimeMillis();
    		/*Para mostrar la asignaci'on*/
    	
      /*  	Solution s = Controller.getController().getSolution();

        	Cluster c = new Cluster();
        	
        	System.out.println("Algoritmo de asignaci�n a ejecutar: " + AssignmentType.PAM);
        	System.out.println("Tiempo" + " " + (end - start) + "ms");
        	
        	for(int j = 0; j < s.getListClusters().size(); j++)
        	{
        		c = s.getListClusters().get(j);
        		System.out.println("");					
        		System.out.println("******************************************Cluster: "+ (j+1)+"******************************************");
        		System.out.println("");
        		System.out.println("Dep�sito: "+ c.getIdDepot());
        		System.out.println("");
        		System.out.println("Demanda satisfecha: " + c.getRequestCluster());
        		System.out.println("");
        		System.out.println("Clientes asignados al cluster "+ (j+1)+ ":");
        		for(int k = 0; k < c.getListIdCustomers().size(); k++)
        		{
        			System.out.print(c.getListIdCustomers().get(k) + ",");
        		}
        		System.out.println("");

        	}
        	
        	if(!s.existUnassigned())
        	{
        		System.out.println("");					
        		System.out.println("******************************************Clientes no Asignados******************************************");

        		for(int m = 0; m < s.getListUnassigned().size(); m++)
        		{
        			System.out.print(s.getListUnassigned().get(m) + ",");
        			System.out.println("");

        		} 
        	}
        	else
        	{
        		System.out.println("");
        		System.out.println("Todos los clientes fueron asignados");
        	}
        	
 //       	start = System.currentTimeMillis();
        	
        	
        	if (Problem.getProblem().getTypeProblem() == ProblemType.MDVRP) {
        	
    		StrategyHeuristic.getStrategyHeuristic().executeHeuristic(1, HeuristicType.SaveParallel);
 //   		end = System.currentTimeMillis();
    		System.out.println("");
    		System.out.println("");
    		System.out.println("");
    		System.out.println("");
    		System.out.println("Algoritmo de planifici�n de la ruta a ejecutar: " + HeuristicType.SaveParallel);
 //   		System.out.println("Tiempo" + " " + (end - start) + "ms");
        	
    		
    		
    		Solution mySolution = StrategyHeuristic.getStrategyHeuristic().getBestSolution();
    		
    		
    		System.out.println("**********************************************************Rutas********************************************************** :" );
			
    		
    		for(int i = 0; i < mySolution.getListRoutes().size(); i++)
    		{
    			System.out.println("");
    			System.out.println("Ruta :" + (i+1));
    			System.out.println("Deposito de la ruta :" + mySolution.getListRoutes().get(i).getIdDepot());
    			System.out.println("Demanda de la ruta :"  + mySolution.getListRoutes().get(i).getRequestRoute());
    			System.out.println("Costo de la ruta :" + mySolution.getListRoutes().get(i).getCostRoute());
    			System.out.println("Id de clientes asignados a la ruta :");
    			for(int j = 0; j < mySolution.getListRoutes().get(i).getListIdCustomers().size(); j++)
    				System.out.println(mySolution.getListRoutes().get(i).getListIdCustomers().get(j) + ",");
    			
    		}
    		
    		System.out.println("Costo de la soluci�n :" + mySolution.getCostSolution());
        	}
        	
        	System.out.println((end - start));
        	
//    		System.out.println("");
//    		System.out.println(" <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<Soluci�n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>");
//    		System.out.println("");
////    		System.out.println("Algoritmo de asignaci�n a ejecutar: "+typeA);
        	
//    		System.out.println("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!ANTES DE ORDENAR!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!");
//    		
//    		for(int m = 0; m < InfoProblem.getProblem().getListIDDepots().size(); m ++)
//        	{
//        		System.out.println("Id dep�sito " + (m+1)+ ": " + InfoProblem.getProblem().getListIDDepots().get(m));
//        		
//        		
//        		System.out.println("Capacidad total del dep�sito: "+ InfoProblem.getProblem().getTotalCapacityByDepot(InfoProblem.getProblem().getListIDDepots().get(m)));
//        		
//        		
//        	}
    		
//    		ArrayList<Integer> list = Controller.getController().randomOrdenate(idDepots);
//    		System.out.println("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!DESPUES DE ORDENAR!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!");
//    		
//    		for(int m = 0; m < list.size(); m ++)
//        	{
//        		System.out.println("Id dep�sito " + (m+1)+ ": " + list.get(m));
//        		
//        		
//        		System.out.println("Capacidad total del dep�sito: "+ InfoProblem.getProblem().getTotalCapacityByDepot(list.get(m)));
//        		
//        		
//        	}
//    		
    		
//    		
//        	
//        	/*Para mostrar la soluci�n*/
//        	Solution s = Controller.getController().getSolution();
//
//        	Cluster c = new Cluster();
//        	
//        	for(int j = 0; j < s.getListClusters().size(); j++)
//        	{
//        		c = s.getListClusters().get(j);
//        		System.out.println("");					
//        		System.out.println("******************************************Cluster: "+ (j+1)+"******************************************");
//        		System.out.println("");
//        		System.out.println("Dep�sito: "+ c.getIdDepot());
//        		System.out.println("");
//        		System.out.println("Demanda satisfecha: " + c.getRequestCluster());
//        		System.out.println("");
//        		System.out.println("Clientes asignados al cluster "+ (j+1)+ ":");
//        		for(int k = 0; k < c.getListIdCustomers().size(); k++)
//        		{
//        			System.out.print(c.getListIdCustomers().get(k) + ",");
//        		}
//        		System.out.println("");
//
//        	}
//        	
//        	if(!s.existUnassignedCustomers())
//        	{
//        		System.out.println("");					
//        		System.out.println("******************************************Clientes no Asignados******************************************");
//
//        		for(int m = 0; m < s.getListUnassignedCustomers().size(); m++)
//        		{
//        			System.out.print(s.getListUnassignedCustomers().get(m) + ",");
//        			System.out.println("");
//
//        		} 
//        	}
//        	else
//        	{
//        		System.out.println("");
//        		System.out.println("Todos los clientes fueron asignados");
//        	}
//        	
//  	}
    	
		//typeA = getTypeAssignment(9);
//		Controller.getController().loadProblem(idCustomers, requestCustomers, idDepots, countVehicles, capacitiesVehicles, distances, typeA);
//		long start = System.currentTimeMillis();
//		Controller.getController().executeAssignment(typeA);
//    	long end = System.currentTimeMillis();
//    	System.out.println("Time" + " " + (end - start) + "ms");

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
	/*
	public static AssignmentType getTypeAssignment(Integer value){
		AssignmentType type = AssignmentType.NearestByCustomer;
		
		switch(value)
		{
		case 0:
			type = AssignmentType.BestNearest;
			break;
		case 1:
			type = AssignmentType.CoefficientPropagation;
			break;
		case 2:
			type = AssignmentType.CyclicAssignment;
			break;
		case 3:
			type = AssignmentType.NearestByCustomer;
			break;
		case 4:
			type = AssignmentType.Parallel;
			break;
		case 5:
			type = AssignmentType.RandomByCustomer;
			break;
		case 6:
			type = AssignmentType.SequentialCyclic;
			break;
		case 7:
			type = AssignmentType.Simplified;
			break;
		case 8:
			type = AssignmentType.Sweep;
			break;
		case 9:
			type = AssignmentType.Kmeans;
			break;
		case 10:
			type = AssignmentType.PAM;
			break;
		case 11:
			type = AssignmentType.UPGMC;
			break;
		}
		
		return type;
	}*/
	
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
