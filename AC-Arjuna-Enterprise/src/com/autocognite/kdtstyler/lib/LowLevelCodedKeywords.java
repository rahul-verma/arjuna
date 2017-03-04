package com.autocognite.kdtstyler.lib;

import com.autocognite.kdtstyler.ex.keywords.Calculator;
import com.autocognite.kdtstyler.ex.keywords.DummyMath;
import com.autocognite.kdtstyler.ex.keywords.Formatter;

public class LowLevelCodedKeywords {
	public Calculator calc = null;
	public Formatter formatter = null;
	public DummyMath math = null;
	
	public void createCalculator() {
		calc = new Calculator();
	}
	
	public void resetCalculator() {
		calc.reset();
	}
	
	public void createFormatter() {
		formatter = new Formatter();
	}
	
	public void createDummyMath() {
		math = new DummyMath();
	}
	
	private int parseInt(String number) {
		return Integer.parseInt(number);
	}
	
	public int add(String a, String b) {
		return calc.add(parseInt(a), parseInt(b));
	}
	
	public int subtract(String a, String b) {
		return calc.subtract(parseInt(a), parseInt(b));
	}
	
	public int multiply(String a, String b) {
		return calc.multiply(parseInt(a), parseInt(b));
	}
	
	public int square(String a) {
		return math.square(parseInt(a));
	}
	
	public void print(Object o) {
		formatter.print(o);
	}
	
	public void printFormatted(Object o) {
		formatter.printFormatted(o);
	}
}
