/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package cujae.inf.citi.om.exceptions;

/**
 *
 * @author nanda
 */

public class BusStopCapacityException extends Exception{
    private int capacityBusStop;
    
    public BusStopCapacityException(int capacityBusStop){
        this.capacityBusStop = capacityBusStop;
    
    }
    
    public int getCapacityBusStop(){
        return capacityBusStop;
    }
    
    public BusStopCapacityException(String message){   
        super(message);
    }
    
}
