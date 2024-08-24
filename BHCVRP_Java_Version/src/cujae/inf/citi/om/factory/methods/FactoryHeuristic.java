package cujae.inf.citi.om.factory.methods;

import java.lang.reflect.InvocationTargetException;

import cujae.inf.citi.om.factory.interfaces.HeuristicType;
import cujae.inf.citi.om.factory.interfaces.IFactoryHeuristic;
import cujae.inf.citi.om.generator.heuristic.Heuristic;

/* Clase que implementa el Patrón Factory para la carga dinámica de una determinada heurística de construcción*/

public class FactoryHeuristic implements IFactoryHeuristic {

	public Heuristic createHeuristic(HeuristicType heuristicType) {
		String className = "cujae.inf.citi.om.generator.heuristic." + heuristicType.toString();
		Heuristic heuristic  = null;
		
		try {
			heuristic = (Heuristic) FactoryLoader.getInstance(className);
		} catch (ClassNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IllegalArgumentException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (SecurityException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (InstantiationException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IllegalAccessException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (InvocationTargetException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (NoSuchMethodException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

		return heuristic;
	}
}
