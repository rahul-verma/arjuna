package com.autocognite.kdtstyler.lib;

import com.autocognite.kdtstyler.ex.keywords.Calculator;

public class StaticKeywords {
	public static int addNumbers(String a, String b) {
		int intA = Integer.parseInt(a);
		int intB = Integer.parseInt(b);
		Calculator calc = new Calculator();
		return calc.add(intA, intB);
	}
	
	public static int multiplyNumbers(String a, String b) {
		int intA = Integer.parseInt(a);
		int intB = Integer.parseInt(b);
		Calculator calc = new Calculator();
		return calc.multiply(intA, intB);
	}
	
}
