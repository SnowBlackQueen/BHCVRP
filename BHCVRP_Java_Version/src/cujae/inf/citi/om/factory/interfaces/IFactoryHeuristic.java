package cujae.inf.citi.om.factory.interfaces;

import cujae.inf.citi.om.generator.heuristic.Heuristic;

/* Interfaz que define como crear una objeto Heuristic*/

public interface IFactoryHeuristic {
	
	Heuristic createHeuristic(HeuristicType heuristicType);
}
