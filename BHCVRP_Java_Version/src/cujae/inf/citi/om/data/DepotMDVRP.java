package cujae.inf.citi.om.data;

import java.util.ArrayList;

/* Clase que modela los datos de un depósito en el MDVRP*/

public class DepotMDVRP extends Depot{
	
	private ArrayList<Integer> listAssignedCustomers;

	public DepotMDVRP() {
		super();
		listAssignedCustomers = new ArrayList<Integer>();
	}
	 
	public DepotMDVRP(ArrayList<Integer> listAssignedCustomers) {
		super();
		this.listAssignedCustomers = listAssignedCustomers;
	}

	public ArrayList<Integer> getListAssignedCustomers() {
		return listAssignedCustomers;
	}

	public void setListAssignedCustomers(ArrayList<Integer> listAssignedCustomers) {
		this.listAssignedCustomers = listAssignedCustomers;
	}
}
