/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package cujae.inf.citi.om.exceptions;

/**
 *
 * @author nanda
 */

public class CostException extends Exception{
    private float cost;
    
    public CostException(float cost){
        this.cost = cost;
    
    }
    
    public float getCost(){
        return cost;
    }
    
    public CostException(String message){   
        super(message);
    }
    
}
