package cujae.inf.citi.om.generator.solution;

import java.util.ArrayList;

import cujae.inf.citi.om.data.Problem;
import cujae.inf.citi.om.data.ProblemType;

/* Clase que modela los datos de una solucion en un VRP */

public class Solution {
	
	private ArrayList<Route> listRoutes;
	
	public Solution() {
		super();
		listRoutes = new ArrayList<Route>();
		// TODO Auto-generated constructor stub
	}

	public Solution(ArrayList<Route> listRoutes) {
		super();
		this.listRoutes = listRoutes;
	}

	public ArrayList<Route> getListRoutes() {
		return listRoutes;
	}

	public void setListRoutes(ArrayList<Route> listRoutes) {
		this.listRoutes = listRoutes;
	}
	
	/* Método que calcula el costo total de la solución */
	public Double calculateCost(){
		double totalCost = 0.0;

		for(int i = 0; i < listRoutes.size(); i++)
		{
			if(!Problem.getProblem().getTypeProblem().equals(ProblemType.TTRP) || (Problem.getProblem().getTypeProblem().equals(ProblemType.TTRP) && (((RouteTTRP)listRoutes.get(i)).equals(RouteType.PTR) || ((RouteTTRP)listRoutes.get(i)).equals(RouteType.PVR))))
				totalCost += listRoutes.get(i).getCostSingleRoute();
			else
				totalCost =  ((RouteTTRP)listRoutes.get(i)).getCostRouteWithSubTour();	
		}
		
		return totalCost;	
	}
	
	/* Método que devuelve el costo total de la solución */
	public Double getCostSolution(){
		double costSolution = 0.0;
		
		for(int i = 0; i < listRoutes.size(); i++)
			costSolution += listRoutes.get(i).getCostRoute();
		
		return costSolution;
	}
}
