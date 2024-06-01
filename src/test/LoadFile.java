package test;

import cujae.inf.citi.om.data.CustomerType;
import java.io.FileReader;
import java.io.IOException;
import java.io.LineNumberReader;
import java.lang.reflect.InvocationTargetException;
import java.util.ArrayList;
import java.util.StringTokenizer;
//import cujae.inf.citi.om.factory.interfaces.DistanceType;
//import problem_data.*;
//import cujae.inf.citi.om.input.*;
//import cujae.inf.citi.om.matrix.NumericMatrix;

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
		int totalCustomers = loadTotalCustomers();
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
	
    public Double calculateDistance(double axisXStart, double axisYStart, double axisXEnd, double axisYEnd) {
    	double distance = 0.0;
    	double axisX = 0.0;
    	double axisY = 0.0;

    	axisX = Math.pow((axisXStart - axisXEnd), 2);
    	axisY = Math.pow((axisYStart - axisYEnd), 2);
    	distance = Math.sqrt((axisX + axisY));

    	//Math.sqrt((Math.pow((axisXPointOne - axisXPointTwo), 2)) + Math.pow((axisYPointOne - axisYPointTwo), 2));
    	
    	return distance;
    }
    
    public void fillListDistances(ArrayList<Integer> idCustomers, ArrayList<Double> axisXCustomers, ArrayList<Double> axisYCustomers, ArrayList<Integer> idDepots, ArrayList<Double> axisXDepots, ArrayList<Double> axisYDepots, ArrayList<ArrayList<Double>> listDistances) throws IllegalArgumentException, SecurityException, ClassNotFoundException, InstantiationException, IllegalAccessException, InvocationTargetException, NoSuchMethodException{
    	int totalCustomers = idCustomers.size();
    	int totalDepots = idDepots.size();
    	
    	for(int i = 0; i < totalCustomers; i++)
    	{	    	
    		ArrayList<Double> distancesFromCustomers = new ArrayList<Double>();

    		for(int j = 0; j < totalCustomers; j++)
    			distancesFromCustomers.add(calculateDistance(axisXCustomers.get(j), axisYCustomers.get(j), axisXCustomers.get(i), axisYCustomers.get(i)));

    		for(int k = 0; k < totalDepots; k++)
    			distancesFromCustomers.add(calculateDistance(axisXDepots.get(k), axisYDepots.get(k), axisXCustomers.get(i), axisYCustomers.get(i)));

    		listDistances.add(distancesFromCustomers);//hasta aqui voy a tener la lista de distancias llena de cada cliente y deposito a los clientes
    	}

    	for(int i = 0; i < totalDepots; i++)
    	{
    		ArrayList<Double> distancesFromCustomers = new ArrayList<Double>();

    		for(int j = 0; j < totalCustomers; j++)
    			distancesFromCustomers.add(calculateDistance(axisXCustomers.get(j), axisYCustomers.get(j), axisXDepots.get(i), axisYDepots.get(i)));

    		for(int k = 0; k < totalDepots; k++)
    			distancesFromCustomers.add(calculateDistance(axisXDepots.get(k), axisYDepots.get(k), axisXDepots.get(i), axisYDepots.get(i)));

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

	
//	public int getCountVehilces(){
//		StringTokenizer tool = new StringTokenizer(instanceFile.get(0), " ");
//		
//		return Integer.valueOf(tool.nextToken());
//	}
//	

//	

//	
//	public Integer getValueOfTypeAssignment(){
//		StringTokenizer tool = new StringTokenizer(instanceFile.get(0), " ");
//		tool.nextToken();
//		tool.nextToken();
//		tool.nextToken();
//		
//		return Integer.valueOf(tool.nextToken());
//	}
//	
//	public AssignmentType getTypeAssignment(Integer value){
//		AssignmentType type = AssignmentType.Simplified;
//		
//		switch(value)
//		{
//		case 0:
//			type = AssignmentType.BestNearest;
//		case 1:
//			type = AssignmentType.CyclicInParallel;
//		case 2:
//			type = AssignmentType.CyclicInSequential;
//		case 3:
//			type = AssignmentType.NearestByCustomer;
//		case 4:
//			type = AssignmentType.Parallel;
//		case 5:
//			type = AssignmentType.RandomByCustomer;
//		case 6:
//			type = AssignmentType.Simplified;
//		case 7:
//			type = AssignmentType.Sweep;
//		}
//		
//		return type;
//	}
//	
//	public double getCapacityVehicles(){
//		StringTokenizer tool = new StringTokenizer(instanceFile.get(1), " ");
//		
//		return Double.valueOf(tool.nextToken());
//		
//	}
	
	
//	public ArrayList<Integer> getListCountVehicles(){
//		ArrayList<Integer> listCountVehicles = new ArrayList<Integer>();
//		int countVehicles = getCountVehilces();
//		
//		for(int i = 0; i < getCountDepots(); i++)
//			listCountVehicles.add(countVehicles);
//		
//		return listCountVehicles;
//	}
//	
//	public ArrayList<Double> getListCapacityVehicles(){
//		ArrayList<Double> listCapacityVehicles = new ArrayList<Double>();
//		double capacityVehicles = getCapacityVehicles();
//		
//		for(int i = 0; i < getCountDepots(); i++)
//			listCapacityVehicles.add(capacityVehicles);
//		
//		return listCapacityVehicles;
//	}
	

	
//	public ArrayList<ArrayList<Double>> createListDistances(){
//		ArrayList<ArrayList<Double>> listDistances = new ArrayList<ArrayList<Double>>();
//		int countCustomers = getCountCustomers();
//		int countDepots = getCountDepots(); 
//	
//		ArrayList<Double> listDistances2 = new ArrayList<Double>();
//		
//		//este for es para llenar la lista de distancias de adentro, q nada mas van a teenr valore 2 y 5, es para probar, xq no tengo la lista de las distancias verdadera
//		for(int i = 0; i < countCustomers + countDepots - 1; i++){
//			listDistances2.add(i, 0.0);//xq es la pos de cada 1 a el mismo, q es 0
//
//			for(int j = 0; j < i; j++)
//				listDistances2.add(j, 2.0);
//			
//			for(int k = i + 1; k < countCustomers - 1; k++)
//				listDistances2.add(k, 5.0);
//					
//		}	
//		for(int l = 0; l < (countCustomers + countDepots); l++)
//			listDistances.add(l, listDistances2);
//
//		return listDistances;
//	}
//		
//		
//	
//	public ArrayList<Integer> getIdCustomers(){		
//	ArrayList<Integer> listIdCustomers = new ArrayList<Integer>();
//	
//	for(int i = getCountDepots() + 1; i < (instanceFile.size() - 1); i++)		
//	{
//		StringTokenizer tool = new StringTokenizer(instanceFile.get(i), " ");
//		listIdCustomers.add(Integer.valueOf(tool.nextToken()));
//	}
//	return listIdCustomers;
//}
//	
//	public ArrayList<Double> getRequestCustomers(){		
//	ArrayList<Double> listRequestCustomers = new ArrayList<Double>();
//	
//	for(int i = getCountDepots() + 1; i < (instanceFile.size() - 1); i++)		
//	{
//		StringTokenizer tool = new StringTokenizer(instanceFile.get(i), " ");
//		tool.nextToken();
//		listRequestCustomers.add(Double.valueOf(tool.nextToken()));
//	}
//	return listRequestCustomers;
//}
//	
//	public ArrayList<Integer> getIdDepots(){
//		ArrayList<Integer> listIdDepots = new ArrayList<Integer>();
//																		//ver hasta donde va con el EOF
//		for(int i = getCountCustomers() + getCountDepots(); i < instanceFile.size() - 1; i++)
//		{
//			StringTokenizer tool = new StringTokenizer(instanceFile.get(i), " ");
//			listIdDepots.add(Integer.valueOf(tool.nextToken()));
//			
//		}
//		
//		return listIdDepots;
//		
//	}
//	
//	public void loadInfoProblem() throws IllegalArgumentException, SecurityException, ClassNotFoundException, InstantiationException, IllegalAccessException, InvocationTargetException, NoSuchMethodException{
//		//InfoProblem.getProblem().setFleet(loadHeader());
//		//InfoProblem.getProblem().setListCustomers(loadBody());	
//		
//																																		///duda como obtengo el listDistances
//		Controller.getController().loadProblem(getIdCustomers(), getRequestCustomers(), getIdDepots(), getListCountVehicles(), getListCapacityVehicles(), createListDistances(), getTypeAssignment(getValueOfTypeAssignment()));
//		//		//como llamo al loadProblem de controller, es a ese al q tengo q llamar?
////		Controller.getController().loadProblem(loadBody(), /*si ya sette'e las listas de clientes con los id y las demandas??para q papsar todo eso de nuevo?*/, idDepots, countVehicles, capacityVehicles, listDistances, typeAssignment)
//		}
}
