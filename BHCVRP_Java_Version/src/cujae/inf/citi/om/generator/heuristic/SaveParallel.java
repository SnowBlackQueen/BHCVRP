package cujae.inf.citi.om.generator.heuristic;

import java.util.ArrayList;

import cujae.inf.citi.om.data.Customer;
import cujae.inf.citi.om.data.DepotMDVRP;
import cujae.inf.citi.om.data.FleetTTRP;
import cujae.inf.citi.om.data.Problem;
import cujae.inf.citi.om.data.ProblemType;
import cujae.inf.citi.om.generator.postoptimization.Operator_3opt;
import cujae.inf.citi.om.generator.solution.*;
import cujae.inf.citi.om.matrix.NumericMatrix;
import cujae.inf.citi.om.matrix.RowCol;

/* Clase que modela la heur�stica de Ahorro en su versi�n Paralela */

public class SaveParallel extends Save {

	public SaveParallel() {
		super();
		// TODO Auto-generated constructor stub
	}

	public Solution getSolutionInicial() {
		if(parameterShape <= 0)
			parameterShape = 1;
		
		Solution solution = new Solution();
		ArrayList<Customer> CustomersToVisit = null;
		int idDepot = -1;
		int posDepot = -1;
		
		if(Problem.getProblem().getTypeProblem().equals(ProblemType.CVRP) || Problem.getProblem().getTypeProblem().equals(ProblemType.HFVRP) || Problem.getProblem().getTypeProblem().equals(ProblemType.OVRP) || Problem.getProblem().getTypeProblem().equals(ProblemType.TTRP))
		{
			posDepot = 0;
			idDepot = Problem.getProblem().getListDepots().get(posDepot).getIdDepot();
			CustomersToVisit = new ArrayList<Customer>(Problem.getProblem().getListCustomers());
		}
		else
		{
			int i = 0;			
			boolean found = false;
	    
			while((i < Problem.getProblem().getListDepots().size()) && (!found))	
			{
				if(!((DepotMDVRP)Problem.getProblem().getListDepots().get(i)).getListAssignedCustomers().isEmpty())
				{					
					posDepot = i;
					
					idDepot = Problem.getProblem().getListDepots().get(posDepot).getIdDepot();	
					CustomersToVisit = new ArrayList<Customer>(Problem.getProblem().getCustomersAssignedByIDDepot(idDepot));
					
					found = true;
				}
				else
					i++;
			}	
		}
		
    	
		
		double capacityVehicle = Problem.getProblem().getListDepots().get(posDepot).getListFleets().get(0).getCapacityVehicle();
		int countVehicles = Problem.getProblem().getListDepots().get(posDepot).getListFleets().get(0).getCountVehicles();


		ArrayList<Double> listCapacities = new ArrayList<Double>(Problem.getProblem().fillListCapacities(posDepot)/*getListCapacities()*/);	/// fill o list
		
		Operator_3opt ThreeOpt = new Operator_3opt();

		ArrayList<Route> listRoutes = new ArrayList<Route>();
		listRoutes = createInitialRoutes(CustomersToVisit);
		inspectRoutes(listRoutes, listCapacities, solution, CustomersToVisit); ///

		int cantCustomers = CustomersToVisit.size();
		NumericMatrix saveMatrix = new NumericMatrix(cantCustomers, cantCustomers);
		saveMatrix = fillSaveMatrix(idDepot, CustomersToVisit);

		double totalCapacity = capacityVehicle;

		int iterations = (cantCustomers * (cantCustomers - 1))/2;
		int counter = 0;
		int rowCustomer;
		int colCustomer;
		int posRow;
		int posCol;

		RowCol rowcol;
		Route routeRow;
		Route routeCol;

		switch(Problem.getProblem().getTypeProblem().ordinal())
		{
			case 0:
			{		
				while((counter < iterations) && (listRoutes.size() > 1) && (!saveMatrix.fullMatrix(Double.NEGATIVE_INFINITY))) 
				{
					rowcol = new RowCol();
					rowcol = saveMatrix.indexBiggerValue();
					
					Double saveValue = saveMatrix.getItem(rowcol.getRow(), rowcol.getCol());
					
					if ((saveValue > 0) || ((saveValue <= 0) && (listRoutes.size() > countVehicles)))
					{ 
						rowCustomer = CustomersToVisit.get(rowcol.getRow()).getIdCustomer(); 
						colCustomer = CustomersToVisit.get(rowcol.getCol()).getIdCustomer(); 
						counter++;
		
						saveMatrix.setItem(rowcol.getRow(), rowcol.getCol(), Double.NEGATIVE_INFINITY);
						saveMatrix.setItem(rowcol.getCol(), rowcol.getRow(), Double.NEGATIVE_INFINITY); 
		
						posRow = getPositionRoute(listRoutes, rowCustomer);
						posCol = getPositionRoute(listRoutes, colCustomer);
		
						if(posRow == posCol)
							continue;
		
						routeRow = listRoutes.get(posRow);
						routeCol = listRoutes.get(posCol);
		
						Route route = new Route();
						boolean join = false;
		
						if(checkingJoin(routeRow, routeCol, rowCustomer, colCustomer, totalCapacity))
						{
							route.getListIdCustomers().addAll(routeRow.getListIdCustomers());
							route.getListIdCustomers().addAll(routeCol.getListIdCustomers());
							join = true;
		
						}
						else
						{
							if(checkingJoin(routeCol, routeRow, colCustomer, rowCustomer, totalCapacity))
							{
								route.getListIdCustomers().addAll(routeCol.getListIdCustomers());
								route.getListIdCustomers().addAll(routeRow.getListIdCustomers());
								join = true;
							}	
						}
		
						if(join)
						{
							route.setRequestRoute(routeRow.getRequestRoute() + routeCol.getRequestRoute());
							route.setIdDepot(idDepot);
		
							listRoutes.remove(routeRow);
							listRoutes.remove(routeCol);
							listRoutes.add(route);
						}
					}
					else
						if ((saveValue <= 0) && (listRoutes.size() <= countVehicles))
							saveMatrix.fillValue(Double.NEGATIVE_INFINITY);
				}
	
				for(int j = 0; j < listRoutes.size(); j++)
					if(listRoutes.get(j).getListIdCustomers().size() >= 6)
						ThreeOpt.toOptimize(listRoutes.get(j));
	
				solution.getListRoutes().addAll(listRoutes);
	
				break;
			}
		
			case 1:
			{
				boolean isFirst = true;
				boolean isOpen = false;
	
				while((!listRoutes.isEmpty()) && (!listCapacities.isEmpty()))
				{
					if((counter == iterations) && (!isOpen))//es q recorri ya la matriz completa
					{
						Route closeRoute = routeToClose(listRoutes);
						closeRoute.setIdDepot(idDepot);

						if(closeRoute.getListIdCustomers().size() >= 6)
							ThreeOpt.toOptimize(closeRoute);
	
						solution.getListRoutes().add(closeRoute);
						listCapacities.remove(0);
	
						isOpen = true;
						updateCustomersToVisit(closeRoute, CustomersToVisit);
	
						if(listRoutes.size() == 1)
						{
	
							listRoutes.get(0).setIdDepot(idDepot);

							if(listRoutes.get(0).getListIdCustomers().size() >= 6)
								ThreeOpt.toOptimize(listRoutes.get(0));
							
							solution.getListRoutes().add(listRoutes.get(0));
							listRoutes.remove(0);
						}			
					}
	
					isOpen = false;
	
					if(!isFirst)
					{
						cantCustomers = CustomersToVisit.size();
						saveMatrix = new NumericMatrix(cantCustomers, cantCustomers);
						saveMatrix = fillSaveMatrix(idDepot, CustomersToVisit);
	
						iterations = (cantCustomers * (cantCustomers - 1))/2;
						counter = 0;
					}
	
					isFirst = false;
	
					while(counter < iterations && listRoutes.size() > 1 && (!saveMatrix.fullMatrix(Double.NEGATIVE_INFINITY)) && (!listCapacities.isEmpty()) && (!isOpen)) 
					{
						rowcol = new RowCol();
						rowcol = saveMatrix.indexBiggerValue();
						
						Double saveValue = saveMatrix.getItem(rowcol.getRow(), rowcol.getCol());
						
						if ((saveValue > 0) || ((saveValue <= 0) && (listRoutes.size() > countVehicles)))
						{
							rowCustomer = CustomersToVisit.get(rowcol.getRow()).getIdCustomer();  
							colCustomer = CustomersToVisit.get(rowcol.getCol()).getIdCustomer();
							counter++;

							saveMatrix.setItem(rowcol.getRow(), rowcol.getCol(), Double.NEGATIVE_INFINITY); 
							saveMatrix.setItem(rowcol.getCol(), rowcol.getRow(), Double.NEGATIVE_INFINITY); 

							posRow = getPositionRoute(listRoutes, rowCustomer);
							posCol = getPositionRoute(listRoutes, colCustomer);

							if(posRow == posCol)
								continue;

							routeRow = listRoutes.get(posRow);
							routeCol = listRoutes.get(posCol);

							Route route = new Route();
							boolean join = false;

							if(checkingJoin(routeRow, routeCol, rowCustomer, colCustomer, listCapacities.get(0)))
							{
								route.getListIdCustomers().addAll(routeRow.getListIdCustomers());
								route.getListIdCustomers().addAll(routeCol.getListIdCustomers());
								join = true;

							}
							else
							{
								if(checkingJoin(routeCol, routeRow, colCustomer, rowCustomer, listCapacities.get(0)))
								{
									route.getListIdCustomers().addAll(routeCol.getListIdCustomers());
									route.getListIdCustomers().addAll(routeRow.getListIdCustomers());
									join = true;
								}	
							}

							if(join)
							{
								route.setRequestRoute(routeRow.getRequestRoute() + routeCol.getRequestRoute());

								listRoutes.remove(routeRow);
								listRoutes.remove(routeCol);

								if(route.getRequestRoute() == listCapacities.get(0))
								{
									route.setIdDepot(idDepot);//y xq no la agrego a la lista de rutas???

									if(route.getListIdCustomers().size() >= 6)
										ThreeOpt.toOptimize(route);
									
									solution.getListRoutes().add(route);
									listCapacities.remove(0);

									isOpen = true;
									updateCustomersToVisit(route, CustomersToVisit);

								}
								else//xq???!!
									listRoutes.add(route); //list|Routes es la de las rutas iniciales
							}
						}
						if(counter == iterations || (saveMatrix.fullMatrix(Double.NEGATIVE_INFINITY)))//si ya todos los q me quedan son infinitos
						{
							Route closeRoute = routeToClose(listRoutes);
		
							closeRoute.setIdDepot(idDepot);

							if(closeRoute.getListIdCustomers().size() >= 6)
								ThreeOpt.toOptimize(closeRoute);
							
							solution.getListRoutes().add(closeRoute);
							listCapacities.remove(0);
	
							isOpen = true;
							updateCustomersToVisit(closeRoute, CustomersToVisit);
	
						}
	
						if(listRoutes.size() == 1)//si me queda una sola ruta la agrego y cierro y ya
						{
							listRoutes.get(0).setIdDepot(idDepot);

							if(listRoutes.get(0).getListIdCustomers().size() >= 6)
								ThreeOpt.toOptimize(listRoutes.get(0));
							
							solution.getListRoutes().add(listRoutes.get(0));
							listRoutes.remove(0);
	
							isOpen = true;
						}
					}
				}
	
				if(listRoutes.size() > 0)
				{
					Route route = new Route();
					double newRequest = 0.0;
	
					route.setIdDepot(idDepot);
	
					while(!listRoutes.isEmpty())
					{
	
						newRequest += listRoutes.get(0).getRequestRoute();
						route.setRequestRoute(newRequest);
						route.getListIdCustomers().addAll(listRoutes.get(0).getListIdCustomers());
						listRoutes.remove(0);
					}
	
					if(route.getListIdCustomers().size() >= 6)
						ThreeOpt.toOptimize(route);
					
					solution.getListRoutes().add(route);
				}
				
				break;
			}
		
			case 2:
			{
				for(int j = posDepot; j < Problem.getProblem().getListDepots().size(); j++)
				{
					if(j != posDepot)
					{
						idDepot = Problem.getProblem().getListDepots().get(j).getIdDepot();
						CustomersToVisit = new ArrayList<Customer>(Problem.getProblem().getCustomersAssignedByIDDepot(idDepot));
						
						capacityVehicle = Problem.getProblem().getListDepots().get(j).getListFleets().get(0).getCapacityVehicle();
						countVehicles = Problem.getProblem().getListDepots().get(j).getListFleets().get(0).getCountVehicles();
						
						listCapacities = new ArrayList<Double>(Problem.getProblem().getListCapacities());	// fill o listparametro con el depot
						
						if(!CustomersToVisit.isEmpty())
						{
							listRoutes = createInitialRoutes(CustomersToVisit);
							inspectRoutes(listRoutes, listCapacities, solution, CustomersToVisit);
		
							cantCustomers = CustomersToVisit.size();
							saveMatrix = new NumericMatrix(cantCustomers, cantCustomers);
							saveMatrix = fillSaveMatrix(Problem.getProblem().getListDepots().get(j).getIdDepot(), CustomersToVisit);
		
							totalCapacity = capacityVehicle;
							iterations = (cantCustomers * (cantCustomers - 1))/2;
							counter = 0;
						}
						else
							continue;
					}
					
					while((counter < iterations) && (listRoutes.size() > 1) && (!saveMatrix.fullMatrix(Double.NEGATIVE_INFINITY))) 
					{
						rowcol = new RowCol();
						rowcol = saveMatrix.indexBiggerValue();
						
						Double saveValue = saveMatrix.getItem(rowcol.getRow(), rowcol.getCol());
						
						if ((saveValue > 0) || ((saveValue <= 0) && (listRoutes.size() > countVehicles)))
						{ 
							rowCustomer = CustomersToVisit.get(rowcol.getRow()).getIdCustomer(); 
							colCustomer = CustomersToVisit.get(rowcol.getCol()).getIdCustomer(); 
							counter++;
		
							saveMatrix.setItem(rowcol.getRow(), rowcol.getCol(), Double.NEGATIVE_INFINITY); 
							saveMatrix.setItem(rowcol.getCol(), rowcol.getRow(), Double.NEGATIVE_INFINITY); 
		
							posRow = getPositionRoute(listRoutes, rowCustomer);
							posCol = getPositionRoute(listRoutes, colCustomer);
		
							if(posRow == posCol)
								continue;
		
							routeRow = listRoutes.get(posRow);
							routeCol = listRoutes.get(posCol);
		
							Route route = new Route();
							boolean join = false;
		
							if(checkingJoin(routeRow, routeCol, rowCustomer, colCustomer, totalCapacity))
							{
		
								route.getListIdCustomers().addAll(routeRow.getListIdCustomers());
								route.getListIdCustomers().addAll(routeCol.getListIdCustomers());
								join = true;
		
							}
							else
							{
								if(checkingJoin(routeCol, routeRow, colCustomer, rowCustomer, totalCapacity))
								{
									route.getListIdCustomers().addAll(routeCol.getListIdCustomers());
									route.getListIdCustomers().addAll(routeRow.getListIdCustomers());
									join = true;
								}	
							}
		
							if(join)
							{
								route.setRequestRoute(routeRow.getRequestRoute() + routeCol.getRequestRoute());
								route.setIdDepot(idDepot);
		
								listRoutes.remove(routeRow);
								listRoutes.remove(routeCol);
								listRoutes.add(route);
							}
						}	
						else
							if ((saveValue <= 0) && (listRoutes.size() <= countVehicles))
								saveMatrix.fillValue(Double.NEGATIVE_INFINITY);
					}
	
					/*for(int k = 0; k < listRoutes.size(); k++)
						if(listRoutes.get(k).getListIdCustomers().size() >= 6)
							ThreeOpt.toOptimize(listRoutes.get(k));*/
					
					solution.getListRoutes().addAll(listRoutes);
				}
				
				break;
			}
		
			case 4:
			{
				double capacityTrailer = ((FleetTTRP)Problem.getProblem().getListDepots().get(posDepot).getListFleets().get(0)).getCapacityTrailer(); 
	
				while((counter < iterations) && (listRoutes.size() > 1) && (!saveMatrix.fullMatrix(Double.NEGATIVE_INFINITY))) 
				{
	
					rowcol = new RowCol();
					rowcol = saveMatrix.indexBiggerValue();
					
					Double saveValue = saveMatrix.getItem(rowcol.getRow(), rowcol.getCol());
					
					if ((saveValue > 0) || ((saveValue <= 0) && (listRoutes.size() > countVehicles)))
					{ 
						rowCustomer = CustomersToVisit.get(rowcol.getRow()).getIdCustomer(); 
						colCustomer = CustomersToVisit.get(rowcol.getCol()).getIdCustomer();
						counter++;
		
						saveMatrix.setItem(rowcol.getRow(), rowcol.getCol(), Double.NEGATIVE_INFINITY); 
						saveMatrix.setItem(rowcol.getCol(), rowcol.getRow(),Double.NEGATIVE_INFINITY); 
		
						posRow = getPositionRoute(listRoutes, rowCustomer);
						posCol = getPositionRoute(listRoutes, colCustomer);
		
						if(posRow == posCol)
							continue;
		
						routeRow = listRoutes.get(posRow);
						routeCol = listRoutes.get(posCol);
		
						Route route = new Route();;
						boolean join = false;
						RouteType typeRoute = null;
		
						totalCapacity = capacityVehicle;
						
						if(compatibleRoutes(routeRow, routeCol) || compatibleRoutes(routeCol, routeRow))
						{
							if(((RouteTTRP)routeRow).getTypeRoute().ordinal() != 0)
								totalCapacity += capacityTrailer;
		
							if(checkingJoin(routeRow, routeCol, rowCustomer, colCustomer, totalCapacity))
							{
								route.getListIdCustomers().addAll(routeRow.getListIdCustomers());
								route.getListIdCustomers().addAll(routeCol.getListIdCustomers());
								join = true;
		
								if(((RouteTTRP)routeRow).getTypeRoute().ordinal() == ((RouteTTRP)routeCol).getTypeRoute().ordinal())
									typeRoute = ((RouteTTRP)routeRow).getTypeRoute();
								else
									if(!((RouteTTRP)routeRow).getTypeRoute().equals(RouteType.PTR))
										typeRoute = RouteType.CVR;
									else
										typeRoute = RouteType.PTR;
							}
							else
							{
								totalCapacity = capacityVehicle;
								
								if(!((RouteTTRP)routeCol).getTypeRoute().equals(RouteType.PTR))
									totalCapacity += capacityTrailer;
		
								if(checkingJoin(routeCol, routeRow, colCustomer, rowCustomer, totalCapacity))
								{
									route.getListIdCustomers().addAll(routeCol.getListIdCustomers());
									route.getListIdCustomers().addAll(routeRow.getListIdCustomers());
									join = true;
		
									if(((RouteTTRP)routeCol).getTypeRoute().ordinal() == ((RouteTTRP)routeRow).getTypeRoute().ordinal())
										typeRoute = ((RouteTTRP)routeCol).getTypeRoute();
									else
										if(!((RouteTTRP)routeCol).getTypeRoute().equals(RouteType.PTR))
											typeRoute = RouteType.CVR;
										else
											typeRoute = RouteType.PTR;
								}
							}
						}
						
						if(join)
						{
							route.setRequestRoute(routeRow.getRequestRoute() + routeCol.getRequestRoute());
							//((RouteTTRP)route).setTypeRoute(typeRoute);
							route.setIdDepot(idDepot);
                                                        ArrayList<Integer> listAccessVC = new ArrayList<Integer>();
                                                        route = new RouteTTRP(route.getListIdCustomers(), route.getRequestRoute(), route.getCostRoute(),
                                                        route.getIdDepot(), listAccessVC, typeRoute);
		
							listRoutes.remove(routeRow);
							listRoutes.remove(routeCol);
							listRoutes.add(route);
		
							reduceOptions(route, saveMatrix);
						}	
					}
				}
	
				for(int j = 0; j < listRoutes.size(); j++)
					if(listRoutes.get(j).getListIdCustomers().size() >= 6)
						ThreeOpt.toOptimize(listRoutes.get(j));
	
				solution.getListRoutes().addAll(listRoutes);
	
				break;
			}
		}
		return solution;
}

	/*M�todo que revisa si alguna ruta cumple con la capacidad, la cierra y actualiza CustomersToVisite*/
	public void inspectRoutes(ArrayList<Route> listRoutes, ArrayList<Double> listCapacities, Solution solution, ArrayList<Customer> CustomersToVisit){
		for(int i = 0; i < listRoutes.size(); i++)
		{
			int j = 0;
			boolean found = false;

			while((j < listCapacities.size()) && (!found)) // se debe eliminar la capacidad de la lista
			{
				if(listRoutes.get(i).getRequestRoute() == listCapacities.get(j))
				{ 
					solution.getListRoutes().add(listRoutes.get(i));
					listRoutes.remove(i);
					listCapacities.remove(j);
					updateCustomersToVisit(listRoutes.get(i), CustomersToVisit);
					
					found = true;
					
				}
				else
					j++;
			}
		}
	}

	/* M�todo que actualiza la lista de CustomersToVisit */
	public void updateCustomersToVisit(Route closeRoute, ArrayList<Customer> CustomersToVisit){
		for(int i = 0; i < closeRoute.getListIdCustomers().size(); i++)
		{
			int j = 0;
			boolean found = false;

			while((j < CustomersToVisit.size()) && (!found))
			{
				if(CustomersToVisit.get(j).getIdCustomer() == closeRoute.getListIdCustomers().get(i))
				{
					CustomersToVisit.remove(j);
					found = true;
				}
				else
					j++;
			}
		}	
	}

	/* M�todo que devuelve la ruta con la demanda mas cercana a la capacidad */
	public Route routeToClose(ArrayList<Route> listRoutes){
		Route route = new Route();

		double maxCapacity = listRoutes.get(0).getRequestRoute();
		int posMax = 0;

		for(int i = 1; i < listRoutes.size(); i++)
		{
			if(listRoutes.get(i).getRequestRoute() > maxCapacity)
			{
				maxCapacity = listRoutes.get(i).getRequestRoute();		
				posMax = i;
			}
		}

		route = listRoutes.get(posMax);			
		listRoutes.remove(posMax);

		return route;
	}

	/* M�todo que indica si dos rutas pueden unirse */
	public boolean checkingJoin(Route routeIni, Route routeEnd, int idCustomerIni, int idCustomerEnd, double totalCapacity){

		boolean join = false;
		int sizeRoute = routeIni.getListIdCustomers().size();

		if((routeIni.getRequestRoute() + routeEnd.getRequestRoute()) <= totalCapacity)
		{
			if((routeIni.getListIdCustomers().get(sizeRoute - 1) == idCustomerIni) && (routeEnd.getListIdCustomers().get(0) == idCustomerEnd))
				join = true; 	
		}

		return join;
	}

	/* M�todo que indica si dos rutas son compatibles */
	public boolean compatibleRoutes(Route routeIni, Route routeEnd){
		boolean isCompatible = true;

		if(((RouteTTRP)routeIni).getTypeRoute().equals(RouteType.PTR) && (!((RouteTTRP)routeEnd).getTypeRoute().equals(RouteType.PTR)))
			isCompatible = false;

		return isCompatible; 
	}
}
