package cujae.inf.citi.om.distance;

/*Clase que modela como calcular la distancia mediante la fórmula Euclidiana*/

public class Euclidean extends Distance{

	public Euclidean() {
		super();
		// TODO Auto-generated constructor stub
	}

	@Override
	public Double calculateDistance(double axisXStart, double axisYStart, double axisXEnd, double axisYEnd) {
		double distance = 0.0;
		double axisX = 0.0;
		double axisY = 0.0;
		
		axisX = Math.pow((axisXStart - axisXEnd), 2);
		axisY = Math.pow((axisYStart - axisYEnd), 2);
		distance = Math.sqrt((axisX + axisY));
		
		return distance;
	}
}
