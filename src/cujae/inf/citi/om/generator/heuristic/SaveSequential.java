package cujae.inf.citi.om.generator.heuristic;

import java.util.ArrayList;
import java.util.Random;

import cujae.inf.citi.om.data.Customer;
import cujae.inf.citi.om.data.FleetTTRP;
import cujae.inf.citi.om.data.Problem;
import cujae.inf.citi.om.data.ProblemType;
import cujae.inf.citi.om.generator.postoptimization.Operator_3opt;
import cujae.inf.citi.om.generator.solution.*;
import cujae.inf.citi.om.matrix.NumericMatrix;
import cujae.inf.citi.om.matrix.RowCol;

/* Clase que modela la heurística de Ahorro en su versión Secuencial */

public class SaveSequential extends Save {

	public SaveSequential() {
		super();
		// TODO Auto-generated constructor stub
	}

	/* Método encargado de generar la solución */
	
	public Solution getSolutionInicial() {
		if(parameterShape <= 0)
			parameterShape = 1;
		
		Solution solution = new Solution();
		ArrayList<Customer> CustomersToVisit = null;
		int idDepot = -1;
		int posDepot = -1;

		if(Problem.getProblem().getTypeProblem().equals(ProblemType.CVRP) || Problem.getProblem().getTypeProblem().equals(ProblemType.HFVRP) || Problem.getProblem().getTypeProblem().equals(ProblemType.OVRP) || Problem.getProblem().getTypeProblem().equals(ProblemType.TTRP))
		{
			CustomersToVisit = new ArrayList<Customer>(Problem.getProblem().getListCustomers());
			posDepot = 0;
		}	
		else
		{
			int i = 0;
			boolean found = false;
			
			while((i < Problem.getProblem().getListDepots().size()) && (!found))
			{
				CustomersToVisit = new ArrayList<Customer>(Problem.getProblem().getCustomersAssignedByIDDepot(Problem.getProblem().getListDepots().get(i).getIdDepot()));
			
				if(!CustomersToVisit.isEmpty())
				{
					found = true;
					posDepot = i;
				}	
				else
					i++;
			}	
		}
		
		double capacityVehicle = Problem.getProblem().getListDepots().get(posDepot).getListFleets().get(0).getCapacityVehicle();
//		double countVehicles = Problem.getProblem().getListDepots().get(posDepot).getListFleets().get(0).getCountVehicles();

		Operator_3opt ThreeOpt = new Operator_3opt();
		
		ArrayList<Route> listRoutes = new ArrayList<Route>();
		listRoutes = createInitialRoutes(CustomersToVisit);
		//inspect ?
		
		int cantCustomers = CustomersToVisit.size();
		NumericMatrix saveMatrix = new NumericMatrix(cantCustomers, cantCustomers);
		saveMatrix = fillSaveMatrix(idDepot, CustomersToVisit);

		Random random = new Random ();
		int index = -1;
				
		int extInic = -1;
		int extEnd = -1;
		int noExtreme = -1;
		boolean existSave;
		
		switch(Problem.getProblem().getTypeProblem().ordinal())
		{
			case 0: case 3:
			{
				while(!listRoutes.isEmpty()) 
				{
					index = random.nextInt(listRoutes.size());
					Route currentRoute = listRoutes.remove(index);
					existSave = true;

					extInic = currentRoute.getListIdCustomers().get(0);
					extEnd = currentRoute.getListIdCustomers().get(currentRoute.getListIdCustomers().size() - 1);	

					while(existSave)
					{
						RowCol maxSaveInic = null;
						RowCol maxSaveEnd = null;
						RowCol maxSave = null;
						boolean positionSave = false; 

						maxSaveInic = saveMatrix.indexBiggerValue(Problem.getProblem().getPosElement(extInic), 0, Problem.getProblem().getPosElement(extInic), (cantCustomers - 1));
						
						if(extInic != extEnd)
							maxSaveEnd = saveMatrix.indexBiggerValue(Problem.getProblem().getPosElement(extEnd), 0, Problem.getProblem().getPosElement(extEnd), (cantCustomers - 1));
						else
							maxSaveEnd = maxSaveInic;

						if(saveMatrix.getItem(maxSaveInic.getRow(), maxSaveInic.getCol()) > saveMatrix.getItem(maxSaveEnd.getRow(), maxSaveEnd.getCol()))
							maxSave = maxSaveInic;
						else
						{
							maxSave = maxSaveEnd;
							positionSave = true;
						}

						if(currentRoute.getRequestRoute() == capacityVehicle)
						{
							saveMatrix.fillValue(Problem.getProblem().getPosElement(extInic), 0, Problem.getProblem().getPosElement(extInic), (cantCustomers - 1), Double.NEGATIVE_INFINITY);
							saveMatrix.fillValue(0, Problem.getProblem().getPosElement(extInic), (cantCustomers - 1), Problem.getProblem().getPosElement(extInic), Double.NEGATIVE_INFINITY);

							saveMatrix.fillValue(Problem.getProblem().getPosElement(extEnd), 0, Problem.getProblem().getPosElement(extEnd), (cantCustomers - 1), Double.NEGATIVE_INFINITY);
							saveMatrix.fillValue(0, Problem.getProblem().getPosElement(extEnd), (cantCustomers - 1), Problem.getProblem().getPosElement(extEnd), Double.NEGATIVE_INFINITY);

							existSave = false;
							continue;
						}

						Double saveValue = saveMatrix.getItem(maxSave.getRow(), maxSave.getCol());

						if(saveValue.isInfinite())
						{
							existSave = false;
							continue;
						}	
						else
						{
							int posRoute = getPositionRoute(listRoutes, CustomersToVisit.get(maxSave.getCol()).getIdCustomer());
							Route saveRoute = listRoutes.get(posRoute);

							int isFactible = checkingMerge(currentRoute, saveRoute, capacityVehicle, 0.0, positionSave);

							if(isFactible != -1)
							{
								if(positionSave)
								{
									currentRoute.getListIdCustomers().addAll(saveRoute.getListIdCustomers());
									extEnd = CustomersToVisit.get(maxSave.getCol()).getIdCustomer();
								}
								else
								{
									currentRoute.getListIdCustomers().addAll(0, saveRoute.getListIdCustomers());
									extInic = CustomersToVisit.get(maxSave.getCol()).getIdCustomer();
								}

								currentRoute.setIdDepot(idDepot);
								currentRoute.setRequestRoute((currentRoute.getRequestRoute() + saveRoute.getRequestRoute()));
								listRoutes.remove(saveRoute);

								if(currentRoute.getListIdCustomers().size() > 2)
								{
									noExtreme = maxSave.getRow();
									saveMatrix.fillValue(noExtreme, 0, noExtreme, (cantCustomers - 1), Double.NEGATIVE_INFINITY);
									saveMatrix.fillValue(0, noExtreme, (cantCustomers - 1), noExtreme, Double.NEGATIVE_INFINITY);

									saveMatrix.setItem(Problem.getProblem().getPosElement(extInic), Problem.getProblem().getPosElement(extEnd), Double.NEGATIVE_INFINITY); 
									saveMatrix.setItem(Problem.getProblem().getPosElement(extEnd), Problem.getProblem().getPosElement(extInic), Double.NEGATIVE_INFINITY); 
								}
							}	

							saveMatrix.setItem(maxSave.getRow(), maxSave.getCol(), Double.NEGATIVE_INFINITY); 
							saveMatrix.setItem(maxSave.getCol(), maxSave.getRow(), Double.NEGATIVE_INFINITY);
						}
					}
					//3opt
					if(currentRoute.getListIdCustomers().size() >= 6)
						ThreeOpt.toOptimize(currentRoute);
					
					solution.getListRoutes().add(currentRoute);
				}
				break;
			}
			case 1:
			{
				ArrayList<Double> listCapacities = new ArrayList<Double>(Problem.getProblem().getListCapacities());
				
				while((!listRoutes.isEmpty()) && (!listCapacities.isEmpty())) 
				{
					index = random.nextInt(listRoutes.size());
					Route currentRoute = listRoutes.remove(index);
					existSave = true;

					extInic = currentRoute.getListIdCustomers().get(0);
					extEnd = currentRoute.getListIdCustomers().get(currentRoute.getListIdCustomers().size() - 1);	

					while(existSave)
					{
						RowCol maxSaveInic = null;
						RowCol maxSaveEnd = null;
						RowCol maxSave = null;
						boolean positionSave = false;

						maxSaveInic = saveMatrix.indexBiggerValue(Problem.getProblem().getPosElement(extInic), 0, Problem.getProblem().getPosElement(extInic), (cantCustomers - 1));

						if(extInic != extEnd)
							maxSaveEnd = saveMatrix.indexBiggerValue(Problem.getProblem().getPosElement(extEnd), 0, Problem.getProblem().getPosElement(extEnd), (cantCustomers - 1));
						else
							maxSaveEnd = maxSaveInic;

						if(saveMatrix.getItem(maxSaveInic.getRow(), maxSaveInic.getCol()) > saveMatrix.getItem(maxSaveEnd.getRow(), maxSaveEnd.getCol()))
							maxSave = maxSaveInic;
						else
						{
							maxSave = maxSaveEnd;
							positionSave = true;
						}

						if(currentRoute.getRequestRoute() == listCapacities.get(0)) // capacityVehicle
						{
							saveMatrix.fillValue(Problem.getProblem().getPosElement(extInic), 0, Problem.getProblem().getPosElement(extInic), (cantCustomers - 1), Double.NEGATIVE_INFINITY);
							saveMatrix.fillValue(0, Problem.getProblem().getPosElement(extInic), (cantCustomers - 1), Problem.getProblem().getPosElement(extInic), Double.NEGATIVE_INFINITY);

							saveMatrix.fillValue(Problem.getProblem().getPosElement(extEnd), 0, Problem.getProblem().getPosElement(extEnd), (cantCustomers - 1), Double.NEGATIVE_INFINITY);
							saveMatrix.fillValue(0, Problem.getProblem().getPosElement(extEnd), (cantCustomers - 1), Problem.getProblem().getPosElement(extEnd), Double.NEGATIVE_INFINITY);

							existSave = false;
							continue;
						}

						Double saveValue = saveMatrix.getItem(maxSave.getRow(), maxSave.getCol());

						if(saveValue.isInfinite())
						{
							existSave = false;
							continue;
						}	
						else
						{
							int posRoute = getPositionRoute(listRoutes, CustomersToVisit.get(maxSave.getCol()).getIdCustomer());
							Route saveRoute = listRoutes.get(posRoute);

							int isFactible = checkingMerge(currentRoute, saveRoute, listCapacities.get(0), 0.0, positionSave);

							if(isFactible != -1)
							{
								if(positionSave)
								{
									currentRoute.getListIdCustomers().addAll(saveRoute.getListIdCustomers());
									extEnd = CustomersToVisit.get(maxSave.getCol()).getIdCustomer();
								}
								else
								{
									currentRoute.getListIdCustomers().addAll(0, saveRoute.getListIdCustomers());
									extInic = CustomersToVisit.get(maxSave.getCol()).getIdCustomer();
								}

								currentRoute.setIdDepot(idDepot);
								currentRoute.setRequestRoute((currentRoute.getRequestRoute() + saveRoute.getRequestRoute()));
								listRoutes.remove(saveRoute);

								if(currentRoute.getListIdCustomers().size() > 2)
								{
									noExtreme = maxSave.getRow();
									saveMatrix.fillValue(noExtreme, 0, noExtreme, (cantCustomers - 1), Double.NEGATIVE_INFINITY);
									saveMatrix.fillValue(0, noExtreme, (cantCustomers - 1), noExtreme, Double.NEGATIVE_INFINITY);

									saveMatrix.setItem(Problem.getProblem().getPosElement(extInic), Problem.getProblem().getPosElement(extEnd), Double.NEGATIVE_INFINITY); 
									saveMatrix.setItem(Problem.getProblem().getPosElement(extEnd), Problem.getProblem().getPosElement(extInic), Double.NEGATIVE_INFINITY); 
								}
							}	

							saveMatrix.setItem(maxSave.getRow(), maxSave.getCol(), Double.NEGATIVE_INFINITY); 
							saveMatrix.setItem(maxSave.getCol(), maxSave.getRow(), Double.NEGATIVE_INFINITY);
						}
					}

					if(currentRoute.getListIdCustomers().size() >= 6)
						ThreeOpt.toOptimize(currentRoute);
					
					solution.getListRoutes().add(currentRoute);
					listCapacities.remove(0); /***/
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
						
						capacityVehicle = Problem.getProblem().getListDepots().get(j).getListFleets().get(0).getCapacityVehicle();
					
						if(!CustomersToVisit.isEmpty())
						{
							listRoutes = createInitialRoutes(CustomersToVisit);//xq aqui??
							//inspect ?
							cantCustomers = CustomersToVisit.size();
							saveMatrix = new NumericMatrix(cantCustomers, cantCustomers);
							saveMatrix = fillSaveMatrix(idDepot, CustomersToVisit);
						}	
					}
					
					while(!listRoutes.isEmpty()) 
					{
						index = random.nextInt(listRoutes.size());
						Route currentRoute = listRoutes.remove(index);
						existSave = true;

						extInic = currentRoute.getListIdCustomers().get(0);
						extEnd = currentRoute.getListIdCustomers().get(currentRoute.getListIdCustomers().size() - 1);	

						while(existSave)
						{
							RowCol maxSaveInic = null;
							RowCol maxSaveEnd = null;
							RowCol maxSave = null;
							boolean positionSave = false;

							maxSaveInic = saveMatrix.indexBiggerValue(Problem.getProblem().getPosElementByIDDepot(idDepot, extInic), 0, Problem.getProblem().getPosElementByIDDepot(idDepot, extInic), (cantCustomers - 1));
							if(extInic != extEnd)
								maxSaveEnd = saveMatrix.indexBiggerValue(Problem.getProblem().getPosElementByIDDepot(idDepot, extEnd), 0, Problem.getProblem().getPosElementByIDDepot(idDepot, extEnd), (cantCustomers - 1));
							else
								maxSaveEnd = maxSaveInic;

							if(saveMatrix.getItem(maxSaveInic.getRow(), maxSaveInic.getCol()) > saveMatrix.getItem(maxSaveEnd.getRow(), maxSaveEnd.getCol()))
								maxSave = maxSaveInic;
							else
							{
								maxSave = maxSaveEnd;
								positionSave = true;
							}

							if(currentRoute.getRequestRoute() == capacityVehicle) //here
							{
								saveMatrix.fillValue(Problem.getProblem().getPosElementByIDDepot(idDepot, extInic), 0, Problem.getProblem().getPosElementByIDDepot(idDepot, extInic), (cantCustomers - 1), Double.NEGATIVE_INFINITY);
								saveMatrix.fillValue(0, Problem.getProblem().getPosElementByIDDepot(idDepot, extInic), (cantCustomers - 1), Problem.getProblem().getPosElementByIDDepot(idDepot, extInic), Double.NEGATIVE_INFINITY);

								saveMatrix.fillValue(Problem.getProblem().getPosElementByIDDepot(idDepot, extEnd), 0, Problem.getProblem().getPosElementByIDDepot(idDepot, extEnd), (cantCustomers - 1), Double.NEGATIVE_INFINITY);
								saveMatrix.fillValue(0, Problem.getProblem().getPosElementByIDDepot(idDepot, extEnd), (cantCustomers - 1), Problem.getProblem().getPosElementByIDDepot(idDepot, extEnd), Double.NEGATIVE_INFINITY);

								existSave = false;
								continue;
							}

							Double saveValue = saveMatrix.getItem(maxSave.getRow(), maxSave.getCol());

							if(saveValue.isInfinite())
							{
								existSave = false;
								continue;
							}	
							else
							{
								int posRoute = getPositionRoute(listRoutes, CustomersToVisit.get(maxSave.getCol()).getIdCustomer());
								Route saveRoute = listRoutes.get(posRoute);

								int isFactible = checkingMerge(currentRoute, saveRoute, capacityVehicle, 0.0, positionSave);

								if(isFactible != -1)
								{
									if(positionSave)
									{
										currentRoute.getListIdCustomers().addAll(saveRoute.getListIdCustomers());
										extEnd = CustomersToVisit.get(maxSave.getCol()).getIdCustomer();
									}
									else
									{
										currentRoute.getListIdCustomers().addAll(0, saveRoute.getListIdCustomers());
										extInic = CustomersToVisit.get(maxSave.getCol()).getIdCustomer();
									}

									currentRoute.setIdDepot(idDepot);
									currentRoute.setRequestRoute((currentRoute.getRequestRoute() + saveRoute.getRequestRoute()));
									listRoutes.remove(saveRoute);

									if(currentRoute.getListIdCustomers().size() > 2) //here
									{
										noExtreme = maxSave.getRow();
										saveMatrix.fillValue(noExtreme, 0, noExtreme, (cantCustomers - 1), Double.NEGATIVE_INFINITY);
										saveMatrix.fillValue(0, noExtreme, (cantCustomers - 1), noExtreme, Double.NEGATIVE_INFINITY);

										saveMatrix.setItem(Problem.getProblem().getPosElementByIDDepot(idDepot, extInic), Problem.getProblem().getPosElementByIDDepot(idDepot, extEnd), Double.NEGATIVE_INFINITY); 
										saveMatrix.setItem(Problem.getProblem().getPosElementByIDDepot(idDepot, extEnd), Problem.getProblem().getPosElementByIDDepot(idDepot, extInic), Double.NEGATIVE_INFINITY); 
									}
								}	

								saveMatrix.setItem(maxSave.getRow(), maxSave.getCol(), Double.NEGATIVE_INFINITY); 
								saveMatrix.setItem(maxSave.getCol(), maxSave.getRow(), Double.NEGATIVE_INFINITY);
							}
						}

						if(currentRoute.getListIdCustomers().size() >= 6)
							ThreeOpt.toOptimize(currentRoute);
						
						solution.getListRoutes().add(currentRoute);
					}
				}
				break;
			}
			case 4:
			{
				double capacityTrailer = ((FleetTTRP)Problem.getProblem().getListDepots().get(posDepot).getListFleets().get(0)).getCapacityTrailer(); 

				while(!listRoutes.isEmpty())
				{
					index = random.nextInt(listRoutes.size());
					Route currentRoute = listRoutes.remove(index);

					existSave = true;

					extInic = currentRoute.getListIdCustomers().get(0);
					extEnd = currentRoute.getListIdCustomers().get(currentRoute.getListIdCustomers().size() - 1);	

					while(existSave)
					{
						RowCol maxSaveInic = null;
						RowCol maxSaveEnd = null;
						RowCol maxSave = null;
						boolean positionSave = false;

						maxSaveInic = saveMatrix.indexBiggerValue(Problem.getProblem().getPosElement(extInic), 0, Problem.getProblem().getPosElement(extInic), (cantCustomers - 1));

						if(extInic != extEnd)
							maxSaveEnd = saveMatrix.indexBiggerValue(Problem.getProblem().getPosElement(extEnd), 0, Problem.getProblem().getPosElement(extEnd), (cantCustomers - 1));
						else
							maxSaveEnd = maxSaveInic;

						if(saveMatrix.getItem(maxSaveInic.getRow(), maxSaveInic.getCol()) > saveMatrix.getItem(maxSaveEnd.getRow(), maxSaveEnd.getCol()))
							maxSave = maxSaveInic;
						else
						{
							maxSave = maxSaveEnd;
							positionSave = true;
						}

						if((((RouteTTRP)currentRoute).getTypeRoute().ordinal() == 0 && ((RouteTTRP)currentRoute).getRequestRoute() == capacityVehicle) || ((((RouteTTRP)currentRoute).getTypeRoute().ordinal() == 1 || ((RouteTTRP)currentRoute).getTypeRoute().ordinal() == 2) && ((RouteTTRP)currentRoute).getRequestRoute() == (capacityVehicle + capacityTrailer)))
						{
							saveMatrix.fillValue(Problem.getProblem().getPosElement(extInic), 0, Problem.getProblem().getPosElement(extInic), (cantCustomers - 1), Double.NEGATIVE_INFINITY);
							saveMatrix.fillValue(0, Problem.getProblem().getPosElement(extInic), (cantCustomers - 1), Problem.getProblem().getPosElement(extInic), Double.NEGATIVE_INFINITY);

							saveMatrix.fillValue(Problem.getProblem().getPosElement(extEnd), 0, Problem.getProblem().getPosElement(extEnd), (cantCustomers - 1), Double.NEGATIVE_INFINITY);
							saveMatrix.fillValue(0, Problem.getProblem().getPosElement(extEnd), (cantCustomers - 1), Problem.getProblem().getPosElement(extEnd), Double.NEGATIVE_INFINITY);

							existSave = false;
							continue;
						}

						Double saveValue = saveMatrix.getItem(maxSave.getRow(), maxSave.getCol());
						
						if(saveValue.isInfinite())
						{
							existSave = false;
							continue;
						}
						else
						{
							int posRoute = getPositionRoute(listRoutes, CustomersToVisit.get(maxSave.getCol()).getIdCustomer());
							Route saveRoute = listRoutes.get(posRoute);

							int isFactible = checkingMerge(currentRoute, saveRoute, capacityVehicle, capacityTrailer, positionSave);

							if(isFactible != -1)
							{
								RouteType typeRoute = null;

								if(positionSave)
								{
									currentRoute.getListIdCustomers().addAll(saveRoute.getListIdCustomers());
									extEnd = CustomersToVisit.get(maxSave.getCol()).getIdCustomer();

									if(((RouteTTRP)currentRoute).getTypeRoute().equals(((RouteTTRP)saveRoute).getTypeRoute()))
										typeRoute = ((RouteTTRP)currentRoute).getTypeRoute();
									else
										if(!((RouteTTRP)currentRoute).getTypeRoute().equals(RouteType.PTR))
											typeRoute = RouteType.CVR;
										else
											typeRoute = ((RouteTTRP)currentRoute).getTypeRoute();
								}
								else
								{
									currentRoute.getListIdCustomers().addAll(0, saveRoute.getListIdCustomers());
									extInic = CustomersToVisit.get(maxSave.getCol()).getIdCustomer();

									if(((RouteTTRP)saveRoute).getTypeRoute().ordinal() == ((RouteTTRP)currentRoute).getTypeRoute().ordinal())
										typeRoute = ((RouteTTRP)saveRoute).getTypeRoute();
									else
										if(((RouteTTRP)saveRoute).getTypeRoute().ordinal() > 0)
											typeRoute = RouteType.CVR;	
										else
											typeRoute = ((RouteTTRP)saveRoute).getTypeRoute();
								}

								((RouteTTRP)currentRoute).setTypeRoute(typeRoute);
								currentRoute.setIdDepot(idDepot);
								currentRoute.setRequestRoute((currentRoute.getRequestRoute() + saveRoute.getRequestRoute()));
								listRoutes.remove(saveRoute);

								if(currentRoute.getListIdCustomers().size() > 2)
								{
									noExtreme = maxSave.getRow();
									saveMatrix.fillValue(noExtreme, 0, noExtreme, (cantCustomers - 1), Double.NEGATIVE_INFINITY);
									saveMatrix.fillValue(0, noExtreme, (cantCustomers - 1), noExtreme, Double.NEGATIVE_INFINITY);

									saveMatrix.setItem(Problem.getProblem().getPosElement(extInic), Problem.getProblem().getPosElement(extEnd), Double.NEGATIVE_INFINITY); 
									saveMatrix.setItem(Problem.getProblem().getPosElement(extEnd), Problem.getProblem().getPosElement(extInic), Double.NEGATIVE_INFINITY);
								}
							}

							saveMatrix.setItem(maxSave.getRow(), maxSave.getCol(), Double.NEGATIVE_INFINITY); 
							saveMatrix.setItem(maxSave.getCol(), maxSave.getRow(),Double.NEGATIVE_INFINITY);
						}
					}
					
					/*if(currentRoute.getListIdCustomer().size() >= 6)
						stepOptimizacion.stepOptimizacion(currentRoute);*/
					
					solution.getListRoutes().add(currentRoute);
				}	
				break;
			}
		}
		return solution;
	}

	/* Metodo que verifica si se pueden unir dos rutas */
	public int checkingMerge(Route currentRoute, Route saveRoute, double capacityTruck, double capacityTrailer, boolean posSave){
		int join = 0;
		
		RouteType typeRouteIni = null;
		double requestTotal = currentRoute.getRequestRoute() + saveRoute.getRequestRoute();
		 
		if(posSave) //fin
			typeRouteIni = ((RouteTTRP)currentRoute).getTypeRoute();
		else
			typeRouteIni = ((RouteTTRP)saveRoute).getTypeRoute();	
	
		if(typeRouteIni.equals(RouteType.PTR))
			if(requestTotal > capacityTruck)
				join = -1;
		else
			if((typeRouteIni.equals(RouteType.PVR)) || (typeRouteIni.equals(RouteType.CVR)))	
				if(requestTotal > (capacityTruck + capacityTrailer))
					join = -1;
		
		return join;
	}
}
