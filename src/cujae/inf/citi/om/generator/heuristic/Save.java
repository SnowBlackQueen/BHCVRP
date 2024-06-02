package cujae.inf.citi.om.generator.heuristic;

import java.util.ArrayList;

import cujae.inf.citi.om.data.Customer;
import cujae.inf.citi.om.data.CustomerTTRP;
import cujae.inf.citi.om.data.CustomerType;
import cujae.inf.citi.om.data.Problem;
import cujae.inf.citi.om.data.ProblemType;
import cujae.inf.citi.om.generator.solution.Route;
import cujae.inf.citi.om.generator.solution.RouteTTRP;
import cujae.inf.citi.om.generator.solution.RouteType;
import cujae.inf.citi.om.matrix.NumericMatrix;

public abstract class Save extends Heuristic{

	public static int parameterShape = 1;
	
	protected Save() {
		super();
		// TODO Auto-generated constructor stub
	}

/* M�todo que construye la matriz de ahorro */	
	protected NumericMatrix fillSaveMatrix(int idDepot, ArrayList<Customer> CustomersToVisit){
		int countCustomer = CustomersToVisit.size();
		NumericMatrix saveMatrix = new NumericMatrix(countCustomer, countCustomer);
		double save = 0.0;
		
		for(int i = 0; i < countCustomer; i++)
		{
                    //Fill save matrix
			for(int j = i; j < countCustomer; j++)
			{
				if(i == j)
					saveMatrix.setItem(i, j, Double.NEGATIVE_INFINITY);
				else 
				{
                                    //Problema aquí
					save = Problem.getProblem().getCostMatrix().getItem(Problem.getProblem().getPosElement(CustomersToVisit.get(i).getIdCustomer()), Problem.getProblem().getPosElement(idDepot)) + Problem.getProblem().getCostMatrix().getItem(Problem.getProblem().getPosElement(idDepot), Problem.getProblem().getPosElement(CustomersToVisit.get(j).getIdCustomer())) - (parameterShape * Problem.getProblem().getCostMatrix().getItem(Problem.getProblem().getPosElement(CustomersToVisit.get(i).getIdCustomer()), Problem.getProblem().getPosElement(CustomersToVisit.get(j).getIdCustomer())));
					saveMatrix.setItem(i, j, save);
					saveMatrix.setItem(j, i, save);
				}
			}
		}
			 
		return saveMatrix;
	}

	/* M�todo que devuelve la posici�n de una ruta */
	protected int getPositionRoute(ArrayList<Route> listRoutes, int idCustomer){
		int index = -1;
		boolean stop = false;
		int i = 0;
		int j;
		
		while((i < listRoutes.size()) && (!stop)) 
		{
			j = 0;
			while ((j < listRoutes.get(i).getListIdCustomers().size()) && (!stop))
			{
				if(listRoutes.get(i).getListIdCustomers().get(j).intValue() == idCustomer)
				{
					stop = true;
					index = i; 
				}	
				j++;
			}
			i++;
		}
		
		return index;
	}
	
	/* M�todo para crear las rutas iniciales */
	protected ArrayList<Route> createInitialRoutes(ArrayList<Customer> listCustomers){
		ArrayList<Route> listRoutes = new ArrayList<Route>();
		Route route;
                ArrayList<Integer> listAccessVC = new ArrayList<Integer>();

		for(int i = 0; i < listCustomers.size(); i++)
		{
			route = new Route();
			route.setRequestRoute(listCustomers.get(i).getRequestCustomer());
			route.setIdDepot(Problem.getProblem().getIDDepotByIDCustomer(listCustomers.get(i).getIdCustomer()));
			route.getListIdCustomers().add(listCustomers.get(i).getIdCustomer()); 
			
			if(Problem.getProblem().getTypeProblem().equals(ProblemType.TTRP))
			{
				/*if(((CustomerTTRP)listCustomers.get(i)).getTypeCustomer().equals(CustomerType.VC))
					((RouteTTRP)route).setTypeRoute(RouteType.PVR);
				else
					((RouteTTRP)route).setTypeRoute(RouteType.PTR);*/
                            
                            route = new RouteTTRP(route.getListIdCustomers(), route.getRequestRoute(), 
                                    route.getCostRoute(), route.getIdDepot(), listAccessVC, 
                          ((CustomerTTRP) listCustomers.get(i)).getTypeCustomer().equals(CustomerType.VC) ? RouteType.PVR : RouteType.PTR);
			}

			listRoutes.add(route);
		}

		return listRoutes;
	}
	
	protected void reduceOptions(Route route, NumericMatrix saveMatrix){
		int countCustomers = Problem.getProblem().getListCustomers().size();
		
		for(int i = 1; i < (route.getListIdCustomers().size() - 1); i++)
		{
			if(saveMatrix.countEqualThan(Problem.getProblem().getPosElement(route.getListIdCustomers().get(i)), 0, Problem.getProblem().getPosElement(route.getListIdCustomers().get(i)), (countCustomers - 1), Double.NEGATIVE_INFINITY) != countCustomers)
			{
				saveMatrix.fillValue(Problem.getProblem().getPosElement(route.getListIdCustomers().get(i)), 0, Problem.getProblem().getPosElement(route.getListIdCustomers().get(i)), (countCustomers - 1), Double.NEGATIVE_INFINITY);
				saveMatrix.fillValue(0, Problem.getProblem().getPosElement(route.getListIdCustomers().get(i)), (countCustomers - 1), Problem.getProblem().getPosElement(route.getListIdCustomers().get(i)), Double.NEGATIVE_INFINITY);
			}  
		}
	}	
	
	
	/* M�todo que retorna la ruta que fue cerrada porque cumplia con la capacidad de un veh�culo*/
/*	public Route closedRoute(ArrayList<Route> listRoutes, double capacityTotal){
		Route route = new Route();
		boolean isPossible = false;
		int i = 0;

		while((i < listRoutes.size()) && (!isPossible))
		{		
			if(listRoutes.get(i).getRequestRoute() == capacityTotal)
			{
				route.setListIdCustomers(listRoutes.get(i).getListIdCustomers());
				route.setIdDepot(listRoutes.get(i).getIdDepot());

				isPossible = true;
			}

		}
		return route; 
	}*/
	
	/* Metodo booleano que determina si una ruta esta llena */
	/*public boolean requestPerfect(ArrayList<Route> listRoute, double capacityTotal, double requestRoute){
		boolean pass = false;
		double idealRequest = capacityTotal - requestRoute;

		if(idealRequest != 0)
		{
			int i = 0;

			while(i < listRoute.size() && !pass){

				if(listRoute.get(i).getRequestRoute() <= idealRequest){
					pass = true;
				}
				else
					i++;
			}
		}	
		return pass;
	}*/
}
