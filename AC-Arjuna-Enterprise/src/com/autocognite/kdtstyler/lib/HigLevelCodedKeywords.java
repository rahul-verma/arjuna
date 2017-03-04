package com.autocognite.kdtstyler.lib;

import com.autocognite.kdtstyler.ex.keywords.Calculator;
import com.autocognite.kdtstyler.ex.keywords.DummyMath;
import com.autocognite.kdtstyler.ex.keywords.Formatter;

public class HigLevelCodedKeywords {
	public Calculator calc = null;
	public Formatter formatter = null;
	public DummyMath math = null;
	
	private int parseInt(String number) {
		return Integer.parseInt(number);
	}
	
	public int addAndSquare(String a, String b) {
		int sum = calc.add(parseInt(a), parseInt(b));
		int square = math.square(sum);
		return square;
	}
}
