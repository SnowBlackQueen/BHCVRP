package cujae.inf.citi.om.data;

/* Clase que modela los datos de un problema VRP*/

import cujae.inf.citi.om.exceptions.DistanceNotAccessibleException;
import cujae.inf.citi.om.exceptions.ItemNotFoundException;
import cujae.inf.citi.om.exceptions.VehicleSpeedException;
import java.util.ArrayList;

//import cujae.inf.citi.om.matrix.NumericMatrix;
import java.util.HashMap;
import cujae.inf.ic.om.matrix.NumericArray;
import cujae.inf.ic.om.matrix.NumericMatrix;

public class Problem {
	
	private ArrayList<Customer> listCustomers;
	private ArrayList<Depot> listDepots;
	private ProblemType typeProblem;
	private NumericMatrix costMatrix;
        private NumericMatrix timeMatrix;
	
	private static Problem problem = null;
	private ArrayList<Double> listCapacities = null;
        private ArrayList<BusStop> listBusesStop;
        private double maximumWalkDistance;
        private float vehicleSpeed = (float) 83.33;
	
	private Problem() {
		super();
		listCustomers = new ArrayList<Customer>();
		listDepots = new ArrayList<Depot>();
                listBusesStop = new ArrayList<BusStop>();
		costMatrix = new NumericMatrix();
                timeMatrix = new NumericMatrix();
	}

	/* M�todo que implementa el Patr�n Singleton*/
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
                  
                  case 5:
                  {
                      this.typeProblem = ProblemType.SBRP;
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
	
        public NumericMatrix getTimeMatrix() {
		return timeMatrix;
	}

	public void setTimeMatrix(NumericMatrix timeMatrix) {
		this.timeMatrix = timeMatrix;
	}
        
	public ArrayList<Double> getListCapacities() {
		return listCapacities;
	}

	public void setListCapacities(ArrayList<Double> listCapacities) {
		this.listCapacities = listCapacities;
	}
        
        public double getMaximumWalkDistance() {
            return maximumWalkDistance;
        }
        
        public void setMaximumWalkDistance(double maximumWalkDistance) throws DistanceNotAccessibleException{
            if (maximumWalkDistance > 0){
                this.maximumWalkDistance = maximumWalkDistance;
            }
            else {
                throw new DistanceNotAccessibleException("La distancia a recorrer no es accesible. Debe ser mayor que 0");
            }  
                
        }
        
        public float getVehicleSpeed(){
            return vehicleSpeed;
        }
        
        public void setVehicleSpeed(float vehicleSpeed) throws VehicleSpeedException{
            if (vehicleSpeed > 0){
                this.vehicleSpeed = vehicleSpeed;
            }
            else {
                throw new VehicleSpeedException("La velocidad del vehículo debe ser mayor que 0");
            }  
        }
        
        public ArrayList<BusStop> getListBusesStop(){
            return listBusesStop;
        }
        
        public void setListBusesStop(ArrayList<BusStop> listBusesStop){
            this.listBusesStop = listBusesStop;
        }

	/*M�todo para obtener la lista de id de los clientes*/
	public ArrayList<Integer> getListIDCustomers(){
		int countCustomers = listCustomers.size();
		ArrayList<Integer> listIDCustomers = new ArrayList<Integer>();
	
		for(int i = 0; i < countCustomers; i++) 
			listIDCustomers.add(listCustomers.get(i).getIdCustomer());

		return listIDCustomers;
	}

	/*M�todo que devuelve la demanda total*/
    public double getTotalRequest(){
		double totalRequest = 0.0;
		int countCustomers = listCustomers.size();
		
		for(int i = 0; i < countCustomers; i++)
			totalRequest += listCustomers.get(i).getRequestCustomer();

		return totalRequest;
	}
        
	/*M�todo que busca un cliente dado su identificador*/
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
	
	/*M�todo que devuelve el tipo de un cliente dado su identificador*/
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
	
	/*M�todo que devuelve la demanda de un cliente dado su identificador*/
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
		
	/*M�todo que dado un id (deposito � cliente) devuelve la posicion*/
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
	
	/*M�todo que dado el id del deposito y del cliente devuelve la posicion*/
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
	
	/*M�todo que devuelve el id del dep�sito correspondiente a un cliente dado*/
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

	/*M�todo que devuelve la demanda de un deposito dado*/
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

	/*M�todo que dice si hay o no capacidad disponible en los dep�sitos*/
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
     
	/*M�todo que devuelve la capacidad total de los veh�culos de MDVRP*/
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
     
    /*M�todo que dado el dep�sito devuelve la lista de clientes asignados*/
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
    
    /* M�todo que llena la lista de capacidades de la flota de veh�culos en FHVRP*/
    public ArrayList<Double> fillListCapacities(int posDepot){ /**md**/
    	listCapacities = new ArrayList<Double>();

    	for(int i = 0; i < listDepots.get(posDepot).getListFleets().size(); i++)
    		for(int j = 0; j < listDepots.get(posDepot).getListFleets().get(i).getCountVehicles(); j++)
    			listCapacities.add(listDepots.get(posDepot).getListFleets().get(i).getCapacityVehicle());
    	
    	return listCapacities;
    }
    
    /* M�todo que llena la lista de capacidades de la flota de veh�culos en FHVRP*/
    public ArrayList<Double> fillListCapacitiesTest(){
    	listCapacities = new ArrayList<Double>();

    	for(int i = 0; i < listDepots.get(0).getListFleets().size(); i++)
    		for(int j = 0; j < listDepots.get(0).getListFleets().get(i).getCountVehicles(); j++)
    			listCapacities.add(listDepots.get(0).getListFleets().get(i).getCapacityVehicle());
    	
    	return listCapacities;
    }
    
	/*M�todo para obtener la lista de los id de los depositos*/
	public ArrayList<Integer> getListIDDepots(){
		int countDepot = listDepots.size();
		ArrayList<Integer> listIDDepots = new ArrayList<Integer>();
	
		for(int i = 0; i < countDepot; i++) 
			listIDDepots.add(listDepots.get(i).getIdDepot());

		return listIDDepots;
	}
	
	/* M�todo que determina si existen clientes que puedan ser asignado al dep�sito */
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
        
        public int getTotalBusesStop(){
            return this.listBusesStop.size();
        }
        
        //Lista de pasajeros asignados dado una parada
        public HashMap<String, ArrayList<String>> customerAssignedByBusStop(String busStop) throws ItemNotFoundException{
            ArrayList<String> passengers = new ArrayList<String>();
            HashMap<String, ArrayList<String>> values = new HashMap<String, ArrayList<String>>();

            int count = 0;

            int busPosition = this.getBusStopPosition(busStop);

            passengers = this.listBusesStop.get(busPosition).getListCustomers();

            for (String p : passengers) {

               // int passenger = this.getPosElement(passengers.get(i));

                //double distance = Math.round(this.passanger_stop_matrix.getItem(passenger, bus_position) * 100.0) / 100.0;

                //Passenger p = this.listPassengers.get(passenger);

                ArrayList<String> data = new ArrayList<String>();

                //data.add(p.getLocationPassenger().getAddress());
                //data.add((Math.round(distance * 100.0) / 100.00) + "");

                data.add(0.00+"");

                values.put(p, data);

            }

            return values;
        }
        
        //Obtener la posicion de una parada dado su identificador
        public int getBusStopPosition(String id) throws ItemNotFoundException {

            int count = 0;
            boolean found = false;

            do {

                if (this.listBusesStop.get(count).getIdBusStop().equalsIgnoreCase(id)) {
                    found = true;
                } else {
                    count++;
                }

            } while (count < this.listBusesStop.size() && !found);

            if (!found) {
                throw new ItemNotFoundException("El vehículo de identificador: " + id + " no existe");
            }

            return count;

        }
        
        //Lista de paradas alcanzables para un pasajero
        public ArrayList<String> alcanzableBusStopForCustomer(int id) {

            ArrayList<String> alcanzableBusStop = new ArrayList<>();

            int passengerPosition = getPosElement(id);

            NumericArray list = this.costMatrix.getRow(passengerPosition);

            for (int i = 0; i < list.getLength(); i++) {

                String bus_stop;

                if (list.getItem(i) != Double.POSITIVE_INFINITY) {

                    bus_stop = this.listBusesStop.get(i).getIdBusStop();

                    alcanzableBusStop.add(bus_stop);

                }

            }//for

            return alcanzableBusStop;

        }
        
        //Comprobar que un pasajero este asignado
        private boolean passengerAssigned(int id) throws ItemNotFoundException {

            int position = this.getPosElement(id);

            boolean found = false;

            int count = 0;

            if (position > -1) {

                do {

                    found = listBusesStop.get(count++).getListCustomers().contains(id);

                } while (!found && count < listBusesStop.size());

            }

            return found;

        }
        
        public int getTotalBusStopWithCustomersAssigned() {

            int count = 0;

            for (BusStop b : listBusesStop) {
                if (!b.getListCustomers().isEmpty()) {
                    count++;
                }
            }

            return count;

        }

    public int getPosElement(BusStop busStop) {
        int i = 0;
        boolean found = false;
        int posElement = -1;
        int countCustomers = listCustomers.size();
        int countDepots = listDepots.size();
        int countBusStops = listBusesStop.size();
        int idElement = Integer.parseInt(busStop.getIdBusStop());
        
        // Buscar en la lista de depósitos
        while (i < countDepots && !found) {
            if (listDepots.get(i).getIdDepot() == idElement) {
                posElement = i + countBusStops;
                found = true;
            } else {
                i++;
            }
        }

        i = 0;
        // Buscar en la lista de paradas de autobús
        while (i < countBusStops && !found) {
            if (listBusesStop.get(i).getIdBusStop().equals(busStop.getIdBusStop())) {
                posElement = i;
                found = true;
            } else {
                i++;
            }
        }  
        
        return posElement;        
    } 
        
}
