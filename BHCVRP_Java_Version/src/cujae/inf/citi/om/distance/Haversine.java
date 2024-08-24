package cujae.inf.citi.om.distance;

public class Haversine extends Distance{

	public static final double EARTH_RADIUS_KM = 6371;
	
	public Haversine() {
		super();
		// TODO Auto-generated constructor stub
	}

	@Override
	public Double calculateDistance(double axisXStart, double axisYStart, double axisXEnd, double axisYEnd) {
		double distance = 0.0;
		
		double longitudeStart = axisXStart * (Math.PI/180);
		double latitudeStart = axisYStart * (Math.PI/180);
		
		double longitudeEnd = axisXEnd * (Math.PI/180);
		double latitudeEnd = axisYEnd * (Math.PI/180);
		
		double difLatitude = latitudeEnd - latitudeStart;
		double difLongtitude = longitudeEnd - longitudeStart;
		
		distance = Math.pow(Math.sin((difLatitude/2)), 2) + Math.cos(latitudeStart) * Math.cos(latitudeEnd) * Math.pow(Math.sin((difLongtitude/2)), 2);		
		distance = 2 * EARTH_RADIUS_KM * Math.atan2(Math.sqrt(distance), Math.sqrt((1 - distance)));
		
		return distance;
	}
}
