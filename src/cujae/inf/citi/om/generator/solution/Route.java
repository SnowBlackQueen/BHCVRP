package cujae.inf.citi.om.generator.solution;

import java.util.ArrayList;

import cujae.inf.citi.om.data.Problem;

/* Clase que modela los datos de una ruta en un VRP*/

public class Route {

	protected ArrayList<Integer> listIdCustomers;
	protected double requestRoute;
	protected double costRoute;
	protected int idDepot;
	
	public Route() {
		super();
		this.listIdCustomers = new ArrayList<Integer>();
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

	public ArrayList<Integer> getListIdCustomers() {
		return listIdCustomers;
	}
	
	public void setListIdCustomers(ArrayList<Integer> listIdCustomers) {
		this.listIdCustomers = listIdCustomers;
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
	public Double getCostSingleRoute(){
		Double costRoute = 0.0;
		int customerIni;
		int customerNext;
		int posCustomerIni = -1;
		int posCustomerNext = -1;

		customerIni = listIdCustomers.get(0).intValue();
		posCustomerIni = Problem.getProblem().getPosElement(customerIni);
		
		costRoute += Problem.getProblem().getCostMatrix().getItem(Problem.getProblem().getPosElement(idDepot), posCustomerIni);

		for(int i = 1; i < listIdCustomers.size(); i++)
		{
			customerNext = listIdCustomers.get(i).intValue();
			posCustomerNext = Problem.getProblem().getPosElement(customerNext);
			
			costRoute += Problem.getProblem().getCostMatrix().getItem(posCustomerIni, posCustomerNext);
			
			customerIni = customerNext;
			posCustomerIni = posCustomerNext;
		}
		
		costRoute += Problem.getProblem().getCostMatrix().getItem(posCustomerIni, Problem.getProblem().getPosElement(idDepot));
		setCostRoute(costRoute);
		
		return costRoute;
	}
}
