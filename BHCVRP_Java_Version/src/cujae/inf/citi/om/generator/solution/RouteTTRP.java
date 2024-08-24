package cujae.inf.citi.om.generator.solution;

import java.util.ArrayList;

import cujae.inf.citi.om.data.CustomerType;
import cujae.inf.citi.om.data.Problem;

/* Clase que modela los datos de una ruta en el TTRP*/

public class RouteTTRP extends Route{

	private RouteType typeRoute;
	private ArrayList<Integer> listAccessVC;

	public RouteTTRP() {
		super();
		this.listAccessVC = new ArrayList<Integer>();
		// TODO Auto-generated constructor stub
	}

	public RouteTTRP(RouteType typeRoute, ArrayList<Integer> listAccessVC) {
		super();
		this.typeRoute = typeRoute;
		this.listAccessVC = listAccessVC;
		// TODO Auto-generated constructor stub
	}
        
        public RouteTTRP(ArrayList<Integer> listIdCustomers, double requestRoute, double costRoute, int idDepot,
                ArrayList<Integer> listAccessVC, RouteType typeRoute){
            super(listIdCustomers, requestRoute, costRoute, idDepot, listAccessVC);
            setListAccessVC(listAccessVC);
            setTypeRoute(typeRoute);
        }

	public RouteType getTypeRoute() {
		return typeRoute;
	}

	public void setTypeRoute(RouteType typeRoute) {
		this.typeRoute = typeRoute;
	}
	
	public void setTypeRoute(int typeRoute) {
		switch(typeRoute)
		{
		 case 0 :
		  {
			  this.typeRoute = RouteType.PTR;
			  break;
		  }
		  case 1:
		  {
			  this.typeRoute = RouteType.PVR;
			  break;
		  }
		  case 2:
		  {
			  this.typeRoute = RouteType.CVR;
			  break;
		  }
		}
	}
	
	public ArrayList<Integer> getListAccessVC() {
		return listAccessVC;
	}

	public void setListAccessVC(ArrayList<Integer> listAccessVC) {
		this.listAccessVC = listAccessVC;
	}
	
	/* M�todo que calcula el costo de una ruta con subtour (CVR) incluyendo los clientes de tipo VC en las sub-rutas*/
	public Double getCostRouteWithSubTour(){
		Double costRoute = 0.0;
		Double requestSubRoute = 0.0;
		Integer customerIni = 0;
		Integer customerNext = null;
		CustomerType typeCustomerIni = null;
		CustomerType typeCustomerNext = null;
		Integer idLastVC = -1;
		boolean vcInSub = false;
		
		int posCustomerIni = -1;
		int posCustomerNext = -1;
		int posCustomerLastVC = 0;

		double capacityVehicle =  Problem.getProblem().getListDepots().get(0).getListFleets().get(0).getCapacityVehicle();	

		customerIni = listIdCustomers.get(0).intValue();
		posCustomerIni = Problem.getProblem().getPosElement(customerIni);
		typeCustomerIni = Problem.getProblem().getTypeByIDCustomer(customerIni);
		listAccessVC.add(0);

		costRoute += Problem.getProblem().getCostMatrix().getItem(Problem.getProblem().getPosElement(idDepot), posCustomerIni);

		for(int i = 1; i < listIdCustomers.size(); i++)
		{
			customerNext = listIdCustomers.get(i).intValue();
			posCustomerNext = Problem.getProblem().getPosElement(customerNext);
			typeCustomerNext = Problem.getProblem().getTypeByIDCustomer(customerNext);

			if(typeCustomerIni.equals(CustomerType.VC) && typeCustomerNext.equals(CustomerType.VC) && !vcInSub) 
			{
				costRoute += Problem.getProblem().getCostMatrix().getItem(posCustomerIni, posCustomerNext);
				listAccessVC.add(0);
			}
			else
			{ 
				if(typeCustomerIni.equals(CustomerType.VC) && typeCustomerNext.equals(CustomerType.TC) && !vcInSub)
				{
					idLastVC = customerIni;
					posCustomerLastVC = posCustomerIni;
					costRoute += Problem.getProblem().getCostMatrix().getItem(posCustomerIni, posCustomerNext);

					requestSubRoute += Problem.getProblem().getRequestByIDCustomer(customerNext);
				}
				else
				{
					if((typeCustomerIni.equals(CustomerType.TC) && typeCustomerNext.equals(CustomerType.TC)) || (typeCustomerIni.equals(CustomerType.VC) && typeCustomerNext.equals(CustomerType.TC) && vcInSub)) //subruta
					{
						requestSubRoute +=  Problem.getProblem().getRequestByIDCustomer(customerNext);

						if(requestSubRoute <= capacityVehicle)
							costRoute += Problem.getProblem().getCostMatrix().getItem(posCustomerIni, posCustomerNext);

						else
						{
							requestSubRoute = Problem.getProblem().getRequestByIDCustomer(customerNext);

							costRoute += Problem.getProblem().getCostMatrix().getItem(posCustomerIni, posCustomerLastVC);
							costRoute += Problem.getProblem().getCostMatrix().getItem(posCustomerLastVC, posCustomerNext);

							vcInSub = false;
						}
					}
					else
					{
						if((typeCustomerIni.equals(CustomerType.TC) && typeCustomerNext.equals(CustomerType.VC)) || (typeCustomerIni.equals(CustomerType.VC) && typeCustomerNext.equals(CustomerType.VC) && vcInSub)) // mantener en la subruta pq cabe o recoger remolque retornar al tour principal
						{
							requestSubRoute +=  Problem.getProblem().getRequestByIDCustomer(customerNext);

							if(requestSubRoute <= capacityVehicle) 
							{
								costRoute += Problem.getProblem().getCostMatrix().getItem(posCustomerIni, posCustomerNext);

								vcInSub = true;
								listAccessVC.add(1);
							}

							else
							{
								requestSubRoute = 0.0;

								costRoute += Problem.getProblem().getCostMatrix().getItem(posCustomerIni, posCustomerLastVC);
								costRoute += Problem.getProblem().getCostMatrix().getItem(posCustomerLastVC, posCustomerNext);

								idLastVC = -1;
								vcInSub = false;
								listAccessVC.add(0);
							}		
						}	
					}	
				}
			}

			customerIni = customerNext;
			posCustomerIni = posCustomerNext;
			typeCustomerIni = typeCustomerNext;
		
		}

		if(idLastVC != -1)
		{
			costRoute += Problem.getProblem().getCostMatrix().getItem(posCustomerIni, posCustomerLastVC);
			customerIni = idLastVC;
			posCustomerIni = posCustomerLastVC;
			idLastVC = -1;
		}
		
		costRoute += Problem.getProblem().getCostMatrix().getItem(posCustomerIni, Problem.getProblem().getPosElement(idDepot));
		setCostRoute(costRoute);
		
		return costRoute;	
	}
}
