/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package cujae.inf.citi.om.exceptions;

/**
 *
 * @author nanda
 */

public class RlcException extends Exception {
    private int rlc;
    
    public RlcException(int rlc){
        this.rlc = rlc;
    
    }
    
    public int getRLC(){
        return rlc;
    }
    
    public RlcException(String message){   
        super(message);
    }
    
}
