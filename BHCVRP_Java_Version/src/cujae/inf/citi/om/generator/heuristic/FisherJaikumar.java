/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package cujae.inf.citi.om.generator.heuristic;

/**
 *
 * @author kmych
 */
import cujae.inf.citi.om.data.BusStop;
import cujae.inf.citi.om.data.Customer;
import cujae.inf.citi.om.data.CustomerTTRP;
import cujae.inf.citi.om.data.CustomerType;
import cujae.inf.citi.om.data.Depot;
import cujae.inf.citi.om.data.FleetTTRP;
import cujae.inf.citi.om.data.Problem;
import cujae.inf.citi.om.data.ProblemType;
import cujae.inf.citi.om.solution.Route;
import cujae.inf.citi.om.solution.RouteTTRP;
import cujae.inf.citi.om.solution.RouteType;
import cujae.inf.citi.om.solution.Solution;
import cujae.inf.ic.om.matrix.NumericMatrix;
import java.util.*;

public class FisherJaikumar extends Heuristic {

    private ArrayList<Customer> seedPoints;
    private double vehicleCapacity;
    private int numVehicles;
    private Map<Integer, ArrayList<Customer>> assignedElements;
    private double trailerCapacity;
    private int numTrailers;
    private ArrayList<Depot> depots;
    private Solution solution;
    private ArrayList<Customer> feasibleCustomers;
    private double timeRoute;

    public FisherJaikumar() {
        this.seedPoints = new ArrayList<>();
        this.assignedElements = new HashMap<>();
        this.depots = new ArrayList<>();
    }

    public void initializeSpecifics() {
        // Inicializar parámetros específicos de la heurística
        Problem problem = Problem.getProblem();
        this.numVehicles = problem.getListDepots().get(0).getListFleets().get(0).getCountVehicles();

        if (this.typeProblem == ProblemType.HFVRP) {
            this.vehicleCapacity = problem.getListCapacities().get(0);
            for (int i = 0; i < this.numVehicles; i++) {
                this.assignedElements.put(i, new ArrayList<>());
            }
        } else {
            this.vehicleCapacity = problem.getListDepots().get(0).getListFleets().get(0).getCapacityVehicle();
        }

        if (this.typeProblem == ProblemType.TTRP) {
            FleetTTRP fleetTTRP = (FleetTTRP) problem.getListDepots().get(0).getListFleets().get(0);
            this.trailerCapacity = fleetTTRP.getCapacityTrailer();
            this.numTrailers = fleetTTRP.getCountTrailers();

            for (int i = 0; i < this.numVehicles + this.numTrailers; i++) {
                this.assignedElements.put(i, new ArrayList<>());
            }
        }

        this.depots = problem.getListDepots();

        if (this.typeProblem == ProblemType.MDVRP) {
            for (Depot depot : this.depots) {
                Map<Integer, List<Customer>> depotAssignedElements = new HashMap<>();
                for (int i = 0; i < depot.getListFleets().get(0).getCountVehicles(); i++) {
                    depotAssignedElements.put(i, new ArrayList<>());
                }
                this.assignedElements.put(depot.getIdDepot(), (ArrayList<Customer>) depotAssignedElements);
            }
        }

        this.seedPoints = this.getSeedPoints();
    }

    public Solution getSolutionInicial() {
        this.processing();
        this.execute();
        return this.solution;
    }

    public ArrayList<Customer> getSeedPoints() {
        ArrayList<Customer> elements;
        ArrayList<Customer> sortedElements;

        // Seleccionar los clientes con mayor demanda como puntos semilla
        elements = Problem.getProblem().getListCustomers();
        sortedElements = new ArrayList<>(elements);
        sortedElements.sort(Comparator.comparing(Customer::getRequestCustomer).reversed());

        if (this.typeProblem == ProblemType.CVRP || this.typeProblem == ProblemType.OVRP ||
            this.typeProblem == ProblemType.SBRP || this.typeProblem == ProblemType.VRPTW) {
            // Seleccionar los primeros `numVehicles` clientes como puntos semilla
            return (ArrayList<Customer>) sortedElements.subList(0, Math.min(this.numVehicles, sortedElements.size()));
        } else if (this.typeProblem == ProblemType.HFVRP ) {
            // Ordenar vehículos por capacidad (de mayor a menor)
            List<Integer> sortedVehicles = new ArrayList<>();
            for (int i = 0; i < this.numVehicles; i++) {
                sortedVehicles.add(i);
            }
            sortedVehicles.sort(Comparator.comparingDouble(i -> this.vehicleCapacity)); // Orden ascendente
            Collections.reverse(sortedVehicles); 

            // Asignar los clientes con mayor demanda a los vehículos con mayor capacidad
            ArrayList<Customer> seedPoints = new ArrayList<>();
            for (int i = 0; i < Math.min(this.numVehicles, sortedElements.size()); i++) {
                seedPoints.add(sortedElements.get(i));
                this.assignedElements.get(sortedVehicles.get(i)).add((Customer) sortedElements.get(i));
            }

            return seedPoints;
        } else if (this.typeProblem == ProblemType.TTRP ) {
            // Seleccionar los primeros `numVehicles` clientes TC como puntos semilla para camiones
            List<Customer> tcCustomers = new ArrayList<>();
            for (Customer element : sortedElements) {
                Customer customer = element;
                if (((CustomerTTRP)customer).getTypeCustomer() == CustomerType.TC) {
                    tcCustomers.add(customer);
                }
            }
            ArrayList<Customer> seedPointsTC = (ArrayList<Customer>) tcCustomers.subList(0, Math.min(this.numVehicles, tcCustomers.size()));

            // Seleccionar los primeros `numTrailers` clientes VC como puntos semilla para remolques
            ArrayList<Customer> vcCustomers = new ArrayList<>();
            for (Object element : sortedElements) {
                Customer customer = (Customer) element;
                if (((CustomerTTRP)customer).getTypeCustomer() == CustomerType.VC ) {
                    vcCustomers.add(customer);
                }
            }
            List<Customer> seedPointsVC = vcCustomers.subList(0, Math.min(this.numTrailers, vcCustomers.size()));

            // Combinar los puntos semilla para camiones y remolques
            ArrayList<Customer> seedPoints = new ArrayList<>();
            seedPoints.addAll(seedPointsTC);
            seedPoints.addAll(seedPointsVC);

            // Asignar los puntos semilla a los vehículos correspondientes
            for (int i = 0; i < seedPoints.size(); i++) {
                if (i < this.numVehicles) {
                    this.assignedElements.get(i).add((Customer) seedPoints.get(i)); // Asignar a camiones
                } else {
                    this.assignedElements.get(i).add((Customer) seedPoints.get(i)); // Asignar a remolques
                }
            }

            return seedPoints;
        } else if (this.typeProblem == ProblemType.MDVRP) {
            ArrayList<Customer> seedPoints = new ArrayList<>();
            for (Depot depot : this.depots) {
                // Obtener los clientes asignados a este depósito
                ArrayList<Customer> depotCustomers = Problem.getProblem().getCustomersAssignedByIDDepot(depot.getIdDepot(), (ArrayList<Customer>) elements, (ArrayList<Depot>) this.depots);
                // Seleccionar los primeros `numVehicles` clientes como puntos semilla para este depósito
                ArrayList<Customer> depotSeedPoints = new ArrayList<>(depotCustomers);
                depotSeedPoints.sort(Comparator.comparing(Customer::getRequestCustomer).reversed());
                depotSeedPoints = (ArrayList<Customer>) depotSeedPoints.subList(0, Math.min(depot.getListFleets().get(0).getCountVehicles(), depotSeedPoints.size()));
                seedPoints.addAll(depotSeedPoints);

                // Asignar los puntos semilla a los vehículos correspondientes
                for (int i = 0; i < depotSeedPoints.size(); i++) {
                    this.assignedElements.get(i).add(depotSeedPoints.get(i));
                }
            }

            return seedPoints;
        }

        return new ArrayList<>(); // Retornar una lista vacía si no se cumple ninguna condición
    }

    @Override
    public void processing() {
        if (this.typeProblem == ProblemType.CVRP || this.typeProblem == ProblemType.OVRP || this.typeProblem == ProblemType.SBRP || this.typeProblem == ProblemType.VRPTW ) {
            ArrayList<Customer> elements;
            elements = Problem.getProblem().getListCustomers();
            NumericMatrix costMatrix = Problem.getProblem().getCostMatrix();

            for (int i = 0; i < this.numVehicles; i++) {
                this.assignedElements.put(i, new ArrayList<>());
            }

            for (Customer element : elements) {
                if (this.seedPoints.contains(element)) {
                    int vehicleIndex = this.seedPoints.indexOf(element);
                    this.assignedElements.get(vehicleIndex).add(element);
                } else {
                    double minCost = Double.MAX_VALUE;
                    int bestVehicle = 0;

                    for (int i = 0; i < this.seedPoints.size(); i++) {
                        Customer seed = this.seedPoints.get(i);
                        double cost;
                        cost = costMatrix.getItem(element.getIdCustomer(), seed.getIdCustomer());
                        if (cost < minCost) {
                            minCost = cost;
                            bestVehicle = i;
                        }
                    }

                    int totalDemand = 0;
                    for (Customer customer : this.assignedElements.get(bestVehicle)) {
                        totalDemand += customer.getRequestCustomer();
                    }
                        if (totalDemand + element.getRequestCustomer() <= this.vehicleCapacity) {
                            this.assignedElements.get(bestVehicle).add(element);
                        }
                    }
                }
        } else if (this.typeProblem == ProblemType.HFVRP) {
            List<Customer> elements = Problem.getProblem().getListCustomers();
            NumericMatrix costMatrix = Problem.getProblem().getCostMatrix();

            for (Customer element : elements) {
                if (this.seedPoints.contains(element)) {
                    continue;
                }

                double minCost = Double.MAX_VALUE;
                int bestVehicle = -1;

                for (int i = 0; i < this.seedPoints.size(); i++) {
                    Customer seed = this.seedPoints.get(i);
                    double cost = costMatrix.getItem(element.getIdCustomer(), seed.getIdCustomer());
                    if (cost < minCost) {
                        int totalDemand = 0;
                        for (Customer customer : this.assignedElements.get(i)) {
                            totalDemand += customer.getRequestCustomer();
                        }
                        if (totalDemand + element.getRequestCustomer() <= this.vehicleCapacity) {
                            minCost = cost;
                            bestVehicle = i;
                        }
                    }
                }

                if (bestVehicle != -1) {
                    this.assignedElements.get(bestVehicle).add(element);
                }
            }
        } else if (this.typeProblem == ProblemType.TTRP) {
            List<Customer> elements = Problem.getProblem().getListCustomers();
            NumericMatrix costMatrix = Problem.getProblem().getCostMatrix();

            for (Customer element : elements) {
                if (this.seedPoints.contains(element)) {
                    continue;
                }

                double minCost = Double.MAX_VALUE;
                int bestVehicle = -1;

                for (int i = 0; i < this.seedPoints.size(); i++) {
                    Customer seed = this.seedPoints.get(i);
                    double cost = costMatrix.getItem(element.getIdCustomer(), seed.getIdCustomer());
                    if (cost < minCost) {
                        if (((CustomerTTRP)element).getTypeCustomer() == CustomerType.TC) {
                            if (i < this.numVehicles) {
                                int totalDemand = 0;
                                for (Customer customer : this.assignedElements.get(i)) {
                                    totalDemand += customer.getRequestCustomer();
                                }
                                if (totalDemand + element.getRequestCustomer() <= this.vehicleCapacity) {
                                    minCost = cost;
                                    bestVehicle = i;
                                }
                            }
                        } else {
                            if (i < this.numVehicles + this.numTrailers) {
                                int totalDemand = 0;
                                for (Customer customer : this.assignedElements.get(i)) {
                                    totalDemand += customer.getRequestCustomer();
                                }
                                if (totalDemand + element.getRequestCustomer() <= this.vehicleCapacity + this.trailerCapacity) {
                                    minCost = cost;
                                    bestVehicle = i;
                                }
                            }
                        }
                    }
                }

                if (bestVehicle != -1) {
                    this.assignedElements.get(bestVehicle).add(element);
                }
            }
        } else if (this.typeProblem == ProblemType.MDVRP) {
            ArrayList<Customer> customers = Problem.getProblem().getListCustomers();
            NumericMatrix costMatrix = Problem.getProblem().getCostMatrix();

            for (Depot depot : this.depots) {
                ArrayList<Customer> depotCustomers = Problem.getProblem().getCustomersAssignedByIDDepot(depot.getIdDepot(), customers, this.depots);
                for (Customer customer : depotCustomers) {
                    if (this.seedPoints.contains(customer)) {
                        continue;
                    }

                    double minCost = Double.MAX_VALUE;
                    int bestVehicle = -1;

                    for (int i = 0; i < this.seedPoints.size(); i++) {
                        Customer seed = this.seedPoints.get(i);
                        int id_depot = Problem.getProblem().getIDDepotByIDCustomer(seed.getIdCustomer());
                        if (id_depot == depot.getIdDepot()) {
                            double cost = costMatrix.getItem(customer.getIdCustomer(), seed.getIdCustomer());
                            if (cost < minCost) {
                                int totalDemand = 0;
                                for (Customer assignedCustomer : this.assignedElements.get(depot.getIdDepot())) {
                                    totalDemand += assignedCustomer.getRequestCustomer();
                                }
                                if (totalDemand + customer.getRequestCustomer() <= this.vehicleCapacity) {
                                    minCost = cost;
                                    bestVehicle = i;
                                }
                            }
                        }
                    }

                    if (bestVehicle != -1) {
                        this.assignedElements.get(bestVehicle).add(customer);
                    }
                }
            }
        }
    }

    public void routing() {
        if (this.typeProblem == ProblemType.CVRP || this.typeProblem == ProblemType.OVRP || this.typeProblem == ProblemType.HFVRP || this.typeProblem == ProblemType.TTRP || this.typeProblem == ProblemType.SBRP || this.typeProblem == ProblemType.VRPTW ) {
            Depot depot = Problem.getProblem().getListDepots().get(0);
            NumericMatrix costMatrix = Problem.getProblem().getCostMatrix();

            for (Map.Entry<Integer, ArrayList<Customer>> entry : this.assignedElements.entrySet()) {
                int vehicleId = entry.getKey();
                List<Customer> elements = entry.getValue();

                if (elements.isEmpty()) {
                    continue;
                }

                Route route;
                if (this.typeProblem == ProblemType.TTRP) {
                    route = new RouteTTRP();
                    route.setIdDepot(depot.getIdDepot());

                    if (vehicleId < this.numVehicles) {
                        ((RouteTTRP)route).setTypeRoute(RouteType.PVR);
                    } else {
                        ((RouteTTRP)route).setTypeRoute(RouteType.PTR);
                    }
                } else {
                    route = new Route();
                    route.setIdDepot(depot.getIdDepot());
                }

                int currentNode = depot.getIdDepot();
                ArrayList<Customer> remainingElements = new ArrayList<>(elements);

                if (this.typeProblem == ProblemType.VRPTW) {
                    Customer nearestElement = this.getNNElement(remainingElements, currentNode);
                    route.getListIdCustomers().add(nearestElement.getIdCustomer());
                    currentNode = nearestElement.getIdCustomer();
                }

                while (!remainingElements.isEmpty()) {
                    Customer nearestElement = this.getNNElement(remainingElements, currentNode);

                        if (this.vehicleCapacity >= (route.getRequestRoute() + nearestElement.getRequestCustomer())) {
                            boolean twFlag = true;
                            if (this.typeProblem == ProblemType.VRPTW) {
                                this.timeRoute = this.getTimeRoute(route.getListIdCustomers());
                                this.feasibleCustomers = this.get_feasible_customers(route.getListIdCustomers().get(route.getListIdCustomers().size() - 1));
                                if (this.feasibleCustomers.contains(nearestElement)) {
                                    NumericMatrix timeMatrix = Problem.getProblem().getTimeMatrix();
                                    double currentTime = timeMatrix.getItem(route.getListIdCustomers().get(route.getListIdCustomers().size() - 1), nearestElement.getIdCustomer());
                                    double customerReadyTime = nearestElement.getTimeWindow().getInitialNode();
                                    double customerServiceTime = nearestElement.getTimeWindow().getServiceTime();
                                    this.timeRoute = Math.max(currentTime, customerReadyTime) + customerServiceTime;
                                } else {
                                    twFlag = false;
                                    nearestElement = this.getNNElement(remainingElements, currentNode);
                                }
                            }
                            if (twFlag) {
                                route.getListIdCustomers().add(nearestElement.getIdCustomer());
                                currentNode = nearestElement.getIdCustomer();
                            }
                        } else {
                            route = new Route();
                            route.getListIdCustomers().add(nearestElement.getIdCustomer());
                            currentNode = nearestElement.getIdCustomer();
                        }

                    remainingElements.remove(nearestElement);
                }

                this.solution.getListRoutes().add(route);
            }
        } else if (this.typeProblem == ProblemType.MDVRP) {
            NumericMatrix costMatrix = Problem.getProblem().getCostMatrix();

            for (Depot depot : this.depots) {
                Map<Integer, ArrayList<Customer>> depotElements = (Map<Integer, ArrayList<Customer>>) assignedElements.get(depot.getIdDepot());
                for (Map.Entry<Integer, ArrayList<Customer>> entry : depotElements.entrySet()) {
                    int vehicleId = entry.getKey();
                    ArrayList<Customer> customers = entry.getValue();

                    if (customers.isEmpty()) {
                        continue;
                    }

                    Route route = new Route();
                    route.setIdDepot(depot.getIdDepot());

                    int currentNode = depot.getIdDepot();
                    ArrayList<Customer> remainingCustomers = new ArrayList<>(customers);

                    while (!remainingCustomers.isEmpty()) {
                        Customer nearestCustomer = this.getNNElement(remainingCustomers, currentNode);
                        route.getListIdCustomers().add(nearestCustomer.getIdCustomer());
                        currentNode = nearestCustomer.getIdCustomer();
                        remainingCustomers.remove(nearestCustomer);
                    }

                    this.solution.getListRoutes().add(route);
                }
            }
        }
    }

    private Customer getNNElement(ArrayList<Customer> listElements, int reference) {
        int RLC = 1;

        if (listElements.size() == 1) {
            return listElements.get(0);
        } else {
            List<Customer> listNN = this.getListNN(listElements, reference);
            List<Customer> listRLC = new ArrayList<>();

            listRLC.add(listNN.get(RLC));
            return listRLC.remove(0);
        }
    }

    /* M�todo que devuelve la lista de vecinos m�s cercanos */
	private ArrayList<Customer> getListNN(ArrayList<Customer> listCustomers, int reference){
		ArrayList<Double> listDistances = new ArrayList<Double>();
		ArrayList<Customer> listNN = new ArrayList<Customer>();
		double refDistance = 0.0;
		
		for (int i = 0 ; i < listCustomers.size(); i++)
		{
			refDistance = Problem.getProblem().getCostMatrix().getItem(Problem.getProblem().getPosElement(reference), Problem.getProblem().getPosElement(listCustomers.get(i).getIdCustomer()));
			listDistances.add(refDistance);
			listNN.add(listCustomers.get(i));
		}
		
		AscendentOrdenate(listDistances, listNN);

		return listNN;
	}
        
            
}