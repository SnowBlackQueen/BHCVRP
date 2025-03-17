/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package cujae.inf.citi.om.i_o.input;

import cujae.inf.citi.om.data.BusStop;
import cujae.inf.citi.om.data.Customer;
import cujae.inf.citi.om.data.CustomerTTRP;
import cujae.inf.citi.om.data.Depot;
import cujae.inf.citi.om.data.Fleet;
import cujae.inf.citi.om.data.FleetTTRP;
import cujae.inf.citi.om.data.Location;
import cujae.inf.citi.om.data.Problem;
import cujae.inf.citi.om.data.TimeWindow;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.regex.Pattern;
import java.util.regex.Matcher;
import org.json.JSONArray;
import org.json.JSONObject;
import org.json.JSONTokener;

import cujae.inf.citi.om.i_o.input.CustomerAux;
import cujae.inf.citi.om.i_o.input.CustomerTTRPAux;
import cujae.inf.citi.om.i_o.input.DepotAux;
import cujae.inf.citi.om.i_o.input.FleetAux;
import cujae.inf.citi.om.i_o.input.FleetTTRPAux;
import cujae.inf.ic.om.distance.IDistance;
import cujae.inf.ic.om.factory.DistanceType;
import cujae.inf.ic.om.factory.interfaces.IFactoryDistance;
import cujae.inf.ic.om.factory.methods.FactoryDistance;
import java.io.LineNumberReader;
import java.lang.reflect.InvocationTargetException;
import java.util.StringTokenizer;

/**
 *
 * @author kmych
 */

public class LoadFile {

    private ArrayList<String> instanceFile;

	public LoadFile() {
		super();
		instanceFile = new ArrayList<String>();
		// TODO Auto-generated constructor stub
	}

	public ArrayList<String> getInstanceFile() {
		return instanceFile;
	}

	public void setInstanceFile(ArrayList<String> instanceFile) {
		this.instanceFile = instanceFile;
	}

	public boolean findEndElement(String lines){
		return lines.indexOf("EOF") != -1;

	}
	
	public boolean loadFile(String pathFile) throws IOException{
		boolean load = false;
		LineNumberReader line = new LineNumberReader(new FileReader(pathFile));
		String cad = new String();
		instanceFile = new ArrayList<String>();
		instanceFile.clear();
							
		while(!findEndElement(cad))
		{
			cad = line.readLine();
			if(cad != null){
				instanceFile.add(cad);
				load = true;
			}
			else{
				load = false;
				break;
			}
		}
		line.close();
		
		return load;
	}

	public void loadCountVehiclesForDepot(ArrayList<ArrayList<Integer>> countVehicles){
		StringTokenizer tool = new StringTokenizer(instanceFile.get(0), " ");	
		int totalVehicles = Integer.valueOf(tool.nextToken());
		int totalDepots = loadTotalDepots();
		
		ArrayList<Integer> countFleet = new ArrayList<Integer>();
		countFleet.add(totalVehicles);
		
		for(int i = 0; i < totalDepots; i++)
			countVehicles.add(countFleet);
	}
        
        public void loadCountVehiclesForDepotTTRP(ArrayList<Integer> countVehicles){
		StringTokenizer tool = new StringTokenizer(instanceFile.get(0), " ");
                tool.nextToken();
		tool.nextToken();
                tool.nextToken();
		int totalVehicles = Integer.valueOf(tool.nextToken());
		int totalDepots = 1;
		
		for(int i = 0; i < totalDepots; i++)
			countVehicles.add(totalVehicles);
	}
        
        public void loadCountTrailersForDepotTTRP(ArrayList<Integer> countTrailers){
		StringTokenizer tool = new StringTokenizer(instanceFile.get(0), " ");
                tool.nextToken();
		tool.nextToken();
                tool.nextToken();
                tool.nextToken();
		int totalTrailers = Integer.valueOf(tool.nextToken());
		int totalDepots = 1;
		
		for(int i = 0; i < totalDepots; i++)
			countTrailers.add(totalTrailers);
	}
	
	public int loadTotalCustomers(){
		StringTokenizer tool = new StringTokenizer(instanceFile.get(0), " ");
		tool.nextToken();
		return Integer.valueOf(tool.nextToken());
	}
        
        public int loadTotalCustomersTTRP(){
		StringTokenizer tool = new StringTokenizer(instanceFile.get(0), " ");
		tool.nextToken();
		tool.nextToken();
		return Integer.valueOf(tool.nextToken());
	}
	
	public int loadTotalDepots(){
		StringTokenizer tool = new StringTokenizer(instanceFile.get(0), " ");
		tool.nextToken();
		tool.nextToken();
		return Integer.valueOf(tool.nextToken());
	}
	
	public void loadCapacityVehicles(ArrayList<ArrayList<Double>> capacityVehicles){
		int totalDepots = loadTotalDepots();
		
		for(int i = 1; i < (totalDepots + 1); i++)		
		{
			StringTokenizer tool = new StringTokenizer(instanceFile.get(i), " ");
			ArrayList<Double> capacityFleet = new ArrayList<Double>();
			capacityFleet.add(Double.valueOf(tool.nextToken()));
			capacityVehicles.add(capacityFleet);
		}
	}
        
        public void loadCapacityVehiclesTTRP(ArrayList<Double> capacityVehicles){
		int totalDepots = 1;
		
		for(int i = 1; i < (totalDepots + 1); i++)		
		{
			StringTokenizer tool = new StringTokenizer(instanceFile.get(0), " ");
			capacityVehicles.add(Double.valueOf(tool.nextToken()));
		}
	}
        
        public void loadCapacityTrailersTTRP(ArrayList<Double> capacityTrailers){
		int totalDepots = 1;
		
		for(int i = 1; i < (totalDepots + 1); i++)		
		{
			StringTokenizer tool = new StringTokenizer(instanceFile.get(0), " ");
                        tool.nextToken();
			capacityTrailers.add(Double.valueOf(tool.nextToken()));
		}
	}
        
        public void loadCapacityVehiclesForHFVRP(ArrayList<ArrayList<Double>> capacityVehicles){
            StringTokenizer tool = new StringTokenizer(instanceFile.get(1), " ");
            ArrayList<Double> capacityFleet = new ArrayList<>();
            while (tool.hasMoreTokens()) {
                capacityFleet.add(Double.valueOf(tool.nextToken()));
            }
            
            capacityVehicles.add(capacityFleet);

//            // Dividir las capacidades de los vehículos en sublistas según la cantidad de vehículos por depósito
//            int startIndex = 0;
//            for (ArrayList<Integer> countList : countVehicles) {
//                int endIndex = startIndex + countList.size();
//                capacityVehicles.add(new ArrayList<>(capacityFleet.subList(startIndex, endIndex)));
//                startIndex = endIndex;
//            }
        }

	public void loadCustomers(ArrayList<Integer> idCustomers, ArrayList<Double> axisXCustomers, ArrayList<Double> axisYCustomers, ArrayList<Double> requestCustomers){		
		int totalCustomers = loadTotalCustomers();
		int totalDepots = loadTotalDepots();
		
		for(int i = (totalDepots + 1); i < (totalCustomers + totalDepots + 1); i++)		
		{
			StringTokenizer tool = new StringTokenizer(instanceFile.get(i), " ");
			idCustomers.add(Integer.valueOf(tool.nextToken()));
			axisXCustomers.add(Double.valueOf(tool.nextToken()));
			axisYCustomers.add(Double.valueOf(tool.nextToken()));
			requestCustomers.add(Double.valueOf(tool.nextToken()));
		}
	}
        
        public void loadCustomersTTRP(ArrayList<Integer> idCustomers, ArrayList<Double> axisXCustomers, ArrayList<Double> axisYCustomers, ArrayList<Double> requestCustomers, ArrayList<Integer> typeCustomers){		
		int totalCustomers = loadTotalCustomersTTRP();
		int totalDepots = 1;
		
		for(int i = (totalDepots + 1); i < (totalCustomers + totalDepots + 1); i++)		
		{
			StringTokenizer tool = new StringTokenizer(instanceFile.get(i), " ");
			idCustomers.add(Integer.valueOf(tool.nextToken()));
			axisXCustomers.add(Double.valueOf(tool.nextToken()));
			axisYCustomers.add(Double.valueOf(tool.nextToken()));
			requestCustomers.add(Double.valueOf(tool.nextToken()));
                        typeCustomers.add(Integer.valueOf(tool.nextToken()));
		}
	}

	public void loadDepots(ArrayList<Integer> idDepots, ArrayList<Double> axisXDepots, ArrayList<Double> axisYDepots){		
		int totalCustomers = loadTotalCustomers();
		int totalDepots = loadTotalDepots();
		
		for(int i = (totalDepots + totalCustomers + 1); i < instanceFile.size(); i++)		
		{
			StringTokenizer tool = new StringTokenizer(instanceFile.get(i), " ");
			idDepots.add(Integer.valueOf(tool.nextToken()));
			axisXDepots.add(Double.valueOf(tool.nextToken()));
			axisYDepots.add(Double.valueOf(tool.nextToken()));
		}
	}
        
        public void loadDepotsTTRP(ArrayList<Integer> idDepots, ArrayList<Double> axisXDepots, ArrayList<Double> axisYDepots){		
		StringTokenizer tool = new StringTokenizer(instanceFile.get(1), " ");
		idDepots.add(Integer.valueOf(tool.nextToken()));
		axisXDepots.add(Double.valueOf(tool.nextToken()));
		axisYDepots.add(Double.valueOf(tool.nextToken()));
		
	}
	
    
    public void fillListDistances(ArrayList<Integer> idCustomers, ArrayList<Double> axisXCustomers, ArrayList<Double> axisYCustomers, ArrayList<Integer> idDepots, ArrayList<Double> axisXDepots, ArrayList<Double> axisYDepots, ArrayList<ArrayList<Double>> listDistances, DistanceType typeDistance) throws IllegalArgumentException, SecurityException, ClassNotFoundException, InstantiationException, IllegalAccessException, InvocationTargetException, NoSuchMethodException, Exception{
    	int totalCustomers = idCustomers.size();
    	int totalDepots = idDepots.size();
        IDistance distance = newDistance(typeDistance);
    	
    	for(int i = 0; i < totalCustomers; i++)
    	{	    	
    		ArrayList<Double> distancesFromCustomers = new ArrayList<Double>();

    		for(int j = 0; j < totalCustomers; j++)
    			distancesFromCustomers.add(distance.calculateDistance(axisXCustomers.get(j), axisYCustomers.get(j), axisXCustomers.get(i), axisYCustomers.get(i)));

    		for(int k = 0; k < totalDepots; k++)
    			distancesFromCustomers.add(distance.calculateDistance(axisXDepots.get(k), axisYDepots.get(k), axisXCustomers.get(i), axisYCustomers.get(i)));

    		listDistances.add(distancesFromCustomers);//hasta aqui voy a tener la lista de distancias llena de cada cliente y deposito a los clientes
    	}

    	for(int i = 0; i < totalDepots; i++)
    	{
    		ArrayList<Double> distancesFromCustomers = new ArrayList<Double>();

    		for(int j = 0; j < totalCustomers; j++)
    			distancesFromCustomers.add(distance.calculateDistance(axisXCustomers.get(j), axisYCustomers.get(j), axisXDepots.get(i), axisYDepots.get(i)));

    		for(int k = 0; k < totalDepots; k++)
    			distancesFromCustomers.add(distance.calculateDistance(axisXDepots.get(k), axisYDepots.get(k), axisXDepots.get(i), axisYDepots.get(i)));

    		listDistances.add(distancesFromCustomers);//ya aqui la voy a tener llena completa
    	}
    }

	public FleetAux loadCountVehiclesFleet(){
		FleetAux fleet = new FleetAux();
		StringTokenizer tool = new StringTokenizer(instanceFile.get(0), " ");
		
		fleet.setCountVehicles(Integer.valueOf(tool.nextToken()));
		return fleet;
	}
        
        public FleetTTRPAux loadCountVehiclesTTRPFleet(){
		FleetTTRPAux fleet = new FleetTTRPAux();
		StringTokenizer tool = new StringTokenizer(instanceFile.get(0), " ");
		tool.nextToken();
                tool.nextToken();
                tool.nextToken();
		fleet.setCountVehicles(Integer.valueOf(tool.nextToken()));
                fleet.setCountTrailers(Integer.valueOf(tool.nextToken()));
		return fleet;
	}
	
	public int loadCountCustomers(){
		StringTokenizer tool = new StringTokenizer(instanceFile.get(0), " ");	
		tool.nextToken();
		return Integer.valueOf(tool.nextToken());

	}

	public int loadCountDepots(){
	StringTokenizer tool = new StringTokenizer(instanceFile.get(0), " ");
	tool.nextToken();
	tool.nextToken();
	
	return Integer.valueOf(tool.nextToken());
	
	}
	
	public ArrayList<Double> loadCapacityVehicles(){
		ArrayList<Double> capacityVehicles = new ArrayList<Double>();
		
		for(int i = 1; i < (loadCountDepots() + 1); i++)		
		{
			StringTokenizer tool = new StringTokenizer(instanceFile.get(i), " ");
			capacityVehicles.add(Double.valueOf(tool.nextToken()));
			
		}
		return capacityVehicles;
	}
	
	public ArrayList<CustomerAux> loadCustomers(){		
		ArrayList<CustomerAux> listCustomer = new ArrayList<CustomerAux>();
		
		for(int i = loadCountDepots() + 1; i < loadCountCustomers() + loadCountDepots() + 1; i++)		
		{
			StringTokenizer tool = new StringTokenizer(instanceFile.get(i), " ");
			
			CustomerAux customer = new CustomerAux();	
			customer.setIdCustomer(Integer.valueOf(tool.nextToken()));
			customer.setAxisX(Double.valueOf(tool.nextToken()));
			customer.setAxisY(Double.valueOf(tool.nextToken()));
			customer.setRequestCustomer(Double.valueOf(tool.nextToken()));
			
			listCustomer.add(customer);
		}
		return listCustomer;
	}
        
        public ArrayList<CustomerTTRPAux> loadCustomersTTRP(){		
		ArrayList<CustomerTTRPAux> listCustomer = new ArrayList<CustomerTTRPAux>();
		
		for(int i = loadCountDepots() + 1; i < loadCountCustomers() + loadCountDepots() + 1; i++)		
		{
			StringTokenizer tool = new StringTokenizer(instanceFile.get(i), " ");
			
			CustomerTTRPAux customer = new CustomerTTRPAux();	
			customer.setIdCustomer(Integer.valueOf(tool.nextToken()));
			customer.setAxisX(Double.valueOf(tool.nextToken()));
			customer.setAxisY(Double.valueOf(tool.nextToken()));
			customer.setRequestCustomer(Double.valueOf(tool.nextToken()));
                        customer.setTypeCustomer(Integer.valueOf(tool.nextToken()));
			
			listCustomer.add(customer);
		}
		return listCustomer;
	}
        
	
	public ArrayList<DepotAux> loadDepots(){		
		ArrayList<DepotAux> listDepots = new ArrayList<DepotAux>();
		
		for(int i = loadCountDepots() + loadCountCustomers() + 1; i < (instanceFile.size()); i++)		
		{
			StringTokenizer tool = new StringTokenizer(instanceFile.get(i), " ");
			
			DepotAux depot = new DepotAux();	
			depot.setIdDepot(Integer.valueOf(tool.nextToken()));
			depot.setAxisX(Double.valueOf(tool.nextToken()));
			depot.setAxisY(Double.valueOf(tool.nextToken()));
			listDepots.add(depot);
		}
		
		ArrayList<Double> listCapacities = loadCapacityVehicles();
		
		for(int j = 0; j < listDepots.size(); j++)
		{
			FleetAux fleet = loadCountVehiclesFleet();
			fleet.setCapacityVehicle(listCapacities.get(j));
			listDepots.get(j).getListFleets().add(fleet);
		}
		return listDepots;
	}

    public ArrayList<BusStop> loadBusStopsFromJson(String filePath) {
        try (FileReader fileReader = new FileReader(new File(filePath))) {
            JSONTokener tokener = new JSONTokener(fileReader);
            JSONObject data = new JSONObject(tokener);
            Problem problemInstance = Problem.getProblem();

            JSONArray busStops = data.getJSONArray("bus_stops");
            for (int i = 0; i < busStops.length(); i++) {
                JSONObject busStopData = busStops.getJSONObject(i);
                double coordinateX = busStopData.getDouble("coordinate_x");
                double coordinateY = busStopData.getDouble("coordinate_y");
                Location location = new Location(coordinateX, coordinateY);

                JSONArray passengerList = busStopData.getJSONArray("passenger_list");
                ArrayList<Integer> listCustomers = new ArrayList<>();
                for (int j = 0; j < passengerList.length(); j++) {
                    listCustomers.add(passengerList.getJSONObject(j).getInt("passenger_id"));
                }

                BusStop busStop = new BusStop(
                    busStopData.getInt("id"),
                    busStopData.getInt("total_passengers_assigned"),
                    location,
                    listCustomers
                );
                problemInstance.getListBusesStop().add(busStop);
            }
            return problemInstance.getListBusesStop();
        } catch (IOException e) {
            e.printStackTrace();
            return new ArrayList<>();
        }
    }

    public ArrayList<Depot> loadDepotsFromJson(String filePath) {
        try (FileReader fileReader = new FileReader(new File(filePath))) {
            JSONTokener tokener = new JSONTokener(fileReader);
            JSONObject data = new JSONObject(tokener);
            Problem problemInstance = Problem.getProblem();

            int maxVehicles = data.getInt("max_vehicles");
            double maxVehiclesCapacity = data.getDouble("max_vehicles_capacity");
            ArrayList<Double> listCapacities = new ArrayList<>();
            for (int i = 0; i < maxVehicles; i++) {
                listCapacities.add(maxVehiclesCapacity);
            }
            problemInstance.setListCapacities(listCapacities);

            JSONArray depots = data.getJSONArray("depots");
            for (int i = 0; i < depots.length(); i++) {
                JSONObject depotData = depots.getJSONObject(i);
                double coordinateX = depotData.getDouble("coordinate_x");
                double coordinateY = depotData.getDouble("coordinate_y");
                Location location = new Location(coordinateX, coordinateY);

                ArrayList<Fleet> fleets = new ArrayList<>();
                fleets.add(new Fleet(maxVehicles, maxVehiclesCapacity));

                Depot depot = new Depot(
                    depotData.getInt("id"),
                    location,
                    fleets
                );
                problemInstance.getListDepots().add(depot);
            }
            return problemInstance.getListDepots();
        } catch (IOException e) {
            e.printStackTrace();
            return new ArrayList<>();
        }
    }

        public void fillListDistancesSbrp(
        ArrayList<Integer> idBusStops, ArrayList<Double> axisXBusStops, ArrayList<Double> axisYBusStops,
        ArrayList<Integer> idDepots, ArrayList<Double> axisXDepots, ArrayList<Double> axisYDepots,
        ArrayList<List<Double>> listDistances, DistanceType typeDistance
    ) throws IllegalArgumentException, SecurityException, ClassNotFoundException, InstantiationException, IllegalAccessException, InvocationTargetException, NoSuchMethodException, Exception {
        int totalBusStops = idBusStops.size();
        int totalDepots = idDepots.size();
        IDistance distance = newDistance(typeDistance);
        
        for (int i = 0; i < totalBusStops; i++) {
            ArrayList<Double> distancesFromBusStops = new ArrayList<>();
            for (int j = 0; j < totalBusStops; j++) {
                distancesFromBusStops.add(distance.calculateDistance(
                    axisXBusStops.get(j), axisYBusStops.get(j),
                    axisXBusStops.get(i), axisYBusStops.get(i)
                ));
            }
            for (int k = 0; k < totalDepots; k++) {
                distancesFromBusStops.add(distance.calculateDistance(
                    axisXDepots.get(k), axisYDepots.get(k),
                    axisXBusStops.get(i), axisYBusStops.get(i)
                ));
            }
            listDistances.add(distancesFromBusStops);
        }
        for (int i = 0; i < totalDepots; i++) {
            ArrayList<Double> distancesFromDepots = new ArrayList<>();
            for (int j = 0; j < totalBusStops; j++) {
                distancesFromDepots.add(distance.calculateDistance(
                    axisXBusStops.get(j), axisYBusStops.get(j),
                    axisXDepots.get(i), axisYDepots.get(i)
                ));
            }
            for (int k = 0; k < totalDepots; k++) {
                distancesFromDepots.add(distance.calculateDistance(
                    axisXDepots.get(k), axisYDepots.get(k),
                    axisXDepots.get(i), axisYDepots.get(i)
                ));
            }
            listDistances.add(distancesFromDepots);
        }
    }
        
        /* M�todo encargado de crear una distancia.*/
	private IDistance newDistance(DistanceType distanceType) throws IllegalArgumentException, SecurityException, ClassNotFoundException, InstantiationException, IllegalAccessException, InvocationTargetException, NoSuchMethodException {
		IFactoryDistance iFactoryDistance = new FactoryDistance();
		IDistance distance = (IDistance) iFactoryDistance.createDistance(distanceType);
		return distance;
	}

    public void isLoadTimeWindows(ArrayList<Double> initialNodes, ArrayList<Double> endNodes, ArrayList<Double> serviceTimes){
        int totalCustomers = loadTotalCustomers();
        int totalDepots = loadTotalDepots();
        for (int i = totalDepots + 1; i <= totalCustomers + totalDepots; i++) {
            String[] tokens = instanceFile.get(i).split("\\s+");
            initialNodes.add(Double.parseDouble(tokens[4]));
            endNodes.add(Double.parseDouble(tokens[5]));
            serviceTimes.add(Double.parseDouble(tokens[6]));
        }
    }

    public Problem loadCVRPFromJson(String filePath) {
        try (FileReader reader = new FileReader(filePath)) {
            JSONTokener tokener = new JSONTokener(reader);
            JSONObject data = new JSONObject(tokener);

            Problem problemInstance = Problem.getProblem();

            int countVehicles = data.getInt("count_vehicles");
            double capacityVehicles = data.getDouble("capacity_vehicles");

            Fleet fleet = new Fleet(countVehicles, capacityVehicles);

            ArrayList<Customer> customers = new ArrayList<>();
            JSONArray customersArray = data.getJSONArray("customers");
            for (int i = 0; i < customersArray.length(); i++) {
                JSONObject customerData = customersArray.getJSONObject(i);
                Location location = new Location(customerData.getDouble("coordinate_x"), customerData.getDouble("coordinate_y"));
                Customer customer = new Customer(
                        customerData.getInt("id_customer"),
                        customerData.getDouble("request"),
                        location
                );
                customers.add(customer);
            }

            ArrayList<Depot> depots = new ArrayList<>();
            JSONArray depotsArray = data.getJSONArray("depots");
            for (int i = 0; i < depotsArray.length(); i++) {
                JSONObject depotData = depotsArray.getJSONObject(i);
                Location location = new Location(depotData.getDouble("coordinate_x"), depotData.getDouble("coordinate_y"));
                Depot depot = new Depot(
                        depotData.getInt("id_depot"),
                        location,
                        new ArrayList<Fleet>(List.of(fleet))                       
                );
                depots.add(depot);
            }

            problemInstance.setListCustomers(customers);
            problemInstance.setListDepots(depots);

            return problemInstance;
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }

    public Problem loadHFVRPFromJson(String filePath) {
        try (FileReader reader = new FileReader(filePath)) {
            JSONTokener tokener = new JSONTokener(reader);
            JSONObject data = new JSONObject(tokener);

            Problem problemInstance = Problem.getProblem();

            int countVehicles = data.getInt("count_vehicles");
            double capacityVehicles = data.getDouble("capacity_vehicles");

            Fleet fleet = new Fleet(countVehicles, capacityVehicles);

            ArrayList<Customer> customers = new ArrayList<>();
            JSONArray customersArray = data.getJSONArray("customers");
            for (int i = 0; i < customersArray.length(); i++) {
                JSONObject customerData = customersArray.getJSONObject(i);
                Location location = new Location(customerData.getDouble("coordinate_x"), customerData.getDouble("coordinate_y"));
                Customer customer = new Customer(
                        customerData.getInt("id_customer"),
                        customerData.getDouble("request"),
                        location
                );
                customers.add(customer);
            }

            ArrayList<Depot> depots = new ArrayList<>();
            JSONArray depotsArray = data.getJSONArray("depots");
            for (int i = 0; i < depotsArray.length(); i++) {
                JSONObject depotData = depotsArray.getJSONObject(i);
                Location location = new Location(depotData.getDouble("coordinate_x"), depotData.getDouble("coordinate_y"));
                Depot depot = new Depot(
                        depotData.getInt("id_depot"),
                        location,
                        new ArrayList<>(List.of(fleet))
                );
                depots.add(depot);
            }

            problemInstance.setListCustomers(customers);
            problemInstance.setListDepots(depots);

            return problemInstance;
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }

    public Problem loadMDVRPFromJson(String filePath) {
        try (FileReader reader = new FileReader(filePath)) {
            JSONTokener tokener = new JSONTokener(reader);
            JSONObject data = new JSONObject(tokener);

            Problem problemInstance = Problem.getProblem();

            int countVehicles = data.getInt("count_vehicles");
            double capacityVehicles = data.getDouble("capacity_vehicles");

            Fleet fleet = new Fleet(countVehicles, capacityVehicles);

            ArrayList<Customer> customers = new ArrayList<>();
            JSONArray customersArray = data.getJSONArray("customers");
            for (int i = 0; i < customersArray.length(); i++) {
                JSONObject customerData = customersArray.getJSONObject(i);
                Location location = new Location(customerData.getDouble("coordinate_x"), customerData.getDouble("coordinate_y"));
                Customer customer = new Customer(
                        customerData.getInt("id_customer"),
                        customerData.getDouble("request"),
                        location
                );
                customers.add(customer);
            }

            ArrayList<Depot> depots = new ArrayList<>();
            JSONArray depotsArray = data.getJSONArray("depots");
            for (int i = 0; i < depotsArray.length(); i++) {
                JSONObject depotData = depotsArray.getJSONObject(i);
                Location location = new Location(depotData.getDouble("coordinate_x"), depotData.getDouble("coordinate_y"));
                Depot depot = new Depot(
                        depotData.getInt("id_depot"),
                        location,
                        new ArrayList<>(List.of(fleet))
                );
                depots.add(depot);
            }

            problemInstance.setListCustomers(customers);
            problemInstance.setListDepots(depots);

            return problemInstance;
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }

    public Problem loadTTRPFromJson(String filePath) {
        try (FileReader reader = new FileReader(filePath)) {
            JSONTokener tokener = new JSONTokener(reader);
            JSONObject data = new JSONObject(tokener);

            Problem problemInstance = Problem.getProblem();

            double capacityVehicle = data.getDouble("capacity_vehicle");
            double capacityTrailer = data.getDouble("capacity_trailer");
            int countVehicles = data.getInt("count_vehicles");
            int countTrailers = data.getInt("count_trailers");

            FleetTTRP fleet = new FleetTTRP(countVehicles, capacityVehicle, countTrailers, capacityTrailer);

            ArrayList<CustomerTTRP> customers = new ArrayList<>();
            JSONArray customersArray = data.getJSONArray("customers");
            for (int i = 0; i < customersArray.length(); i++) {
                JSONObject customerData = customersArray.getJSONObject(i);
                Location location = new Location(customerData.getDouble("coordinate_x"), customerData.getDouble("coordinate_y"));
                CustomerTTRP customer = new CustomerTTRP(
                        customerData.getInt("id_customer"),
                        customerData.getDouble("request"),
                        location,
                        customerData.getInt("type_customer")
                );
                customers.add(customer);
            }

            ArrayList<Depot> depots = new ArrayList<>();
            JSONArray depotsArray = data.getJSONArray("depots");
            for (int i = 0; i < depotsArray.length(); i++) {
                JSONObject depotData = depotsArray.getJSONObject(i);
                Location location = new Location(depotData.getDouble("coordinate_x"), depotData.getDouble("coordinate_y"));
                Depot depot = new Depot(
                        depotData.getInt("id_depot"),
                        location,
                        new ArrayList<>(List.of(fleet))
                );
                depots.add(depot);
            }
            
            ArrayList<Customer> customers_ttrp = new ArrayList<>(customers);

            problemInstance.setListCustomers(customers_ttrp);
            problemInstance.setListDepots(depots);

            return problemInstance;
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }

    public Problem loadVRPTWFromJson(String filePath) {
        try (FileReader reader = new FileReader(filePath)) {
            JSONTokener tokener = new JSONTokener(reader);
            JSONObject data = new JSONObject(tokener);

            Problem problemInstance = Problem.getProblem();

            int countVehicles = data.getInt("count_vehicles");
            double capacityVehicles = data.getDouble("capacity_vehicles");

            Fleet fleet = new Fleet(countVehicles, capacityVehicles);

            ArrayList<Customer> customers = new ArrayList<>();
            JSONArray customersArray = data.getJSONArray("customers");
            for (int i = 0; i < customersArray.length(); i++) {
                JSONObject customerData = customersArray.getJSONObject(i);
                TimeWindow timeWindow = new TimeWindow(
                        customerData.getFloat("initial_node"),
                        customerData.getFloat("end_node"),
                        customerData.getFloat("service_time")
                );

                Location location = new Location(customerData.getDouble("coordinate_x"), customerData.getDouble("coordinate_y"));
                Customer customer = new Customer(
                        customerData.getInt("id_customer"),
                        customerData.getDouble("request"),
                        location,
                        timeWindow
                );
                customers.add(customer);
            }

            ArrayList<Depot> depots = new ArrayList<>();
            JSONArray depotsArray = data.getJSONArray("depots");
            for (int i = 0; i < depotsArray.length(); i++) {
                JSONObject depotData = depotsArray.getJSONObject(i);
                Location location = new Location(depotData.getDouble("coordinate_x"), depotData.getDouble("coordinate_y"));
                Depot depot = new Depot(
                        depotData.getInt("id_depot"),
                        location,
                        new ArrayList<>(List.of(fleet))
                );
                depots.add(depot);
            }

            problemInstance.setListCustomers(customers);
            problemInstance.setListDepots(depots);

            return problemInstance;
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }
    
}
        
