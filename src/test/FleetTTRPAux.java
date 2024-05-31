/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package test;

/**
 *
 * @author kmych
 */
public class FleetTTRPAux extends FleetAux {
    private int countTrailers;
	private double capacityTrailer;

	public FleetTTRPAux() {
		super();
		// TODO Auto-generated constructor stub
	}

	public FleetTTRPAux(int countTrailers,
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
