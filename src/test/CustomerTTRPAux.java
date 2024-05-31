/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package test;

import cujae.inf.citi.om.data.CustomerType;

/**
 *
 * @author kmych
 */
public class CustomerTTRPAux extends CustomerAux {
    private CustomerType typeCustomer;
	
	public CustomerTTRPAux() {
		super();
	}
	
	public CustomerTTRPAux(CustomerType typeCustomer) {
		super();
		this.typeCustomer = typeCustomer;
	}

	public CustomerType getTypeCustomer() {
		return typeCustomer;
	}

	public void setTypeCustomer(CustomerType typeCustomer) {
		this.typeCustomer = typeCustomer;
	}

	public void setTypeCustomer(int typeCustomer) {	
		switch(typeCustomer)
		{
		  case 0 :
		  {
			  this.typeCustomer = CustomerType.VC;
			  break;
		  }
		  case 1:
		  {
			  this.typeCustomer = CustomerType.TC;
			  break;
		  }
	   }
	}
    
}
