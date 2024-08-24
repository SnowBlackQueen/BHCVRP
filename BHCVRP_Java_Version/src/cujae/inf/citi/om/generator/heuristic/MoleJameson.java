package cujae.inf.citi.om.generator.heuristic;

import java.util.ArrayList;

import cujae.inf.citi.om.data.Customer;
import cujae.inf.citi.om.data.CustomerType;
import cujae.inf.citi.om.data.DepotMDVRP;
import cujae.inf.citi.om.data.FleetTTRP;
import cujae.inf.citi.om.data.Problem;
import cujae.inf.citi.om.data.ProblemType;
import cujae.inf.citi.om.generator.postoptimization.Operator_3opt;
import cujae.inf.citi.om.generator.solution.*;

public class MoleJameson extends Heuristic{

	public static int parameterC1 = 1;
	public static int parameterC2 = 1;
	public static FirstCustomerType firstCustomerType = FirstCustomerType.FurthestCustomer;
	
	public MoleJameson() {
		super();
		// TODO Auto-generated constructor stub
	}

	@Override
	public Solution getSolutionInicial() {
		if(parameterC1 <= 0)
			parameterC1 = 1;
		
		if(parameterC2 <= 0)
			parameterC2 = 1;
		
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

		Operator_3opt ThreeOpt = new Operator_3opt();
		
		Customer customer = new Customer();
		Route route = new Route();
		double requestRoute = 0.0;

		ArrayList<Metric> listBestPositions = null;
		Metric metricMJ = null;
		int countNoFeasible = 0;
		
		customer = getFirstCustomer(CustomersToVisit, firstCustomerType, idDepot);   
		requestRoute = customer.getRequestCustomer();
		route.getListIdCustomers().add(idDepot);		
		route.getListIdCustomers().add(customer.getIdCustomer());
		route.getListIdCustomers().add(idDepot);
		route.setIdDepot(idDepot);
		CustomersToVisit.remove(customer);
	
		switch(Problem.getProblem().getTypeProblem().ordinal())
		{
			case 0: case 3:
			{
				while((!CustomersToVisit.isEmpty()) && (countVehicles > 0))
				{
					countNoFeasible = 0;
					listBestPositions = new ArrayList<Metric>();
					
					for(int i = 0; i < CustomersToVisit.size(); i++) 
					{
						if(capacityVehicle >= (requestRoute + CustomersToVisit.get(i).getRequestCustomer()))

                                                   listBestPositions.add(getPositionWithBestCost(route, CustomersToVisit.get(i).getIdCustomer()));
						else
							countNoFeasible++;		
					}
					
					if(countNoFeasible == CustomersToVisit.size())
					{
						route.getListIdCustomers().remove(0);
						route.getListIdCustomers().remove((route.getListIdCustomers().size() - 1));	
						route.setRequestRoute(requestRoute);
						solution.getListRoutes().add(route);
						
						route = null;
						--countVehicles;
					
						if(countVehicles > 0)
						{
							route = new Route();
							
							customer = getFirstCustomer(CustomersToVisit, firstCustomerType, idDepot);
							requestRoute = customer.getRequestCustomer();
							route.getListIdCustomers().add(idDepot);		
							route.getListIdCustomers().add(customer.getIdCustomer());
							route.getListIdCustomers().add(idDepot);
							route.setIdDepot(idDepot);
							CustomersToVisit.remove(customer);
						}
					}
					else
					{
						metricMJ = getMJCustomer(listBestPositions, idDepot);
						requestRoute += Problem.getProblem().getRequestByIDCustomer(metricMJ.getIdElement());
						route.getListIdCustomers().add(metricMJ.getIndex(), metricMJ.getIdElement());
						CustomersToVisit.remove(Problem.getProblem().getCustomerByIDCustomer(metricMJ.getIdElement()));
									
						if(route.getListIdCustomers().size() >= 6)
						{
							route.getListIdCustomers().remove(0);
							route.getListIdCustomers().remove((route.getListIdCustomers().size() - 1));
							
							if(route.getListIdCustomers().size() >= 6)
                                                            ThreeOpt.toOptimize(route);
							
							route.getListIdCustomers().add(0, idDepot);
							route.getListIdCustomers().add(idDepot);	
						}						
					}
				}
				
				if(route != null)
				{
					route.getListIdCustomers().remove(0);
					route.getListIdCustomers().remove((route.getListIdCustomers().size() - 1));
					route.setRequestRoute(requestRoute);		
					solution.getListRoutes().add(route);	
				}
				
				if(!CustomersToVisit.isEmpty())
				{
					route = new Route();	
					metricMJ = new Metric();
					
					customer = getFirstCustomer(CustomersToVisit, firstCustomerType, idDepot);   
					requestRoute = customer.getRequestCustomer();
					route.getListIdCustomers().add(idDepot);
					route.getListIdCustomers().add(customer.getIdCustomer());
					route.getListIdCustomers().add(idDepot);		
					route.setIdDepot(idDepot);
					CustomersToVisit.remove(customer);
					
					while(!CustomersToVisit.isEmpty())
					{
						listBestPositions = new ArrayList<Metric>();
						
						for(int i = 0; i < CustomersToVisit.size(); i++) 
							listBestPositions.add(getPositionWithBestCost(route, CustomersToVisit.get(i).getIdCustomer()));
						
						metricMJ = getMJCustomer(listBestPositions, idDepot);
						requestRoute += Problem.getProblem().getRequestByIDCustomer(metricMJ.getIdElement()); 
						route.getListIdCustomers().add(metricMJ.getIndex(), metricMJ.getIdElement());
						CustomersToVisit.remove(Problem.getProblem().getCustomerByIDCustomer(metricMJ.getIdElement()));
											
						if(route.getListIdCustomers().size() >= 6)
						{
							route.getListIdCustomers().remove(0);
							route.getListIdCustomers().remove((route.getListIdCustomers().size() - 1));
							
                                                        if(route.getListIdCustomers().size() >= 6)
                                                            ThreeOpt.toOptimize(route);
							
							route.getListIdCustomers().add(0, idDepot);
							route.getListIdCustomers().add(idDepot); 
						}
					}
					
					route.getListIdCustomers().remove(0);
					route.getListIdCustomers().remove((route.getListIdCustomers().size() - 1));
					route.setRequestRoute(requestRoute);		
					solution.getListRoutes().add(route);
				}
				
				break;
			}
			
			case 1:
			{
				ArrayList<Double> listCapacities = new ArrayList<Double>(Problem.getProblem().getListCapacities());
				capacityVehicle = listCapacities.get(0);
				
				while((!CustomersToVisit.isEmpty()) && (!listCapacities.isEmpty()))
				{
					countNoFeasible = 0;
					listBestPositions = new ArrayList<Metric>();
					
					for(int i = 0; i < CustomersToVisit.size(); i++) 
					{
						if(capacityVehicle >= requestRoute + CustomersToVisit.get(i).getRequestCustomer())
							listBestPositions.add(getPositionWithBestCost(route, CustomersToVisit.get(i).getIdCustomer()));
						else
							countNoFeasible++;		
					}

					if(countNoFeasible == CustomersToVisit.size())
					{
						route.getListIdCustomers().remove(0);
						route.getListIdCustomers().remove((route.getListIdCustomers().size() - 1));
						route.setRequestRoute(requestRoute);
						solution.getListRoutes().add(route);
						
						route = null;
						listCapacities.remove(0);
						
						if(!listCapacities.isEmpty())
						{
							route = new Route();
							
							customer = getFirstCustomer(CustomersToVisit, firstCustomerType, idDepot);
							requestRoute = customer.getRequestCustomer();
							route.getListIdCustomers().add(idDepot);
							route.getListIdCustomers().add(customer.getIdCustomer());
							route.getListIdCustomers().add(idDepot);					 
							route.setIdDepot(idDepot);
							CustomersToVisit.remove(customer);
	
							capacityVehicle = listCapacities.get(0);
						}
					}
					else
					{
						metricMJ = getMJCustomer(listBestPositions, idDepot);
						requestRoute += Problem.getProblem().getRequestByIDCustomer(metricMJ.getIdElement());
						route.getListIdCustomers().add(metricMJ.getIndex(), metricMJ.getIdElement());
						CustomersToVisit.remove(Problem.getProblem().getCustomerByIDCustomer(metricMJ.getIdElement()));
			
						if(route.getListIdCustomers().size() >= 6)
						{
							route.getListIdCustomers().remove(0);
							route.getListIdCustomers().remove((route.getListIdCustomers().size() - 1));
							
                                                        if(route.getListIdCustomers().size() >= 6)
                                                            ThreeOpt.toOptimize(route);
                                                        
							route.getListIdCustomers().add(0, idDepot);
							route.getListIdCustomers().add(idDepot);
						}
					}
				}

				if(route != null)	
				{
					route.getListIdCustomers().remove(0);
					route.getListIdCustomers().remove((route.getListIdCustomers().size() - 1));
					route.setRequestRoute(requestRoute);
					solution.getListRoutes().add(route);
				}

				if(!CustomersToVisit.isEmpty())
				{
					route = new Route();	
					metricMJ = new Metric();
					
					customer = getFirstCustomer(CustomersToVisit, firstCustomerType, idDepot);   
					requestRoute = customer.getRequestCustomer();
					route.getListIdCustomers().add(idDepot);
					route.getListIdCustomers().add(customer.getIdCustomer());
					route.getListIdCustomers().add(idDepot);		
					route.setIdDepot(idDepot);
					CustomersToVisit.remove(customer);
					
					while(!CustomersToVisit.isEmpty())
					{
						listBestPositions = new ArrayList<Metric>();
						
						for(int i = 0; i < CustomersToVisit.size(); i++) 
							listBestPositions.add(getPositionWithBestCost(route, CustomersToVisit.get(i).getIdCustomer()));
						
						metricMJ = getMJCustomer(listBestPositions, idDepot);
						requestRoute += Problem.getProblem().getRequestByIDCustomer(metricMJ.getIdElement()); 
						route.getListIdCustomers().add(metricMJ.getIndex(), metricMJ.getIdElement());
						CustomersToVisit.remove(Problem.getProblem().getCustomerByIDCustomer(metricMJ.getIdElement()));
								
						if(route.getListIdCustomers().size() >= 6)
						{
							route.getListIdCustomers().remove(0);
							route.getListIdCustomers().remove((route.getListIdCustomers().size() - 1));
							
							if(route.getListIdCustomers().size() >= 6)
                                                            ThreeOpt.toOptimize(route);
							
							route.getListIdCustomers().add(0, idDepot);
							route.getListIdCustomers().add(idDepot);
						} 
					}
					
					route.getListIdCustomers().remove(0);
					route.getListIdCustomers().remove((route.getListIdCustomers().size() - 1));
					route.setRequestRoute(requestRoute);
								
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
						CustomersToVisit = Problem.getProblem().getCustomersAssignedByIDDepot(idDepot);
						
						capacityVehicle= Problem.getProblem().getListDepots().get(j).getListFleets().get(0).getCapacityVehicle();
						countVehicles = Problem.getProblem().getListDepots().get(j).getListFleets().get(0).getCountVehicles();

						if(!CustomersToVisit.isEmpty())
						{
							route = new Route();
							
							customer = getFirstCustomer(CustomersToVisit, firstCustomerType, idDepot);
							requestRoute = customer.getRequestCustomer();
							route.getListIdCustomers().add(idDepot);
							route.getListIdCustomers().add(customer.getIdCustomer());
							route.getListIdCustomers().add(idDepot);
							route.setIdDepot(idDepot);
							CustomersToVisit.remove(customer);
						}
					}
					
					while((!CustomersToVisit.isEmpty()) && (countVehicles > 0))
					{
						countNoFeasible = 0;
						listBestPositions = new ArrayList<Metric>();
						
						for(int k = 0; k < CustomersToVisit.size(); k++) 
						{
							if(capacityVehicle >= (requestRoute + CustomersToVisit.get(k).getRequestCustomer()))
								listBestPositions.add(getPositionWithBestCost(route, CustomersToVisit.get(k).getIdCustomer()));
							else
								countNoFeasible++;		
						}
						
						if(countNoFeasible == CustomersToVisit.size())
						{
							route.getListIdCustomers().remove(0);
							route.getListIdCustomers().remove((route.getListIdCustomers().size() - 1));
							route.setRequestRoute(requestRoute);
							solution.getListRoutes().add(route);
							
							route = null;
							--countVehicles;
	
							if(countVehicles > 0)
							{
								route = new Route();
								
								customer = getFirstCustomer(CustomersToVisit, firstCustomerType, idDepot);
								requestRoute = customer.getRequestCustomer();
								route.getListIdCustomers().add(idDepot);
								route.getListIdCustomers().add(customer.getIdCustomer());
								route.getListIdCustomers().add(idDepot);
								route.setIdDepot(idDepot);
								CustomersToVisit.remove(customer);
							}
						}
						else
						{
							metricMJ = getMJCustomer(listBestPositions, idDepot);
							requestRoute += Problem.getProblem().getRequestByIDCustomer(metricMJ.getIdElement());
							route.getListIdCustomers().add(metricMJ.getIndex(), metricMJ.getIdElement());
							CustomersToVisit.remove(Problem.getProblem().getCustomerByIDCustomer(metricMJ.getIdElement()));
										
							if(route.getListIdCustomers().size() >= 6)
							{
								route.getListIdCustomers().remove(0);
								route.getListIdCustomers().remove((route.getListIdCustomers().size() - 1));
								
								if(route.getListIdCustomers().size() >= 6)
                                                                    ThreeOpt.toOptimize(route);
								
								route.getListIdCustomers().add(0, idDepot);
								route.getListIdCustomers().add(idDepot); 
							}
						}
					}
					
					if(route != null)
					{
						route.getListIdCustomers().remove(0);
						route.getListIdCustomers().remove((route.getListIdCustomers().size() - 1));
						route.setRequestRoute(requestRoute);
						solution.getListRoutes().add(route);
					}
					
					if(!CustomersToVisit.isEmpty())
					{
						route = new Route();						
						metricMJ = new Metric();
						
						customer = getFirstCustomer(CustomersToVisit, firstCustomerType, idDepot);   
						requestRoute = customer.getRequestCustomer();
						route.getListIdCustomers().add(idDepot);
						route.getListIdCustomers().add(customer.getIdCustomer());
						route.getListIdCustomers().add(idDepot);		
						route.setIdDepot(idDepot);
						CustomersToVisit.remove(customer);
						
						while(!CustomersToVisit.isEmpty())
						{
							listBestPositions = new ArrayList<Metric>();
							
							for(int l = 0; l < CustomersToVisit.size(); l++) 
								listBestPositions.add(getPositionWithBestCost(route, CustomersToVisit.get(l).getIdCustomer()));
							
							metricMJ = getMJCustomer(listBestPositions, idDepot);
							requestRoute += Problem.getProblem().getRequestByIDCustomer(metricMJ.getIdElement());
							route.getListIdCustomers().add(metricMJ.getIndex(), metricMJ.getIdElement());
							CustomersToVisit.remove(Problem.getProblem().getCustomerByIDCustomer(metricMJ.getIdElement()));
									
							if(route.getListIdCustomers().size() >= 6)
							{
								route.getListIdCustomers().remove(0);
								route.getListIdCustomers().remove((route.getListIdCustomers().size() - 1));
							
                                                                if(route.getListIdCustomers().size() >= 6)
                                                                    ThreeOpt.toOptimize(route);
							
								route.getListIdCustomers().add(0, idDepot);
								route.getListIdCustomers().add(idDepot);
							}
						
						}
						
						route.getListIdCustomers().remove(0);
						route.getListIdCustomers().remove((route.getListIdCustomers().size() - 1));
						route.setRequestRoute(requestRoute);
						solution.getListRoutes().add(route);
					}
				}
				
				break;
			}
			
			
			
			case 4:
			{
				//boolean isTC = false;
				double capacityTrailer = ((FleetTTRP)Problem.getProblem().getListDepots().get(posDepot).getListFleets().get(0)).getCapacityTrailer();
				
				CustomerType typeCustomer;
                                
                                ArrayList<Integer> listAccessVC = new ArrayList<Integer>();
				
				while(!CustomersToVisit.isEmpty())
				{
					listBestPositions = new ArrayList<Metric>();
					typeCustomer = Problem.getProblem().getTypeByIDCustomer(route.getListIdCustomers().get(1));
					
					switch (typeCustomer.ordinal()) 
					{
						case 0:
						{
							countNoFeasible = 0;
							
							for (int i = 0; i < CustomersToVisit.size(); i++) 
							{
								if((capacityVehicle + capacityTrailer) >= (requestRoute + CustomersToVisit.get(i).getRequestCustomer()))
									listBestPositions.add(getPositionWithBestCost(route, CustomersToVisit.get(i).getIdCustomer()));
								else
									countNoFeasible++;		
							}
							
							break;
						}
						
						case 1:
						{
							countNoFeasible = 0;
							
							for (int i = 0; i < CustomersToVisit.size(); i++) 
							{
								if(capacityVehicle >= (requestRoute + CustomersToVisit.get(i).getRequestCustomer()))
									listBestPositions.add(getPositionWithBestCost(route, CustomersToVisit.get(i).getIdCustomer()));
								else
									countNoFeasible++;		
							}
							
							break;
						}
					}
					
					if(countNoFeasible == CustomersToVisit.size())
					{
						route.getListIdCustomers().remove(0);
						route.getListIdCustomers().remove((route.getListIdCustomers().size() - 1));
						route.setRequestRoute(requestRoute);
						
						if(Problem.getProblem().getTypeByIDCustomer(route.getListIdCustomers().get(0)).equals(CustomerType.TC))
                                                    route = new RouteTTRP(route.getListIdCustomers(), route.getRequestRoute(), route.getCostRoute(),
                                                        route.getIdDepot(), listAccessVC, RouteType.PTR);
							//((RouteTTRP)route).setTypeRoute(RouteType.PTR);
						else
						{
							if(existTC(route))
                                                            route = new RouteTTRP(route.getListIdCustomers(), route.getRequestRoute(), route.getCostRoute(),
                                                        route.getIdDepot(), listAccessVC, RouteType.CVR);
								//((RouteTTRP)route).setTypeRoute(RouteType.CVR);
							else
                                                            route = new RouteTTRP(route.getListIdCustomers(), route.getRequestRoute(), route.getCostRoute(),
                                                        route.getIdDepot(), listAccessVC, RouteType.PVR);
								//((RouteTTRP)route).setTypeRoute(RouteType.PVR);
						}
						
						//3opt
						if(route.getListIdCustomers().size() >= 6)
							ThreeOpt.toOptimize(route);
						
						solution.getListRoutes().add(route);
						
						if(!CustomersToVisit.isEmpty())
						{
							route = new Route();
							
							customer = getFirstCustomer(CustomersToVisit, firstCustomerType, idDepot);
							requestRoute = customer.getRequestCustomer();
							route.getListIdCustomers().add(idDepot);
							route.getListIdCustomers().add(idDepot);
							route.getListIdCustomers().add(1, customer.getIdCustomer());
							route.setIdDepot(idDepot);
							CustomersToVisit.remove(customer);
						}
					}
					else
					{
						metricMJ = getMJCustomer(listBestPositions, idDepot);
						
						/*if(Problem.getProblem().getTypeByIDCustomer(bestMetricMJ.getIdElement()).equals(CustomerType.TC))
							isTC = true;*/
						
						requestRoute += Problem.getProblem().getRequestByIDCustomer(metricMJ.getIdElement());
						route.getListIdCustomers().add(metricMJ.getIndex(), metricMJ.getIdElement());
						CustomersToVisit.remove(Problem.getProblem().getCustomerByIDCustomer(metricMJ.getIdElement()));
					}
				}
				
				if(requestRoute > 0.0) // cambiar condicion
				{
					route.getListIdCustomers().remove(0);
					route.getListIdCustomers().remove((route.getListIdCustomers().size() - 1));
					route.setRequestRoute(requestRoute);

					if(Problem.getProblem().getTypeByIDCustomer(route.getListIdCustomers().get(0)).equals(CustomerType.TC))
                                            route = new RouteTTRP(route.getListIdCustomers(), route.getRequestRoute(), route.getCostRoute(),
                                                        route.getIdDepot(), listAccessVC, RouteType.PTR);
						//((RouteTTRP)route).setTypeRoute(RouteType.PTR);
					else
					{
						if(existTC(route))
                                                    route = new RouteTTRP(route.getListIdCustomers(), route.getRequestRoute(), route.getCostRoute(),
                                                        route.getIdDepot(), listAccessVC, RouteType.CVR);
							//((RouteTTRP)route).setTypeRoute(RouteType.CVR);
						else
                                                    route = new RouteTTRP(route.getListIdCustomers(), route.getRequestRoute(), route.getCostRoute(),
                                                        route.getIdDepot(), listAccessVC, RouteType.PVR);
							//((RouteTTRP)route).setTypeRoute(RouteType.PVR);	
					}
						
					//3opt
					if(route.getListIdCustomers().size() >= 6)
						ThreeOpt.toOptimize(route);
					
					solution.getListRoutes().add(route);
				}
				
				break;
			}
		}
		
		return solution;
	}

	/* M�todo que devuelve la m�trica del cliente con el mejor C1*/	
	private Metric getPositionWithBestCost(Route route, int idCustomer){
		int bestPosition = 1;
		double bestCost = 0.0;
		double currentCost = 0.0;
		int sizeRoute = route.getListIdCustomers().size();
		
		if(Problem.getProblem().getTypeProblem().equals(ProblemType.OVRP)) // no haria falta con case 3
			sizeRoute--;	
		
		for(int i = 1; i < sizeRoute; i++) 
		{
			currentCost = calculateC1(route.getListIdCustomers().get(i - 1), route.getListIdCustomers().get(i), idCustomer);

			if(i == 1)
				bestCost = currentCost;
			else
			{
				if(currentCost < bestCost)
				{
					bestCost = currentCost;
					bestPosition = i;
				}
			}	
		}

		Metric bestC1 = new Metric();
		bestC1.setInsertionCost(bestCost);
		bestC1.setIndex(bestPosition);
		bestC1.setIdElement(idCustomer);

		return bestC1;
	}
	
	/* M�todo que calcula la m�trica c1 */
	private double calculateC1(int previousElement, int nextElement, int currentElement){
		double costFirst = Problem.getProblem().getCostMatrix().getItem(Problem.getProblem().getPosElement(previousElement), Problem.getProblem().getPosElement(currentElement));
		double costSecond = Problem.getProblem().getCostMatrix().getItem(Problem.getProblem().getPosElement(currentElement), Problem.getProblem().getPosElement(nextElement));
		double costThird = Problem.getProblem().getCostMatrix().getItem(Problem.getProblem().getPosElement(previousElement), Problem.getProblem().getPosElement(nextElement));
		
		return ((costFirst + costSecond) - (parameterC1 * costThird));
	}
	
	/* Metodo que implementa la metrica c2 */
	private double calculateC2(double costToDepot, double costC1){
		return ((parameterC2 * costToDepot) - costC1);
	}
	
	/* M�todo que devuelve el cliente con el mejor C2*/
	private Metric getMJCustomer(ArrayList<Metric> listBestPositions, int idDepot){
		double currentValue = 0.0;
		double maxValue = 0.0;
		int positionMJ = 0;

		for(int i = 0; i < listBestPositions.size(); i++) 
		{
			int bestCustomer = listBestPositions.get(i).getIdElement();
			double costToDepot = Problem.getProblem().getCostMatrix().getItem(Problem.getProblem().getPosElement(idDepot), Problem.getProblem().getPosElement(bestCustomer));

			currentValue = calculateC2(costToDepot, listBestPositions.get(i).getInsertionCost());

			if(i == 0)
				maxValue = currentValue;
			else
			{
				if(currentValue > maxValue)
				{
					maxValue = currentValue;
					positionMJ = i;
				}
			}
		}
		
		return listBestPositions.remove(positionMJ);
	}
	
	/* M�todo que dice si existen clientes de tipo TC en la ruta construida */
	private boolean existTC(Route route){
		boolean exist = false;
		int i = 0;
		
		while((i < route.getListIdCustomers().size()) && (!exist))
		{
			if(Problem.getProblem().getTypeByIDCustomer(route.getListIdCustomers().get(i)).equals(CustomerType.TC))
			   exist = true;
			else
				i++;
		}
		
		return exist;
	}
}
