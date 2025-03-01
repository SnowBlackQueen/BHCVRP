/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package cujae.inf.citi.om.data;

import cujae.inf.citi.om.exceptions.ServiceTimeException;
import cujae.inf.citi.om.exceptions.TimeWindowException;

/**
 *
 * @author kmych
 */
public class TimeWindow {
    private float initialNode;
    private float endNode;
    private float serviceTime;
    
    public TimeWindow(){
        super();
    }
    
    public TimeWindow(float initialNode, float endNode, float serviceTime){
        
    }
    
    public float getInitialNode(){
        return initialNode;
    }
    
    public void setInitialNode(float initialNode) throws TimeWindowException{
        if(initialNode >= 0){
            this.initialNode = initialNode;
        }
        else
            throw new TimeWindowException("El nodo inicial debe ser mayor que cero.");   
    }
    
    public float getEndNode(){
        return initialNode;
    }
    
    public void setEndNode(float endNode) throws TimeWindowException{
        if(endNode >= 0){
            this.endNode = endNode;
        }
        else
            throw new TimeWindowException("El nodo final debe ser mayor que cero.");     
    }
    
    public float getServiceTime(){
        return initialNode;
    }
    
    public void setServiceTime(float serviceTime) throws ServiceTimeException{
        if(serviceTime >= 0){
            this.serviceTime = serviceTime;
        }
        else
            throw new ServiceTimeException("El tiempo de servicio tiene que ser mayor que cero.");
    }
    
    public float calculateExitTime(float travelTime, float arrivalTime){
        return 0; //max(travel_time, arrive_time) + serviceTime
    }
    
    public boolean verifyTW(float arriveTime){
        return arriveTime <= this.endNode;
    }
}
