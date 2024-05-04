package cujae.inf.citi.om.data;

/* Clase que modela los datos de una flota en el TTRP*/

public class FleetTTRP extends Fleet {
	
	private int countTrailers;
	private double capacityTrailer;

	public FleetTTRP() {
		super();
		// TODO Auto-generated constructor stub
	}

	public FleetTTRP(int countTrailers,
			double capacityTrailer) {
		super();
		this.countTrailers = countTrailers;
		this.capacityTrailer = capacityTrailer;
	}

	public int getCountTrailers() {
		return countTrailers;
	}

	public void setCountTrailers(int countTrailers) {
		this.countTrailers = countTrailers;
	}

	public double getCapacityTrailer() {
		return capacityTrailer;
	}

	public void setCapacityTrailer(double capacityTrailer) {
		this.capacityTrailer = capacityTrailer;
	}
}
