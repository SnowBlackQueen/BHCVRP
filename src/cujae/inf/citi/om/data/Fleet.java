package cujae.inf.citi.om.data;

/* Clase que modela los datos de una flota en un VRP*/

public class Fleet {
	
	protected int countVehicles;
	protected double capacityVehicle;

	public Fleet() {
		super();
		// TODO Auto-generated constructor stub
	}

	public Fleet(int countVehicles, double capacityVehicle) {
		super();
		this.countVehicles = countVehicles;
		this.capacityVehicle = capacityVehicle;
	}

	public int getCountVehicles() {
		return countVehicles;
	}

	public void setCountVehicles(int countVehicles) {
		this.countVehicles = countVehicles;
	}

	public double getCapacityVehicle() {
		return capacityVehicle;
	}

	public void setCapacityVehicle(double capacityVehicle) {
		this.capacityVehicle = capacityVehicle;
	}
}
