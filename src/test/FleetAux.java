package test;

public class FleetAux {
	
	private int countVehicles;
	private double capacityVehicle;

	public FleetAux() {
		super();
		// TODO Auto-generated constructor stub
	}

	public FleetAux(int countVehicles, double capacityVehicle) {
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
