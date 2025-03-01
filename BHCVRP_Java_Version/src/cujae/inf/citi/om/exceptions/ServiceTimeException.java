/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package cujae.inf.citi.om.exceptions;

/**
 *
 * @author kmych
 */
public class ServiceTimeException extends Exception{
    private float serviceTime;
    
    public ServiceTimeException(float serviceTime){
        this.serviceTime = serviceTime;
    
    }
    
    public float getServiceTime(){
        return serviceTime;
    }
    
    public ServiceTimeException(String message){   
        super(message);
    }
    
}
