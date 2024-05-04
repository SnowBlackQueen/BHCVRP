package test;


public class CustomerAux {

	
	private int idCustomer;
	private double requestCustomer;
	private double axisX;
	private double axisY;

	public CustomerAux() {
		// TODO Auto-generated constructor stub
	}
	

	
	public CustomerAux(int idCustomer, double requestCustomer,
			double axisX, double axisY) {
		super();
		this.idCustomer = idCustomer;
		this.requestCustomer = requestCustomer;
		this.axisX = axisX;
		this.axisY = axisY;
	}

	public int getIdCustomer() {
		return idCustomer;
	}

	public void setIdCustomer(int idCustomer) {
		this.idCustomer = idCustomer;
	}

	public double getRequestCustomer() {
		return requestCustomer;
	}

	public void setRequestCustomer(double requestCustomer) {
		this.requestCustomer = requestCustomer;
	}

	public double getAxisX() {
		return axisX;
	}

	public void setAxisX(double axisX) {
		this.axisX = axisX;
	}
	
	public double getAxisY() {
		return axisY;
	}
	
	public void setAxisY(double axisY) {
		this.axisY = axisY;
	}
}

