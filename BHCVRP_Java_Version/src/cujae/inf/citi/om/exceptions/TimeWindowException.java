/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package cujae.inf.citi.om.exceptions;

/**
 *
 * @author kmych
 */
public class TimeWindowException extends Exception{
    private float initialNode;
    private float endNode;
    
    public TimeWindowException(float initialNode, float endNode){
        this.initialNode = initialNode;
        this.endNode = endNode;
    
    }
    
    public float getInitialNode(){
        return initialNode;
    }
    
    public float getEndNode(){
        return endNode;
    }
    
    public TimeWindowException(String message){   
        super(message);
    }
    
}
