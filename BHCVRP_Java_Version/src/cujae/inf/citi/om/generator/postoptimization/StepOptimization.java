package cujae.inf.citi.om.generator.postoptimization;

import java.util.ArrayList;
import java.util.List;

import cujae.inf.citi.om.generator.solution.Route;

/*Clase abstracta que define el comportamiento de un m�todo de post-optimizaci�n */

public abstract class StepOptimization{
	
	/* Metodo que define el comportamiento del paso de optimizaci�n */
	public abstract void toOptimize(Route route);
	
	/* M�todo que invierte el orden de una cadena*/
	public void invert(ArrayList<Integer> listCandidates, int posIni, int posEnd) {
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
