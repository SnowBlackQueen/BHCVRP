package cujae.inf.citi.om.generator.controller;

import java.lang.reflect.InvocationTargetException;
import java.util.ArrayList;

//import com.sun.org.apache.xerces.internal.impl.dv.xs.MonthDV;

import cujae.inf.citi.om.data.Customer;
import cujae.inf.citi.om.data.CustomerTTRP;
import cujae.inf.citi.om.data.Depot;
import cujae.inf.citi.om.data.DepotMDVRP;
import cujae.inf.citi.om.data.Fleet;
import cujae.inf.citi.om.data.FleetTTRP;
import cujae.inf.citi.om.data.Location;
import cujae.inf.citi.om.data.Problem;
import cujae.inf.citi.om.data.ProblemType;
import cujae.inf.citi.om.factory.interfaces.*;
import cujae.inf.citi.om.factory.methods.FactoryDistance;
import cujae.inf.citi.om.factory.methods.FactoryHeuristic;
import cujae.inf.citi.om.distance.Distance;
import cujae.inf.citi.om.generator.heuristic.Heuristic;
import cujae.inf.citi.om.generator.solution.RouteTTRP;
import cujae.inf.citi.om.generator.solution.RouteType;
import cujae.inf.citi.om.generator.solution.Solution;
import cujae.inf.citi.om.heuristic.controller.Controller;
import cujae.inf.citi.om.heuristic.output.Cluster;
import cujae.inf.citi.om.matrix.NumericMatrix;
import cujae.inf.citi.om.tools.*;

public class StrategyHeuristic {

	private static StrategyHeuristic strategyHeuristic = null;

	private Solution bestSolution;
	private ArrayList<Solution> listSolutions = null;
	private long timeExecute;
	public boolean calculateTime = false;

	private StrategyHeuristic() {
		super();
		listSolutions = new ArrayList<Solution>();
		// TODO Auto-generated constructor stub
	}

	/* M�todo que implementa el Patr�n Singleton*/
	public static StrategyHeuristic getStrategyHeuristic(){

		if (strategyHeuristic == null) {
			strategyHeuristic = new StrategyHeuristic();
		}
		return strategyHeuristic;
	}

	public Solution getBestSolution() {
		return bestSolution;
	}

	public void setBestSolution(Solution bestSolution) {
		this.bestSolution = bestSolution;
	}

	public ArrayList<Solution> getListSolutions() {
		return listSolutions;
	}

	public void setListSolutions(ArrayList<Solution> listSolutions) {
		this.listSolutions = listSolutions;
	}

	public long getTimeExecute() {
		return timeExecute;
	}

	/* M�todo encargado de crear una heur�stica de construcci�n*/
	private Heuristic newHeuristic(HeuristicType heuristicType) throws IllegalArgumentException, SecurityException, ClassNotFoundException, InstantiationException, IllegalAccessException, InvocationTargetException, NoSuchMethodException {
		IFactoryHeuristic iFactoryHeuristic = new FactoryHeuristic();
		Heuristic heuristic = iFactoryHeuristic.createHeuristic(heuristicType);
		return heuristic;
	}
	/* M�todo encargado de crear una distancia*/
	private Distance newDistance(DistanceType typeDistance) throws IllegalArgumentException, SecurityException, ClassNotFoundException, InstantiationException, IllegalAccessException, InvocationTargetException, NoSuchMethodException {
		IFactoryDistance iFactoryDistance = new FactoryDistance();
		Distance distance = iFactoryDistance.createDistance(typeDistance);
		return distance;
	}

	//	/* M�todo encargado de crear una m�todo de asignaci�n*/
	//	private Assignment newAssignment(AssignmentType typeAssignment) throws IllegalArgumentException, SecurityException, ClassNotFoundException, InstantiationException, IllegalAccessException, InvocationTargetException, NoSuchMethodException {
	//		IFactoryAssignment iFactoryAssigned = new FactoryAssignment();
	//		Assignment assignment = iFactoryAssigned.createAssignment(typeAssignment);
	//		return assignment;
	//	}

	/* M�todo encargado de cargar los datos de los clientes con coordenadas*/
	private ArrayList<Customer> loadCustomer(ArrayList<Integer> idCustomers, ArrayList<Double> requestCustomers, ArrayList<Double> axisXCustomers, ArrayList<Double> axisYCustomers){
		ArrayList<Customer> listCustomers = new ArrayList<Customer>();
		Customer customer;
		Location location;

		for (int i = 0; i < idCustomers.size(); i++) 
		{	
			location = new Location();
			location.setAxisX(axisXCustomers.get(i));
			location.setAxisY(axisYCustomers.get(i));

			customer = new Customer();
			customer.setIdCustomer(idCustomers.get(i));
			customer.setRequestCustomer(requestCustomers.get(i));
			customer.setLocationCustomer(location);

			listCustomers.add(customer);
		}

		return listCustomers;
	}

	/* M�todo encargado de cargar los datos de los clientes sin coordenadas*/
	private ArrayList<Customer> loadCustomer(ArrayList<Integer> idCustomers, ArrayList<Double> requestCustomers){
		ArrayList<Customer> listCustomers = new ArrayList<Customer>();
		Customer customer;

		for (int i = 0; i < idCustomers.size(); i++) 
		{	
			customer = new Customer();
			customer.setIdCustomer(idCustomers.get(i));
			customer.setRequestCustomer(requestCustomers.get(i));

			listCustomers.add(customer);
		}

		return listCustomers;
	}

	/* M�todo encargado de cargar los datos de los clientes TTRP con coordenadas*/
	private ArrayList<Customer> loadCustomerTTRP(ArrayList<Integer> idCustomers, ArrayList<Double> requestCustomers, ArrayList<Double> axisXCustomers, ArrayList<Double> axisYCustomers, ArrayList<Integer> typeCustomers){
		ArrayList<Customer> listCustomers = new ArrayList<Customer>();

		listCustomers = loadCustomer(idCustomers, requestCustomers, axisXCustomers, axisYCustomers);

		for (int i = 0; i < listCustomers.size(); i++) 
			((CustomerTTRP)listCustomers.get(i)).setTypeCustomer(typeCustomers.get(i).intValue());

		return listCustomers;
	}

	/* M�todo encargado de cargar los datos de los clientes TTRP sin coordenadas*/
        private ArrayList<Customer> loadCustomerTTRP(ArrayList<Integer> idCustomers, ArrayList<Double> requestCustomers, ArrayList<Integer> typeCustomers) {
            ArrayList<Customer> listCustomers = loadCustomer(idCustomers, requestCustomers);


            for (int i = 0; i < listCustomers.size(); i++) {
                Customer c = listCustomers.get(i);

                CustomerTTRP customerTTRP = new CustomerTTRP(c.getIdCustomer(), c.getRequestCustomer(), c.getLocationCustomer(), typeCustomers.get(i).intValue());

                listCustomers.set(i, customerTTRP);
            }

            return listCustomers;
        }

	/* M�todo encargado de cargar los datos de los dep�sitos y las flotas con coordenadas y asignaci�n predeterminada*/
	private ArrayList<Depot> loadDepot(ArrayList<Integer> idDepots, ArrayList<Double> axisXDepots, ArrayList<Double> axisYDepots, ArrayList<ArrayList<Integer>> idAssignedCustomers, ArrayList<Integer> countVehicles, ArrayList<Double> capacityVehicles){
		ArrayList<Depot> listDepots = new ArrayList<Depot>();
		ArrayList<Fleet> listFleets;
		DepotMDVRP depot;
		Location location;

		for(int i = 0; i < idDepots.size(); i++)
		{
			location = new Location();
			location.setAxisX(axisXDepots.get(i));
			location.setAxisY(axisYDepots.get(i));

			depot = new DepotMDVRP();
			depot.setIdDepot(idDepots.get(i));
			depot.setLocationDepot(location);
			depot.setListAssignedCustomers(idAssignedCustomers.get(i));

			listFleets = new ArrayList<Fleet>();
			Fleet fleet;

			for(int j = 0; j < countVehicles.size(); j++)
			{
				fleet = new Fleet();
				fleet.setCountVehicles(countVehicles.get(j));
				fleet.setCapacityVehicle(capacityVehicles.get(j));

				listFleets.add(fleet);
			}

			depot.setListFleets(listFleets);
			listDepots.add(depot);
		}

		return listDepots;		
	}

	/* M�todo encargado de cargar los datos de los dep�sitos y las flotas con coordenadas*/
	private ArrayList<Depot> loadDepot(ArrayList<Integer> idDepots, ArrayList<Double> axisXDepots, ArrayList<Double> axisYDepots, ArrayList<Integer> countVehicles, ArrayList<Double> capacityVehicles){
		ArrayList<Depot> listDepots = new ArrayList<Depot>();
		ArrayList<Fleet> listFleets;
		DepotMDVRP depot;
		Location location;

		for(int i = 0; i < idDepots.size(); i++)
		{
			location = new Location();
			location.setAxisX(axisXDepots.get(i));
			location.setAxisY(axisYDepots.get(i));

			depot = new DepotMDVRP();
			depot.setIdDepot(idDepots.get(i));
			depot.setLocationDepot(location);

			listFleets = new ArrayList<Fleet>();
			Fleet fleet;

			for(int j = 0; j < countVehicles.size(); j++)
			{
				fleet = new Fleet();
				fleet.setCountVehicles(countVehicles.get(j));
				fleet.setCapacityVehicle(capacityVehicles.get(j));

				listFleets.add(fleet);
			}

			depot.setListFleets(listFleets);
			listDepots.add(depot);
		}

		return listDepots;		
	}

	/* M�todo encargado de cargar los datos de los dep�sitos y las flotas sin coordenadas y asignaci�n de clientes predeterminada*/
	private ArrayList<Depot> loadDepot(ArrayList<Integer> idDepots, ArrayList<ArrayList<Integer>> idAssignedCustomers, ArrayList<Integer> countVehicles, ArrayList<Double> capacityVehicles){
		ArrayList<Depot> listDepots = new ArrayList<Depot>();
		ArrayList<Fleet> listFleets;
		DepotMDVRP depot;

		for(int i = 0; i < idDepots.size(); i++)
		{
			depot = new DepotMDVRP();
			depot.setIdDepot(idDepots.get(i));
			depot.setListAssignedCustomers(idAssignedCustomers.get(i));

			listFleets = new ArrayList<Fleet>();
			Fleet fleet;

			for(int j = 0; j < countVehicles.size(); j++)
			{
				fleet = new Fleet();
				fleet.setCountVehicles(countVehicles.get(j));
				fleet.setCapacityVehicle(capacityVehicles.get(j));

				listFleets.add(fleet);
			}

			depot.setListFleets(listFleets);
			listDepots.add(depot);
		}

		return listDepots;		
	}

	/* M�todo encargado de cargar los datos de los dep�sitos y las flotas sin coordenadas*/
	private ArrayList<Depot> loadDepot(ArrayList<Integer> idDepots, ArrayList<Integer> countVehicles, ArrayList<Double> capacityVehicles){
		ArrayList<Depot> listDepots = new ArrayList<Depot>();
		ArrayList<Fleet> listFleets;
		DepotMDVRP depot;//

		for(int i = 0; i < idDepots.size(); i++)
		{
			depot = new DepotMDVRP();//
			depot.setIdDepot(idDepots.get(i));

			listFleets = new ArrayList<Fleet>();
			Fleet fleet;

			for(int j = 0; j < countVehicles.size(); j++)
			{
				fleet = new Fleet();
				fleet.setCountVehicles(countVehicles.get(j));
				fleet.setCapacityVehicle(capacityVehicles.get(j));

				listFleets.add(fleet);
			}

			depot.setListFleets(listFleets);
			listDepots.add(depot);
		}

		return listDepots;		
	}

	/* M�todo encargado de cargar los datos de los dep�sitos y las flotas TTRP con coordenadas*/
	private ArrayList<Depot> loadDepotTTRP(ArrayList<Integer> idDepots, ArrayList<Double> axisXDepots, ArrayList<Double> axisYDepots, ArrayList<Integer> countVehicles, ArrayList<Double> capacityVehicles, ArrayList<Integer> countTrailers, ArrayList<Double> capacityTrailers){
		ArrayList<Depot> listDepots = new ArrayList<Depot>();

		listDepots = loadDepot(idDepots, axisXDepots, axisYDepots, countVehicles, capacityVehicles);

		for (int i = 0; i < listDepots.size(); i++) 
		{
			((FleetTTRP)listDepots.get(i).getListFleets().get(0)).setCountTrailers(countTrailers.get(i));
			((FleetTTRP)listDepots.get(i).getListFleets().get(0)).setCapacityTrailer(capacityTrailers.get(i));			
		}

		return listDepots;
	}

	/* M�todo encargado de cargar los datos de los dep�sitos y las flotas TTRP sin coordenadas*/
	private ArrayList<Depot> loadDepotTTRP(ArrayList<Integer> idDepots, ArrayList<Integer> countVehicles, ArrayList<Double> capacityVehicles, ArrayList<Integer> countTrailers, ArrayList<Double> capacityTrailers){
		ArrayList<Depot> listDepots = new ArrayList<Depot>();

		listDepots = loadDepot(idDepots, countVehicles, capacityVehicles);

		for (int i = 0; i < listDepots.size(); i++) 
		{
                    Fleet f = listDepots.get(i).getListFleets().get(0);
                    FleetTTRP fleetTTRP = new FleetTTRP(f.getCountVehicles(), f.getCapacityVehicle(), countTrailers.get(i), capacityTrailers.get(i));
                    
                    listDepots.get(i).getListFleets().set(0, fleetTTRP);
		}

		return listDepots;
	}

	/* M�todo encargado de cargar los datos del problema con coordenadas*/
	/*	public boolean loadProblem(ArrayList<Integer> idCustomers, ArrayList<Double> requestCustomers, ArrayList<Double> axisXCustomers, ArrayList<Double> axisYCustomers, ArrayList<Integer> typeCustomers, ArrayList<Integer> idDepots, ArrayList<Double> axisXDepots, ArrayList<Double> axisYDepots, ArrayList<Integer> countVehicles, ArrayList<Double> capacityVehicles, ArrayList<Integer> countTrailers, ArrayList<Double> capacityTrailers, ProblemType typeProblem, AssignmentType typeAssignment, OrderType typeOrder, DistanceType typeDistance, ArrayList<ArrayList<Double>> distances)throws IllegalArgumentException, SecurityException, ClassNotFoundException, InstantiationException, IllegalAccessException, InvocationTargetException, NoSuchMethodException{
		boolean loaded = false;


		if((idCustomers != null && !idCustomers.isEmpty()) && (requestCustomers != null && !requestCustomers.isEmpty()) && (axisXCustomers != null && !axisXCustomers.isEmpty()) && (axisYCustomers != null && !axisYCustomers.isEmpty()) && (idDepots != null && !idDepots.isEmpty()) && (axisXDepots != null && !axisXDepots.isEmpty()) && (axisYDepots != null && !axisYDepots.isEmpty()) && (countVehicles != null && !countVehicles.isEmpty()) && (capacityVehicles != null && !capacityVehicles.isEmpty()) && (typeProblem.ordinal() >= 0 && typeProblem.ordinal() <= 5))
		{
			Problem.getProblem().setTypeProblem(typeProblem);

			if((typeCustomers != null && !typeCustomers.isEmpty()) && (countTrailers != null && !countTrailers.isEmpty()) && (capacityTrailers != null &&!capacityTrailers.isEmpty()))
			{
				Problem.getProblem().setListCustomers(loadCustomerTTRP(idCustomers, requestCustomers, axisXCustomers, axisYCustomers, typeCustomers));
				Problem.getProblem().setListDepots(loadDepotTTRP(idDepots, axisXDepots, axisYDepots, countVehicles, capacityVehicles, countTrailers, capacityTrailers));

				loaded = true;
			}
			else
			{
				Problem.getProblem().setListCustomers(loadCustomer(idCustomers, requestCustomers, axisXCustomers, axisYCustomers));
				Problem.getProblem().setListDepots(loadDepot(idDepots, axisXDepots, axisYDepots, countVehicles, capacityVehicles));

				loaded = true;
			}

			if(typeDistance == null)
				typeDistance = DistanceType.Euclidean;

			Problem.getProblem().setCostMatrix(fillCostMatrix(idCustomers, axisXCustomers, axisYCustomers, idDepots, axisXDepots, axisYDepots, typeDistance));

			if(typeProblem.equals(ProblemType.MDVRP) && (Problem.getProblem().getTotalCapacity() >= Problem.getProblem().getTotalRequest()))
			{
				ArrayList<Integer> idCustomers = Problem.getProblem().getListIDCustomers() ;
				ArrayList<Double> requestCustomers = Problem.getProblem().getListRequestCustomers();
//				ArrayList<Double> axisXCustomers = Problem.getProblem().get
//				ArrayList<Double> axisYCustomers = new ArrayList<Double>();
				ArrayList<Integer> idDepots = Problem.getProblem().getListIDDepots();
				ArrayList<Integer> listCountVehicles = Problem.getProblem().getListCountVehicles();
				ArrayList<Double> listCapacityVehicles = Problem.getProblem().getListCapacityVehicles();



				ArrayList<ArrayList<Integer>> countVehicles = new ArrayList<ArrayList<Integer>>();
				ArrayList<ArrayList<Double>> capacityVehicles = new ArrayList<ArrayList<Double>>();

				ArrayList<ArrayList<Double>> listDistances = new ArrayList<ArrayList<Double>>();

				/*load.)u-oadCountVehiclesForDepot(countVehicles);
				load.loadCapacityVehicles(capacityVehicles);
				load.loadCustomers(idCustomers, axisXCustomers, axisYCustomers, requestCustomers);
				load.loadDepots(idDepots, axisXDepots, axisYDepots);*/

	//load.fillListDistances(idCustomers, axisXCustomers, axisYCustomers, idDepots, axisXDepots, axisYDepots, listDistances);
	//				Controller.getController().loadProblem(listIdCustomers, listRequestCustomers, listIdDepots, listCountVehicles, listCapacityVehicles, distances,axisXCustomers, axisYCustomers, axisXDepots, axisYDepots, typeAssignment);
	//				if(typeAssignment == null)
	//					typeAssignment = AssignmentType.BestNearest;
	//				Co_IU_ntroller.getController().executeAssignment(typeAssignment);

	/*				if(cujae.inf.citi.om.heuristic.controller.Controller.getController().loadProblem(idCustomers, listRequestCustomers, listIdDepots, countVehicles, capacityVehicles, listDistances))
				{

				if(Controller.getController().loadProblem(listIdCustomers, listRequestCustomers, axisXCustomers, axisYCustomers, listIdDepots, axisXDepots, axisYDepots, countVehicles, capacityVehicles, listDistances))

				if(Controller.getController().loadProblem(listIdCustomers, listRequestCustomers, axisXCustomers, axisYCustomers, listIdDepots, axisXDepots, axisYDepots, listCountVehicles, listCapacityVehicles, listDistances))

						//	listIdCustomers, listRequestCustomers, listIdDepots, listCountVehicles, listCapacityVehicles, distances,axisXCustomers, axisYCustomers, axisXDepots, axisYDepots, typeAssignment))
				{
					if(typeAssignment == null)
						typeAssignment = AssignmentType.Simplified;

					Controller.typeOrder = cujae.inf.citi.om.controller.OrderType.Random;

					Controller.getController().executeAssignment(typeAssignment);
					//ver esto
					if(!Controller.getController().getSolution().existUnassigned())
						System.out.println("Vuelva a ejecutar la heur�stica de asignaci�n");
					else
						adapt(Controller.getController().getSolution().getListClusters());

				ij}
			}

			if(typeProblem.equals(ProblemType.HFVRP))
			{
				if(typeOrder == null)
					typeOrder = OrderType.Ascending;

				Problem.getProblem().fillListCapacities(0); /***/
	//Tools.OrdenateMethod(Problem.getProblem().getListCapacities(), typeOrder);
	/*	}
		}

		return loaded;
	}*/

        //Método para la carga de datos de CVRP con coordenadas y listas de distancias
        public boolean loadCVRP(ArrayList<Integer> idCustomers, ArrayList<Double> requestCustomers, ArrayList<Integer> idDepots, ArrayList<Integer> countVehicles, ArrayList<Double> capacityVehicles,
			ArrayList<ArrayList<Double>> listDistances, ArrayList<Double> axisXCustomers, ArrayList<Double> axisYCustomers, ArrayList<Double> axisXDepots, ArrayList<Double> axisYDepots, ProblemType typeProblem)throws IllegalArgumentException, SecurityException, ClassNotFoundException, InstantiationException, IllegalAccessException, InvocationTargetException, NoSuchMethodException{
            
            boolean loaded = false;
            
            Problem.getProblem().setTypeProblem(typeProblem);
            
            if((idCustomers != null && !idCustomers.isEmpty()) && (requestCustomers != null && !requestCustomers.isEmpty()) && 
				(idDepots != null && !idDepots.isEmpty()) && (countVehicles != null && !countVehicles.isEmpty()) && 
				(capacityVehicles != null && !capacityVehicles.isEmpty()) && (listDistances != null && !listDistances.isEmpty()) && 
				(axisXCustomers != null && !axisXCustomers.isEmpty()) && (axisYCustomers != null && !axisYCustomers.isEmpty()) && (axisXDepots != null && !axisXDepots.isEmpty()) && (axisYDepots != null && !axisYDepots.isEmpty()))
		{
			ArrayList<Customer> listCustomers = new ArrayList<Customer>();
			ArrayList<Depot> listDepots = new ArrayList<Depot>();

			for(int i = 0; i < idCustomers.size(); i ++)
			{
				Customer customer = new Customer();
				customer.setIdCustomer(idCustomers.get(i).intValue());
				customer.setRequestCustomer(requestCustomers.get(i).doubleValue());

				Location locationCustomer = new Location();
				locationCustomer.setAxisX(axisXCustomers.get(i));
				locationCustomer.setAxisY(axisYCustomers.get(i));
				customer.setLocationCustomer(locationCustomer);

				listCustomers.add(customer);
			}

			DepotMDVRP depot = new DepotMDVRP();
			depot.setIdDepot(idDepots.get(0));
                        Location locationDepot = new Location();
			locationDepot.setAxisX(axisXDepots.get(0));
			locationDepot.setAxisY(axisYDepots.get(0));
			depot.setLocationDepot(locationDepot);
                                
                        Fleet fleet = new Fleet();
			fleet.setCountVehicles(countVehicles.get(0));
			fleet.setCapacityVehicle(capacityVehicles.get(0));

			ArrayList<Fleet> listFleets = new ArrayList<Fleet>();
			listFleets.add(fleet);
			depot.setListFleets(listFleets);

			listDepots.add(depot);
			

			Problem.getProblem().setListCustomers(listCustomers);
			Problem.getProblem().setListDepots(listDepots);
                        
                        //System.out.println("Llegué hasta aquí");

			if((Problem.getProblem().getTotalCapacity() >= Problem.getProblem().getTotalRequest()))
			{
				loaded = true;
                                //System.out.println("Se cargó");

				Problem.getProblem().setCostMatrix(fillCostMatrix(listDistances));
				//fillCostMatrix(idCustomers, axisXCustomers, axisYCustomers, idDepots, axisXDepots, axisYDepots, DistanceType.Euclidean);

				ArrayList<ArrayList<Integer>> listCountV = new ArrayList<ArrayList<Integer>>(); 
				ArrayList<ArrayList<Double>> listCapV = new ArrayList<ArrayList<Double>>();

				listCountV.add(countVehicles);
				listCapV.add(capacityVehicles);	
			}
                        else
                            System.out.println("La demanda total excede a la capacidad total");
		}
            
            return loaded;
                        
        }
        
	/* M�todo encargado de cargar los datos del problema usando listas de distancias y las coordenadas*/
	public boolean loadProblem(ArrayList<Integer> idCustomers, ArrayList<Double> requestCustomers, ArrayList<Integer> idDepots, ArrayList<Integer> countVehicles, ArrayList<Double> capacityVehicles,
			ArrayList<ArrayList<Double>> listDistances, ArrayList<Double> axisXCustomers, ArrayList<Double> axisYCustomers, ArrayList<Double> axisXDepots, ArrayList<Double> axisYDepots, ProblemType typeProblem, AssignmentType typeAssignment)throws IllegalArgumentException, SecurityException, ClassNotFoundException, InstantiationException, IllegalAccessException, InvocationTargetException, NoSuchMethodException{
		boolean loaded = false;

		Problem.getProblem().setTypeProblem(typeProblem);

		if((idCustomers != null && !idCustomers.isEmpty()) && (requestCustomers != null && !requestCustomers.isEmpty()) && 
				(idDepots != null && !idDepots.isEmpty()) && (countVehicles != null && !countVehicles.isEmpty()) && 
				(capacityVehicles != null && !capacityVehicles.isEmpty()) && (listDistances != null && !listDistances.isEmpty()) && 
				(axisXCustomers != null && !axisXCustomers.isEmpty()) && (axisYCustomers != null && !axisYCustomers.isEmpty()) && (axisXDepots != null && !axisXDepots.isEmpty()) && (axisYDepots != null && !axisYDepots.isEmpty()))
		{
			ArrayList<Customer> listCustomers = new ArrayList<Customer>();
			ArrayList<Depot> listDepots = new ArrayList<Depot>();

			for(int i = 0; i < idCustomers.size(); i ++)
			{
				Customer customer = new Customer();
				customer.setIdCustomer(idCustomers.get(i).intValue());
				customer.setRequestCustomer(requestCustomers.get(i).doubleValue());

				Location locationCustomer = new Location();
				locationCustomer.setAxisX(axisXCustomers.get(i));
				locationCustomer.setAxisY(axisYCustomers.get(i));
				customer.setLocationCustomer(locationCustomer);

				listCustomers.add(customer);
			}

			for(int i = 0; i < idDepots.size(); i ++)
			{ 
				DepotMDVRP depot = new DepotMDVRP();
				depot.setIdDepot(idDepots.get(i));

				Location locationDepot = new Location();
				locationDepot.setAxisX(axisXDepots.get(i));
				locationDepot.setAxisY(axisYDepots.get(i));
				depot.setLocationDepot(locationDepot);

				Fleet fleet = new Fleet();
				fleet.setCountVehicles(countVehicles.get(0));
				fleet.setCapacityVehicle(capacityVehicles.get(0));

				ArrayList<Fleet> listFleets = new ArrayList<Fleet>();
				listFleets.add(fleet);
				depot.setListFleets(listFleets);

				listDepots.add(depot);
			}

			Problem.getProblem().setListCustomers(listCustomers);
			Problem.getProblem().setListDepots(listDepots);

			if((Problem.getProblem().getTotalCapacity() >= Problem.getProblem().getTotalRequest()))
			{
				loaded = true;

				Problem.getProblem().setCostMatrix(fillCostMatrix(listDistances));
				//fillCostMatrix(idCustomers, axisXCustomers, axisYCustomers, idDepots, axisXDepots, axisYDepots, DistanceType.Euclidean);

				ArrayList<ArrayList<Integer>> listCountV = new ArrayList<ArrayList<Integer>>(); 
				ArrayList<ArrayList<Double>> listCapV = new ArrayList<ArrayList<Double>>();

				for(int j = 0; j < idDepots.size(); j++)
				{
					listCountV.add(countVehicles);
					listCapV.add(capacityVehicles);
				}
				
				if(Controller.getController().loadProblem(idCustomers, requestCustomers, axisXCustomers, axisYCustomers, idDepots, axisXDepots, axisYDepots, listCountV, listCapV, listDistances))
				{
					Controller.getController().executeAssignment(typeAssignment);
					adapt(Controller.getController().getSolution().getClusters());

					//System.out.println(Controller.getController().getSolution().getClusters().size());
				}	
			}
		}
		return loaded;
	}

        //Método para la carga de datos del HFVRP usando listas de distancias y coordenadas
        public boolean loadHFVRP(ArrayList<Integer> idCustomers, ArrayList<Double> requestCustomers, ArrayList<Integer> idDepots, 
                ArrayList<Integer> countVehicles, ArrayList<Double> capacityVehicles, ArrayList<ArrayList<Double>> listDistances,
                ArrayList<Double> axisXCustomers, ArrayList<Double> axisYCustomers, ArrayList<Double> axisXDepots, ArrayList<Double> axisYDepots,
                ProblemType typeProblem, OrderType typeOrder)throws IllegalArgumentException, SecurityException, ClassNotFoundException, InstantiationException, IllegalAccessException, InvocationTargetException, NoSuchMethodException{
            boolean loaded = false;
            
            if((typeProblem != null) && (idCustomers != null && !idCustomers.isEmpty()) && (requestCustomers != null && !requestCustomers.isEmpty()) && 
				(idDepots != null && !idDepots.isEmpty()) && (countVehicles != null && !countVehicles.isEmpty()) && 
				(capacityVehicles != null && !capacityVehicles.isEmpty()) && (listDistances != null && !listDistances.isEmpty()) && 
				(axisXCustomers != null && !axisXCustomers.isEmpty()) && (axisYCustomers != null && !axisYCustomers.isEmpty()) && (axisXDepots != null && !axisXDepots.isEmpty()) && (axisYDepots != null && !axisYDepots.isEmpty()))
            {
			ArrayList<Customer> listCustomers = new ArrayList<Customer>();
			ArrayList<Depot> listDepots = new ArrayList<Depot>();

			for(int i = 0; i < idCustomers.size(); i ++)
			{
				Customer customer = new Customer();
				customer.setIdCustomer(idCustomers.get(i).intValue());
				customer.setRequestCustomer(requestCustomers.get(i).doubleValue());

				Location locationCustomer = new Location();
				locationCustomer.setAxisX(axisXCustomers.get(i));
				locationCustomer.setAxisY(axisYCustomers.get(i));
				customer.setLocationCustomer(locationCustomer);

				listCustomers.add(customer);
			}

			DepotMDVRP depot = new DepotMDVRP();
			depot.setIdDepot(idDepots.get(0));
                        Location locationDepot = new Location();
			locationDepot.setAxisX(axisXDepots.get(0));
			locationDepot.setAxisY(axisYDepots.get(0));
			depot.setLocationDepot(locationDepot);
                                
                        Fleet fleet = new Fleet();
			fleet.setCountVehicles(countVehicles.get(0));
                        ArrayList<Fleet> listFleets = new ArrayList<Fleet>();
                        
                        for(int i = 0; i < (countVehicles.get(0)); i++)
                        {
                            fleet.setCapacityVehicle(capacityVehicles.get(i));
                            listFleets.add(fleet);
                            depot.setListFleets(listFleets);                    
                        }

                        listDepots.add(depot);
                        
			Problem.getProblem().setListCustomers(listCustomers);
			Problem.getProblem().setListDepots(listDepots);
                        Problem.getProblem().setTypeProblem(typeProblem);
                        
                        //System.out.println("Llegué hasta aquí");
                        
                        if((Problem.getProblem().getTotalCapacity() >= Problem.getProblem().getTotalRequest()))
			{
				loaded = true;
                                //System.out.println("Se cargó");

				Problem.getProblem().setCostMatrix(fillCostMatrix(listDistances));
				//fillCostMatrix(idCustomers, axisXCustomers, axisYCustomers, idDepots, axisXDepots, axisYDepots, DistanceType.Euclidean);

				ArrayList<ArrayList<Integer>> listCountV = new ArrayList<ArrayList<Integer>>(); 
				ArrayList<ArrayList<Double>> listCapV = new ArrayList<ArrayList<Double>>();

				listCountV.add(countVehicles);
				listCapV.add(capacityVehicles);
                                
                                if(typeProblem.equals(ProblemType.HFVRP))
                                {
                                    if(typeOrder == null)
                                        typeOrder = OrderType.Ascending;

                                    Problem.getProblem().fillListCapacities(0); /***/
                                    Tools.OrdenateMethod(Problem.getProblem().getListCapacities(), typeOrder);
                                    
                                    //System.out.println("Ordenó las capacidades HFVRP");
                                }
			}
                        else
                            System.out.println("La demanda total excede a la capacidad total");
                    
            }
            
            return loaded;
        }

	/* M�todo encargado de cargar los datos del problema usando listas de distancias*/
	public boolean loadProblem(ArrayList<Integer> idCustomers, ArrayList<Double> requestCustomers, ArrayList<Integer> typeCustomers, ArrayList<Integer> idDepots, ArrayList<Integer> countVehicles, ArrayList<Double> capacityVehicles, ArrayList<Integer> countTrailers, ArrayList<Double> capacityTrailers, ArrayList<ArrayList<Double>> listDistances, ProblemType typeProblem, AssignmentType typeAssignment, OrderType typeOrder)throws IllegalArgumentException, SecurityException, ClassNotFoundException, InstantiationException, IllegalAccessException, InvocationTargetException, NoSuchMethodException{
		boolean loaded = false;

		if((idCustomers != null && !idCustomers.isEmpty()) && (requestCustomers != null && !requestCustomers.isEmpty()) && (idDepots != null && !idDepots.isEmpty()) && (countVehicles != null && !countVehicles.isEmpty()) && (capacityVehicles != null && !capacityVehicles.isEmpty()) && (listDistances != null && !listDistances.isEmpty()) && (typeProblem.ordinal() >= 0 && typeProblem.ordinal() <= 5))
		{
			Problem.getProblem().setTypeProblem(typeProblem);

			if((typeCustomers != null && !typeCustomers.isEmpty()) && (countTrailers != null && !countTrailers.isEmpty()) && (capacityTrailers != null &&!capacityTrailers.isEmpty()))
			{
				Problem.getProblem().setListCustomers(loadCustomerTTRP(idCustomers, requestCustomers, typeCustomers));
				Problem.getProblem().setListDepots(loadDepotTTRP(idDepots, countVehicles, capacityVehicles, countTrailers, capacityTrailers));

				loaded = true;
			}
			else
			{
				Problem.getProblem().setListCustomers(loadCustomer(idCustomers, requestCustomers));
				Problem.getProblem().setListDepots(loadDepot(idDepots, countVehicles, capacityVehicles));

				loaded = true;
			}

			Problem.getProblem().setCostMatrix(fillCostMatrix(listDistances));

			//			if(typeProblem.equals(ProblemType.MDVRP) && (Problem.getProblem().getTotalCapacity() >= Problem.getProblem().getTotalRequest()))
			//			{
			//
			//				ArrayList<Integer> listIdCustomers = Problem.getProblem().getListIDCustomers() ;
			//				ArrayList<Double> listRequestCustomers = Problem.getProblem().getListRequestCustomers();
			//				ArrayList<Integer> listIdDepots = Problem.getProblem().getListIDDepots();
			//				ArrayList<Integer> listCountVehicles = Problem.getProblem().getListCountVehicles();
			//				ArrayList<Double> listCapacityVehicles = Problem.getProblem().getListCapacityVehicles();

			/*	
				if(Controller.getController().loadProblem(idCustomers, requestCustomers, idDepots, countVehicles, capacityVehicles, listDistances))
				{
					if(typeAssignment == null)
						typeAssignment = AssignmentType.Simplified;

					Controller.typeOrder = cujae.inf.citi.om.controller.OrderType.Random;

					Controller.getController().executeAssignment(typeAssignment);
					//ver esto
					if(!Controller.getController().getSolution().existUnassigned())
						System.out.println("Vuelva a ejecutar la heur�stica de asignaci�n");
					else
						adapt(Controller.getController().getSolution().getListClusters());

				}*/

			//				Assignment assignment = newAssignment(typeAssignment);
			//				assignment.toClustering();	

			//				if(typeAssignment == null)
			//					typeAssignment = AssignmentType.BestNearest;
			//				
			//				Assignment assignment = newAssignment(typeAssignment);
			//				assignment.toClustering();	
		}

		if(typeProblem.equals(ProblemType.HFVRP))
		{
			if(typeOrder == null)
				typeOrder = OrderType.Ascending;

			Problem.getProblem().fillListCapacities(0); /***/
			Tools.OrdenateMethod(Problem.getProblem().getListCapacities(), typeOrder);
		}
		//		}

		return loaded;
	}


	/*M'etodo encargado de adaptar la solucion que devuelve BHAVRP a lo que necesita BHCVRP*/
	public void adapt(ArrayList<Cluster> listClusters){
		ArrayList<DepotMDVRP> depots = new ArrayList<DepotMDVRP>();
		//	DepotMDVRP depotAux;
		ArrayList<Integer> listIdCustomers;
		boolean found;

		for(int i = 0; i < listClusters.size(); i++)
		{
			found = false;

			for(int j = 0; j < Problem.getProblem().getListDepots().size() && !found; j++)
			{
				if(listClusters.get(i).getIDCluster() == Problem.getProblem().getListDepots().get(j).getIdDepot())
				{
					found = true;
					//				depotAux = new DepotMDVRP();
					listIdCustomers = new ArrayList<Integer>();

					//				depotAux.setIdDepot(listClusters.get(i).getIdDepot());

					for(int k = 0; k < listClusters.get(i).getItemsOfCluster().size(); k++)
						listIdCustomers.add(listClusters.get(i).getItemsOfCluster().get(k));

					//				depotAux.setListAssignedCustomers(listIdCustomers);

					//				depots.add(depotAux);


					((DepotMDVRP)Problem.getProblem().getListDepots().get(j)).setListAssignedCustomers(listIdCustomers);
					//					(((DepotMDVRP)Problem.getProblem().getListDepots().get(j)).getListAssignedCustomers());//.setListAssignedCustomers(listIdCustomers));

				}
			}
		}
		//		for(int i = 0; i < Problem.getProblem().getListDepots().size(); i++)
		//		{
		//			for(int j = 0; j < listClusters.size(); j++)
		//			{
		//				if(Problem.getProblem().getListDepots().get(i).getIdDepot() == listClusters.get(j).getIdDepot())
		//				{
		//					depotAux = new DepotMDVRP();
		//					listIdCustomers.clear();
		//					
		//					depotAux.setIdDepot(listClusters.get(j).getIdDepot());
		//					
		//					for(int k = 0; k < listClusters.get(j).getListIdCustomers().size(); k++)
		//						listIdCustomers.add(listClusters.get(j).getListIdCustomers().get(k));
		//					
		//					depotAux.setListAssignedCustomers(listIdCustomers);
		//					
		//					depots.add(depotAux);
		//				}
		//			}
		//		}
	}

	/* M�todo encargado de cargar los datos del problema con coordenadas y asignaci�n predeterminada*/
	public boolean loadProblem(ArrayList<Integer> idCustomers, ArrayList<Double> requestCustomers, ArrayList<Double> axisXCustomers, ArrayList<Double> axisYCustomers, ArrayList<Integer> typeCustomers, ArrayList<Integer> idDepots, ArrayList<Double> axisXDepots, ArrayList<Double> axisYDepots, ArrayList<ArrayList<Integer>> idAssignedCustomers, ArrayList<Integer> countVehicles, ArrayList<Double> capacityVehicles, ArrayList<Integer> countTrailers, ArrayList<Double> capacityTrailers, ProblemType typeProblem, DistanceType typeDistance)throws IllegalArgumentException, SecurityException, ClassNotFoundException, InstantiationException, IllegalAccessException, InvocationTargetException, NoSuchMethodException{
		boolean loaded = false;

		if((idCustomers != null && !idCustomers.isEmpty()) && (requestCustomers != null && !requestCustomers.isEmpty()) && (axisXCustomers != null && !axisXCustomers.isEmpty()) && (axisYCustomers != null && !axisYCustomers.isEmpty()) && (idDepots != null && !idDepots.isEmpty()) && (axisXDepots != null && !axisXDepots.isEmpty()) && (axisYDepots != null && !axisYDepots.isEmpty()) && (idAssignedCustomers != null && !idAssignedCustomers.isEmpty()) && (countVehicles != null && !countVehicles.isEmpty()) && (capacityVehicles != null && !capacityVehicles.isEmpty()) && (typeProblem.ordinal() >= 0 && typeProblem.ordinal() <= 5))
		{
			Problem.getProblem().setTypeProblem(typeProblem);

			if((typeCustomers != null && !typeCustomers.isEmpty()) && (countTrailers != null && !countTrailers.isEmpty()) && (capacityTrailers != null &&!capacityTrailers.isEmpty()))
			{
				Problem.getProblem().setListCustomers(loadCustomerTTRP(idCustomers, requestCustomers, axisXCustomers, axisYCustomers, typeCustomers));
				Problem.getProblem().setListDepots(loadDepotTTRP(idDepots, axisXDepots, axisYDepots, countVehicles, capacityVehicles, countTrailers, capacityTrailers));

				loaded = true;
			}
			else
			{
				Problem.getProblem().setListCustomers(loadCustomer(idCustomers, requestCustomers, axisXCustomers, axisYCustomers));
				Problem.getProblem().setListDepots(loadDepot(idDepots, axisXDepots, axisYDepots, idAssignedCustomers, countVehicles, capacityVehicles));

				loaded = true;
			}

			if(typeDistance == null)
				typeDistance = DistanceType.Euclidean;

			Problem.getProblem().setCostMatrix(fillCostMatrix(idCustomers, axisXCustomers, axisYCustomers, idDepots, axisXDepots, axisYDepots, typeDistance));
		}

		return loaded;
	}



	/* M�todo encargado de cargar los datos del problema usando listas de distancias con asignaci�n predeterminada*/
	public boolean loadProblem(ArrayList<Integer> idCustomers, ArrayList<Double> requestCustomers, ArrayList<Integer> typeCustomers, ArrayList<Integer> idDepots, ArrayList<ArrayList<Integer>> idAssignedCustomers, ArrayList<Integer> countVehicles, ArrayList<Double> capacityVehicles, ArrayList<Integer> countTrailers, ArrayList<Double> capacityTrailers, ArrayList<ArrayList<Double>> listDistances, ProblemType typeProblem)throws IllegalArgumentException, SecurityException, ClassNotFoundException, InstantiationException, IllegalAccessException, InvocationTargetException, NoSuchMethodException{
		boolean loaded = false;

		if((idCustomers != null && !idCustomers.isEmpty()) && (requestCustomers != null && !requestCustomers.isEmpty()) && (idDepots != null && !idDepots.isEmpty()) && (idAssignedCustomers != null && !idAssignedCustomers.isEmpty()) && (countVehicles != null && !countVehicles.isEmpty()) && (capacityVehicles != null && !capacityVehicles.isEmpty()) && (listDistances != null && !listDistances.isEmpty()) && (typeProblem.ordinal() >= 0 && typeProblem.ordinal() <= 5))
		{
			Problem.getProblem().setTypeProblem(typeProblem);

			if((typeCustomers != null && !typeCustomers.isEmpty()) && (countTrailers != null && !countTrailers.isEmpty()) && (capacityTrailers != null &&!capacityTrailers.isEmpty()))
			{
				Problem.getProblem().setListCustomers(loadCustomerTTRP(idCustomers, requestCustomers, typeCustomers));
				Problem.getProblem().setListDepots(loadDepotTTRP(idDepots, countVehicles, capacityVehicles, countTrailers, capacityTrailers));

				loaded = true;
			}
			else
			{
				Problem.getProblem().setListCustomers(loadCustomer(idCustomers, requestCustomers));
				Problem.getProblem().setListDepots(loadDepot(idDepots, idAssignedCustomers, countVehicles, capacityVehicles));

				loaded = true;
			}

			Problem.getProblem().setCostMatrix(fillCostMatrix(listDistances));
		}

		return loaded;
	}

	/* Metodo encargado de llenar la matriz de costo*/
	private NumericMatrix fillCostMatrix(ArrayList<Integer> idCustomers, ArrayList<Double> axisXCustomers, ArrayList<Double> axisYCustomers, ArrayList<Integer> idDepots, ArrayList<Double> axisXDepots, ArrayList<Double> axisYDepots, DistanceType typeDistance) throws IllegalArgumentException, SecurityException, ClassNotFoundException, InstantiationException, IllegalAccessException, InvocationTargetException, NoSuchMethodException{
		int size = idCustomers.size() + idDepots.size(); 
		NumericMatrix costMatrix = new NumericMatrix(size, size);
		Distance distance = newDistance(typeDistance);

		int row = -1;
		int col = -1;
		int lastCustomer;
		double costInDistance = 0.0;

		for(int i = 0; i < size; i++)
		{
			if(i < idCustomers.size())
				row = Problem.getProblem().getPosElement(idCustomers.get(i));
			else
				row = Problem.getProblem().getPosElement(idDepots.get(i - idCustomers.size()));

			lastCustomer = 0;

			for(int j = (i + 1); j < size; j++)
			{
				if(j < idCustomers.size())
				{
					col = Problem.getProblem().getPosElement(idCustomers.get(j));
					costInDistance = distance.calculateDistance(axisXCustomers.get(i), axisYCustomers.get(i), axisXCustomers.get(j), axisYCustomers.get(j));
				}	//aqui calcular la distancia x la formula de euclidean
				else
				{
					col = Problem.getProblem().getPosElement(idDepots.get(lastCustomer));

					if(i < idCustomers.size())
						costInDistance = distance.calculateDistance(axisXCustomers.get(i), axisYCustomers.get(i), axisXDepots.get(lastCustomer), axisYDepots.get(lastCustomer));
					else
						costInDistance = distance.calculateDistance(axisXDepots.get(i - idCustomers.size()), axisYDepots.get(i - idCustomers.size()), axisXDepots.get(lastCustomer), axisYDepots.get(lastCustomer));

					lastCustomer++;
				}

				costMatrix.setItem(row, col, costInDistance);	
				costMatrix.setItem(col, row, costInDistance);	
			}
		}
		return costMatrix;
	}

	/* M�todo encargado de llenar la matriz de costo usando listas de distancias*/
	private NumericMatrix fillCostMatrix(ArrayList<ArrayList<Double>> listDistances) throws IllegalArgumentException, SecurityException, ClassNotFoundException, InstantiationException, IllegalAccessException, InvocationTargetException, NoSuchMethodException{
		int size = listDistances.size(); 
		NumericMatrix costMatrix = new NumericMatrix(size, size);

		int row = -1;
		int col = -1;
		double costInDistance = 0.0;

		for(int i = 0; i < listDistances.size(); i++)
		{
			row = i;

			for(int j = 0; j < listDistances.get(i).size(); j++)
			{
				col = j;	
				costInDistance = listDistances.get(i).get(j);
				costMatrix.setItem(row, col, costInDistance);	
			}
		}
		return costMatrix;
	}

	/* M�todo encargado de ejecutar una heur�stica de construcci�n*/
	public void executeHeuristic(int countExecution, HeuristicType heuristicType) throws IllegalArgumentException, SecurityException, ClassNotFoundException, InstantiationException, IllegalAccessException, InvocationTargetException, NoSuchMethodException{
		if(calculateTime == true)
			timeExecute = System.currentTimeMillis();

		/*	if(heuristicType.equals(HeuristicType.KilbyAlgorithm)|| heuristicType.equals(HeuristicType.SaveParallel))
			Problem.getProblem().OrdenateMethod(OrderType.Ascending);*/

		Heuristic heuristic = newHeuristic(heuristicType);

		for(int i = 1; i <= countExecution; i++)
		{
			Solution currentSolution = heuristic.getSolutionInicial();	
			currentSolution.calculateCost();
			listSolutions.add(currentSolution);

			if(i == 1)
				bestSolution = currentSolution;
			else
				if(Tools.roundDouble(currentSolution.getCostSolution(), 2) < Tools.roundDouble(bestSolution.getCostSolution(), 2))
					bestSolution = currentSolution; 
		}

		if(calculateTime == true)
		{
			timeExecute -= System.currentTimeMillis();
			timeExecute = Math.abs(timeExecute);
		}

	}

	/* M�todo que devuelve el listado de los clientes de la mejor soluci�n obtenida*/
	public ArrayList<Object> getOrdenVisit(){
		ArrayList<Object> code = new ArrayList<Object>();

		for (int i = 0; i < bestSolution.getListRoutes().size(); i++) 
			for (int j = 0; j < bestSolution.getListRoutes().get(i).getListIdCustomers().size(); j++) 
				code.add(bestSolution.getListRoutes().get(i).getListIdCustomers().get(j));	

		return code;
	}

	/*M�todo que devuelve todas las soluciones obtenidas con la heur�stica*/
	public ArrayList<ArrayList<Object>> getAllSolutions (){
		ArrayList<ArrayList<Object>> allSolutions = new ArrayList<ArrayList<Object>>();
		ArrayList<Object> code = new ArrayList<Object>();

		for (int i = 0; i < listSolutions.size(); i++) 
		{
			for (int j = 0; j < listSolutions.get(i).getListRoutes().size(); j++) 
				for (int k = 0; k < listSolutions.get(i).getListRoutes().get(j).getListIdCustomers().size(); k++) 
					code.add(listSolutions.get(i).getListRoutes().get(j).getListIdCustomers().get(k));	

			allSolutions.add(code);
		}
		return allSolutions;
	}

	/* M�todo que devuelve el costo total de la mejor solucion */
	public double getTotalCostSolution(){

		return Tools.roundDouble(bestSolution.getCostSolution(), 2);
	}

	/* M�todo que devuelve la cantidad de rutas de una soluci�n */
	public int countRoutes(){
		int countRoutes = bestSolution.getListRoutes().size();

		return countRoutes;
	}

	/* M�todo que devuelve la demanda para cada una de las rutas de la mejor soluci�n */
	public ArrayList<Double> getRequestByRoute(){
		ArrayList<Double> listRequests = new ArrayList<Double>();

		for(int i = 0; i < bestSolution.getListRoutes().size(); i++)
			listRequests.add(bestSolution.getListRoutes().get(i).getRequestRoute());			

		return listRequests;
	}

	/* M�todo que devuelve el tipo de cada una de las rutas de la mejor soluci�n*/
	public ArrayList<RouteType> getTypeRouteByRoute(){
		ArrayList<RouteType> listTypes = new ArrayList<RouteType>();

		for(int i = 0; i < bestSolution.getListRoutes().size(); i++)
			listTypes.add(((RouteTTRP)bestSolution.getListRoutes().get(i)).getTypeRoute());	

		return listTypes;
	}

	/*M�todo que devuelve la cantida de rutas para un dep�sito dado en la mejor soluci�n */
	public int countRoutesForDepot(int idDepot){
		int countRoutes = 0;

		for(int i = 0; i < bestSolution.getListRoutes().size(); i++)
			if(bestSolution.getListRoutes().get(i).getIdDepot() == idDepot)
				countRoutes++;

		return countRoutes;
	}

	/*M�todo que devuelve la demanda cubierta para un dep�sito dado en la mejor soluci�n*/
	public double requestForDepot(int idDepot){
		double requestDepot = -1;

		for(int i = 0; i < bestSolution.getListRoutes().size(); i++)
			if(bestSolution.getListRoutes().get(i).getIdDepot() == idDepot)
				requestDepot += bestSolution.getListRoutes().get(i).getRequestRoute();

		return requestDepot;
	}

	/*M�todo que devuelve las rutas para un dep�sito dado en la mejor soluci�n*/
	public ArrayList<ArrayList<Integer>> routesForDepot(int idDepot){
		ArrayList<ArrayList<Integer>> listRoutesDepot = new ArrayList<ArrayList<Integer>>();

		for(int i = 0; i < bestSolution.getListRoutes().size(); i++)
			if(bestSolution.getListRoutes().get(i).getIdDepot() == idDepot)
				listRoutesDepot.add(bestSolution.getListRoutes().get(i).getListIdCustomers());

		return listRoutesDepot;
	}

	/*Metodo que devuelve el costo total para un dep�sito dado en la mejor soluci�n*/
	public double costForDepot(int idDepot){
		double costDepot = -1;

		for(int i = 0; i < bestSolution.getListRoutes().size(); i++)
			if(bestSolution.getListRoutes().get(i).getIdDepot() == idDepot)
				costDepot += bestSolution.getListRoutes().get(i).getCostRoute();

		return Tools.roundDouble(costDepot, 2);
	}

	/*Metodo que restaura los par�metros globales de la clase Strategy*/
	public void cleanStrategy() {
		bestSolution = null;
		listSolutions.clear();

		timeExecute = (long) 0.0;
	}

	/* Metodo que destruye la instancia de la controladora */
	public static void destroyStrategy() {
		strategyHeuristic = null;
	}
}
