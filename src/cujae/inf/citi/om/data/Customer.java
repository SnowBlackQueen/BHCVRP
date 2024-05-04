package cujae.inf.citi.om.data;

/* Clase que modela los datos de un cliente en un VRP*/

public class Customer {
	
	protected int idCustomer;
	protected double requestCustomer;
	protected Location locationCustomer;

	public Customer() {
		super();
	}
	
	public Customer(int idCustomer, double requestCustomer,
			Location locationCustomer) {
		super();
		this.idCustomer = idCustomer;
		this.requestCustomer = requestCustomer;
		this.locationCustomer = locationCustomer;
	}

	public int getIdCustomer() {
		return idCustomer;
	}

	public void setIdCustomer(int idCustomer) {
		this.idCustomer = idCustomer;
	}

	public double getRequestCustomer() {
		return requestCustomer;
	}

	public void setRequestCustomer(double requestCustomer) {
		this.requestCustomer = requestCustomer;
	}

	public Location getLocationCustomer() {
		return locationCustomer;
	}

	public void setLocationCustomer(Location locationCustomer) {
		this.locationCustomer = locationCustomer;
	}
}
