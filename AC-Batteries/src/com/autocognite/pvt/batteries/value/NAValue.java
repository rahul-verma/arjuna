package com.autocognite.pvt.batteries.value;

import com.autocognite.arjuna.interfaces.Value;

public class NAValue extends AbstractValue {
	private static String val = "NA";

	public NAValue() {
		super(ValueType.NA, val);
	}

	@Override
	public Value clone() {
		return this;
	}

	@Override
	public String asString() {
		return val;
	}

	@Override
	public boolean isNull() {
		return true;
	}

}
