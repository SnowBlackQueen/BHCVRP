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

/* Clase que modela la heurística del Vecino más Cercano con RLC*/

public class NearestNeighborWithRLC extends Heuristic{

	public static int sizeRCL = 1;
	
	public NearestNeighborWithRLC() {
		super();
		// TODO Auto-generated constructor stub
	}

	@Override
	public Solution getSolutionInicial() {
		if(sizeRCL == 0)
			sizeRCL = 1;
		
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
		
		Customer customer = new Customer();
		Route route = new Route();
		double requestRoute = 0.0;
		
		customer = getNNCustomer(CustomersToVisit, idDepot);
		requestRoute = customer.getRequestCustomer();
		route.getListIdCustomers().add(customer.getIdCustomer());
		CustomersToVisit.remove(customer);

		switch(Problem.getProblem().getTypeProblem().ordinal())
		{
			case 0: case 3:
			{
				while((!CustomersToVisit.isEmpty()) && (countVehicles > 0))
				{
					customer = getNNCustomer(CustomersToVisit, customer.getIdCustomer());
					
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
							customer = getNNCustomer(CustomersToVisit, customer.getIdCustomer());
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
					customer = getNNCustomer(CustomersToVisit, customer.getIdCustomer());
						
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
				
				if(!CustomersToVisit.isEmpty())
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
							customer = getNNCustomer(CustomersToVisit, customer.getIdCustomer());
					}
					
					if(!route.getListIdCustomers().isEmpty())
					{
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
	
						if(!CustomersToVisit.isEmpty())
						{
							route = new Route();

							customer = getNNCustomer(CustomersToVisit, idDepot);
							requestRoute = customer.getRequestCustomer();
							route.getListIdCustomers().add(customer.getIdCustomer());
							CustomersToVisit.remove(customer);
						}
						else
							continue;
					}

					while((!CustomersToVisit.isEmpty()) && (countVehicles > 0))
					{
						customer = getNNCustomer(CustomersToVisit, customer.getIdCustomer());
						
						if(capacityVehicle >= (requestRoute + customer.getRequestCustomer()))
						{
							route.getListIdCustomers().add(customer.getIdCustomer());
							requestRoute += customer.getRequestCustomer();
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
								if(capacityVehicle >= (requestRoute + customer.getRequestCustomer()))
								{
									solution.getListRoutes().get(k).setRequestRoute(requestRoute + customer.getRequestCustomer());
									solution.getListRoutes().get(k).getListIdCustomers().add(customer.getIdCustomer());
									CustomersToVisit.remove(customer);
									
									found = true;
								}
								else
								{
//									k++;	
//									requestRoute = solution.getListRoutes().get(k).getRequestRoute();
									
									k++;
									if(k != solution.getListRoutes().size())
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
								customer = getNNCustomer(CustomersToVisit, customer.getIdCustomer());
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
					customer = getNNCustomer(CustomersToVisit, customer.getIdCustomer());

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

						if((capacityVehicle + capacityTrailer) >= (requestRoute + customer.getRequestCustomer()))
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
	
	/* Método que devuelve el cliente más cercano al cliente referencia*/
	private Customer getNNCustomer(ArrayList<Customer> listCustomers, int reference){
		Customer customer = new Customer();
		int RLC = -1;
		
		if(listCustomers.size() == 1)
			customer = listCustomers.get(0);
		else
		{
			ArrayList<Customer> listNN = getListNN(listCustomers, reference);
			ArrayList<Customer> listRCL = new ArrayList<Customer>();
			
			RLC = Math.min(sizeRCL, listCustomers.size());
			
			for(int i = 0; i < RLC; i++)	
				listRCL.add(listNN.get(i));		

			Random random = new Random();
			int index = random.nextInt(RLC);	
			customer = listRCL.remove(index);
		}
		
		return customer;
	}

	/* Método que devuelve la lista de vecinos más cercanos */
	private ArrayList<Customer> getListNN(ArrayList<Customer> listCustomers, int reference){
		ArrayList<Double> listDistances = new ArrayList<Double>();
		ArrayList<Customer> listNN = new ArrayList<Customer>();
		double refDistance = 0.0;
		
		for (int i = 0 ; i < listCustomers.size(); i++)
		{
			refDistance = Problem.getProblem().getCostMatrix().getItem(Problem.getProblem().getPosElement(reference), Problem.getProblem().getPosElement(listCustomers.get(i).getIdCustomer()));
			listDistances.add(refDistance);
			listNN.add(listCustomers.get(i));
		}
		
		AscendentOrdenate(listDistances, listNN);

		return listNN;
	}
}
