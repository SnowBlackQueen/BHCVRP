package cujae.inf.citi.om.generator.heuristic;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.Random;

import cujae.inf.citi.om.data.Customer;
import cujae.inf.citi.om.data.CustomerTTRP;
import cujae.inf.citi.om.data.CustomerType;
import cujae.inf.citi.om.data.DepotMDVRP;
import cujae.inf.citi.om.data.FleetTTRP;
import cujae.inf.citi.om.data.Problem;
import cujae.inf.citi.om.data.ProblemType;
import cujae.inf.citi.om.generator.solution.*;

public class Sweep extends Heuristic{

	public Sweep() {
		super();
		// TODO Auto-generated constructor stub
	}

	@Override
	public Solution getSolutionInicial() {
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
		
		Random random = new Random ();
		int index = -1;
		
		Customer customer = new Customer();
		Route route = new Route();
		double requestRoute = 0.0;
		
		bubbleMethod(CustomersToVisit); 

		index = random.nextInt(CustomersToVisit.size());
		customer = CustomersToVisit.get(index);
		requestRoute = customer.getRequestCustomer();
		route.getListIdCustomers().add(customer.getIdCustomer());
		CustomersToVisit.remove(customer);

		switch(Problem.getProblem().getTypeProblem().ordinal())
		{
			case 0: case 3:
			{
				while(!CustomersToVisit.isEmpty() && (countVehicles > 0))
				{
					if(index == CustomersToVisit.size()) 
						index = 0;
					
					customer = CustomersToVisit.get(index);
			
					if(capacityVehicle >= (requestRoute + customer.getRequestCustomer()))
					{
						requestRoute += customer.getRequestCustomer();
						route.getListIdCustomers().add(customer.getIdCustomer());
						CustomersToVisit.remove(customer);
					}
					else
					{
						route.setRequestRoute(requestRoute);
						route.setIdDepot(idDepot);
						solution.getListRoutes().add(route);
						
						route = null;
						--countVehicles;

						if(countVehicles > 0)
						{
							route = new Route();
							
							requestRoute = customer.getRequestCustomer();
							route.getListIdCustomers().add(customer.getIdCustomer());
							CustomersToVisit.remove(customer);
						}
					}
				}
				
				if(route != null)
				{
					route.setRequestRoute(requestRoute);
					route.setIdDepot(idDepot);
					solution.getListRoutes().add(route);
				}
				
				if(!CustomersToVisit.isEmpty())
				{
					route = new Route();
					requestRoute = 0.0;
					
					while(!CustomersToVisit.isEmpty())
					{
						int j = 0;
						boolean found = false;	
						
						requestRoute = solution.getListRoutes().get(j).getRequestRoute();

						while((j < solution.getListRoutes().size()) && (!found))
						{	
							if(capacityVehicle >= (requestRoute + customer.getRequestCustomer()))
							{
								solution.getListRoutes().get(j).setRequestRoute(requestRoute + customer.getRequestCustomer());
								solution.getListRoutes().get(j).getListIdCustomers().add(customer.getIdCustomer());
								CustomersToVisit.remove(customer);
								
								found = true;
							}
							else
							{
								j++;	
								requestRoute = solution.getListRoutes().get(j).getRequestRoute();
							}	
						}

						if(!found)
						{
							route.getListIdCustomers().add(customer.getIdCustomer());
							route.setRequestRoute(route.getRequestRoute() + customer.getRequestCustomer());
							CustomersToVisit.remove(customer);
						}
						
						if(!CustomersToVisit.isEmpty())
						{
							if(index == CustomersToVisit.size())
								index = 0;
							
							customer = CustomersToVisit.get(index);
						}	
					}
					
					if(!route.getListIdCustomers().isEmpty())
					{
						route.setIdDepot(idDepot);
						solution.getListRoutes().add(route);
					}
				}
				
				break;
			}
			
			case 1:
			{
				ArrayList<Double> listCapacities = new ArrayList<Double>(Problem.getProblem().getListCapacities());
				capacityVehicle = listCapacities.get(0);
				boolean isOpen = true;
	
				while((!CustomersToVisit.isEmpty()) && (!listCapacities.isEmpty()))
				{
					if(index == CustomersToVisit.size()) 
						index = 0;
					
					customer = CustomersToVisit.get(index);
					
					if(capacityVehicle >= (requestRoute + customer.getRequestCustomer()))
					{
						requestRoute += customer.getRequestCustomer();
						route.getListIdCustomers().add(customer.getIdCustomer());
						CustomersToVisit.remove(customer);
					}
					else
					{
						route.setRequestRoute(requestRoute);
						route.setIdDepot(idDepot);
						solution.getListRoutes().add(route);
						
						isOpen = false;
						listCapacities.remove(0);
						
						if(!listCapacities.isEmpty())
						{
							route = new Route();
							
							requestRoute = customer.getRequestCustomer();
							route.getListIdCustomers().add(customer.getIdCustomer());
							CustomersToVisit.remove(customer);
							
							isOpen = true;
							capacityVehicle = listCapacities.get(0);
						}
					}
				}
				
				if(isOpen)
				{
					route.setRequestRoute(requestRoute);
					route.setIdDepot(idDepot);
					solution.getListRoutes().add(route);
				}
				
				if(CustomersToVisit.size() > 0)
				{
					route = new Route();
					requestRoute = 0.0;
					
					listCapacities = new ArrayList<Double>(Problem.getProblem().getListCapacities());
					Iterator<Double> iteratorCapVehicle = listCapacities.iterator();

					while(!CustomersToVisit.isEmpty())
					{
						int j = 0;
						boolean found = false;	
						
						requestRoute = solution.getListRoutes().get(j).getRequestRoute();

						while((iteratorCapVehicle.hasNext()) && (!found))
						{	
							if(iteratorCapVehicle.next() >= (requestRoute + customer.getRequestCustomer()))
							{
								solution.getListRoutes().get(j).setRequestRoute(requestRoute + customer.getRequestCustomer());
								solution.getListRoutes().get(j).getListIdCustomers().add(customer.getIdCustomer());
								CustomersToVisit.remove(customer);
								
								found = true;
							}
							else
							{
								j++;	
								requestRoute = solution.getListRoutes().get(j).getRequestRoute();
							}	
						}
						
						if(!found)
						{
							route.getListIdCustomers().add(customer.getIdCustomer());
							route.setRequestRoute(route.getRequestRoute() + customer.getRequestCustomer());
							CustomersToVisit.remove(customer);
						}

						if(!CustomersToVisit.isEmpty())
						{
							if(index == CustomersToVisit.size())
								index = 0;
							
							customer = CustomersToVisit.get(index);
						}
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
						
						if(!CustomersToVisit.isEmpty())
						{
							bubbleMethod(CustomersToVisit);
						
							route = new Route();
							
							index = random.nextInt(CustomersToVisit.size());
							customer = CustomersToVisit.get(index);
							requestRoute = customer.getRequestCustomer();
							route.getListIdCustomers().add(customer.getIdCustomer());
							CustomersToVisit.remove(customer);
						}
						else
							continue;
					}
					
					while((!CustomersToVisit.isEmpty()) && (countVehicles > 0))	
					{	
						if(index == CustomersToVisit.size()) 
							index = 0;
						
						customer = CustomersToVisit.get(index);
				
						if(capacityVehicle >= (requestRoute + customer.getRequestCustomer()))
						{
							requestRoute += customer.getRequestCustomer();
							route.getListIdCustomers().add(customer.getIdCustomer());
							CustomersToVisit.remove(customer);
						}
						else
						{
							route.setRequestRoute(requestRoute);
							route.setIdDepot(idDepot);
							solution.getListRoutes().add(route);
							
							route = null;
							--countVehicles;
							
							if(countVehicles > 0)
							{
								route = new Route();
								
								requestRoute = customer.getRequestCustomer();
								route.getListIdCustomers().add(customer.getIdCustomer());
								CustomersToVisit.remove(customer);
							}
						}
					}
					
					if(route != null)
					{
						route.setRequestRoute(requestRoute);
						route.setIdDepot(idDepot);
						solution.getListRoutes().add(route);
					}

					if(!CustomersToVisit.isEmpty())
					{
						route = new Route();
						requestRoute = 0.0;

						while(!CustomersToVisit.isEmpty())
						{
							int k = 0;
							boolean found = false;	
							
							requestRoute = solution.getListRoutes().get(k).getRequestRoute();

							while((k < solution.getListRoutes().size()) && (!found))
							{	
								if((requestRoute + customer.getRequestCustomer()) <= capacityVehicle)
								{
									solution.getListRoutes().get(k).setRequestRoute(requestRoute + customer.getRequestCustomer());
									solution.getListRoutes().get(k).getListIdCustomers().add(customer.getIdCustomer());
									CustomersToVisit.remove(customer);
									
									found = true;
								}
								else
								{
									k++;	
									requestRoute = solution.getListRoutes().get(k).getRequestRoute();
								}		
							}

							if(!found)
							{
								route.getListIdCustomers().add(customer.getIdCustomer());
								route.setRequestRoute(route.getRequestRoute() + customer.getRequestCustomer());
								CustomersToVisit.remove(customer);
							}

							if(!CustomersToVisit.isEmpty())
							{
								if(index == CustomersToVisit.size())
									index = 0;
								
								customer = CustomersToVisit.get(index);
							}							
						}
						
						if(!route.getListIdCustomers().isEmpty())
						{
							route.setIdDepot(idDepot);
							solution.getListRoutes().add(route);
						}
					}
				}
				
				break;
			}
			
			case 4:
			{
				boolean isTC = false;
				double capacityTrailer = ((FleetTTRP)Problem.getProblem().getListDepots().get(posDepot).getListFleets().get(0)).getCapacityTrailer();
			
				CustomerType typeCustomer = ((CustomerTTRP)customer).getTypeCustomer();
				
				while(!CustomersToVisit.isEmpty())
				{
					if(index == CustomersToVisit.size()) 
						index = 0;

					customer = CustomersToVisit.get(index);

					if(typeCustomer.equals(CustomerType.TC))
					{
						if(capacityVehicle >= (requestRoute + customer.getRequestCustomer()))
						{	
							requestRoute += customer.getRequestCustomer();
							route.getListIdCustomers().add(customer.getIdCustomer());
							CustomersToVisit.remove(customer);	
						}
						else
						{
							route.setRequestRoute(requestRoute);
							((RouteTTRP)route).setTypeRoute(RouteType.PTR);
							route.setIdDepot(idDepot);
							solution.getListRoutes().add(route);
							
							route = new Route();
							
							requestRoute = customer.getRequestCustomer();
							typeCustomer = ((CustomerTTRP)customer).getTypeCustomer();
							route.getListIdCustomers().add(customer.getIdCustomer());
							CustomersToVisit.remove(customer);
						}
					}
					else
					{
						if(((CustomerTTRP)customer).getTypeCustomer().equals(CustomerType.TC))
							isTC = true;

						if((capacityVehicle+ capacityTrailer) >= (requestRoute + customer.getRequestCustomer()))
						{	
							requestRoute += customer.getRequestCustomer();
							route.getListIdCustomers().add(customer.getIdCustomer());
							CustomersToVisit.remove(customer);	
						}
						else
						{
							route.setRequestRoute(requestRoute);
							
							if(isTC)
								((RouteTTRP)route).setTypeRoute(RouteType.CVR);
							else
								((RouteTTRP)route).setTypeRoute(RouteType.PVR);
							
							route.setIdDepot(idDepot);
							solution.getListRoutes().add(route);
							isTC = false;
							
							route = new Route();
							requestRoute = customer.getRequestCustomer();
							typeCustomer = ((CustomerTTRP)customer).getTypeCustomer();
							route.getListIdCustomers().add(customer.getIdCustomer());
							CustomersToVisit.remove(customer);
						}
					}
				}

				route.setRequestRoute(requestRoute);
				
				if(typeCustomer.equals(CustomerType.TC))
					((RouteTTRP)route).setTypeRoute(RouteType.PTR);
				else
				{
					if(isTC)
						((RouteTTRP)route).setTypeRoute(RouteType.CVR);
					else
						((RouteTTRP)route).setTypeRoute(RouteType.PVR);
				}
				
				route.setIdDepot(idDepot);
				solution.getListRoutes().add(route);

				break;
			}
		}
		
		return solution;
	}

	/*Método de ordenamiento Burbujas utilizando las coordenadas polares*/
	private void bubbleMethod(ArrayList<Customer> listCustomers){
		double valueThetaOne = 0.0;
		double valueRhoOne = 0.0;
		double valueThetaTwo = 0.0;
		double valueRhoTwo = 0.0;
		
		for(int i = 0; i < (listCustomers.size() - 1); i++)
		{
			valueThetaOne = listCustomers.get(i).getLocationCustomer().getPolarTheta();
			
			for(int j = (i + 1); j < listCustomers.size(); j++)
			{
				Customer customer = new Customer();

				valueThetaTwo = listCustomers.get(j).getLocationCustomer().getPolarTheta();
					
				if(valueThetaOne > valueThetaTwo)
				{
					customer = listCustomers.get(i);
					listCustomers.set(i, listCustomers.get(j));
					listCustomers.set(j, customer);
					
					valueThetaOne = valueThetaTwo;
				}
				else
				{
					if(valueThetaOne == valueThetaTwo)
					{
						valueRhoOne = listCustomers.get(i).getLocationCustomer().getPolarRho();
						valueRhoTwo = listCustomers.get(j).getLocationCustomer().getPolarRho();
						
						if(valueRhoOne > valueRhoTwo)
						{
							customer = listCustomers.get(i);
							listCustomers.set(i, listCustomers.get(j));
							listCustomers.set(j, customer);
							
							valueThetaOne = valueThetaTwo;
						}
					}
				}
			}
		}
	}
//	/*Método de ordenamiento Quicksort utilizando las coordenadas polares*/
//	private void quicksortMethod(ArrayList<Customer> listCustomers, int initial, int end){  
//		Customer pivote = listCustomers.get(initial);
//		
//		int i = initial;
//		int j = end; 
//		Customer customer = new Customer();
//
//		while(i < j)
//		{           
//			while((listCustomers.get(i).getLocationCustomer().getPolarTheta() < pivote.getLocationCustomer().getPolarTheta()) || (listCustomers.get(i).getLocationCustomer().getPolarTheta() == pivote.getLocationCustomer().getPolarTheta() && listCustomers.get(i).getLocationCustomer().getPolarRho() <= pivote.getLocationCustomer().getPolarRho()) && (i < j))
//				i++;
//
//			while((listCustomers.get(j).getLocationCustomer().getPolarTheta() > pivote.getLocationCustomer().getPolarTheta()) || (listCustomers.get(j).getLocationCustomer().getPolarTheta() == pivote.getLocationCustomer().getPolarTheta() && listCustomers.get(j).getLocationCustomer().getPolarRho() > pivote.getLocationCustomer().getPolarRho()))
//				j--;       				
//
//			if(i < j) 
//			{                                    
//				customer = listCustomers.get(i);
//				listCustomers.set(i, listCustomers.get(j));
//				listCustomers.set(j, customer); 
//			} 
//		} 
//
//		listCustomers.set(initial, listCustomers.get(j));
//		listCustomers.set(j, pivote);
//
//		if(initial < (j - 1))
//			quicksortMethod(listCustomers, initial, (j - 1));
//		
//		if((j + 1) < end)
//			quicksortMethod(listCustomers, (j + 1), end);
//	}
//	
//	private void mergesortMethod(ArrayList<Customer> listCustomers, int initial, int end){	
//		if (initial < end)
//		{
//			int middle = ((initial + end))/2; 
//			mergesortMethod(listCustomers, initial, middle); 
//			mergesortMethod(listCustomers, (middle + 1), end);
//			merge(listCustomers, initial, middle, end);	
//		}
//	}
//	
//	private  void merge(ArrayList<Customer> listCustomers, int initial, int middle, int end){
//		ArrayList<Customer> customers = new ArrayList<Customer>(listCustomers.size());
//		int i, j, k;
//		
//		for (int l = 0; l < listCustomers.size(); l++) 
//			customers.add(null);
//
//		for (i = initial; i <= end; i++)
//			customers.set(i, listCustomers.get(i));
//							
//		i = initial;
//		j = middle + 1; 
//		k = initial;
//		
//		while ((i <= middle) && (j <= end))
//		{
//			if(customers.get(i).getLocationCustomer().getPolarTheta() <= customers.get(j).getLocationCustomer().getPolarTheta())
//				listCustomers.set(k++, customers.get(i++));
//			else
//				listCustomers.set(k++, customers.get(j++));
//		}
//		
//		while (i <= middle) 
//			listCustomers.set(k++, customers.get(i++));
//	}
}

