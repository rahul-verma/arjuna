package com.autocognite.kdtstyler.ex.keywords;

public class Calculator {
	private int currentCalculation = 0;
	
	public int add(int a, int b) {
		currentCalculation += a + b;
		return currentCalculation;
	}
	
	public int subtract(int a, int b) {
		currentCalculation += a - b;
		return currentCalculation;
	}
	
	public int multiply(int a, int b) {
		currentCalculation += a * b;
		return currentCalculation;
	}
	
	public void reset() {
		currentCalculation = 0;
	}
}
