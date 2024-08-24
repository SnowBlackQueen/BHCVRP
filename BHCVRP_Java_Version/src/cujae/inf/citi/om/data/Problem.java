package cujae.inf.citi.om.data;

/* Clase que modela los datos de un problema VRP*/

import java.util.ArrayList;

import cujae.inf.citi.om.matrix.NumericMatrix;

public class Problem {
	
	private ArrayList<Customer> listCustomers;
	private ArrayList<Depot> listDepots;
	private ProblemType typeProblem;
	private NumericMatrix costMatrix;
	
	private static Problem problem = null;
	private ArrayList<Double> listCapacities = null;
	
	private Problem() {
		super();
		listCustomers = new ArrayList<Customer>();
		listDepots = new ArrayList<Depot>();
		costMatrix = new NumericMatrix();
	}

	/* Método que implementa el Patrón Singleton*/
	public static Problem getProblem () {
		if (problem == null) {
			problem = new Problem();
		}
		return problem;
	}
	
	public ArrayList<Customer> getListCustomers() {
		return listCustomers;
	}

	public void setListCustomers(ArrayList<Customer> listCustomers) {
		this.listCustomers = listCustomers;
	}

	public ArrayList<Depot> getListDepots() {
		return listDepots;
	}

	public void setListDepots(ArrayList<Depot> listDepots) {
		this.listDepots = listDepots;
	}

	public ProblemType getTypeProblem() {
		return typeProblem;
	}

	public void setTypeProblem(ProblemType typeProblem) {
		this.typeProblem = typeProblem;
	}

	public void setTypeProblem(int typeProblem) {
		switch(typeProblem)
		{
		 case 0 :
		  {
			  this.typeProblem = ProblemType.CVRP;
			  break;
		  }
		  
		  case 1:
		  {
			  this.typeProblem = ProblemType.HFVRP;
			  break;
		  }
		  
		  case 2:
		  {
			  this.typeProblem = ProblemType.MDVRP;
			  break;
		  }
		  
		  case 3:
		  {
			  this.typeProblem = ProblemType.OVRP;
			  break;
		  }
		  
		  case 4:
		  {
			  this.typeProblem = ProblemType.TTRP;
			  break;
		  }
		}			
	}
	
	public NumericMatrix getCostMatrix() {
		return costMatrix;
	}

	public void setCostMatrix(NumericMatrix costMatrix) {
		this.costMatrix = costMatrix;
	}
	
	public ArrayList<Double> getListCapacities() {
		return listCapacities;
	}

	public void setListCapacities(ArrayList<Double> listCapacities) {
		this.listCapacities = listCapacities;
	}

	/*Método para obtener la lista de id de los clientes*/
	public ArrayList<Integer> getListIDCustomers(){
		int countCustomers = listCustomers.size();
		ArrayList<Integer> listIDCustomers = new ArrayList<Integer>();
	
		for(int i = 0; i < countCustomers; i++) 
			listIDCustomers.add(listCustomers.get(i).getIdCustomer());

		return listIDCustomers;
	}

	/*Método que devuelve la demanda total*/
    public double getTotalRequest(){
		double totalRequest = 0.0;
		int countCustomers = listCustomers.size();
		
		for(int i = 0; i < countCustomers; i++)
			totalRequest += listCustomers.get(i).getRequestCustomer();

		return totalRequest;
	}
        
	/*Método que busca un cliente dado su identificador*/
	public Customer getCustomerByIDCustomer(int idCustomer){
		Customer customer = null;
		int i = 0;
		boolean found = false;
		int countCustomers = listCustomers.size();
		
		while((i < countCustomers) && (!found))
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
	
	/*Método que devuelve el tipo de un cliente dado su identificador*/
	public CustomerType getTypeByIDCustomer(int idCustomer){
		CustomerType typeCustomer = null;
		int i = 0;
		boolean found = false;
		int countCustomers = listCustomers.size();
		
		while((i < countCustomers) && (!found))
		{
			if(listCustomers.get(i).getIdCustomer() == idCustomer)
			{
				typeCustomer = ((CustomerTTRP)listCustomers.get(i)).getTypeCustomer();
				found = true;
			}
			else
				i++;
		}
		
		return typeCustomer;
	}
	
	/*Método que devuelve la demanda de un cliente dado su identificador*/
	public double getRequestByIDCustomer(int idCustomer){
		double requestCustomer = 0.0;
		int i = 0;
		boolean found = false;
		int countCustomers = listCustomers.size();
		
		while((i < countCustomers) && (!found))
		{
			if(listCustomers.get(i).getIdCustomer() == idCustomer)
			{
				requestCustomer = listCustomers.get(i).getRequestCustomer();
				found = true;
			}
			else
				i++;
		}
		
		return requestCustomer;
	}
	
	public ArrayList<Double> getListRequestCustomers(){
		ArrayList<Double> listRequestCustomers = new ArrayList<Double>();
		
		for(int i = 0; i < listCustomers.size(); i++)
			listRequestCustomers.add(listCustomers.get(i).getRequestCustomer());
		
		return listRequestCustomers;
	}
	
	public ArrayList<Integer> getListCountVehicles(){
		ArrayList<Integer> listCountVehicles = new ArrayList<Integer>();
		
		for(int i = 0; i < listDepots.size(); i++)
			listCountVehicles.add(listDepots.get(i).getListFleets().get(0).getCountVehicles());
		
		return listCountVehicles;
	}
	
	public ArrayList<Double> getListCapacityVehicles(){
		ArrayList<Double> listCapacityVehicles = new ArrayList<Double>();
		
		for(int i = 0; i < listDepots.size(); i++)
			listCapacityVehicles.add(listDepots.get(i).getListFleets().get(0).getCapacityVehicle());
		
		return listCapacityVehicles;
	}
		
	/*Método que dado un id (deposito ó cliente) devuelve la posicion*/
	public int getPosElement(int idElement){
		int i = 0;
		boolean found = false;
		int posElement = -1;
		int countCustomers = listCustomers.size();
		int countDepots = listDepots.size();
		
		while ((i < countDepots) && (!found)) 
		{
			if (listDepots.get(i).getIdDepot() == idElement) 
			{
				posElement = i + countCustomers;
				found = true;
			} 
			else
				i++;
		}

		i = 0;
		while ((i < countCustomers) && (!found)) 
		{
			if (listCustomers.get(i).getIdCustomer() == idElement) 
			{
				posElement = i;
				found = true;
			} 
			else
				i++;
		}
		
		return posElement;
	}
	
	/*Método que dado el id del deposito y del cliente devuelve la posicion*/
	public int getPosElementByIDDepot(int idDepot, int idCustomer){
		boolean found = false;
		int posElement = -1;
		int i = 0;
		int countDepots = listDepots.size();
		
		while((i < countDepots) && (!found)) {

			if (listDepots.get(i).getIdDepot() == idDepot){

				int j = 0;
				int countAssignedCustomers = ((DepotMDVRP)listDepots.get(i)).getListAssignedCustomers().size();
				
				while ((j < countAssignedCustomers) && (!found)) {
					if (((DepotMDVRP)listDepots.get(i)).getListAssignedCustomers().get(j) == idCustomer) {
						posElement = j;
						found = true;
					} 
					else
						j++;
				}
			}
			else
				i++;
		}
		
		return posElement;
	}
	
	/*Método que devuelve el id del depósito correspondiente a un cliente dado*/
	public int getIDDepotByIDCustomer(int idCustomer){
		boolean found = false;
		int idDepot = -1;
		int countDepots = listDepots.size();
		int i = 0;
		
		while((i < countDepots) && (!found)) 
		{
			int j = 0;
			int countAssignedCustomers = ((DepotMDVRP)listDepots.get(i)).getListAssignedCustomers().size();
			
			while ((j < countAssignedCustomers) && (!found)) 
			{
				if (((DepotMDVRP)listDepots.get(i)).getListAssignedCustomers().get(j).intValue() == idCustomer) 
				{
					idDepot = listDepots.get(i).getIdDepot();
					found = true;
				} 
				else 
					j++;
			}
			i++;
		}
		
		return idDepot;
	}

	/*Método que devuelve la demanda de un deposito dado*/
	public double currentRequestByDepot(int posDepot) {    
		double currentRequest = 0.0;
		int idCustomer = -1;
		int countCustomers = listCustomers.size();
		int countAssignedCustomers = ((DepotMDVRP)listDepots.get(posDepot)).getListAssignedCustomers().size();

		for (int i = 0; i < countAssignedCustomers; i++) 
		{
			int j = 0;
			boolean found = false;
			idCustomer = ((DepotMDVRP)listDepots.get(posDepot)).getListAssignedCustomers().get(i).intValue();
		
			while ((j < countCustomers) && (!found)) 
			{
				if (idCustomer == listCustomers.get(j).getIdCustomer()) 
				{
					currentRequest += listCustomers.get(j).getRequestCustomer();
					found = true;
				}
				j++;
			}
		}
		
		return currentRequest;
	}

	/*Método que dice si hay o no capacidad disponible en los depósitos*/
    public boolean existCapacityInSomeDepot() {   
    	boolean exist = false;
        double currentRequest = 0.0;
        double totalCapacity = getTotalCapacity();
        int countDepots = listDepots.size();
        
        for (int i = 0; i < countDepots; i++)
            currentRequest += currentRequestByDepot(i);
        
        if (currentRequest == totalCapacity)
            exist = true;
   
        return exist;
    }
     
	/*Método que devuelve la capacidad total de los vehículos de MDVRP*/
	public double getTotalCapacity(){
		double totalCapacity = 0.0; 
		int countDepots = listDepots.size();
		
		for (int i = 0; i < countDepots; i++) 
		{	
			int countFleets = listDepots.get(i).getListFleets().size();
			
			for (int j = 0; j < countFleets; j++)
			{
				totalCapacity += listDepots.get(i).getListFleets().get(j).getCapacityVehicle() * listDepots.get(i).getListFleets().get(j).getCountVehicles();
				
				if(typeProblem.equals(ProblemType.TTRP))
					totalCapacity += ((FleetTTRP)listDepots.get(i).getListFleets().get(j)).getCapacityTrailer() * ((FleetTTRP)listDepots.get(i).getListFleets().get(j)).getCountTrailers();
			}
		}
		
		return totalCapacity;
	}
     
    /*Método que dado el depósito devuelve la lista de clientes asignados*/
    public ArrayList<Customer> getCustomersAssignedByIDDepot(int idDepot){
    	ArrayList<Customer> listCustomersAssigned = new ArrayList<Customer>();
    	int countCustomers = listCustomers.size();
    	int posDepot = getPosElement(idDepot) - countCustomers;
    	int countAssignedCustomers = ((DepotMDVRP)listDepots.get(posDepot)).getListAssignedCustomers().size();

    	for(int i = 0; i < countAssignedCustomers; i++)
    	{
    		int j = 0;
    		boolean found = false;

    		while((j < countCustomers) && (!found))
    		{

    			if(((DepotMDVRP)listDepots.get(posDepot)).getListAssignedCustomers().get(i).intValue() == listCustomers.get(j).getIdCustomer())
    			{
    				listCustomersAssigned.add(listCustomers.get(j));
    				found = true;
    			}
    			else
    				j++;
    		}
    	}
    	
    	return listCustomersAssigned;
    }
    
    /* Método que llena la lista de capacidades de la flota de vehículos en FHVRP*/
    public ArrayList<Double> fillListCapacities(int posDepot){ /**md**/
    	listCapacities = new ArrayList<Double>();

    	for(int i = 0; i < listDepots.get(posDepot).getListFleets().size(); i++)
    		for(int j = 0; j < listDepots.get(posDepot).getListFleets().get(i).getCountVehicles(); j++)
    			listCapacities.add(listDepots.get(posDepot).getListFleets().get(i).getCapacityVehicle());
    	
    	return listCapacities;
    }
    
    /* Método que llena la lista de capacidades de la flota de vehículos en FHVRP*/
    public ArrayList<Double> fillListCapacitiesTest(){
    	listCapacities = new ArrayList<Double>();

    	for(int i = 0; i < listDepots.get(0).getListFleets().size(); i++)
    		for(int j = 0; j < listDepots.get(0).getListFleets().get(i).getCountVehicles(); j++)
    			listCapacities.add(listDepots.get(0).getListFleets().get(i).getCapacityVehicle());
    	
    	return listCapacities;
    }
    
	/*Método para obtener la lista de los id de los depositos*/
	public ArrayList<Integer> getListIDDepots(){
		int countDepot = listDepots.size();
		ArrayList<Integer> listIDDepots = new ArrayList<Integer>();
	
		for(int i = 0; i < countDepot; i++) 
			listIDDepots.add(listDepots.get(i).getIdDepot());

		return listIDDepots;
	}
	
	/* Método que determina si existen clientes que puedan ser asignado al depósito */
	public boolean isFullDepot(ArrayList<Customer> listCustomers, int posDepot){
		boolean isFull = false;
		double capacityTotal = (listDepots.get(posDepot).getListFleets().get(0).getCapacityVehicle() * listDepots.get(posDepot).getListFleets().get(0).getCountVehicles());
		double requestDepot = currentRequestByDepot(posDepot);
		
		double idealRequest = capacityTotal - requestDepot;

		if(idealRequest != 0)
		{
			int i = 0;

			while((i < listCustomers.size()) && (!isFull)){

				if(listCustomers.get(i).getRequestCustomer() <= idealRequest)
					isFull = true;
				else
					i++;
			}
		}	
		
		return isFull;
	}
}
