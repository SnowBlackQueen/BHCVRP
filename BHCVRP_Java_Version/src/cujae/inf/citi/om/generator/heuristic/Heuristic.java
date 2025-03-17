package cujae.inf.citi.om.generator.heuristic;

import java.util.ArrayList;
import java.util.Random;

import cujae.inf.citi.om.data.Customer;
import cujae.inf.citi.om.data.CustomerType;
import cujae.inf.citi.om.data.Problem;
import cujae.inf.citi.om.data.ProblemType;
import cujae.inf.citi.om.data.Depot;
import cujae.inf.citi.om.data.DepotMDVRP;
import cujae.inf.citi.om.controller.StrategyHeuristic;
import cujae.inf.citi.om.data.CustomerTTRP;
import cujae.inf.citi.om.data.Fleet;
import cujae.inf.citi.om.data.FleetTTRP;
import cujae.inf.citi.om.solution.Route;
import cujae.inf.citi.om.solution.RouteTTRP;
import cujae.inf.citi.om.solution.RouteType;
import cujae.inf.citi.om.solution.Solution;
import java.util.Iterator;
import cujae.inf.ic.om.matrix.NumericMatrix;
import cujae.inf.ic.om.matrix.RowCol;

/* Clase abstracta que modela una heur�stica de construcci�n*/

public abstract class Heuristic {
	
        boolean initialized = false;
        ProblemType typeProblem = Problem.getProblem().getTypeProblem();
    private int posDepot;
    private int idDepot;
    private double capacityVehicle;
    private int countVehicles;
    Route route;
    private Customer customer;
    double requestRoute;
    ArrayList<Customer> customersToVisit;
    private Solution solution;
    private int vehicleCount;
    private ArrayList<Double> listCapacities;
    boolean isTC;
    private double capacityTrailer;
    private NumericMatrix time_matrix;
    private double time_route;
    
	/* M�todo abstracto encargado de generar la soluci�n*/
	public abstract Solution getSolutionInicial();
        
        // Método abstracto para inicializar parámetros específicos de algunas heurísticas
        public abstract void initializeSpecifics();
        
        public void comunInitialize() {
            Solution solution = new Solution();
            ArrayList<Customer> customersToVisit = new ArrayList<Customer>();
            int idDepot = -1;
            int posDepot = -1;

            if (Problem.getProblem().getTypeProblem() == ProblemType.CVRP
                || Problem.getProblem().getTypeProblem() == ProblemType.HFVRP
                || Problem.getProblem().getTypeProblem() == ProblemType.OVRP
                || Problem.getProblem().getTypeProblem() == ProblemType.TTRP){
                posDepot = 0;
                idDepot = Problem.getProblem().getListDepots().get(posDepot).getIdDepot();
                customersToVisit = Problem.getProblem().getListCustomers();
            }
            else {
                int i = 0;
                boolean found = false;

                ArrayList<Depot> depots = Problem.getProblem().getListDepots();

                while (i < depots.size() && !found){
                    if ((depots.get(i) instanceof DepotMDVRP) || ((DepotMDVRP)depots.get(i)).getListAssignedCustomers().isEmpty()) {
                        posDepot = i;
                        idDepot = depots.get(posDepot).getIdDepot();  // VERIFICAR!!
                        ArrayList<Customer> customersAssignedByDepot = Problem.getProblem().getCustomersAssignedByIDDepot(idDepot, Problem.getProblem().getListCustomers(), Problem.getProblem().getListDepots());
                        customersToVisit = new ArrayList<>(customersAssignedByDepot);

                        found = true;
                    }   
                    else {
                        i += 1;
                    }
                }
            }

            double capacityVehicle = (Problem.getProblem().getListDepots().get(posDepot).getListFleets().get(0).getCapacityVehicle());
            int countVehicles = (Problem.getProblem().getListDepots().get(posDepot).getListFleets().get(0).getCountVehicles());

            Customer customer = new Customer();
            double requestRoute = 0.0;
            Route route = new Route();

            ProblemType typeProblem = Problem.getProblem().getTypeProblem();

            if (typeProblem.equals(ProblemType.TTRP) || (typeProblem.ordinal() == 4)) {
                route = new RouteTTRP();
            }
                 
        }
        
        public Solution templateMethod(){
            comunInitialize();
            initializeSpecifics();
            initialized = true;
            
            return getSolutionInicial(); 
        }
        
        public Solution execute(){
            Solution solution = new Solution();
            
            if (Problem.getProblem().getTypeProblem().equals(ProblemType.CVRP) || Problem.getProblem().getTypeProblem().ordinal() == 1){
                processing();
            }
            else if (Problem.getProblem().getTypeProblem().equals(ProblemType.HFVRP) || Problem.getProblem().getTypeProblem().ordinal() == 2){
                processing();
                ArrayList<Customer> customersToVisit = Problem.getProblem().getListCustomers();
                
                if(!customersToVisit.isEmpty())
		{
                    Route route = new Route();
                    double requestRoute = 0.0;
                    Customer customer = new Customer(); //Esto está mal, xq el customer viene del método initializeSpecifics();

                    ArrayList<Double> listCapacities = new ArrayList<Double>(Problem.getProblem().getListCapacities());
                    Iterator<Double> iteratorCapVehicle = listCapacities.iterator();

                    while(!customersToVisit.isEmpty())
                    {
                        int j = 0;
                            boolean found = false;	

                            requestRoute = solution.getListRoutes().get(j).getRequestRoute();

                            while((iteratorCapVehicle.hasNext()) && (!found))
                            {	
                                    if(iteratorCapVehicle.next() >= (requestRoute + customer.getRequestCustomer()))
                                    {
                                            solution.getListRoutes().get(j).setRequestRoute(requestRoute + customer.getRequestCustomer());
                                            solution.getListRoutes().get(j).getListIdCustomers().add(customer.getIdCustomer());
                                            customersToVisit.remove(customer);

                                            found = true;
                                    }
                                    else
                                    {
                                            j++;	
                                            requestRoute = solution.getListRoutes().get(j).getRequestRoute();
                                    }	
                            }

                            if(!found)
                            {
                                    route.getListIdCustomers().add(customer.getIdCustomer());
                                    route.setRequestRoute(route.getRequestRoute() + customer.getRequestCustomer());
                                    customersToVisit.remove(customer);
                            }

                            if(!customersToVisit.isEmpty())
                                    initializeSpecifics();
                    }
                
                }
            }
            else if (Problem.getProblem().getTypeProblem().equals(ProblemType.MDVRP) || Problem.getProblem().getTypeProblem().ordinal() == 3){
                ArrayList<Depot> depots = Problem.getProblem().getListDepots();
                for (int depotIndex = this.posDepot; depotIndex < depots.size(); depotIndex++) {
                    if (depotIndex != this.posDepot) {
                        this.idDepot = depots.get(depotIndex).getIdDepot();
                        ArrayList<Customer> customersToVisit = Problem.getProblem().getCustomersAssignedByIDDepot(
                                                                                    this.idDepot,
                                                                                    Problem.getProblem().getListCustomers(),
                                                                                    Problem.getProblem().getListDepots());
                        this.capacityVehicle = depots.get(depotIndex).getListFleets().get(0).getCapacityVehicle();
                        this.countVehicles = depots.get(depotIndex).getListFleets().get(0).getCountVehicles();

                        if (!customersToVisit.isEmpty()) {
                            this.route = new Route();
                            this.initializeSpecifics();
                            double requestRoute = this.customer.getRequestCustomer();
                            this.route.getListIdCustomers().add(this.customer.getIdCustomer());
                            customersToVisit.remove(this.customer);
                        } else {
                            continue;
                        }
                    }
                    this.creating();
                }
                
            }
            
            else if (Problem.getProblem().getTypeProblem().equals(ProblemType.TTRP) || Problem.getProblem().getTypeProblem().ordinal() == 4){
                boolean isTC = false;
                double capacityTrailer = ((FleetTTRP) Problem.getProblem()
                        .getListDepots().get(posDepot)
                        .getListFleets().get(0)).getCapacityTrailer();

                CustomerType customerType = ((CustomerTTRP) customer).getTypeCustomer();

                processing();

                route.setRequestRoute(requestRoute);

                if (((CustomerTTRP) customer).getTypeCustomer() == CustomerType.TC /*|| ((CustomerTTRP) customer).getTypeCustomer() == 1*/) {
                    ((RouteTTRP)route).setTypeRoute(RouteType.PTR);
                } else {
                    if (isTC) {
                        ((RouteTTRP)route).setTypeRoute(RouteType.CVR);
                    } else {
                        ((RouteTTRP)route).setTypeRoute(RouteType.PVR);
                    }
                }

                route.setIdDepot(idDepot);
                solution.getListRoutes().add(route);
                
                
            }
            
            return solution;
        }
        
        public void processing() {
            boolean created = false;
            if (this.typeProblem == ProblemType.CVRP) {
                if (this.requestRoute + this.customer.getRequestCustomer() <= this.capacityVehicle) {
                    this.requestRoute += this.customer.getRequestCustomer();
                    this.route.getListIdCustomers().add(this.customer.getIdCustomer());
                    this.customersToVisit.remove(this.customer);
                    if (this.customersToVisit.isEmpty()) {
                        this.route.setRequestRoute(this.requestRoute);
                        this.route.setIdDepot(this.idDepot);
                        this.solution.getListRoutes().add(this.route);
                    }
                } else {
                    this.route.setRequestRoute(this.requestRoute);
                    this.route.setIdDepot(this.idDepot);
                    this.solution.getListRoutes().add(this.route);
                    this.route = new Route();
                    this.route.getListIdCustomers().add(this.customer.getIdCustomer());
                    this.requestRoute = this.customer.getRequestCustomer();
                    this.customersToVisit.remove(this.customer);
                    created = true;
                }

            } else if (this.typeProblem == ProblemType.HFVRP) {
                while (!this.customersToVisit.isEmpty()) {
                    this.initializeSpecifics();

                    if (this.capacityVehicle >= (this.requestRoute + this.customer.getRequestCustomer())) {
                        this.requestRoute += this.customer.getRequestCustomer();
                        this.route.getListIdCustomers().add(this.customer.getIdCustomer());
                        this.customersToVisit.remove(this.customer); // Removes the first processed customer
                    } else {
                        this.route.setRequestRoute(this.requestRoute);
                        this.route.setIdDepot(this.idDepot);
                        this.solution.getListRoutes().add(this.route);
                    }
                }
                //return new Tuple<>(true, null); // Indicating that the vehicle still has capacity
            } else if (this.typeProblem == ProblemType.MDVRP) {
                while (!this.customersToVisit.isEmpty() && this.countVehicles > 0) {
                    this.initializeSpecifics();

                    if (this.capacityVehicle >= (this.requestRoute + this.customer.getRequestCustomer())) {
                        this.requestRoute += this.customer.getRequestCustomer();
                        this.route.getListIdCustomers().add(this.customer.getIdCustomer());
                        this.customersToVisit.remove(this.customer);
                    } else {
                        this.route.setRequestRoute(this.requestRoute);
                        this.route.setIdDepot(this.idDepot);
                        this.solution.getListRoutes().add(this.route);
                        this.countVehicles--;

                        if (this.countVehicles > 0) {
                            this.route = new Route();
                            this.route.getListIdCustomers().add(this.customer.getIdCustomer());
                            this.requestRoute = this.customer.getRequestCustomer();
                            this.customersToVisit.remove(this.customer);
                        }
                    }
                }

                if (this.route != null) {
                    this.route.setRequestRoute(this.requestRoute);
                    this.route.setIdDepot(this.idDepot);
                }

                if (!this.customersToVisit.isEmpty()) {
                    this.route = new Route();
                    this.requestRoute = 0.0;

                    while (!this.customersToVisit.isEmpty()) {
                        int k = 0;
                        boolean found = false;
                        this.requestRoute = this.solution.getListRoutes().get(k).getRequestRoute();

                        while (k < this.solution.getListRoutes().size() && !found) {
                            if (this.capacityVehicle >= (this.requestRoute + this.customer.getRequestCustomer())) {
                                this.solution.getListRoutes().get(k).setRequestRoute(
                                    this.requestRoute + this.customer.getRequestCustomer());
                                this.solution.getListRoutes().get(k).getListIdCustomers().add(this.customer.getIdCustomer());
                                this.customersToVisit.remove(this.customer);
                                found = true;
                            } else {
                                k++;
                                if (k < this.solution.getListRoutes().size()) {
                                    this.requestRoute = this.solution.getListRoutes().get(k).getRequestRoute();
                                }
                            }
                        }

                        if (!found) {
                            this.route.getListIdCustomers().add(this.customer.getIdCustomer());
                            this.route.setRequestRoute(this.route.getRequestRoute() + this.customer.getRequestCustomer());
                            this.customersToVisit.remove(this.customer);
                        }

                        if (!this.customersToVisit.isEmpty()) {
                            this.initializeSpecifics();
                        }
                    }

                    if (!this.route.getListIdCustomers().isEmpty()) {
                        this.route.setIdDepot(this.idDepot);
                        this.solution.getListRoutes().add(this.route);
                    }
                }
            } else if (this.typeProblem == ProblemType.TTRP) {
                if (this.requestRoute + this.customer.getRequestCustomer() <= this.capacityVehicle) {
                    this.requestRoute += this.customer.getRequestCustomer();
                    this.route.getListIdCustomers().add(this.customer.getIdCustomer());
                    this.customersToVisit.remove(this.customer);
                } else {
                    this.route.setRequestRoute(this.requestRoute);
                    this.route.setIdDepot(this.idDepot);
                    this.route = new RouteTTRP(
                        this.route.getListIdCustomers(),
                        this.route.getRequestRoute(),
                        this.route.getCostRoute(),
                        this.idDepot,
                        new ArrayList<>(),
                        RouteType.PTR
                    );
                    this.solution.getListRoutes().add(this.route); // VERIFY!!

                    this.route = new RouteTTRP();
                    this.requestRoute = this.customer.getRequestCustomer();
                    CustomerType typeCustomer = ((CustomerTTRP)this.customer).getTypeCustomer();
                    this.route.getListIdCustomers().add(this.customer.getIdCustomer());
                    this.customersToVisit.remove(this.customer);
                }
                created = true;
                //return new Tuple<>(created, this.route);
            }
        
        }   
        
        public void creating(){
            if (this.typeProblem == ProblemType.CVRP) {
                int vehicleCountInt = vehicleCount;
                while (customersToVisit != null && !customersToVisit.isEmpty() && vehicleCountInt > 0) {
                    this.initializeSpecifics();  // Para que customer sea tratado según la variante
                    boolean found = true;
                    Route newRoute = new Route();
                    this.creating();
                    if (found) {
                        route = newRoute;
                        vehicleCountInt--;
                    }
                }
            } else if (this.typeProblem == ProblemType.HFVRP) {
                this.listCapacities = new ArrayList<>(Problem.getProblem().getListCapacities());
                Double vehicleCapacity = this.listCapacities.get(0);
                boolean isOpen = true;

                while (customersToVisit != null && !customersToVisit.isEmpty() && !this.listCapacities.isEmpty()) {
                    // this.route = new Route();
                    boolean success = true;
                    this.creating();

                    if (!success) {
                        // Manejo cuando se agota la capacidad del vehículo actual
                        if (!this.listCapacities.isEmpty()) {
                            this.route = new Route();

                            requestRoute = this.customer.getRequestCustomer();
                            this.route.getListIdCustomers().add(this.customer.getIdCustomer());
                            customersToVisit.remove(this.customer);

                            vehicleCapacity = this.listCapacities.remove(0);
                            isOpen = true;
                        } else {
                            isOpen = false;
                        }
                    }
                    // if (isOpen) {
                    //     this.route.setRequestRoute(requestRoute);
                    //     this.route.setIdDepot(depotId);
                    //     this.solution.getListRoutes().add(this.route);
                    // }
                }
            } else if (this.typeProblem == ProblemType.TTRP) {
                while (customersToVisit != null && !customersToVisit.isEmpty()) {
                    this.initializeSpecifics();
                    boolean found = false;
                    if (((CustomerTTRP)this.customer).getTypeCustomer() == CustomerType.TC) {
                        this.creating();
                    } else {
                        if (((CustomerTTRP)this.customer).getTypeCustomer() == CustomerType.TC) {
                            this.isTC = true;
                        }

                        if ((this.capacityVehicle + this.capacityTrailer) >= (requestRoute + this.customer.getRequestCustomer())) {
                            requestRoute += this.customer.getRequestCustomer();
                            this.route.getListIdCustomers().add(this.customer.getIdCustomer());
                            customersToVisit.remove(this.customer);
                        } else {
                            this.route.setRequestRoute(requestRoute);

                            RouteTTRP routeTTRP;
                            if (this.isTC) {
                                routeTTRP = new RouteTTRP(
                                    this.route.getListIdCustomers(),
                                    this.route.getRequestRoute(),
                                    this.route.getCostRoute(),
                                    this.route.getIdDepot(),
                                    new ArrayList<>(),
                                        RouteType.CVR
                                );
                                this.route = routeTTRP;
                                ((RouteTTRP)this.route).setTypeRoute(RouteType.CVR);
                            } else {
                                routeTTRP = new RouteTTRP(
                                    this.route.getListIdCustomers(),
                                    this.route.getRequestRoute(),
                                    this.route.getCostRoute(),
                                    this.route.getIdDepot(),
                                    new ArrayList<>(),
                                        RouteType.PVR
                                );
                                this.route = routeTTRP;
                                ((RouteTTRP)this.route).setTypeRoute(RouteType.PVR);
                            }

                            this.route.setIdDepot(idDepot);
                            this.solution.getListRoutes().add(this.route);
                            this.isTC = false;

                            this.route = new RouteTTRP();

                            requestRoute = this.customer.getRequestCustomer();
                            CustomerType typeCustomer = ((CustomerTTRP)this.customer).getTypeCustomer();
                            this.route.getListIdCustomers().add(this.customer.getIdCustomer());
                            customersToVisit.remove(this.customer);
                        }
                    }
                }
            }

        }
        
        
        
        //----------------------------------------------------------------------------------------------------------//
	 
	/* M�todo que busca un cliente por su identificador*/
	protected Customer getCustomerByID(int idCustomer, ArrayList<Customer> listCustomers){
		int i = 0;
		boolean found = false;
		Customer customer = new Customer();
		
		while((i < listCustomers.size()) && (!found))
		{
			if(listCustomers.get(i).getIdCustomer() == idCustomer)
			{
				customer = listCustomers.get(i);
				found = true;
			}
			else
			 i++;
		}
		return customer;
	}
	
	protected void AscendentOrdenate(ArrayList<Metric> listWithOutOrder){
		double minorInsertionCost;
		Metric minorMetric;
		int referencePos;

		for(int i = 0; i < listWithOutOrder.size(); i++)
		{
			minorInsertionCost = listWithOutOrder.get(i).getInsertionCost();
			minorMetric = listWithOutOrder.get(i);
			referencePos = i;
	
			Metric currentMetric = new Metric();
			int currentPos = -1;
			
			for (int j = (i + 1); j < listWithOutOrder.size(); j++) 
			{
				if ((listWithOutOrder.get(j).getInsertionCost()) < minorInsertionCost)
				{
					minorInsertionCost = listWithOutOrder.get(j).getInsertionCost();
					currentMetric = listWithOutOrder.get(j);
					currentPos = j;
				}
			}
			
			if(currentPos != -1)
			{
				listWithOutOrder.set(referencePos, currentMetric);
				listWithOutOrder.set(currentPos, minorMetric);	
			}
		}
	}
	
	protected void AscendentOrdenate(ArrayList<Double> listDistances, ArrayList<Customer> listNN){
		Double minorDistance;
		Customer customerNN;
		int referencePos;

		for(int i = 0; i < listDistances.size(); i++)
		{
			minorDistance = listDistances.get(i);
			customerNN = listNN.get(i);
			referencePos = i;

			Double currentDistance = 0.0;
			Customer currentCustomer = new Customer();
			int currentPos = -1;

			for(int j = (i + 1); j < listDistances.size(); j++)
			{
				if(minorDistance > listDistances.get(j))
				{
					currentDistance = listDistances.get(j);
					currentCustomer = listNN.get(j);
					currentPos = j;
				}
			}
			
			if(currentPos != -1)
			{
				listDistances.set(referencePos, currentDistance);
				listDistances.set(currentPos, minorDistance);

				listNN.set(referencePos, currentCustomer);
				listNN.set(currentPos, customerNN);	
			}
		}
	}
	
	/* M�todo que devuelve el primer cliente a insertar en la ruta cuando es MDVRP*/	
	private Customer selectFirstCustomerInMDVRP(ArrayList<Customer> CustomersToVisit, FirstCustomerType firstCustomerType, int posMatrixDepot){
		Customer selectedCustomer = null;
		int currentIndex = -1;
		double currentCost = 0.0;
		
		selectedCustomer = CustomersToVisit.get(0);
		int bestIndex = Problem.getProblem().getPosElement(selectedCustomer.getIdCustomer());
		double bestCost = Problem.getProblem().getCostMatrix().getItem(posMatrixDepot, bestIndex);
	
		for(int i = 1; i < CustomersToVisit.size(); i++)
		{
			currentIndex = Problem.getProblem().getPosElement(CustomersToVisit.get(i).getIdCustomer());
			currentCost = Problem.getProblem().getCostMatrix().getItem(posMatrixDepot, currentIndex);

			if(firstCustomerType.equals(FirstCustomerType.FurthestCustomer))
			{
				if(currentCost > bestCost)
				{
					bestCost = currentCost;
					bestIndex = currentIndex;
					selectedCustomer = CustomersToVisit.get(i);	
				}
			}
			else
			{
				if(firstCustomerType.equals(FirstCustomerType.NearestCustomer))
				{
					if(currentCost < bestCost)
					{
						bestCost = currentCost;
						bestIndex = currentIndex;
						selectedCustomer = CustomersToVisit.get(i);
					}	
				}
			}
		}

		return selectedCustomer;
	}
	

	/* M�todo que devuelve el primer cliente a insertar en la ruta*/	
	protected Customer getFirstCustomer(ArrayList<Customer> CustomersToVisit, FirstCustomerType firstCustomerType, int idDepot){ 
		Random random = new Random ();
		Customer firstCustomer = null;
		int index = -1;
		int posMatrixDepot = -1;
		RowCol rc = new RowCol();
		
		switch(firstCustomerType.ordinal())
		{
			case 2:
			{
				index = random.nextInt(CustomersToVisit.size());
				firstCustomer = CustomersToVisit.get(index);

				break;
			}
			default:
			{
				posMatrixDepot = Problem.getProblem().getPosElement(idDepot);
                                System.out.println("Fila" + posMatrixDepot);

				if(Problem.getProblem().getTypeProblem().equals(ProblemType.MDVRP))
					firstCustomer = selectFirstCustomerInMDVRP(CustomersToVisit, firstCustomerType, posMatrixDepot);
				else
				{
					if(firstCustomerType.equals(FirstCustomerType.NearestCustomer))
						rc = Problem.getProblem().getCostMatrix().indexLowerValue(posMatrixDepot, 0, posMatrixDepot, (CustomersToVisit.size() - 1)); 
					else
						if(firstCustomerType.equals(FirstCustomerType.FurthestCustomer))
							rc = Problem.getProblem().getCostMatrix().indexBiggerValue(posMatrixDepot, 0, posMatrixDepot, (CustomersToVisit.size() - 1));
                                                        
                                                        /*for(int i = 0; i <= CustomersToVisit.size(); i++)
                                                            for(int j = 0; j <= CustomersToVisit.size(); j++)
                                                                System.out.println(m.getItem(i, j));*/
                                        NumericMatrix m = Problem.getProblem().getCostMatrix();
                                        System.out.println(m.getItem(rc.getRow(), rc.getCol()));
					index = rc.getCol();
                                        System.out.println("Indice"+index);
					firstCustomer = CustomersToVisit.get(index);
                                        System.out.println("Id cliente"+firstCustomer.getIdCustomer());
				}
			}
		}
		
		return firstCustomer;
	}
        
        protected ArrayList<Customer> get_feasible_customers(int current_node_id){
            ArrayList<Customer> feasible_customers = new ArrayList<>();
            this.time_matrix = Problem.getProblem().getTimeMatrix();
            
            for (Customer cust : this.customersToVisit) {
                double travel_time = this.time_matrix.getItem(current_node_id, cust.getIdCustomer());
                double arrival_time = this.time_route + travel_time;
                // Si se llega antes del ready_time, se espera
                double effectiveTime = Math.max(arrival_time, cust.getTimeWindow().getInitialNode());
                // Verificamos la ventana de tiempo del cliente
                if (effectiveTime > cust.getTimeWindow().getEndNode()) {
                    continue;  // No es factible por ventana de tiempo
                }
                // Verificamos la capacidad
                if (requestRoute + cust.getRequestCustomer() > capacityVehicle) {
                    continue;
                }
                feasible_customers.add(cust);
            }

            return feasible_customers;
        }
        
        protected double getTimeRoute(ArrayList<Integer> listId) {
            ArrayList<Integer> localListId = new ArrayList<>(listId);
            double timeRoute = 0.0;
            localListId.add(0, idDepot);
            for (int index = 0; index < localListId.size() - 1; index++) {
                int id = localListId.get(index);
                this.time_matrix = Problem.getProblem().getTimeMatrix();
                int nextId = localListId.get(index + 1);
                double currentTime = this.time_matrix.getItem(id, nextId);
                Customer customer = Problem.getProblem().getCustomerByIDCustomer(nextId);
                double customerReadyTime = customer.getTimeWindow().getInitialNode();
                double customerServiceTime = customer.getTimeWindow().getServiceTime();
                timeRoute = Math.max(currentTime, customerReadyTime) + customerServiceTime;
            }

            return timeRoute;
        }
        
}
