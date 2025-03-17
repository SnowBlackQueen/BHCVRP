/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Main.java to edit this template
 */
package test;

import cujae.inf.citi.om.controller.StrategyHeuristic;
import cujae.inf.citi.om.data.Customer;
import cujae.inf.citi.om.data.Depot;
import cujae.inf.citi.om.data.Problem;
import cujae.inf.citi.om.data.ProblemType;
import cujae.inf.citi.om.factory.interfaces.HeuristicType;
import cujae.inf.citi.om.i_o.input.LoadFile;
import cujae.inf.citi.om.i_o.output.ExportResult;
import cujae.inf.citi.om.solution.Solution;
import cujae.inf.ic.om.factory.DistanceType;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.PrintStream;
import java.lang.reflect.InvocationTargetException;
import java.util.ArrayList;
import java.util.Map;

/**
 *
 * @author kmych
 */
public class OVRP {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) throws IOException, IllegalArgumentException, SecurityException, ClassNotFoundException, InstantiationException, IllegalAccessException, InvocationTargetException, NoSuchMethodException, Exception 
    {
        try {
            String pathFiles = "D:/Escuela/BHCVRP/resources/instances/cvrp/CVRP_1";
            String pathFileResult = "D:/Escuela/BHCVRP/resources/results/ovrp/result_c1R1";

            // Obtener la extensión del archivo
            String fileExtension = pathFiles.substring(pathFiles.lastIndexOf(".")).toLowerCase();

            LoadFile loadFile = new LoadFile();
            ArrayList<Integer> idCustomers = new ArrayList<>();
            ArrayList<Double> axisXCustomers = new ArrayList<>();
            ArrayList<Double> axisYCustomers = new ArrayList<>();
            ArrayList<Double> requestCustomers = new ArrayList<>();

            ArrayList<Integer> idDepots = new ArrayList<>();
            ArrayList<Double> axisXDepots = new ArrayList<>();
            ArrayList<Double> axisYDepots = new ArrayList<>();
            ArrayList<ArrayList<Integer>> countVehicles = new ArrayList<>();
            ArrayList<ArrayList<Double>> capacityVehicles = new ArrayList<>();

            ArrayList<ArrayList<Double>> listDistances = new ArrayList<>();
            DistanceType distanceType = DistanceType.Euclidean;
            HeuristicType heuristicType = HeuristicType.RandomMethod;

            // Validar si el archivo es .txt o .json
            if (fileExtension.equals(".json")) {
                // Cargar archivo .json usando el método creado anteriormente
                Problem problemInstance = loadFile.loadCVRPFromJson(pathFiles);
                if (problemInstance != null) {
                    idCustomers = problemInstance.getListIDCustomers();
                    for (int i = 0; i < idCustomers.size(); i++) {
                        Customer customer = problemInstance.getListCustomers().get(i);
                        axisXCustomers.add(customer.getLocationCustomer().getAxisX());
                        axisYCustomers.add(customer.getLocationCustomer().getAxisY());
                        requestCustomers.add(customer.getRequestCustomer());
                    }

                    Depot depot = problemInstance.getListDepots().get(0);
                    idDepots.add(depot.getIdDepot());
                    axisXDepots.add(depot.getLocationDepot().getAxisX());
                    axisYDepots.add(depot.getLocationDepot().getAxisY());
                    
                    ArrayList<Integer> cv = problemInstance.getListCountVehicles();
                    ArrayList<Double> capV = problemInstance.getListCapacityVehicles();
                    
                    countVehicles.add(cv);
                    capacityVehicles.add(capV);
                    
                }
            } else {
                loadFile.loadFile(pathFiles); // i + 1

                loadFile.loadCountVehiclesForDepot(countVehicles);
                loadFile.loadCapacityVehicles(capacityVehicles);
                loadFile.loadCustomers(idCustomers, axisXCustomers, axisYCustomers, requestCustomers);
                loadFile.loadDepots(idDepots, axisXDepots, axisYDepots);
            }

            loadFile.fillListDistances(
                    idCustomers,
                    axisXCustomers,
                    axisYCustomers,
                    idDepots,
                    axisXDepots,
                    axisYDepots,
                    listDistances,
                    distanceType
            );

            if (StrategyHeuristic.getStrategyHeuristic().loadCVRP(
                    idCustomers,
                    requestCustomers,
                    idDepots,
                    countVehicles.get(0),
                    capacityVehicles.get(0),
                    listDistances,
                    axisXCustomers,
                    axisYCustomers,
                    axisXDepots,
                    axisYDepots,
                    ProblemType.OVRP
            )) {
                    StrategyHeuristic.getStrategyHeuristic().executeHeuristic(1, heuristicType);
                    Solution result = StrategyHeuristic.getStrategyHeuristic().getBestSolution();
                    double cost = StrategyHeuristic.getStrategyHeuristic().getTotalCostSolution();
                    int requestByRoute = StrategyHeuristic.getStrategyHeuristic().getRequestByRoute().size();
                    long time = StrategyHeuristic.getStrategyHeuristic().getTimeExecute();

                    // Para formato TXT
                    StringBuilder outputText = new StringBuilder();
                    outputText.append(" \n")
                            .append("------------------------------------------\n")
                            .append("DISTANCIA: ").append(distanceType.name()).append("\n")
                            .append("HEURÍSTICA DE CONSTRUCCIÓN: ").append(heuristicType.name()).append("\n")
                            .append("COSTO TOTAL: ").append(cost).append("\n")
                            .append("TOTAL DE RUTAS: ").append(requestByRoute).append("\n")
                            .append("TIEMPO DE EJECUCIÓN: ").append(time).append("\n")
                            .append(" \n");

                    // Agregar las rutas al texto
                    for (int j = 0; j < requestByRoute; j++) {
                        outputText.append("R").append(j + 1)
                                .append(result.getListRoutes().get(j).getListIdCustomers()).append("\n");
                    }

                    outputText.append("------------------------------------------\n");

                    // Exportar resultados en diferentes formatos
                    String fullPath = pathFileResult + ".txt";
                    ExportResult.toTxt(outputText.toString(), fullPath);

                    // Para formato JSON y XML
                    // Recopilar resultados en un diccionario
                    ArrayList<Object> routes = new ArrayList<>();
                    for (int j = 0; j < requestByRoute; j++) {
                        // Crear una copia final de j para usarla en la clase anónima
                        final int routeId = j + 1;
                        final ArrayList<Integer> route_customers = result.getListRoutes().get(j).getListIdCustomers();

                        routes.add(new Object() {
                            public final int route_id = routeId; // Usar la copia final
                            public final ArrayList<Integer> customers = route_customers; // Usar la copia final
                        });
                    }

                    Object results = new Object() {
                        public final String distance_type = distanceType.name();
                        public final String heuristic_type = heuristicType.name();
                        public final double total_cost = cost;
                        public final int total_routes = requestByRoute;
                        public final long execution_time = time;
                        public final ArrayList<Object> final_routes = routes;
                    };

                    fullPath = pathFileResult + ".json";
                    ExportResult.toJson((Map<String, Object>) results, fullPath);
                    fullPath = pathFileResult + ".xml";
                    ExportResult.toXml((Map<String, Object>) results, fullPath);

                    // Para formato CSV
                    // Crear una lista de listas para el CSV
                    ArrayList<ArrayList<String>> csvData = new ArrayList<>();
                    csvData.add(new ArrayList<String>() {{
                        add("Tipo de distancia");
                        add(distanceType.name());
                    }});
                    csvData.add(new ArrayList<String>() {{
                        add("Tipo de heurística");
                        add(heuristicType.name());
                    }});
                    csvData.add(new ArrayList<String>() {{
                        add("Costo total");
                        add(String.valueOf(cost));
                    }});
                    csvData.add(new ArrayList<String>() {{
                        add("Tiempo de ejecución");
                        add(String.valueOf(time));
                    }});
                    csvData.add(new ArrayList<String>() {{
                        add("Ruta");
                        add("Clientes");
                    }});

                    // Agregar las rutas
                    for (int j = 0; j < requestByRoute; j++) {
                        // Crear una lista explícita para la ruta actual
                        ArrayList<String> routeData = new ArrayList<>();
                        routeData.add("R" + (j + 1)); // Número de ruta
                        routeData.add(result.getListRoutes().get(j).getListIdCustomers().toString()); // Clientes

                        // Agregar la lista a csvData
                        csvData.add(routeData);
                    }

                    // Exportar a CSV
                    fullPath = pathFileResult + ".csv";
                    ExportResult.toCsv(csvData, fullPath);
                }
            
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
