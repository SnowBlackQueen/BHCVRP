package cujae.inf.citi.om.generator.heuristic;

import java.util.ArrayList;
import java.util.Random;

import cujae.inf.citi.om.data.Customer;
import cujae.inf.citi.om.data.CustomerTTRP;
import cujae.inf.citi.om.data.CustomerType;
import cujae.inf.citi.om.data.DepotMDVRP;
import cujae.inf.citi.om.data.FleetTTRP;
import cujae.inf.citi.om.data.Problem;
import cujae.inf.citi.om.data.ProblemType;
import cujae.inf.citi.om.generator.postoptimization.Operator_3opt;
import cujae.inf.citi.om.generator.solution.*;

public class CMT extends Heuristic{

	public static int parameterL = 1;
	public static FirstCustomerType firstCustomerType = FirstCustomerType.RandomCustomer;
	
	public CMT() {
		super();
		// TODO Auto-generated constructor stub
	}

	@Override
	public Solution getSolutionInicial() {
		if(parameterL <= 0)
			parameterL = 1;
		
		Solution solution = new Solution();
		ArrayList<Customer> CustomersToVisit = null;
		ArrayList<Route> listCandidateRoutes = new ArrayList<Route>();
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

		Random random = new Random();
		int index = -1;
		
		ArrayList<Customer> listRootCustomers = new ArrayList<Customer>();
		ArrayList<ArrayList<Metric>> listMetricsCMTByCustomer = null;
		ArrayList<Metric> listTauCosts = null;
		Route route = null;
		Customer rootCustomer = null;
		Customer customerToInsert = null;
		double requestRoute = 0.0;
		int posBestTau = -1;

		switch(Problem.getProblem().getTypeProblem().ordinal())
		{
			case 0: case 3:
			{
				while(!CustomersToVisit.isEmpty())
				{
					listCandidateRoutes = doFirstPhase(CustomersToVisit, idDepot, posDepot, capacityVehicle, countVehicles);
					listRootCustomers = updateCustomersToVisit(listCandidateRoutes, CustomersToVisit);
	
					while(!listCandidateRoutes.isEmpty())
					{
						listMetricsCMTByCustomer = new ArrayList<ArrayList<Metric>>();
						listMetricsCMTByCustomer = calculateCostCMTByCustomer(idDepot, CustomersToVisit, listCandidateRoutes);
	
						route = new Route();
	
						index = random.nextInt(listCandidateRoutes.size());
						route = listCandidateRoutes.remove(index);
						
						rootCustomer = new Customer();
						rootCustomer = getCustomerByID(route.getListIdCustomers().get(0).intValue(), listRootCustomers);
						requestRoute = rootCustomer.getRequestCustomer();
						listRootCustomers.remove(rootCustomer);
						route.setIdDepot(idDepot);
	
						listTauCosts = new ArrayList<Metric>();
						listTauCosts = calculateTau(listMetricsCMTByCustomer, index);
	
						while(!listTauCosts.isEmpty())
						{
							customerToInsert = new Customer();
							posBestTau = listTauCosts.size() - 1;
							customerToInsert = getCustomerByID(listTauCosts.get(posBestTau).getIdElement(), CustomersToVisit);
	
							if(capacityVehicle >= (requestRoute + customerToInsert.getRequestCustomer()))
							{
								requestRoute += customerToInsert.getRequestCustomer();
								route.getListIdCustomers().add(customerToInsert.getIdCustomer());
								
								if(route.getListIdCustomers().size() >= 6)
									ThreeOpt.toOptimize(route);
								
								listTauCosts.remove(posBestTau);
								deleteElement(customerToInsert.getIdCustomer(), listMetricsCMTByCustomer);
								CustomersToVisit.remove(customerToInsert);
							}
							else
								listTauCosts.remove(posBestTau);
						}	
	
						route.setRequestRoute(requestRoute);
						solution.getListRoutes().add(route);
					}
					
					// actualizar countvehicles
				}
				
				break;
			}
			
			case 1:
			{
				ArrayList<Double> listCapacities = new ArrayList<Double>(Problem.getProblem().getListCapacities());
				capacityVehicle = listCapacities.get(0);
				boolean isOpen = false;

				while((!CustomersToVisit.isEmpty()) && (!listCapacities.isEmpty()))
				{
					listCandidateRoutes = doFirstPhase(CustomersToVisit, idDepot, posDepot, capacityVehicle, countVehicles);					
					listRootCustomers = updateCustomersToVisit(listCandidateRoutes, CustomersToVisit);
					
					while((!listCandidateRoutes.isEmpty()) && (!listCapacities.isEmpty()))
					{
						listMetricsCMTByCustomer = new ArrayList<ArrayList<Metric>>();
						listMetricsCMTByCustomer = calculateCostCMTByCustomer(idDepot, CustomersToVisit, listCandidateRoutes);
	
						route = new Route();
						isOpen = true;
						
						index = random.nextInt(listCandidateRoutes.size());
						route = listCandidateRoutes.remove(index);
	
						rootCustomer = new Customer();
						rootCustomer = getCustomerByID(route.getListIdCustomers().get(0).intValue(), listRootCustomers);
						requestRoute = rootCustomer.getRequestCustomer();
						listRootCustomers.remove(rootCustomer);
						route.setIdDepot(idDepot);
	
						listTauCosts = new ArrayList<Metric>();
						listTauCosts = calculateTau(listMetricsCMTByCustomer, index);
	
						while(!listTauCosts.isEmpty())
						{
							customerToInsert = new Customer();
							posBestTau = listTauCosts.size() - 1;
							customerToInsert = getCustomerByID(listTauCosts.get(posBestTau).getIdElement(), CustomersToVisit);

							if(capacityVehicle >= (requestRoute + customerToInsert.getRequestCustomer()))
							{
								requestRoute += customerToInsert.getRequestCustomer();
								route.getListIdCustomers().add(customerToInsert.getIdCustomer());
								
								if(route.getListIdCustomers().size() >= 6)
									ThreeOpt.toOptimize(route);
								
								listTauCosts.remove(posBestTau);
								deleteElement(customerToInsert.getIdCustomer(), listMetricsCMTByCustomer);
								CustomersToVisit.remove(customerToInsert);
							}
							else
								listTauCosts.remove(posBestTau);
						}	
	
						route.setRequestRoute(requestRoute);
						solution.getListRoutes().add(route);
						
						listCapacities.remove(0);
						isOpen = false;
					} // capacityVehicle = listCapacities.get(0);
				
					if((isOpen) && (!CustomersToVisit.isEmpty()))
					{
						route.setRequestRoute(requestRoute);
						route.setIdDepot(idDepot);
						
						//3opt
					//	if(route.getListIdCustomers().size() >= 6)
						//	ThreeOpt.toOptimize(route);

						solution.getListRoutes().add(route);
					}
					
					//Si quedan clientes y no quedan veh�culos
					if(!CustomersToVisit.isEmpty()) 
					{
						route = new Route();
						double newRequest = 0.0;
						route.setIdDepot(idDepot);
						
						while(!CustomersToVisit.isEmpty())
						{	
							newRequest += CustomersToVisit.get(0).getRequestCustomer();
							route.setRequestRoute(newRequest);
							route.getListIdCustomers().add(CustomersToVisit.get(0).getIdCustomer());
							CustomersToVisit.remove(0);
						}
						
						solution.getListRoutes().add(route);
					}
					
					//Si quedo alguna ruta abierta
					if(isOpen) // optimizar
					{
						route.setRequestRoute(requestRoute);
						route.setIdDepot(idDepot);
						solution.getListRoutes().add(route);
					}
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
					}

					while(!CustomersToVisit.isEmpty())
					{
						listCandidateRoutes = doFirstPhase(CustomersToVisit, idDepot, j, capacityVehicle, countVehicles);
						listRootCustomers = updateCustomersToVisit(listCandidateRoutes, CustomersToVisit);

						while(!listCandidateRoutes.isEmpty())
						{
							listMetricsCMTByCustomer = new ArrayList<ArrayList<Metric>>();
							listMetricsCMTByCustomer = calculateCostCMTByCustomer(idDepot, CustomersToVisit, listCandidateRoutes); 
								
							route = new Route();
							
							index = random.nextInt(listCandidateRoutes.size());
							route = listCandidateRoutes.remove(index);
							
							rootCustomer = new Customer();
							rootCustomer = getCustomerByID(route.getListIdCustomers().get(0).intValue(), listRootCustomers); //***
							requestRoute = rootCustomer.getRequestCustomer();
							listRootCustomers.remove(rootCustomer);
							route.setIdDepot(idDepot);
		
							listTauCosts = new ArrayList<Metric>();
							listTauCosts = calculateTau(listMetricsCMTByCustomer, index);

							while(!listTauCosts.isEmpty())
							{
								customerToInsert = new Customer();
								posBestTau = listTauCosts.size() - 1;
								customerToInsert = getCustomerByID(listTauCosts.get(posBestTau).getIdElement(), CustomersToVisit);
								
								if(capacityVehicle >= (requestRoute + customerToInsert.getRequestCustomer()))
								{
									requestRoute += customerToInsert.getRequestCustomer();
									route.getListIdCustomers().add(customerToInsert.getIdCustomer());
									//route.setIdDepot(idDepot);
									
									if(route.getListIdCustomers().size() >= 6)
										ThreeOpt.toOptimize(route);

									listTauCosts.remove(posBestTau);
									deleteElement(customerToInsert.getIdCustomer(), listMetricsCMTByCustomer);
									CustomersToVisit.remove(customerToInsert);
								}
								else
									listTauCosts.remove(posBestTau);
							}	

							route.setRequestRoute(requestRoute);
							//route.setIdDepot(idDepot);
							solution.getListRoutes().add(route);
						}
					}
				}
				
				break;	
			}
			
			case 4:
			{
                            ArrayList<Integer> listAccessVC = new ArrayList<Integer>();
				while(!CustomersToVisit.isEmpty())
				{	
					boolean isTC = false;
					double capacityTrailer = ((FleetTTRP)Problem.getProblem().getListDepots().get(posDepot).getListFleets().get(0)).getCapacityTrailer();
					double capacityTotal = 0.0;
					
					CustomerType typeCustomer = CustomerType.TC; //ARREGLAR !!!
				
					listCandidateRoutes = doFirstPhase(CustomersToVisit, idDepot, posDepot, capacityVehicle, countVehicles);
					listRootCustomers = updateCustomersToVisit(listCandidateRoutes, CustomersToVisit);
	
					while(!listCandidateRoutes.isEmpty())
					{
						listMetricsCMTByCustomer = new ArrayList<ArrayList<Metric>>();
						listMetricsCMTByCustomer = calculateCostCMTByCustomer(idDepot, CustomersToVisit, listCandidateRoutes);

						route = new Route();
						
						index = random.nextInt(listCandidateRoutes.size());
						route = listCandidateRoutes.remove(index);

						rootCustomer = new Customer();
						rootCustomer = getCustomerByID(route.getListIdCustomers().get(0).intValue(), listRootCustomers);
						requestRoute = rootCustomer.getRequestCustomer();
                                                
                                                // ARREGLAR !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                                                rootCustomer = new CustomerTTRP(rootCustomer.getIdCustomer(), rootCustomer.getRequestCustomer(), rootCustomer.getLocationCustomer(), typeCustomer.ordinal());
						//typeCustomer = ((CustomerTTRP)rootCustomer).getTypeCustomer();	
						listRootCustomers.remove(rootCustomer);
						route.setIdDepot(idDepot);
						
						if(typeCustomer.equals(CustomerType.TC))
							capacityTotal = capacityVehicle;
						else	
							capacityTotal = capacityVehicle + capacityTrailer;

						listTauCosts = new ArrayList<Metric>();
						listTauCosts = calculateTau(listMetricsCMTByCustomer, index);

						while(!listTauCosts.isEmpty())
						{
							customerToInsert = new Customer();
							posBestTau = listTauCosts.size() - 1;
							customerToInsert = getCustomerByID(listTauCosts.get(posBestTau).getIdElement(), CustomersToVisit);

							if(capacityTotal >= (requestRoute + customerToInsert.getRequestCustomer()))
							{
								requestRoute += customerToInsert.getRequestCustomer();
								route.getListIdCustomers().add(customerToInsert.getIdCustomer());
								
								if(route.getListIdCustomers().size() >= 6)
									ThreeOpt.toOptimize(route);

								listTauCosts.remove(posBestTau);
								deleteElement(customerToInsert.getIdCustomer(), listMetricsCMTByCustomer);
								CustomersToVisit.remove(customerToInsert);
							
								if(typeCustomer.equals(CustomerType.VC) && ((CustomerTTRP)customerToInsert).getTypeCustomer().equals(CustomerType.TC))
									isTC = true;
							}
							else
								listTauCosts.remove(posBestTau);
						}

						route.setRequestRoute(requestRoute);

						if(typeCustomer.equals(CustomerType.TC))
							route = new RouteTTRP(route.getListIdCustomers(), route.getRequestRoute(), route.getCostRoute(),
                                                        route.getIdDepot(), listAccessVC, RouteType.PTR);
						else
						{
							if(isTC)
								route = new RouteTTRP(route.getListIdCustomers(), route.getRequestRoute(), route.getCostRoute(),
                                                        route.getIdDepot(), listAccessVC, RouteType.CVR);
							else
								route = new RouteTTRP(route.getListIdCustomers(), route.getRequestRoute(), route.getCostRoute(),
                                                        route.getIdDepot(), listAccessVC, RouteType.PVR);
						}
							
						//route.setIdDepot(idDepot);
						solution.getListRoutes().add(route);
					}
				}
				
				break;
			}
		}
		
		return solution;
	}

	/* M�todo que realiza la primera fase del algoritmo CMT*/
	private ArrayList<Route> doFirstPhase(ArrayList<Customer> CustomersToVisit, int idDepot, int posDepot, double capacityVehicle, int countVehicles){
		ArrayList<Route> listRoutes = new ArrayList<Route>();
		ArrayList<Customer> listCustomers = new ArrayList<Customer>(CustomersToVisit);
		ArrayList<Metric> listCandidateCustomers = null;
		Customer rootCustomer = new Customer();
		Customer customerToInsert = null;
		Route route = new Route();
		double requestRoute = 0.0;
		
		Operator_3opt ThreeOpt = new Operator_3opt();

		rootCustomer = getFirstCustomer(CustomersToVisit, firstCustomerType, idDepot);   
		requestRoute = rootCustomer.getRequestCustomer();
		route.getListIdCustomers().add(rootCustomer.getIdCustomer());
		route.setIdDepot(idDepot);
		listCustomers.remove(rootCustomer);

		switch(Problem.getProblem().getTypeProblem().ordinal())
		{
			case 0: case 2: case 3:
			{
				if(listCustomers.isEmpty())
					listRoutes.add(route);
				else
				{
					while(!listCustomers.isEmpty())
					{
						listCandidateCustomers = new ArrayList<Metric>();
						
						for(int i = 0; i < listCustomers.size(); i++)
						{
							Metric metricCMT = new Metric();
							
							if(capacityVehicle >= (requestRoute + listCustomers.get(i).getRequestCustomer()))
							{
								metricCMT.setIdElement(listCustomers.get(i).getIdCustomer());
								metricCMT.setInsertionCost(calculateCostOfCMT(idDepot, rootCustomer.getIdCustomer(), listCustomers.get(i).getIdCustomer()));
								listCandidateCustomers.add(metricCMT);
							}
						}
						
						AscendentOrdenate(listCandidateCustomers);

						while(!listCandidateCustomers.isEmpty())
						{
							customerToInsert = new Customer();
							customerToInsert = getCustomerByID(listCandidateCustomers.get(0).getIdElement(), listCustomers);
							
							if(capacityVehicle >= (requestRoute + customerToInsert.getRequestCustomer()))
							{
								requestRoute += customerToInsert.getRequestCustomer();
								route.getListIdCustomers().add(customerToInsert.getIdCustomer());
						
								if(route.getListIdCustomers().size() >= 6)
									ThreeOpt.toOptimize(route);
								
								listCandidateCustomers.remove(0);
								listCustomers.remove(customerToInsert);
							}
							else
								listCandidateCustomers.remove(0);
						}
						
						listRoutes.add(route);
						
						if(listCustomers.size() > 0) 
						{
							route = new Route();
							requestRoute = 0.0;
							
							rootCustomer = getFirstCustomer(CustomersToVisit, firstCustomerType, idDepot);   
							requestRoute = rootCustomer.getRequestCustomer();
							route.getListIdCustomers().add(rootCustomer.getIdCustomer());
							route.setIdDepot(idDepot);
							listCustomers.remove(rootCustomer);
							
							if(listCustomers.isEmpty())
								listRoutes.add(route);					
						}
					}
				}
		
				break;
			}
			
			case 1:
			{
				if(listCustomers.isEmpty())
					listRoutes.add(route);
				else
				{
					ArrayList<Double> listCapacities = new ArrayList<Double>(Problem.getProblem().getListCapacities());
					capacityVehicle = listCapacities.get(0);
					
					while((!listCustomers.isEmpty()) && (!listCapacities.isEmpty()))
					{
						listCandidateCustomers = new ArrayList<Metric>();
						
						for(int i = 0; i < listCustomers.size(); i++)
						{
							Metric metricCMT = new Metric();
							
							if(capacityVehicle >= (requestRoute + listCustomers.get(i).getRequestCustomer()))
							{
								metricCMT.setIdElement(listCustomers.get(i).getIdCustomer());
								metricCMT.setInsertionCost(calculateCostOfCMT(idDepot, rootCustomer.getIdCustomer(), listCustomers.get(i).getIdCustomer()));
								listCandidateCustomers.add(metricCMT);
							}
						}
						
						AscendentOrdenate(listCandidateCustomers);

						while(!listCandidateCustomers.isEmpty())
						{
							customerToInsert = new Customer();
							customerToInsert = getCustomerByID(listCandidateCustomers.get(0).getIdElement(), listCustomers);
							
							if(capacityVehicle >= (requestRoute + customerToInsert.getRequestCustomer()))
							{
								requestRoute += customerToInsert.getRequestCustomer();
								route.getListIdCustomers().add(customerToInsert.getIdCustomer());
								route.setIdDepot(idDepot);
						
								if(route.getListIdCustomers().size() >= 6)
									ThreeOpt.toOptimize(route);
								
								listCandidateCustomers.remove(0);
								listCustomers.remove(customerToInsert);
							}
							else
								listCandidateCustomers.remove(0);
						}
						
						listRoutes.add(route);
						listCapacities.remove(0);
						
						if(listCustomers.size() > 0)
						{
							requestRoute = 0.0;
							route = new Route();

							rootCustomer = getFirstCustomer(CustomersToVisit, firstCustomerType, idDepot);  
							requestRoute = rootCustomer.getRequestCustomer();
							route.getListIdCustomers().add(rootCustomer.getIdCustomer());
							route.setIdDepot(Problem.getProblem().getListDepots().get(posDepot).getIdDepot());
							listCustomers.remove(rootCustomer);

							capacityVehicle = listCapacities.get(0);
							
							if(listCustomers.isEmpty())
								listRoutes.add(route);					
						}
					}
				}
					
				break;
			}
			
			case 4:
			{
				double capacityTotal = 0.0;
				double capacityTrailer = ((FleetTTRP)Problem.getProblem().getListDepots().get(posDepot).getListFleets().get(0)).getCapacityTrailer();
				
				CustomerType typeCustomer;
				
				if(listCustomers.isEmpty())
					listRoutes.add(route);
				else
				{
					while(!listCustomers.isEmpty())
					{
						listCandidateCustomers = new ArrayList<Metric>();
						typeCustomer = ((CustomerTTRP)rootCustomer).getTypeCustomer();
						
						if(typeCustomer.equals(CustomerType.TC))
							capacityTotal = capacityVehicle;
						else	
							capacityTotal = capacityVehicle + capacityTrailer;
							
						for(int i = 0; i < listCustomers.size(); i++)
						{
							Metric metricCMT = new Metric();
							
							if(capacityTotal >= (requestRoute + listCustomers.get(i).getRequestCustomer()))
							{
								metricCMT.setIdElement(listCustomers.get(i).getIdCustomer());
								metricCMT.setInsertionCost(calculateCostOfCMT(idDepot, rootCustomer.getIdCustomer(), listCustomers.get(i).getIdCustomer()));
								listCandidateCustomers.add(metricCMT);
							}
						}
				
						AscendentOrdenate(listCandidateCustomers);

						while(!listCandidateCustomers.isEmpty())
						{	
							customerToInsert = new Customer();
							customerToInsert = getCustomerByID(listCandidateCustomers.get(0).getIdElement(), listCustomers); 

							if(capacityTotal >= (requestRoute + customerToInsert.getRequestCustomer()))
							{
								requestRoute += customerToInsert.getRequestCustomer();
								route.getListIdCustomers().add(customerToInsert.getIdCustomer()); //
								route.setIdDepot(Problem.getProblem().getListDepots().get(posDepot).getIdDepot());

								if(route.getListIdCustomers().size() >= 6)
									ThreeOpt.toOptimize(route);
								
								listCandidateCustomers.remove(0);
								listCustomers.remove(customerToInsert);
							}
							else
								listCandidateCustomers.remove(0);
						}
						
						listRoutes.add(route);
						
						if(listCustomers.size() > 0)
						{
							route = new Route();
							requestRoute = 0.0;
							
							rootCustomer = getFirstCustomer(CustomersToVisit, firstCustomerType, idDepot);  
							requestRoute = rootCustomer.getRequestCustomer();
							route.getListIdCustomers().add(rootCustomer.getIdCustomer());
							route.setIdDepot(Problem.getProblem().getListDepots().get(posDepot).getIdDepot());
							listCustomers.remove(rootCustomer);

							if(listCustomers.isEmpty())
								listRoutes.add(route);
						}
					}
				}

				break;
			}
		}
		
		emptyRoutes(listRoutes);
		
		return listRoutes;
	}
	
	/* M�todo que calcula el costo de insertar un cliente en la ruta */
	private double calculateCostOfCMT(int idDepot, int currentElement, int nextElement){
		double costDepotToNext = Problem.getProblem().getCostMatrix().getItem(Problem.getProblem().getPosElement(idDepot), Problem.getProblem().getPosElement(nextElement));
		double costNextToCurrent = Problem.getProblem().getCostMatrix().getItem(Problem.getProblem().getPosElement(nextElement), Problem.getProblem().getPosElement(currentElement));
		
		return (costDepotToNext + (parameterL * costNextToCurrent)); 
	}
	
	/* M�todo que vacia la lista de rutas dejando solo el primer cliente en cada una */
	private void emptyRoutes(ArrayList<Route> listRoutes){
		for(int i = 0; i < listRoutes.size(); i++)
		{
			int j = 1;
			
			while(j < listRoutes.get(i).getListIdCustomers().size())
				listRoutes.get(i).getListIdCustomers().remove(j);
		}
	}
	
	/* M�todo que devuelve en una lista los clientes a eliminar que ya pertenecen a una ruta */
	private ArrayList<Customer> updateCustomersToVisit(ArrayList<Route> listRoutes, ArrayList<Customer> CustomersToVisit){	
		ArrayList<Customer> listRootCustomers = new ArrayList<Customer>();
		
		for(int i = 0; i < listRoutes.size(); i++)
		{
			int j = 0;
			boolean found = false;

			while((j < CustomersToVisit.size()) && (!found))
			{
				if(CustomersToVisit.get(j).getIdCustomer() == listRoutes.get(i).getListIdCustomers().get(0).intValue())
				{
					listRootCustomers.add(CustomersToVisit.remove(j));
					found = true;
				}
				else
					j++;
			}	
		}
		
		return listRootCustomers;
	}
	
	/* M�todo que retorna la lista ordenada con los costos CMT en cada ruta para cada cliente*/
	private ArrayList<ArrayList<Metric>> calculateCostCMTByCustomer(int idDepot, ArrayList<Customer> listCustomers, ArrayList<Route> listRoutes){
		ArrayList<ArrayList<Metric>> listMetricsCMTByCustomer = new ArrayList<ArrayList<Metric>>();
		ArrayList<Metric> listMetricCMT;
			
		for(int i = 0; i < listCustomers.size(); i++)
		{
			listMetricCMT = new ArrayList<Metric>();
			
			for(int j = 0; j < listRoutes.size(); j++)
			{
				Metric metricCMT = new Metric();
				metricCMT.setIdElement(listCustomers.get(i).getIdCustomer());
				metricCMT.setInsertionCost(calculateCostOfCMT(idDepot, listRoutes.get(j).getListIdCustomers().get(0), listCustomers.get(i).getIdCustomer()));
				metricCMT.setIndex(j);
				listMetricCMT.add(metricCMT);
			}
			
			if(listRoutes.size() > 1)
				AscendentOrdenate(listMetricCMT);

			listMetricsCMTByCustomer.add(listMetricCMT);
		}
		
		return listMetricsCMTByCustomer;
	}
	
	/* M�todo que devuelve listado de clientes con el TAU calculado y ordenado*/
	private ArrayList<Metric> calculateTau(ArrayList<ArrayList<Metric>> listMetricsCMTByCustomer, int posRoute){
		ArrayList<Metric> listTauCosts = new ArrayList<Metric>();
		double tauCost;
		double firstCost = 0.0;
		double secondCost = 0.0;

		for(int i = 0; i < listMetricsCMTByCustomer.size(); i++)
		{
			int j = 0;

			if(listMetricsCMTByCustomer.get(i).get(0).getIndex() == posRoute)
			{
				Metric metricCMT = new Metric();
				metricCMT.setIdElement(listMetricsCMTByCustomer.get(i).get(j).getIdElement());

				firstCost = listMetricsCMTByCustomer.get(i).get(j).getInsertionCost();
				
				if(listMetricsCMTByCustomer.get(i).size() > 1)
				{
					secondCost = listMetricsCMTByCustomer.get(i).get(j + 1).getInsertionCost();
					tauCost = secondCost - firstCost;
				}	
				else
					tauCost = firstCost;	

				metricCMT.setInsertionCost(tauCost);

				listTauCosts.add(metricCMT);
			}	
		}
		
		if(listTauCosts.size() > 1)
			AscendentOrdenate(listTauCosts);
		
		return listTauCosts;
	}

	/* M�todo que elimina un cliente de la lista ordenada de los costos */
	private void deleteElement(int idCustomer, ArrayList<ArrayList<Metric>> listMetricsCMTByCustomer){
		boolean deleted = false;
		int i = 0;

		while((i < listMetricsCMTByCustomer.size()) && (!deleted))
		{
			if(listMetricsCMTByCustomer.get(i).get(0).getIdElement() == idCustomer)
			{
				listMetricsCMTByCustomer.remove(i);
				deleted = true;
			}
			else
				i++;
		}
	}
}