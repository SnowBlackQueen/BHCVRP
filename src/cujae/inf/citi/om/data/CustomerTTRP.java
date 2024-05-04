package cujae.inf.citi.om.data;

/* Clase que modela los datos de un cliente en el TTRP*/

public class CustomerTTRP extends Customer{
	
	private CustomerType typeCustomer;
	
	public CustomerTTRP() {
		super();
	}
	
	public CustomerTTRP(CustomerType typeCustomer) {
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
