package cujae.inf.citi.om.data;

/* Clase que modela la ubicación geográfica de un cliente VRP a partir de sus coordenadas cartesianas*/

public class Location {

	private double axisX;
	private double axisY;
	
	public Location(){
		super();
	}

	public Location(double axisX, double axisY){
		this.axisX = axisX;
		this.axisY = axisY;
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
	
	/*Método que devuelve para un punto su coordenada polar Theta*/
	public double getPolarTheta(){
		return Math.atan(axisY/axisX);
	}
	
	/*Método que devuelve para un punto su coordenada polar Rho*/
	public double getPolarRho(){
		return Math.sqrt((Math.pow(axisX, 2) + Math.pow(axisY, 2)));
	}
}
