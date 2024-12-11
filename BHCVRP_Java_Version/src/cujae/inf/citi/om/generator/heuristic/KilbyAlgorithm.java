/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package cujae.inf.citi.om.generator.heuristic;

import cujae.inf.citi.om.data.Customer;
import cujae.inf.citi.om.data.DepotMDVRP;
import cujae.inf.citi.om.data.FleetTTRP;
import cujae.inf.citi.om.data.Problem;
import cujae.inf.citi.om.data.ProblemType;
import cujae.inf.citi.om.generator.solution.Route;
import cujae.inf.citi.om.generator.solution.Solution;
import java.util.ArrayList;

/**
 *
 * @author nanda
 */
public class KilbyAlgorithm extends Heuristic{

	public KilbyAlgorithm() {
		super();
		// TODO Auto-generated constructor stub
	}
        
        @Override
        public void initializeSpecifics(){
            
        }

	@Override
	public Solution getSolutionInicial() {
		Solution solution = new Solution();
		ArrayList<Customer> CustomersToVisit = null;
	
		int posDepot = -1;
		ArrayList<Route> listCandidateRoutes = new ArrayList<Route>();
		ArrayList<Metric> listKilbyCosts = null;
		//ArrayList<Route> listRouteOpt = new ArrayList<Route>();

		if(Problem.getProblem().getTypeProblem().equals(ProblemType.CVRP) || Problem.getProblem().getTypeProblem().equals(ProblemType.HFVRP) || Problem.getProblem().getTypeProblem().equals(ProblemType.OVRP) || Problem.getProblem().getTypeProblem().equals(ProblemType.TTRP))
		{
			CustomersToVisit = new ArrayList<Customer>(Problem.getProblem().getListCustomers());
			posDepot = 0;
		}
		else //***
		{
			int i = 0;
			boolean found = false;
			
			while((i < Problem.getProblem().getListDepots().size()) && (!found))
			{
				if(!((DepotMDVRP)Problem.getProblem().getListDepots().get(i)).getListAssignedCustomers().isEmpty())
				{
					CustomersToVisit = new ArrayList<Customer>(Problem.getProblem().getCustomersAssignedByIDDepot(Problem.getProblem().getListDepots().get(i).getIdDepot()));
			
					found = true;
					posDepot = i;
				}
				else
					i++;
			}	
		}
			
		int countVehicles = 0;
		int countTrailers = 0;
		double capacityVehicle = Problem.getProblem().getListDepots().get(posDepot).getListFleets().get(0).getCapacityVehicle();
		
		if(Problem.getProblem().getTypeProblem().equals(ProblemType.CVRP))
			countTrailers = ((FleetTTRP)Problem.getProblem().getListDepots().get(posDepot).getListFleets().get(0)).getCountTrailers();

		if(Problem.getProblem().getTypeProblem().equals(ProblemType.HFVRP))
			countVehicles = Problem.getProblem().fillListCapacities(posDepot).size();
		else
			countVehicles = Problem.getProblem().getListDepots().get(posDepot).getListFleets().get(0).getCountVehicles();
	
		//Operator_2opt stepOptimizacion1 = new Operator_2opt();
		//Operator_Relocate stepOptimizacion2 = new Operator_Relocate();
		//Operator_Exchange stepOptimizacion3 = new Operator_Exchange();

		Customer customer = null;
		Metric metricKilby = null;
		double request = 0.0;
		int posRoute = -1;
		boolean isRouteFull = true;
		int routesWithCustomers = 0;

		for(int i = 0; i < countVehicles; i++)
		{
			Route route = new Route();
			listCandidateRoutes.add(route);
		}
                
                //COMPLETAR!!!!
                
            return solution;
        }

}
