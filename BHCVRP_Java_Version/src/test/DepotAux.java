package test;

import java.util.ArrayList;


public class DepotAux {

	private int idDepot;
	private ArrayList<FleetAux> listFleets;
	private double axisX;
	private double axisY;


	public DepotAux() {
		super();
		listFleets = new ArrayList<FleetAux>();
	}
	 
	public DepotAux(int idDepot, ArrayList<FleetAux> listFleets, double axisX, double axisY) {
		super();
		this.idDepot = idDepot;
		this.listFleets = listFleets;
		this.axisX = axisX;
		this.axisY = axisY;
		
	}

	public ArrayList<FleetAux> getListFleets() {
		return listFleets;
	}

	public void setListFleets(ArrayList<FleetAux> listFleets) {
		this.listFleets = listFleets;
	}

	public int getIdDepot() {
		return idDepot;
	}

	public void setIdDepot(int idDepot) {
		this.idDepot = idDepot;
	}
	

	public double getAxisX() {
		return axisX;
	}

	public void setAxisX(double axisX) {
		this.axisX = axisX;
	}
	
	public double getAxisY() {
		return axisY;
	}
	
	public void setAxisY(double axisY) {
		this.axisY = axisY;
	}
}
