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
    private double initialNode;
    private double endNode;
    private double serviceTime;
    
    public TimeWindow(){
        super();
    }
    
    public TimeWindow(float initialNode, float endNode, float serviceTime){
        
    }
    
    public double getInitialNode(){
        return initialNode;
    }
    
    public void setInitialNode(double initialNode) throws TimeWindowException{
        if(initialNode >= 0){
            this.initialNode = initialNode;
        }
        else
            throw new TimeWindowException("El nodo inicial debe ser mayor que cero.");   
    }
    
    public double getEndNode(){
        return initialNode;
    }
    
    public void setEndNode(double endNode) throws TimeWindowException{
        if(endNode >= 0){
            this.endNode = endNode;
        }
        else
            throw new TimeWindowException("El nodo final debe ser mayor que cero.");     
    }
    
    public double getServiceTime(){
        return initialNode;
    }
    
    public void setServiceTime(double serviceTime) throws ServiceTimeException{
        if(serviceTime >= 0){
            this.serviceTime = serviceTime;
        }
        else
            throw new ServiceTimeException("El tiempo de servicio tiene que ser mayor que cero.");
    }
    
    public double calculateExitTime(double travelTime, double arrivalTime){
        return 0; //max(travel_time, arrive_time) + serviceTime
    }
    
    public boolean verifyTW(double arriveTime){
        return arriveTime <= this.endNode;
    }
}
