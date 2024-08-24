package cujae.inf.citi.om.distance;

/*Clase que modela como calcular la distancia mediante la fórmula de Chebyshev*/

public class Chebyshev extends Distance{

	public Chebyshev() {
		super();
		// TODO Auto-generated constructor stub
	}

	@Override
	public Double calculateDistance(double axisXStart, double axisYStart, double axisXEnd, double axisYEnd) {
		double distance = 0.0;
		double axisX = 0.0;
		double axisY = 0.0;
		
		axisX = Math.abs(axisXStart - axisXEnd);
		axisY = Math.abs(axisYStart - axisYEnd);
		distance = Math.max(axisX, axisY);
		
		return distance;
	}
}
