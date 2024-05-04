package cujae.inf.citi.om.generator.postoptimization;

import java.util.ArrayList;
import java.util.List;

import cujae.inf.citi.om.generator.solution.Route;

/*Clase abstracta que define el comportamiento de un método de post-optimización */

public abstract class StepOptimization{
	
	/* Metodo que define el comportamiento del paso de optimización */
	public abstract void toOptimize(Route route);
	
	
	/* Método que invierte el orden de una cadena*/
	public void Invert(ArrayList<Integer> listCandidates, int posIni, int posEnd) {
		if(posIni > posEnd)
		{
			int posTemp = posEnd;
			posEnd = posIni;
			posIni = posTemp;
		}
		
		List<Integer> subList;
		subList = listCandidates.subList((posIni + 1), (posEnd + 1));
		
		int posFinal = subList.size();

		for(int j = 1; j <= (posFinal/2); j++)
		{
			Object valueKeyFirst = subList.get((j - 1)); 
			listCandidates.set((j + posIni), listCandidates.get(posEnd)); 
			listCandidates.set(posEnd,(Integer)valueKeyFirst);
			posEnd--;
		}	
	}
}
