/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package cujae.inf.citi.om.exceptions;

/**
 *
 * @author nanda
 */

public class RequestException extends Exception{
    private float request;
    
    public RequestException(float request){
        this.request = request;
    
    }
    
    public float getRequest(){
        return request;
    }
    
    public RequestException(String message){   
        super(message);
    }
    
}
