/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package cujae.inf.citi.om.exceptions;

/**
 *
 * @author nanda
 */

//Clase que maneja la excepción lanzada cuando la distancia no es accesible.

public class DistanceNotAccessibleException extends Exception{
    private float distance;
    
    public DistanceNotAccessibleException(float distance){
        this.distance = distance;
    
    }
    
    public float getDistance(){
        return distance;
    }
    
    public DistanceNotAccessibleException(String message){   
        super(message);
    }
}

