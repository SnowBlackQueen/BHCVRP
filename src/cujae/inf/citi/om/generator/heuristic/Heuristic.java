package cujae.inf.citi.om.generator.heuristic;

import java.util.ArrayList;
import java.util.Random;

import cujae.inf.citi.om.data.Customer;
import cujae.inf.citi.om.data.Problem;
import cujae.inf.citi.om.data.ProblemType;
import cujae.inf.citi.om.generator.solution.Solution;
import cujae.inf.citi.om.matrix.RowCol;

/* Clase abstracta que modela una heurística de construcción*/

public abstract class Heuristic {
	
	/* Método abstracto encargado de generar la solución*/
	public abstract Solution getSolutionInicial();
	 
	/* Método que busca un cliente por su identificador*/
	protected Customer getCustomerByID(int idCustomer, ArrayList<Customer> listCustomers){
		int i = 0;
		boolean found = false;
		Customer customer = new Customer();
		
		while((i < listCustomers.size()) && (!found))
		{
			if(listCustomers.get(i).getIdCustomer() == idCustomer)
			{
				customer = listCustomers.get(i);
				found = true;
			}
			else
			 i++;
		}
		return customer;
	}
	
	protected void AscendentOrdenate(ArrayList<Metric> listWithOutOrder){
		double minorInsertionCost;
		Metric minorMetric;
		int referencePos;

		for(int i = 0; i < listWithOutOrder.size(); i++)
		{
			minorInsertionCost = listWithOutOrder.get(i).getInsertionCost();
			minorMetric = listWithOutOrder.get(i);
			referencePos = i;
	
			Metric currentMetric = new Metric();
			int currentPos = -1;
			
			for (int j = (i + 1); j < listWithOutOrder.size(); j++) 
			{
				if ((listWithOutOrder.get(j).getInsertionCost()) < minorInsertionCost)
				{
					minorInsertionCost = listWithOutOrder.get(j).getInsertionCost();
					currentMetric = listWithOutOrder.get(j);
					currentPos = j;
				}
			}
			
			if(currentPos != -1)
			{
				listWithOutOrder.set(referencePos, currentMetric);
				listWithOutOrder.set(currentPos, minorMetric);	
			}
		}
	}
	
	protected void AscendentOrdenate(ArrayList<Double> listDistances, ArrayList<Customer> listNN){
		Double minorDistance;
		Customer customerNN;
		int referencePos;

		for(int i = 0; i < listDistances.size(); i++)
		{
			minorDistance = listDistances.get(i);
			customerNN = listNN.get(i);
			referencePos = i;

			Double currentDistance = 0.0;
			Customer currentCustomer = new Customer();
			int currentPos = -1;

			for(int j = (i + 1); j < listDistances.size(); j++)
			{
				if(minorDistance > listDistances.get(j))
				{
					currentDistance = listDistances.get(j);
					currentCustomer = listNN.get(j);
					currentPos = j;
				}
			}
			
			if(currentPos != -1)
			{
				listDistances.set(referencePos, currentDistance);
				listDistances.set(currentPos, minorDistance);

				listNN.set(referencePos, currentCustomer);
				listNN.set(currentPos, customerNN);	
			}
		}
	}
	
	/* Método que devuelve el primer cliente a insertar en la ruta cuando es MDVRP*/	
	private Customer selectFirstCustomerInMDVRP(ArrayList<Customer> CustomersToVisit, FirstCustomerType firstCustomerType, int posMatrixDepot){
		Customer selectedCustomer = null;
		int currentIndex = -1;
		double currentCost = 0.0;
		
		selectedCustomer = CustomersToVisit.get(0);
		int bestIndex = Problem.getProblem().getPosElement(selectedCustomer.getIdCustomer());
		double bestCost = Problem.getProblem().getCostMatrix().getItem(posMatrixDepot, bestIndex);
	
		for(int i = 1; i < CustomersToVisit.size(); i++)
		{
			currentIndex = Problem.getProblem().getPosElement(CustomersToVisit.get(i).getIdCustomer());
			currentCost = Problem.getProblem().getCostMatrix().getItem(posMatrixDepot, currentIndex);

			if(firstCustomerType.equals(FirstCustomerType.FurthestCustomer))
			{
				if(currentCost > bestCost)
				{
					bestCost = currentCost;
					bestIndex = currentIndex;
					selectedCustomer = CustomersToVisit.get(i);	
				}
			}
			else
			{
				if(firstCustomerType.equals(FirstCustomerType.NearestCustomer))
				{
					if(currentCost < bestCost)
					{
						bestCost = currentCost;
						bestIndex = currentIndex;
						selectedCustomer = CustomersToVisit.get(i);
					}	
				}
			}
		}

		return selectedCustomer;
	}
	

	/* Método que devuelve el primer cliente a insertar en la ruta*/	
	protected Customer getFirstCustomer(ArrayList<Customer> CustomersToVisit, FirstCustomerType firstCustomerType, int idDepot){ 
		Random random = new Random ();
		Customer firstCustomer = null;
		int index = -1;
		int posMatrixDepot = -1;
		RowCol rc = new RowCol();
		
		switch(firstCustomerType.ordinal())
		{
			case 2:
			{
				index = random.nextInt(CustomersToVisit.size());
				firstCustomer = CustomersToVisit.get(index);

				break;
			}
			default:
			{
				posMatrixDepot = Problem.getProblem().getPosElement(idDepot);

				if(Problem.getProblem().getTypeProblem().equals(ProblemType.MDVRP))
					firstCustomer = selectFirstCustomerInMDVRP(CustomersToVisit, firstCustomerType, posMatrixDepot);
				else
				{
					if(firstCustomerType.equals(FirstCustomerType.NearestCustomer))
						rc = Problem.getProblem().getCostMatrix().indexLowerValue(posMatrixDepot, 0, posMatrixDepot, (CustomersToVisit.size() - 1)); 
					else
						if(firstCustomerType.equals(FirstCustomerType.FurthestCustomer))
							rc = Problem.getProblem().getCostMatrix().indexBiggerValue(posMatrixDepot, 0, posMatrixDepot, (CustomersToVisit.size() - 1));
					
					index = rc.getCol();
					firstCustomer = CustomersToVisit.get(index);
				}
			}
		}
		
		return firstCustomer;
	}
}
