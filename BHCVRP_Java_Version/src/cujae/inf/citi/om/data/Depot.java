package cujae.inf.citi.om.data;

import java.util.ArrayList;

/* Clase que modela los datos de un depósito en un VRP*/

public class Depot {
	
	protected int idDepot;
	protected Location locationDepot;
	protected ArrayList<Fleet> listFleets;

	public Depot() {
		super();
		listFleets = new ArrayList<Fleet>();
	}
	 
	public Depot(int idDepot, Location locationDepot, ArrayList<Fleet> listFleets) {
		super();
		this.idDepot = idDepot;
		this.locationDepot = locationDepot;
		this.listFleets = listFleets;
	}

	public ArrayList<Fleet> getListFleets() {
		return listFleets;
	}

	public void setListFleets(ArrayList<Fleet> listFleets) {
		this.listFleets = listFleets;
	}

	public Location getLocationDepot() {
		return locationDepot;
	}

	public void setLocationDepot(Location locationDepot) {
		this.locationDepot = locationDepot;
	}

	public int getIdDepot() {
		return idDepot;
	}

	public void setIdDepot(int idDepot) {
		this.idDepot = idDepot;
	}
}
