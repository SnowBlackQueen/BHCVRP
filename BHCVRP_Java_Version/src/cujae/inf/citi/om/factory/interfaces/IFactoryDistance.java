package cujae.inf.citi.om.factory.interfaces;

import cujae.inf.citi.om.distance.Distance;

/* Interfaz que define como crear un objeto Distance*/

public interface IFactoryDistance {
	
	public Distance createDistance(DistanceType typeDistance);

}
