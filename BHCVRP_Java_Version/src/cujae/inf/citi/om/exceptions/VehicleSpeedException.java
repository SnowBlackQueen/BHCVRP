/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package cujae.inf.citi.om.exceptions;

/**
 *
 * @author kmych
 */
public class VehicleSpeedException extends Exception{
    private float vehicleSpeed;
    
    public VehicleSpeedException(float vehicleSpeed){
        this.vehicleSpeed = vehicleSpeed;
    
    }
    
    public float getVehicleSpeed(){
        return vehicleSpeed;
    }
    
    public VehicleSpeedException(String message){   
        super(message);
    }
    
}