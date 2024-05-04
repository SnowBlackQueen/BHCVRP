package cujae.inf.citi.om.generator.heuristic;

/* Clase que modela una métrica para las heurística basadas en inserción */

public class Metric {

	private int idElement;
	private double insertionCost;
	private int index;
	
	public Metric() {
		super();
		index = -1;
		// TODO Auto-generated constructor stub
	}

	public Metric(int idElement, double insertionCost, int index) {
		super();
		this.idElement = idElement;
		this.insertionCost = insertionCost;
		this.index = index;
	}

	public int getIdElement() {
		return idElement;
	}

	public void setIdElement(int idElement) {
		this.idElement = idElement;
	}

	public double getInsertionCost() {
		return insertionCost;
	}

	public void setInsertionCost(double insertionCost) {
		this.insertionCost = insertionCost;
	}

	public int getIndex() {
		return index;
	}

	public void setIndex(int index) {
		this.index = index;
	}
}
