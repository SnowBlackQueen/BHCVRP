/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package cujae.inf.citi.om.exceptions;

/**
 *
 * @author nanda
 */

//Clase que maneja la excepción lanzada cuando no existe capacidad.

public class WithoutCapacityException extends Exception {
    private int capacity;
    
    public WithoutCapacityException(int capacity){
        this.capacity = capacity;
    
    }
    
    public int getCapacity(){
        return capacity;
    }
    
    public WithoutCapacityException(String message){   
        super(message);
    }
}

