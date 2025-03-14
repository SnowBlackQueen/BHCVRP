/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package cujae.inf.citi.om.data;

import java.util.ArrayList;
import java.util.stream.Collectors;

/**
 *
 * @author nanda
 */

//Clase que modela los datos de una parada en un SBRP.

public class BusStop {
    private String idBusStop;
    private Location locationBusStop;
    private int capacityBusStop;
    private ArrayList<String> listCustomers;
    
    public BusStop(){
        super();
    }
    
    public BusStop(String idBusStop, int capacity, Location locationBus) {
        setIdBusStop(idBusStop);
        setLocationBusStop(locationBus);
        setCapacityBusStop(capacity);

        this.listCustomers = new ArrayList<String>();
    }
    
    public BusStop(int idBusStop, int capacity, Location locationBus, ArrayList<Integer> listCustomers){
        this.idBusStop = String.valueOf(idBusStop);
        setLocationBusStop(locationBus);
        setCapacityBusStop(capacity);

        this.listCustomers = (ArrayList<String>) listCustomers.stream().map(String::valueOf).collect(Collectors.toList());
    }
    
    public String getIdBusStop(){
        return idBusStop;
    }
    
    public void setIdBusStop(String idBusStop) throws IllegalArgumentException{
        if(!idBusStop.equals(null)){
            this.idBusStop = idBusStop;
        }
        else
            throw new IllegalArgumentException();     
    }
    
    public Location getLocationBusStop(){
        return locationBusStop;
    }
    
    public void setLocationBusStop(Location locationBusStop) throws IllegalArgumentException{
        if(!locationBusStop.equals(null)){
            this.locationBusStop = locationBusStop;
        }
        else
            throw new IllegalArgumentException();            
    }    
    
    public int getCapacityBusStop(){
        return capacityBusStop;
    } 
    
    public void setCapacityBusStop(int capacityBusStop){
        if(capacityBusStop > 0){
            this.capacityBusStop = capacityBusStop;
        }
    }
    
     public ArrayList<String> getListCustomers(){
         return listCustomers;
     }
     
     //Método para determinar si hay capacidad en la parada.
     public boolean hasCapacity(){
         return capacityBusStop > listCustomers.size();
     }
     
     //Método para saber si se puede insertar un nuevo pasajero.
     public boolean insertCustomer(String idCustomer){
         if(hasCapacity()){
             listCustomers.add(idCustomer);
         }
         
         return hasCapacity();
     }
     
     //Método para aumentar la capacidad de la parada.
     public void increaseCapacityBusStop(int increase){
         if(increase > 0){
             this.capacityBusStop += increase;
         }
     }
     
     //Método para decrementar la capacidad de la parada.
     public void decreaseCapacityBusStop(int decrease){
         if(decrease > 0 && (capacityBusStop - decrease > 0) ){
            this.capacityBusStop -= decrease;
         }
            
     }
     
     public String get_coordinates(){
    
        return this.locationBusStop.getAxisX() + " " + this.locationBusStop.getAxisY();
        
    }
     
}
