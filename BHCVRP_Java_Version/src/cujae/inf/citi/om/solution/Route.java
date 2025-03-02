package cujae.inf.citi.om.solution;

import cujae.inf.citi.om.data.BusStop;
import java.util.ArrayList;

import cujae.inf.citi.om.data.Problem;
import cujae.inf.citi.om.data.ProblemType;
import cujae.inf.ic.om.matrix.NumericMatrix;

/* Clase que modela los datos de una ruta en un VRP*/

public class Route {

	protected ArrayList<Integer> listIdCustomers;
	protected double requestRoute;
	protected double costRoute;
	protected int idDepot;
        protected ArrayList<BusStop> listBusStops;
	
	public Route() {
		super();
		this.listIdCustomers = new ArrayList<Integer>();
                this.listBusStops = new ArrayList<BusStop>();
		this.requestRoute = 0.0;
		this.costRoute = 0.0;
		idDepot = -1;
	}
	
        public Route(ArrayList<Integer> listIdCustomers, double requestRoute, double costRoute, int idDepot, ArrayList<Integer> listAccessVC) {
		super();
		this.listIdCustomers = new ArrayList<Integer>(listIdCustomers);
		this.requestRoute = requestRoute;
		this.costRoute = 0.0;
		this.idDepot = idDepot;
                listAccessVC = new ArrayList<Integer>();
	}
        
	public Route(ArrayList<Integer> listIdCustomers, double requestRoute, double costRoute, int idDepot, ArrayList<Integer> listAccessVC, ArrayList<BusStop> listBusStops) {
		super();
		this.listIdCustomers = new ArrayList<Integer>(listIdCustomers);
                this.listBusStops = new ArrayList<BusStop>();
		this.requestRoute = requestRoute;
		this.costRoute = 0.0;
		this.idDepot = idDepot;
                listAccessVC = new ArrayList<Integer>();
	}

	public ArrayList<Integer> getListIdCustomers() {
		return listIdCustomers;
	}
	
	public void setListIdCustomers(ArrayList<Integer> listIdCustomers) {
		this.listIdCustomers = listIdCustomers;
	}
	
        public ArrayList<BusStop> getListBusStops() {
		return listBusStops;
	}
	
	public void setListBusStops(ArrayList<BusStop> listBusStops) {
		this.listBusStops = listBusStops;
	}
        
	public double getRequestRoute() {
		return requestRoute;
	}

	public void setRequestRoute(double requestRoute) {
		this.requestRoute = requestRoute;
	}

	public double getCostRoute() {
		return costRoute;
	}

	public void setCostRoute(double costRoute) {
		this.costRoute = costRoute;
	}

	public int getIdDepot() {
		return idDepot;
	}

	public void setIdDepot(int idDepot) {
		this.idDepot = idDepot;
	}
	
	/* M�todo que calcula el costo de una ruta simple (PTR � PVR) */
	public Double getCostSingleRoute() {
            Double costRoute = 0.0;
            Problem problem = Problem.getProblem();

            if (problem.getTypeProblem() == ProblemType.SBRP) {
                // Caso para SBRP (School Bus Routing Problem)
                BusStop busStopIni = listBusStops.get(0);
                int posBusStopIni = problem.getPosElement(busStopIni);

                NumericMatrix costMatrix = problem.getCostMatrix();

                // Obtener los índices del depósito y la primera parada de autobús
                int depotIndex = problem.getPosElement(idDepot);
                int busStopIniIndex = problem.getPosElement(posBusStopIni);

                // Calcular el costo inicial desde el depósito hasta la primera parada
                costRoute += costMatrix.getItem(depotIndex, busStopIniIndex);

                // Calcular el costo entre paradas de autobús
                for (int i = 1; i < listBusStops.size(); i++) {
                    BusStop busStopNext = listBusStops.get(i);
                    int posBusStopNext = problem.getPosElement(busStopNext);
                    costRoute += costMatrix.getItem(posBusStopIni, posBusStopNext);

                    busStopIni = busStopNext;
                    posBusStopIni = posBusStopNext;
                }

                // Calcular el costo de regreso al depósito
                costRoute += costMatrix.getItem(posBusStopIni, depotIndex);
            } else {
                // Caso para otros problemas (VRP, OVRP, etc.)
                int customerIni = listIdCustomers.get(0);
                int posCustomerIni = problem.getPosElement(customerIni);

                NumericMatrix costMatrix = problem.getCostMatrix();

                // Obtener los índices del depósito y el primer cliente
                int depotIndex = problem.getPosElement(idDepot);
                int customerIniIndex = problem.getPosElement(posCustomerIni);

                // Calcular el costo inicial desde el depósito hasta el primer cliente
                costRoute += costMatrix.getItem(depotIndex, customerIniIndex);

                // Calcular el costo entre clientes
                for (int i = 1; i < listIdCustomers.size(); i++) {
                    int customerNext = listIdCustomers.get(i);
                    int posCustomerNext = problem.getPosElement(customerNext);
                    costRoute += costMatrix.getItem(posCustomerIni, posCustomerNext);

                    customerIni = customerNext;
                    posCustomerIni = posCustomerNext;
                }

                // Calcular el costo de regreso al depósito (excepto para OVRP)
                if (problem.getTypeProblem() != ProblemType.OVRP) {
                    costRoute += costMatrix.getItem(posCustomerIni, depotIndex);
                }
            }

            setCostRoute(costRoute);
            return costRoute;
        }
}
